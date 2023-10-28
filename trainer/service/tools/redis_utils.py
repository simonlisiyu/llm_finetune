import redis
from ...settings import Settings

my_settings = Settings()


class RedisSingleton:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, host='localhost', port=6379, db=0, password=None):
        self._redis = redis.Redis(host=host, port=port, db=db, password=password)

    def get_redis(self):
        return self._redis
