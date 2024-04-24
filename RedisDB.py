import redis 

class RedisDB:

    # Connect to Redis
    def __init__(self, host='localhost', port=6379):
        self.__r = redis.Redis(host=host, port=port, decode_responses=True)

    
    def __createUsers(self):
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
            self.__r.hset(f"user:{user['userID']}", mapping=user)


    def __createMeetings(self):
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
            self.__r.hset(f"meeting:{meeting['meetingID']}", mapping=meeting)


    def __createMeetingInstances(self):
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
                'todatetime': '2024-04-24 04:49:00'
            }
        ]

        for _instance in meeting_instances:
            self.__r.hset(f"meeting_instance:{_instance['meetingID']}:{_instance['orderID']}", mapping=_instance)


    def __createEventsLog(self):
        self.__r.set('event_id_counter', 1)


    def createDB(self):
        self.__createUsers()
        self.__createMeetings()
        self.__createMeetingInstances()
        self.__createEventsLog()
        print("[>] Database created successfully.\n")


    def exists(self, key):
        return self.__r.exists(key)
    
    def push(self, key, value, left=True):
        if left:
            self.__r.lpush(key, value)
        else:
            self.__r.rpush(key, value)

    def range(self, key, start, end):
        return self.__r.lrange(key, start, end)
    
    def set(self, key, value, hash=True):
        if not hash:
            self.__r.set(key, value)

        self.__r.hset(key, mapping=value)

    def get(self, key, hash=True, all=True, field=None):
        if not hash:
            return self.__r.get(key)
        
        if not all:
            return self.__r.hget(key, field)
        
        return self.__r.hgetall(key)
    
    def getKeys(self, pattern):
        return self.__r.keys(pattern)

    def increase(self, key):
        self.__r.incr(key)

    def clearDB(self):
        self.__r.flushdb()

if __name__ == '__main__':
    
    db = RedisDB()
    db.clearDB()
    db.createDB()
