import redis 

class RedisDB:

    def __init__(self, host='localhost', port=6379):
        # Connect to the Redis server
        self.__r = redis.Redis(host=host, port=port, decode_responses=True)

    
    # Initialize the database
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
            self.set(f"user:{user['userID']}", value=user)

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
            self.set(f"meeting:{meeting['meetingID']}", value=meeting)

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
                'todatetime': '2024-04-24 17:20:00'
            }
        ]

        for _instance in meeting_instances:
            self.set(f"meeting_instance:{_instance['meetingID']}:{_instance['orderID']}", value=_instance)

    def __createEventsLog(self):
        self.set('event_id_counter', hash=False, value=1)


    # Redis Commands
    def exists(self, key):
            """
            Check if a key exists in the Redis database.

            Args:
                key (str): The key to check.

            Returns:
                bool: True if the key exists, False otherwise.
            """
            return self.__r.exists(key)
    
    def push(self, key, value, left=True):
            """
            Pushes a value to a Redis list.

            Args:
                key (str): The key of the Redis list.
                value (str): The value to be pushed.
                left (bool, optional): If True, the value is pushed to the left of the list. 
                                       If False, the value is pushed to the right. 
                                       Defaults to True.
            """
            if left:
                self.__r.lpush(key, value)
            else:
                self.__r.rpush(key, value)

    def range(self, key, start=0, end=-1):
            """
            Retrieve a range of elements from a list stored in Redis.

            Args:
                key (str): The key of the list in Redis.
                start (int): The starting index of the range (inclusive). Default is 0.
                end (int): The ending index of the range (inclusive). Default is -1.

            Returns:
                list: A list containing the elements in the specified range.

            """
            return self.__r.lrange(key, start, end)
    
    def set(self, key, value, hash=True):
        """
        Set the value of a key in the Redis database.

        Args:
            key (str): The key to set.
            value (str): The value to set.
            hash (bool, optional): Whether to use Redis hash or string data type. Defaults to True.

        Returns:
            None
        """
        if not hash:
            self.__r.set(key, value)
            return

        self.__r.hset(key, mapping=value)

    def get(self, key, hash=True, all=True, field=None):
            """
            Retrieve data from Redis based on the provided key and options.

            Args:
                key (str): The key to retrieve data from.
                hash (bool, optional): Specifies whether the key is a hash or not. Defaults to True.
                all (bool, optional): Specifies whether to retrieve all fields or not. Defaults to True.
                field (str, optional): The specific field to retrieve if `all` is False. Defaults to None.

            Returns:
                str or dict: The retrieved data from Redis.
            """
            if not hash:
                return self.__r.get(key)
            
            if not all:
                return self.__r.hget(key, field)
            
            return self.__r.hgetall(key)
    
    def getKeys(self, pattern):
        """
        Retrieve keys from the Redis database that match the given pattern.

        Args:
            pattern (str): The pattern to match the keys against.

        Returns:
            list: A list of keys that match the given pattern.
        """
        return self.__r.keys(pattern)

    def increase(self, key):
        """
        Increase the value of the specified key by 1.

        Args:
            key (str): The key to increase the value of.

        Returns:
            None
        """
        self.__r.incr(key)


    # Database Operations
    def clearDB(self):
        """
        Clears all the data in the Redis database.
        """
        self.__r.flushdb()

    def initDB(self):
        """
        Initializes the database by creating necessary tables and prints a success message.
        """
        self.__createUsers()
        self.__createMeetings()
        self.__createMeetingInstances()
        self.__createEventsLog()
        print("[>] Database created successfully.\n")

    def resetDB(self):
        """
        Resets the Redis database by clearing it and initializing it again.
        """
        self.clearDB()
        self.initDB()


if __name__ == '__main__':
    
    db = RedisDB()
    db.resetDB()
