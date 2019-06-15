import asyncio
import aiomysql
import aioredis


class AioRedis:
    def __init__(self, *args, **kwargs):
        loop = asyncio.get_event_loop()
        self.pool = loop.run_until_complete(self.init_redis(*args, **kwargs))

    async def init_redis(self, *args, **kwargs):
        """redis连接池初始化函数"""
        return await aioredis.Redis(aioredis.ConnectionsPool(*args, **kwargs))


class AioMysql:
    def __init__(self,*args, **kwargs):
        loop = asyncio.get_event_loop()
        self.pool = loop.run_until_complete(self.init_mysql(*args, **kwargs))

    async def init_mysql(self, *args, **kwargs):
        """数据库连接池初始化函数"""
        return await aiomysql.create_pool(*args, **kwargs)
