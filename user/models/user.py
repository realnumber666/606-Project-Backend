import redis

# Create a connection to the Redis server
redis_client = redis.Redis(
  host='redis-14650.c73.us-east-1-2.ec2.cloud.redislabs.com',
  port=14650,
  password='12345678')


def signup(username, password, fullName):
    # Construct the user's key by prepending a namespace
    user_key = f"user:{username}"

    # Check if the username already exists
    if redis_client.exists(user_key):
        raise Exception('Username already exists')

        # Store the user's information in a hash
    redis_client.hset(user_key, mapping={'password': password, 'fullName': fullName})


def login(username, password):
    # Construct the user's key by prepending a namespace
    user_key = f"user:{username}"

    # Check if the user exists and the password matches
    if redis_client.hexists(user_key, 'password'):
        stored_password = redis_client.hget(user_key, 'password').decode('utf-8')
        if password == stored_password:
            # Authentication successful
            return username
        else:
            # Authentication failed
            raise Exception('Invalid password')
    else:
        # User does not exist
        raise Exception('User does not exist')
