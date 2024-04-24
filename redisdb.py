import redis 

class RedisDB:

    def __init__(self, host='localhost', port=6379, db=0):
        # Connect to the Redis server
        self.__r = redis.Redis(host=host, port=port, decode_responses=True, db=db)
        print(f"[>] Database '{db}' connected successfully!\n")

    
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


if __name__ == '__main__':
    
    db = RedisDB()
    db.clearDB()
