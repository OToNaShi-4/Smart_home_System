import _Config
import asyncio
from utils.AioModels import *
from tornado import options, httpserver,ioloop
from utils.Application import Application
from Settings import *
from urls import *

options.define('port', type=int, default=_Config.DEFAULT_SERVER_PORT)


if __name__ == '__main__':
    options.parse_command_line()

    app = Application(
        AioMysql(**mysql_options),
        AioRedis(**redis_options),
        urls,
        **settings
    )
    server = httpserver.HTTPServer(app)
    server.bind(options.options.port)
    server.start()
    ioloop.IOLoop.current().start()
