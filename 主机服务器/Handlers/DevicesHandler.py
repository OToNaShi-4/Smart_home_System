from tornado.websocket import WebSocketHandler
import json


class ClientHandelr(WebSocketHandler):
    request_handler = None

    def __init__(self, *args, **kwargs):
        """类初始化方法"""
        super(ClientHandelr, self).__init__(*args, **kwargs)
        self.session_id = None

    async def open(self, *args: str, **kwargs: str):
        """客户端第一次链接时执行的方法"""
        self.session_id = self.get_argument('session_id')
        self.application.devices[self.session_id] = self  # 往设备堆中添加当前设备实例
        pass

    async def on_message(self, message):
        """当接收到客户端消息时执行的方法"""
        if self.request_handler:
            await self.request_handler.write(message)
        self.request_handler = None

        pass

    def bind(self, obj):
        self.request_handler = obj
        return self

    def on_close(self) -> None:
        """当客户端离线时执行的方法"""
        del (self.devices[self.session_id])  # 从设备堆中删除当前设备实例

    @property
    def devices(self):
        return self.application.devices
