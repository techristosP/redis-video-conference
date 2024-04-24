from redisdb import RedisDB
from initdb import InitDB
import time
import json

class ConferenceApp:

    def __init__(self, reset=True):
        # Connect to DB
        self.db0 = RedisDB(db=0)    # Users, Meetings, Meeting Instances
        self.db1 = RedisDB(db=1)    # Events, Messages

        if reset:
            self.db0.clearDB()
            self.db1.clearDB()
            InitDB(self.db0, self.db1)


    # Helper functions
    def __getMeeting(self, meetingID):
            """
            Retrieve a meeting from the database.

            Args:
                meetingID (str): The ID of the meeting to retrieve.

            Returns:
                dict: The meeting object.

            Raises:
                Exception: If the meeting does not exist in the database.
            """
            meeting = self.db0.get(f"meeting:{meetingID}")
            if not meeting:
                raise Exception("[!] Meeting does not exist!")

            return meeting
    
    def __getUser(self, userID):
            """
            Retrieve a user from the database based on their userID.

            Args:
                userID (str): The ID of the user to retrieve.

            Returns:
                dict: The user object.

            Raises:
                Exception: If the user does not exist in the database.
            """
            user = self.db0.get(f"user:{userID}")
            if not user:
                raise Exception("[!] User does not exist!")
            
            return user
    
    def __getMeetingInstances(self, meetingID):
            """
            Retrieves the meeting instances associated with the given meeting ID.

            Args:
                meetingID (str): The ID of the meeting.

            Returns:
                list: A list of instance keys associated with the meeting ID.

            Raises:
                Exception: If no meeting instances exist for the given meeting ID.
            """
            instance_keys = self.db0.getKeys(f"meeting_instance:{meetingID}:*")
            if not instance_keys:
                raise Exception("[!] Meeting instance does not exist!")
            
            return instance_keys
    
    def __getActiveMeetingInstance(self, meeting, instance_keys, time):
        """
        Get the active instance of a meeting based on the given time.

        Args:
            meeting (dict): The meeting object.
            instance_keys (list): A list of instance keys.
            time (datetime): The current time.

        Returns:
            dict: The active instance of the meeting.

        Raises:
            Exception: If there is no active instance of the meeting.
        """
        instance_keys.sort(reverse=True)
        t_instance = self.db0.get(instance_keys[0])
        if t_instance['fromdatetime'] > time or t_instance['todatetime'] <= time:
            raise Exception(f"[!] There is no active instance of meeting '{meeting['title']}'.")
                    
        return t_instance
    
    def __getLatestInactiveMeetingInstance(self, meeting, instance_keys, time):
        """
        Get the latest inactive meeting instance before a given time.

        Args:
            meeting (str): The meeting identifier.
            instance_keys (list): A list of instance keys.
            time (datetime): The time to compare against.

        Returns:
            dict or None: The latest inactive meeting instance before the given time, or None if no such instance exists.
        """
        instance_keys.sort(reverse=True)
        t_instance = self.db0.get(instance_keys[0])
        while t_instance['todatetime'] > time:
            instance_keys = instance_keys[1:]
            if instance_keys != []:
                t_instance = self.db0.get(instance_keys[0])
            else:
                return None

        return t_instance


    # Main functions
    def join_meeting(self, userID, meetingID):
        """
        Joins a user to a meeting.

        Args:
            userID (str): The ID of the user joining the meeting.
            meetingID (str): The ID of the meeting to join.

        Returns:
            None

        Raises:
            Exception: If an error occurs while joining the meeting.
        """
        time_joined = time.strftime('%Y-%m-%d %H:%M:%S')
        
        try:
            meeting = self.__getMeeting(meetingID)
            user = self.__getUser(userID)
            instance_keys = self.__getMeetingInstances(meetingID)
            
            t_instance = self.__getActiveMeetingInstance(meeting, instance_keys, time_joined)

            # Check if meeting is public or user is invited
            if meeting['isPublic'] == 'False':
                audience = meeting['audience'].split(',')
                if user['email'] not in audience:
                    res = f"[!] User '{user['name']}' is not invited to the meeting '{meeting['title']}'."
                    print(res)
                    return
                
            # Check if user has already joined the meeting
            event_keys = self.db1.getKeys(f"event:*:{userID}:{meetingID}:1")
            event_keys.sort(reverse=True)
            latest_event = self.db1.get(event_keys[0]) if event_keys else None
            if latest_event and t_instance['fromdatetime'] <= latest_event['timestamp'] and latest_event['timestamp'] < t_instance['todatetime']:
                res = f"[!] User '{user['name']}' has already joined meeting '{meeting['title']}' at {latest_event['timestamp']}."
                print(res)
                return

            # Log the event
            event_id = self.db1.get('event_id_counter', hash=False)
            event_type = 1
            event = {
                'event_id': event_id,
                'userID': userID,
                'meetingID': meetingID,
                'event_type': event_type,
                'timestamp': time_joined
            }
            self.db1.set(f"event:{event_id}:{userID}:{meetingID}:{event_type}", value=event)  
            self.db1.increase('event_id_counter')

            res =  f"[+] User '{user['name']}' joined meeting '{meeting['title']}' at {time_joined}."
            print(res)
            return

        except Exception as e:
            print(str(e))
            return

    def leave_meeting(self, userID, meetingID, forceLeave=False, time_left=None):
        """
        Leave a meeting.

        Args:
            userID (str): The ID of the user leaving the meeting.
            meetingID (str): The ID of the meeting.
            forceLeave (bool, optional): If True, force the user to leave the meeting even if they haven't joined. Defaults to False.
            time_left (str, optional): The timestamp indicating the time the user is leaving the meeting. If not provided, the current time will be used. Defaults to None.

        Returns:
            None

        Raises:
            Exception: If an error occurs while leaving the meeting.
        """
        if time_left is None:
            time_left = time.strftime('%Y-%m-%d %H:%M:%S')

        try:
            meeting = self.__getMeeting(meetingID)
            user = self.__getUser(userID)
            instance_keys = self.__getMeetingInstances(meetingID)
        
            if not forceLeave:
                t_instance = self.__getActiveMeetingInstance(meeting, instance_keys, time_left)
            else:
                t_instance = self.__getLatestInactiveMeetingInstance(meeting, instance_keys, time_left)

            # Check if user has joined the meeting 
            events_keys = self.db1.getKeys(f"event:*:{userID}:{meetingID}:*")
            if not events_keys:
                if not forceLeave:
                    res = f"[!] User '{user['name']}' has not joined meeting '{meeting['title']}'."
                    print(res)

                return
            
            # Get the last event of the user for this meeting
            events_keys.sort(reverse=True)
            t_event = self.db1.get(events_keys[0])           
            if t_event['event_type'] == '2' and t_event['timestamp'] <= time_left and t_instance['fromdatetime'] <= t_event['timestamp'] and t_event['timestamp'] <= t_instance['todatetime']:
                res = f"[!] User '{user['name']}' has already left meeting '{meeting['title']}'."
                print(res)
                return
            
            if (t_event['event_type'] == '1' or t_event['event_type'] == '3') and t_instance['fromdatetime'] <= t_event['timestamp'] and t_event['timestamp'] <= t_instance['todatetime']:
                if time_left >= t_event['timestamp'] and time_left <= t_instance['todatetime']:

                    #Log the event
                    event_id = self.db1.get('event_id_counter', hash=False)
                    event_type = 2
                    event = {
                        'event_id': event_id,
                        'userID': userID,
                        'meetingID': meetingID,
                        'event_type': event_type,
                        'timestamp': time_left
                    }
                    self.db1.set(f"event:{event_id}:{userID}:{meetingID}:{event_type}", value=event)
                    self.db1.increase('event_id_counter')

                    res = f"[+] User '{user['name']}' left meeting '{meeting['title']}' at {time_left}."
                    print(res)
                    return 
                
            
            res = f"[!] User '{user['name']}' - ERROR while leaving the meeting."
            print(res)
            return
        
        except Exception as e:
            print(str(e))
            return

    def meeting_participants(self, meetingID):
        """
        Retrieves the participants of a meeting based on the meeting ID.

        Args:
            meetingID (str): The ID of the meeting.

        Returns:
            None
        """
        current_time = time.strftime('%Y-%m-%d %H:%M:%S')

        try:
            meeting = self.__getMeeting(meetingID)
            instance_keys = self.__getMeetingInstances(meetingID)

            t_instance = self.__getActiveMeetingInstance(meeting, instance_keys, current_time)

            # Get all events of type 1(joined) that their timestamp is between the fromdatetime and todatetime of the meeting instance
            participants = {}
            events_keys = self.db1.getKeys(f"event:*:*:{meetingID}:*")
            for _event in events_keys:
                event = self.db1.get(_event)
                if event['event_type'] == '1' and event['timestamp'] >= t_instance['fromdatetime'] and event['timestamp'] <= t_instance['todatetime']:
                    participants[event['userID']] = event['timestamp']

            # Get all events of type 2(left) that their timestamp is between the fromdatetime and todatetime of the meeting instance 
            # and remove the users that have left the meeting
            for _event in events_keys:
                event = self.db1.get(_event)
                if event['event_type'] == '2' and event['timestamp'] >= t_instance['fromdatetime'] and event['timestamp'] <= t_instance['todatetime']:
                    if event['userID'] in participants:
                        del participants[event['userID']]

            current_participants = [(self.db0.get('user:'+k, field='name', all=False), 'joined: '+v) for k, v in participants.items()]
            res = f"[*] Participants of meeting '{meeting['title']}' are: {current_participants}"
            print(res)
            return

        except Exception as e:
            print(str(e))
            return

    def show_active_meetings(self):
        """
        Retrieves and displays information about active meetings.

        Returns:
            list: A list of tuples containing information about active meetings.
                  Each tuple contains the meeting object and the active meeting instance.
                  If there are no active meetings, it returns an empty list.
        """
        current_time = time.strftime('%Y-%m-%d %H:%M:%S')

        # Get all active meetings
        meeting_keys = self.db0.getKeys(f"meeting:*")    # Get all meeting keys
        active_meetings = []
        for _key in meeting_keys:
            t_meeting = self.db0.get(_key)
            try:
                t_instance_keys = self.__getMeetingInstances(t_meeting['meetingID'])
                t_active_instance = self.__getActiveMeetingInstance(t_meeting, t_instance_keys, current_time)
            except Exception as e:
                t_active_instance = None

            if t_active_instance:
                active_meetings.append((t_meeting, t_active_instance))

        if not active_meetings:
            return "[!] There are no active meetings."

        meeting_info = [(_meeting[0], _meeting[1]['fromdatetime'], _meeting[1]['todatetime']) for _meeting in active_meetings]
        res = f"[*] Active meetings are: \n"
        res += ''.join([f"\t[id:{_meeting['meetingID']}] Meeting '{_meeting['title']}' from {_from} to {_to} \n" for _meeting, _from, _to in meeting_info])

        print(res)
        return active_meetings

    def end_meeting(self, meetingID, stopMeeting=False):
        """
        Ends the latest instance of a meeting.

        Args:
            meetingID (str): The ID of the meeting.
            stopMeeting (bool, optional): If True, ends the active meeting instance. If False, ends the latest inactive meeting instance properly for all users. Defaults to False.
        
        Returns:
            None
        """
        current_time = time.strftime('%Y-%m-%d %H:%M:%S')

        try:
            meeting = self.__getMeeting(meetingID)
            instance_keys = self.__getMeetingInstances(meetingID)  

            # Get the latest instance of the meeting that has ended
            if not stopMeeting:
                ended_instance = self.__getLatestInactiveMeetingInstance(meeting, instance_keys, current_time)
            else:
                ended_instance = self.__getActiveMeetingInstance(meeting, instance_keys, current_time)

            if not ended_instance:
                res = f"[!] There is no ended instance for meeting '{meeting['title']}'."
                print(res)
                return
            
            print(f"[*] Ending latest instance of meeting '{meeting['title']}'...")
            # Get all events of type 1(joined) that their timestamp is between the fromdatetime and todatetime of the ended instance
            rel_events = self.db1.getKeys(f"event:*:*:{meetingID}:*")
            for _event in rel_events:
                event = self.db1.get(_event)
                if ended_instance['fromdatetime'] <= event['timestamp'] and event['timestamp'] <= ended_instance['todatetime']:
                    if event['event_type'] == '1':
                        self.leave_meeting(event['userID'], meetingID, forceLeave=True, time_left=ended_instance['todatetime'])

            res = f"\t> Latest instance of meeting '{meeting['title']}' has ended at: {ended_instance['todatetime']}."
            print(res)
            return

        except Exception as e:
            print(str(e))
            return

    def meeting_participants_join_time(self):
        """
        Retrieves the join time of participants for active meetings.

        This method iterates over the active meetings and calls the `meeting_participants` method
        to retrieve the join time of participants for each meeting.

        Returns:
            None
        """
        active_meetings = self.show_active_meetings() 
        for _meeting in active_meetings:
            meetingID = _meeting[0]['meetingID']
            self.meeting_participants(meetingID)

        return

    def post_message(self, userID, meetingID, text):
        """
        Posts a message in a meeting.

        Args:
            userID (str): The ID of the user posting the message.
            meetingID (str): The ID of the meeting where the message is being posted.
            text (str): The content of the message.

        Returns:
            None
        """
        current_time = time.strftime('%Y-%m-%d %H:%M:%S')

        try:
            meeting = self.__getMeeting(meetingID)
            user = self.__getUser(userID)
            instance_keys = self.__getMeetingInstances(meetingID)            
       
            t_instance = self.__getActiveMeetingInstance(meeting, instance_keys, current_time)

            # Log the message   
            message_key = f"message:{meetingID}:{t_instance['orderID']}"
            message = {
                'userID': userID,
                'text': text,
                'timestamp': current_time
            }
            message_json = json.dumps(message)
            self.db1.push(message_key, message_json, left=False)

            res = f"[+] POST: - {text} [by '{user['name']}' at {current_time}]"
            print(res)
            return

        except Exception as e:
            print(str(e))
            return

    def meeting_messages(self, meetingID):
        """
        Retrieve and print all messages of a given meeting.

        Args:
            meetingID (str): The ID of the meeting.

        Returns:
            None
        """
        try:
            meeting = self.__getMeeting(meetingID)
            instance_keys = self.__getMeetingInstances(meetingID)

            # Get all messages of the meeting 
            instance_keys.sort(reverse=True) # Latest instance is the first
            res = f"[*] Messages of meeting '{meeting['title']}' are: \n"
            all_messages = []
            for _instance in instance_keys:
                t_instance = self.db0.get(_instance)
                message_key = f"message:{meetingID}:{t_instance['orderID']}"

                # Get all messages of the meeting instance's list
                messages = [json.loads(_message) for _message in self.db1.range(message_key)]
                all_messages.extend(messages)
                res += f"\tInstance {t_instance['orderID']} from {t_instance['fromdatetime']} to {t_instance['todatetime']}: \n"
                res += ''.join(f"\t - {_message['text']} [by '{self.db0.get('user:'+str(_message['userID']), all=False, field='name')}' at {_message['timestamp']}]\n" for _message in messages)

            print(res)
            return
        
        except Exception as e:
            print(str(e))
            return
            
    def show_meeting_user_messages(self, userID, meetingID):
        """
        Retrieves and displays all messages sent by a specific user in a given meeting.

        Args:
            userID (str): The ID of the user.
            meetingID (str): The ID of the meeting.

        Returns:
            None
        """
        current_time = time.strftime('%Y-%m-%d %H:%M:%S')

        try:
            meeting = self.__getMeeting(meetingID)
            user = self.__getUser(userID)
            instance_keys = self.__getMeetingInstances(meetingID)

            t_instance = self.__getActiveMeetingInstance(meeting, instance_keys, current_time)

            # Get all messages of the meeting's active instance
            message_key = f"message:{meetingID}:{t_instance['orderID']}"
            all_messages = [json.loads(_message) for _message in self.db1.range(message_key)]    

            # Get all messages of the user
            user_messages = [(_message['text'], _message['timestamp']) for _message in all_messages if _message['userID'] == userID]

            res = f"[*] Messages of '{user['name']}' in meeting '{meeting['title']}': \n"
            res += ''.join(f"\t - {_message[0]} [at {_message[1]}]\n" for _message in user_messages)

            print(res)
            return
        
        except Exception as e:
            print(str(e))
            return
        