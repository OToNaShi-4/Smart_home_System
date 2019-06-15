import json
import _Config
from utils.CustomError import *

class Session(object):
    """
    session实现，基于aioredis
    所有session操作建议通过 get（） set（） save（）delete()来进行
    有关session有效期等相关设置请去_Config.py文件修改
    """

    def __init__(self, request_handler):
        self.request_handler = request_handler

    async def get_data(self):

        try:
            data = await self.request_handler.redis.get(
                'sess_id_%s' % self.request_handler.get_secure_cookie('session_id'))
            data = json.loads(data)
        except Exception:
            data = {}
        finally:
            self.data = data

    async def save(self) -> bool:
        """
        将session保存到redis当中
        session有效期请去_Config.py文件内设置
        默认单位为：秒
        """
        try:
            await self.request_handler.redis.setex('sess_id_%s' % self.request_handler.get_secure_cookie('session_id'),
                                                  _Config.SESSION_VALIDITY_PERIOD,
                                                  json.dumps(self.data))
        except Exception as e:
            print(e)
            return False

        else:
            return True

    def get(self, name) -> any:
        """获取session元素"""
        return self.data.get(name)

    def delete(self, name) -> bool:
        """删除session元素"""
        try:
            del self.data[name]
        except Exception:
            """若删除失败则抛出错误"""
            raise RedisDeleteFaildError
        else:
            return True

    async def clear(self):
        """清空当前请求Session内容"""
        await self.request_handler.redis.delete('sess_id_%s' % self.request_handler.get_secure_cookie('session_id'))

    async def set(self, name: str, value: str, auto_save: bool = False) -> None:
        """设置session元素"""
        self.data[name] = value

        if auto_save:
            await self.save()
