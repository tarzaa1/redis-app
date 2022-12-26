from walrus import Database
import os

redis_host = os.environ.get('REDISHOST', 'localhost')
redis_port = os.environ.get('REDISPORT', 6379)
redis_stream = os.environ.get('REDISSTREAM', 'mystream')
last_id = None


db = Database(host=redis_host, port=redis_port)
stream = db.Stream(redis_stream)

while True:
    message = stream.read(count=1, last_id = last_id)
    if message:
        last_id = message[-1][0]
        print(message)