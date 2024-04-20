import redis 

# Connect to Redis
r = redis.Redis(host='localhost', port=6379, decode_responses=True)

# Set a key


# Get a key
print(r.get('name'))

