import redis 

# Connect to Redis
r = redis.Redis(host='localhost', port=6379, decode_responses=True)

def createUsers():
    users = [
        {
            'userID': 1,
            'name': 'Christos',
            'age': 26,
            'gender': 'male',
            'email': 'p3200150@aueb.gr',
        },
        {
            'userID': 2,
            'name': 'Petros',
            'age': 20,
            'gender': 'male',
            'email': 'p3200300@aueb.gr',
        },
    ]

    for user in users:
        r.hset(f"user:{user['userID']}", mapping=user)

def createMeetings():
    meetings = [
        {
            'meetingID': 1,
            'title': 'Student Meeting',
            'description': 'General meeting for students.',
            'isPublic': 'True',
            'audience': 'all'
        },
        {
            'meetingID': 2,
            'title': 'Teacher Meeting',
            'description': 'Invitation only meeting for teachers.',
            'isPublic': 'False',
            'audience': b'p3200150@aueb.gr,p3200400@aueb.gr'
        },
        {
            'meetingID': 3,
            'title': 'Test Meeting',
            'description': 'This is a test purpose meeting.',
            'isPublic': 'True',
            'audience':'all'
        }
    ]

    for meeting in meetings:
        r.hset(f"meeting:{meeting['meetingID']}", mapping=meeting)


def createMeetingInstances():
    meeting_instances = [
        {
            'meetingID': 1,
            'orderID': 1,
            'fromdatetime': '2024-04-20 10:00:00',
            'todatetime': '2024-04-20 11:00:00'
        },
        {
            'meetingID': 1,
            'orderID': 2,
            'fromdatetime': '2024-04-20 12:00:00',
            'todatetime': '2024-04-20 13:00:00'
        },
        {
            'meetingID': 1,
            'orderID': 3,
            'fromdatetime': '2024-04-20 15:00:00',
            'todatetime': '2024-05-13 13:00:00'
        },
        {
            'meetingID': 2,
            'orderID': 1,
            'fromdatetime': '2024-04-20 10:00:00',
            'todatetime': '2024-04-20 11:00:00'
        },
        {
            'meetingID': 2,
            'orderID': 2,
            'fromdatetime': '2024-04-20 12:00:00',
            'todatetime': '2024-04-20 13:00:00'
        },
        {
            'meetingID': 2,
            'orderID': 3,
            'fromdatetime': '2024-04-20 15:00:00',
            'todatetime': '2024-05-13 13:00:00'
        },
        {
            'meetingID': 3,
            'orderID': 1,
            'fromdatetime': '2024-04-21 01:00:00',
            'todatetime': '2024-04-21 04:37:00'
        }
    ]

    for _instance in meeting_instances:
        r.hset(f"meeting_instance:{_instance['meetingID']}:{_instance['orderID']}", mapping=_instance)


def createEventsLog():
    r.set('event_id_counter', 1)


def createDB():
    createUsers()
    createMeetings()
    createMeetingInstances()
    createEventsLog()


if __name__ == '__main__':
    createDB()