from walrus import Database
import os
import logging

log_format = '%(levelname)s:%(message)s'
logging.basicConfig(filename='redis-app.log', format=log_format, filemode='w', level=logging.DEBUG)

redis_host = os.environ.get('REDISHOST')
redis_port = os.environ.get('REDISPORT')
redis_stream = os.environ.get('REDISSTREAM')
last_id = None


db = Database(host=redis_host, port=redis_port)
stream = db.Stream(redis_stream)

while True:
    message = stream.read(count=1, last_id = last_id)
    if message:
        last_id = message[-1][0]
        logging.debug(f'Received message: {message}')