from app.redis_utils.streams import RedisStreamFactory

import os
import time

redis_host = os.environ.get('REDISHOST')
redis_port = os.environ.get('REDISPORT')
redis_stream = os.environ.get('REDISSTREAM')

def main():
    stream_factory = RedisStreamFactory(host=redis_host, port=redis_port)
    stream = stream_factory.create(redis_stream)
    events = [{'sen':1}, {'sen':2}, {'sen':3}, {'sen':4}]

    stream.write_events(*events)

if __name__ == '__main__':
    main()