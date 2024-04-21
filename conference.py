import time
from RedisDB import RedisDB

class ConferenceApp:
    def __init__(self, init=True):
        # Connect to DB
        self.db = RedisDB()

        if init:
            self.db.clearDB()
            self.db.createDB()


    def join_meeting(self, userID, meetingID):
        time_joined = time.strftime('%Y-%m-%d %H:%M:%S')
        
        # Check if meeting exists
        meeting = self.db.get(f"meeting:{meetingID}")
        if not self.db.exists(f"meeting:{meetingID}"):
            return "[!] Meeting does not exist."

        # Check if user exists
        user = self.db.get(f"user:{userID}")
        if not self.db.exists(f"user:{userID}"):
            return "[!] User does not exist."
        
        #Check if meeting instances exists
        instance_keys = self.db.getKeys(f"meeting_instance:{meetingID}:*")   
        if not instance_keys:
            return "[!] Meeting instance does not exist."
        
        # Check if meeting instance is active
        instance_keys.sort(reverse=True)
        t_instance = self.db.get(instance_keys[0])
        if t_instance['fromdatetime'] > time_joined or t_instance['todatetime'] <= time_joined:
            return f"[!] There is no active instance of meeting '{meeting['title']}'."
         
        # Check if meeting is public or user is invited
        if meeting['isPublic'] == 'False':
            audience = meeting['audience'].split(',')
            if user['email'] not in audience:
                return f"[!] User '{user['name']}' is not invited to the meeting '{meeting['title']}'."
            
        # Log the event
        event_id = self.db.get('event_id_counter', hash=False)
        event_type = 1
        event = {
            'event_id': event_id,
            'userID': userID,
            'meetingID': meetingID,
            'event_type': event_type,
            'timestamp': time_joined
        }
        self.db.set(f"event:{event_id}:{userID}:{meetingID}:{event_type}", value=event)  
        self.db.increase('event_id_counter')

        return f"[+] User '{user['name']}' joined meeting '{meeting['title']}' at {time_joined}."


    def leave_meeting(self, userID, meetingID, time_left=None):
        if time_left is None:
            time_left = time.strftime('%Y-%m-%d %H:%M:%S')

        # Check if meeting exists
        meeting = self.db.get(f"meeting:{meetingID}")
        if not self.db.exists(f"meeting:{meetingID}"):
            return "[!] Meeting does not exist."

        # Check if user exists
        user = self.db.get(f"user:{userID}")
        if not self.db.exists(f"user:{userID}"):
            return "[!] User does not exist."

        #Check if meeting instances exists
        instance_keys = self.db.getKeys(f"meeting_instance:{meetingID}:*")
        if not instance_keys:
            return "[!] Meeting instance does not exist."
        
        # Check if meeting instance is active
        instance_keys.sort(reverse=True)
        t_instance = self.db.get(instance_keys[0])
        if t_instance['fromdatetime'] > time_left or t_instance['todatetime'] <= time_left:
            return f"[!] There is no active instance of meeting '{meeting['title']}'."

        # Check if user has joined the meeting 
        events_keys = self.db.getKeys(f"event:*:{userID}:{meetingID}:*")
        if not events_keys:
            return f"[!] User '{user['name']}' has not joined meeting '{meeting['title']}'."
        
        # Get the last event of the user for this meeting
        events_keys.sort(reverse=True)
        t_event = self.db.get(events_keys[0])
        if t_event['event_type'] == '2' and t_event['timestamp'] <= time_left and t_event['timestamp'] >= t_instance['fromdatetime'] and t_event['timestamp'] <= t_instance['todatetime']:
            return f"[!] User '{user['name']}' has already left meeting '{meeting['title']}'."
        if (t_event['event_type'] == '1' or t_event['type'] == '3') and t_instance['fromdatetime'] <= t_event['timestamp'] and t_instance['todatetime'] >= t_event['timestamp']:
            if time_left >= t_event['timestamp'] and time_left <= t_instance['todatetime']:

                #Log the event
                event_id = self.db.get('event_id_counter', hash=False)
                event_type = 2
                event = {
                    'event_id': event_id,
                    'userID': userID,
                    'meetingID': meetingID,
                    'event_type': event_type,
                    'timestamp': time_left
                }
                self.db.set(f"event:{event_id}:{userID}:{meetingID}:{event_type}", value=event)
                self.db.increase('event_id_counter')

                return f"[+] User '{user['name']}' left meeting '{meeting['title']}' at {time_left}."
            
        
        return f"[!] User '{user['name']}' - ERROR while leaving the meeting."
        

    def meeting_participants(self, meetingID):
        current_time = time.strftime('%Y-%m-%d %H:%M:%S')

        # Check if meeting exists
        meeting = self.db.get(f"meeting:{meetingID}")
        if not self.db.exists(f"meeting:{meetingID}"):
            return "[!] Meeting does not exist."

        #Check if meeting instances exists
        instance_keys = self.db.getKeys(f"meeting_instance:{meetingID}:*")
        if not instance_keys:
            return "[!] Meeting instance does not exist."
        
        # Check if meeting instance is active
        instance_keys.sort(reverse=True)
        t_instance = self.db.get(instance_keys[0])
        if t_instance['fromdatetime'] > current_time or t_instance['todatetime'] <= current_time:
            return f"[!] There is no active instance of meeting '{meeting['title']}'."

        # Get all events of type 1(joined) that their timestamp is between the fromdatetime and todatetime of the meeting instance
        participants = {}
        events_keys = self.db.getKeys(f"event:*:*:{meetingID}:*")
        for _event in events_keys:
            event = self.db.get(_event)
            if event['event_type'] == '1' and event['timestamp'] >= t_instance['fromdatetime'] and event['timestamp'] <= t_instance['todatetime']:
                participants[event['userID']] = event['timestamp']

        # Get all events of type 2(left) that their timestamp is between the fromdatetime and todatetime of the meeting instance 
        # and remove the users that have left the meeting
        for _event in events_keys:
            event = self.db.get(_event)
            if event['event_type'] == '2' and event['timestamp'] >= t_instance['fromdatetime'] and event['timestamp'] <= t_instance['todatetime']:
                if event['userID'] in participants:
                    del participants[event['userID']]

        current_participants = [(self.db.get('user:'+k, field='name', all=False), 'joined: '+v) for k, v in participants.items()]
        return f"[*] Participants of meeting '{meeting['title']}' are: {current_participants}"


    def show_active_meetings(self):
        current_time = time.strftime('%Y-%m-%d %H:%M:%S')

        # Get all active meeting instances
        instance_keys = self.db.getKeys(f"meeting_instance:*")
        active_meeting_instances = []
        for _key in instance_keys:
            t_instance = self.db.get(_key)
            time_started = t_instance['fromdatetime']
            time_ended = t_instance['todatetime']
            if time_started <= current_time and current_time < time_ended:
                active_meeting_instances.append(t_instance)

        if not active_meeting_instances:
            return "[!] There are no active meetings."

        meeting_info = [(self.db.get("meeting:"+_instance['meetingID']), _instance['fromdatetime'], _instance['todatetime']) for _instance in active_meeting_instances]
        res = f"[*] Active meetings are: \n"
        res += ''.join([f"\t[id:{_meeting['meetingID']}] Meeting '{_meeting['title']}' from {_from} to {_to} \n" for _meeting, _from, _to in meeting_info])

        return res, active_meeting_instances


    def end_meeting(self, meetingID):
        current_time = time.strftime('%Y-%m-%d %H:%M:%S')

        # Check if meeting exists
        meeting = self.db.get(f"meeting:{meetingID}")
        if not self.db.exists(f"meeting:{meetingID}"):
            return "[!] Meeting does not exist."
        
        #Check if meeting instances exists
        instance_keys = self.db.getKeys(f"meeting_instance:{meetingID}:*")
        if not instance_keys:
            return "[!] Meeting instance does not exist."
        
        # Find ended meeting instances
        ended_instances = []
        for _instance in instance_keys:
            t_instance = self.db.get(_instance)
            if t_instance['fromdatetime'] < current_time and t_instance['todatetime'] <= current_time:
                ended_instances.append(t_instance)

        if not ended_instances:
            return "[!] There is no ended meeting instance."
        
        # Sort the ended instances by orderID, the first instance is the one that ended last
        ended_instances.sort(key= lambda x: x['orderID'], reverse=True)
        ended_instance = ended_instances[0]
        
        users_keys = self.db.getKeys(f"user:*")
        if not users_keys:
            return "[!] There are no users in the meeting."
        
        # Leave all users that have not left the meeting
        for _user in users_keys:
            userID = _user.split(':')[1]
            print(self.leave_meeting(userID, meetingID, ended_instance['todatetime']))

    def meeting_participants_join_time(self):

        res, active_meetings_instances = self.show_active_meetings() 
        print(res)
        for _instance in active_meetings_instances:
            meetingID = _instance['meetingID']
            print('\t'+self.meeting_participants(meetingID))