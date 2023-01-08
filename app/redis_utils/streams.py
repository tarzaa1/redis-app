from walrus import Database

from .base import BasicStream, StreamFactory

class RedisStreamAndConsume(BasicStream):

    def __init__(self, redis_db, key, max_stream_length=None, block=0, create_cg=True):
        BasicStream.__init__(self, key)
        self.block = block
        self.redis_db = redis_db
        self.create_cg = create_cg
        self.output_stream = self._get_stream(key)
        self.input_consumer_group = self._get_consumer_group(key)
        self.max_stream_length = max_stream_length
        self.default_write_kwargs = self._get_default_write_kwargs()

    def _get_default_write_kwargs(self):
        write_kwargs = {}
        if self.max_stream_length is not None:
            write_kwargs.update({
                'maxlen': self.max_stream_length,
                'approximate': False
            })
        return write_kwargs

    def _get_consumer_group(self, key):
        cg_name = 'cg-%s' % key
        cg = self.redis_db.consumer_group(cg_name, key)
        if self.create_cg:
            cg.create()
        cg.set_id(id='$')
        return cg

    def write_events(self, *events):
        return [
            self.output_stream.add(event, **self.default_write_kwargs) for event in events
        ]

    def read_events(self, count=1):
        stream_event_list = self.input_consumer_group.read(count=count, block=self.block)
        for stream_key, event_list in stream_event_list:
            yield from event_list

    def _get_stream(self, key):
        return self.redis_db.Stream(key)

class RedisStreamOnly(BasicStream):

    def __init__(self, redis_db, key, max_stream_length=None, block=0):
        BasicStream.__init__(self, key)
        self.block = block
        self.redis_db = redis_db
        self.stream = self._get_stream(key)
        self.event_id = None
        if self.stream.length() != 0:
            self.event_id = self.stream.info()['last-entry'][0]
        self.max_stream_length = max_stream_length
        self.default_write_kwargs = self._get_default_write_kwargs()

    def _get_default_write_kwargs(self):
        write_kwargs = {}
        if self.max_stream_length is not None:
            write_kwargs.update({
                'maxlen': self.max_stream_length,
                'approximate': False
            })
        return write_kwargs

    def write_events(self, *events):
        return [
            self.stream.add(event, **self.default_write_kwargs) for event in events
        ]

    def read_events(self, count=1):
        events = self.stream.read(count=count, last_id=self.event_id, block=self.block)
        if events:
            self.event_id = events[-1][0]
            yield from events

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
        elif stype == 'streamOnly':
            return RedisStreamOnly(self.redis_db, key, max_stream_length=self.max_stream_length, block=self.block)