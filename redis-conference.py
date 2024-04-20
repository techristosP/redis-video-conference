import redis
import time

import createDB

# Connect to Redis
r = redis.Redis(host='localhost', port=6379, decode_responses=True)

def join_meeting(userID, meetingID):
    time_joined = time.strftime('%Y-%m-%d %H:%M:%S')
    
    # Check if meeting exists
    meeting = r.hgetall(f"meeting:{meetingID}")
    if not r.exists(f"meeting:{meetingID}"):
        return "[!] Meeting does not exist."

    # Check if user exists
    user = r.hgetall(f"user:{userID}")
    if not r.exists(f"user:{userID}"):
        return "[!] User does not exist."
    
    #Check if meeting instances exists
    instance_keys = r.keys(f"meeting_instance:{meetingID}:*")   
    if not instance_keys:
        return "[!] Meeting instance does not exist."
    
    meeting_instance = None
    for _instance in instance_keys:
        t_instance = r.hgetall(_instance)
        if t_instance['fromdatetime'] > time_joined:
            #return "[!] Meeting has not started yet."
            continue
        if t_instance['todatetime'] < time_joined:
            #return "[!] Meeting has ended."
            continue
        meeting_instance = t_instance
        break   # The first instance that is active is selected

    if meeting_instance is None:
        return "[!] There is no active meeting instance."
 
    # Check if meeting is public or user is invited
    if meeting['isPublic'] == 'False':
        audience = meeting['audience'].split(',')
        if user['email'] not in audience:
            return f"[!] User '{user['name']}' is not invited to the meeting '{meeting['title']}'."
        
    # Log the event
    event_id = r.get('event_id_counter')
    event_type = 1
    event = {
        'event_id': event_id,
        'userID': userID,
        'meetingID': meetingID,
        'event_type': event_type,
        'timestamp': time_joined
    }
    r.hset(f"event_id:{event_id}:{userID}:{meetingID}:{event_type}", mapping=event)  
    r.incr('event_id_counter')

    return f"[+] User '{user['name']}' joined meeting '{meeting['title']}' at {time_joined}."


def leave_meeting(userID, meetingID):
    time_left = time.strftime('%Y-%m-%d %H:%M:%S')

    # Check if meeting exists
    meeting = r.hgetall(f"meeting:{meetingID}")
    if not r.exists(f"meeting:{meetingID}"):
        return "[!] Meeting does not exist."

    # Check if user exists
    user = r.hgetall(f"user:{userID}")
    if not r.exists(f"user:{userID}"):
        return "[!] User does not exist."

    #Check if meeting instances exists
    instance_keys = r.keys(f"meeting_instance:{meetingID}:*")
    if not instance_keys:
        return "[!] Meeting instance does not exist."
    
    # Keep the active meeting instance
    t_instance = None
    for _instance in instance_keys:
        t_instance = r.hgetall(_instance)

        if t_instance['fromdatetime'] < time_left and t_instance['todatetime'] > time_left:
            break
    
    if t_instance is None:
        return "[!] There is no active meeting instance."

    # Check if user has joined the meeting 
    events_keys = r.keys(f"event_id:*:{userID}:{meetingID}:*")
    if not events_keys:
        return f"[!] User '{user['name']}' has not joined any meetings."
    
    events_keys.sort(reverse=True)
    t_event = r.hgetall(events_keys[0])
    if t_event['event_type'] == '2' and t_event['timestamp'] <= time_left and t_event['timestamp'] >= t_instance['fromdatetime'] and t_event['timestamp'] <= t_instance['todatetime']:
        return f"[!] User '{user['name']}' has already left the meeting."
    if (t_event['event_type'] == '1' or t_event['type'] == '3') and t_instance['fromdatetime'] <= t_event['timestamp'] and t_instance['todatetime'] >= t_event['timestamp']:
        if time_left >= t_event['timestamp'] and time_left <= t_instance['todatetime']:

            #Log the event
            event_id = r.get('event_id_counter')
            event_type = 2
            event = {
                'event_id': event_id,
                'userID': userID,
                'meetingID': meetingID,
                'event_type': event_type,
                'timestamp': time_left
            }
            r.hset(f"event_id:{event_id}:{userID}:{meetingID}:{event_type}", mapping=event)
            r.incr('event_id_counter')

            return f"[+] User '{user['name']}' left meeting '{meeting['title']}' at {time_left}."
        
    
    return f"[!] User '{user['name']}' has not joined the meeting yet."
     

def meeting_participants(meetingID):
    current_time = time.strftime('%Y-%m-%d %H:%M:%S')

    # Check if meeting exists
    meeting = r.hgetall(f"meeting:{meetingID}")
    if not r.exists(f"meeting:{meetingID}"):
        return "[!] Meeting does not exist."

    #Check if meeting instances exists
    instance_keys = r.keys(f"meeting_instance:{meetingID}:*")
    if not instance_keys:
        return "[!] Meeting instance does not exist."
    
    # Check if meeting instance is active
    t_instance = None
    for _instance in instance_keys:
        t_instance = r.hgetall(_instance)
        if t_instance['fromdatetime'] <= current_time and t_instance['todatetime'] > current_time:
            break

    if t_instance is None:
        return "[!] There is no active meeting instance."

    # Get all events of type 1(joined) that their timestamp is between the fromdatetime and todatetime of the meeting instance
    participants = {}
    events_keys = r.keys(f"event_id:*:*:{meetingID}:*")
    for _event in events_keys:
        event = r.hgetall(_event)
        if event['event_type'] == '1' and event['timestamp'] >= t_instance['fromdatetime'] and event['timestamp'] <= t_instance['todatetime']:
            participants[event['userID']] = event['timestamp']

    # Get all events of type 2(left) that their timestamp is between the fromdatetime and todatetime of the meeting instance 
    # and remove the users that have left the meeting
    for _event in events_keys:
        event = r.hgetall(_event)
        if event['event_type'] == '2' and event['timestamp'] >= t_instance['fromdatetime'] and event['timestamp'] <= t_instance['todatetime']:
            if event['userID'] in participants:
                del participants[event['userID']]

    current_participants = [(r.hget('user:'+k, 'name'), 'joined: '+v) for k, v in participants.items()]
    return f"[*] Participants of meeting '{meeting['title']}' are: {current_participants}"


def show_active_meetings():
    current_time = time.strftime('%Y-%m-%d %H:%M:%S')

    # Get all active meeting instances
    instance_keys = r.keys(f"meeting_instance:*")
    active_meeting_instances = []
    for _key in instance_keys:
        t_instance = r.hgetall(_key)
        time_started = t_instance['fromdatetime']
        time_ended = t_instance['todatetime']
        if time_started <= current_time and current_time < time_ended:
            active_meeting_instances.append(t_instance)

    if not active_meeting_instances:
        return "[!] There are no active meetings."

    meeting_info = [(r.hgetall("meeting:"+_instance['meetingID']), _instance['fromdatetime'], _instance['todatetime']) for _instance in active_meeting_instances]
    res = f"[*] Active meetings are: \n"
    res += ''.join([f"\t [id:{_meeting['meetingID']}] Meeting '{_meeting['title']}' from {_from} to {_to} \n" for _meeting, _from, _to in meeting_info])

    return res

   
if __name__ == '__main__':
    r.flushdb()
    createDB.createDB()

    print(join_meeting(1, 1))
    time.sleep(1)
    print(join_meeting(2, 1))
    time.sleep(1)
    print(join_meeting(1, 2))
    time.sleep(1)
    print(join_meeting(2, 2))
    time.sleep(1)
    print(leave_meeting(1, 1))
    time.sleep(1)
    print(leave_meeting(1, 1))
    time.sleep(1)
    print(meeting_participants(1))
    time.sleep(1)
    print(meeting_participants(2))
    print(show_active_meetings())




        
