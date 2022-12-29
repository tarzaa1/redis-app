from walrus import Database

from .base import BasicStream, StreamFactory

class RedisStreamAndConsume(BasicStream):

    def __init__(self, redis_db, key, max_stream_length=None, block=0):
        super.__init__(self, key)
        self.block = block
        self.redis_db = redis_db
        self.stream = self._get_stream(key)
        self.max_stream_length = max_stream_length

    def write_events(self, *events):
        return [
            self.stream.add(event) for event in events
        ]

    def read_events(self, count=1, last_id=None):
        return self.stream.read(count, last_id)


    def _get_stream(self, key):
        return self.redis_db.Stream(key)



class RedisStreamFactory(StreamFactory):

    def __init__(self, host='localhost', port=6379, max_stream_length=None, block=0):
        self.block = block
        self.max_stream_length = max_stream_length
        self.redis_db = Database(host, port)

    def create(self, key, stype='streamAndConsume'):
        if stype == 'streamAndConsume':
            return RedisStreamAndConsume(self.redis_db, key, max_stream_length=self.max_stream_length, block=self.block)