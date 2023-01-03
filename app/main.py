#!/usr/bin/env python
from app.redis_utils.streams import RedisStreamFactory
import os
import logging

log_format = '%(levelname)s:%(message)s'
logging.basicConfig(filename='redis-app.log', format=log_format, filemode='w', level=logging.DEBUG)

redis_host = os.environ.get('REDISHOST')
redis_port = os.environ.get('REDISPORT')
redis_stream = os.environ.get('REDISSTREAM')


def main():
    stream_factory = RedisStreamFactory(host=redis_host, port=redis_port)
    stream=stream_factory.create(redis_stream)
    event_id = None

    while True:
        message = stream.read_events(last_id=event_id)
        if message:
            event_id = message[-1][0]
            logging.debug(f'Received message: {message}')

if __name__=='__main__':
    main()