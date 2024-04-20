import redis
import time

# Connect to Redis
r = redis.Redis(host='localhost', port=6379, decode_responses=True)

def join_meeting(userID, meetingID):
    
    # Check if meeting exists
    meeting = None
    if not r.exists(f"meeting:{meetingID}"):
        return "[!] Meeting does not exist."
    else:
        meeting = r.hgetall(f"meeting:{meetingID}")

    # Check if user exists
    user = None
    if not r.exists(f"user:{userID}"):
        return "[!] User does not exist."
    else:
        user = r.hgetall(f"user:{userID}")
    
    #Check if meeting instances exists
    instance_keys = r.keys(f"meeting_instance:{meetingID}:*")   
    if not instance_keys:
        return "[!] Meeting instance does not exist."
    
    meeting_instance = None
    for _instance in instance_keys:
        t_instance = r.hgetall(_instance)
        if t_instance['fromdatetime'] > time.strftime('%Y-%m-%d %H:%M:%S'):
            #return "[!] Meeting has not started yet."
            continue
        if t_instance['todatetime'] < time.strftime('%Y-%m-%d %H:%M:%S'):
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
            return "[!] User is not invited to the meeting."
        
    # Log the event
    event_id = r.get('event_id_counter')
    event_type = 1
    timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
    event = {
        'event_id': event_id,
        'userID': userID,
        'event_type': event_type,
        'timestamp': timestamp
    }
    r.hset(f"event_id:{event_id}:{userID}", mapping=event)  
    r.incr('event_id_counter')

    return f"[+] User '{user['name']}' joined meeting '{meeting['title']}' at {timestamp}."


def leave_meeting(userID, meetingID):
    time_left = time.strftime('%Y-%m-%d %H:%M:%S')

    # Check if meeting exists
    meeting = None
    if not r.exists(f"meeting:{meetingID}"):
        return "[!] Meeting does not exist."
    else:
        meeting = r.hgetall(f"meeting:{meetingID}")

    # Check if user exists
    user = None
    if not r.exists(f"user:{userID}"):
        return "[!] User does not exist."
    else:
        user = r.hgetall(f"user:{userID}")

    # Get all events of the user in reverse order to find the last joined event
    user_events = r.keys(f"event_id:*:{userID}") 
    user_events.reverse()

    if not user_events:
        return "[!] User has not joined the meeting yet 1."
    
    for event in user_events:

        if r.hget(event, 'event_type') == '1':

            time_joined = r.hget(event, 'timestamp')
            if time_joined < time_left:
                
                # Log the event
                event_id = r.get('event_id_counter')
                event_type = 2
                timestamp = time_left
                event = {
                    'event_id': event_id,
                    'userID': userID,
                    'event_type': event_type,
                    'timestamp': timestamp
                }
                r.hset(f"event_id:{event_id}:{userID}", mapping=event)
                r.incr('event_id_counter')

                return f"[+] User '{user['name']}' left meeting '{meeting['title']}' at {timestamp}."
            else:
                return "[!] User has not joined the meeting yet 2."
            
    return "[!] User has not joined the meeting yet 3."
     

    



if __name__ == '__main__':
    print(join_meeting(1, 1))
    time.sleep(2)
    print(leave_meeting(1, 1))




        
