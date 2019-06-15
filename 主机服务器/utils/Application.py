from tornado import web
from utils.CustomError import *


class Application(web.Application):
    _devices = dict()  # 储存WebSocket客户端实例

    def __init__(self, db_pool=None, redis_pool=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._db_pool = db_pool
        self._redis = redis_pool

    @property
    def db_pool(self):
        if self._db_pool:
            return self._db_pool.pool
        else:
            raise NoneMysqlPool

    @property
    def redis(self):
        if self._redis:
            return self._redis.pool
        else:
            raise NoneRedisPool

    @property
    def devices(self):
        return self._devices
