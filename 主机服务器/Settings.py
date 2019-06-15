import os
import _Config

current_path = os.path.dirname(__file__)

settings = {  # TODO:服务器设置
    'static_path': os.path.join(current_path, 'Statics'),
    'template_path': os.path.join(current_path, 'Templates'),
    'cookie_secret': _Config.COOKIE_SECRET,
    'xsrf_cookies': _Config.XSRF_PROECT_TUNER,
    'debug': _Config.DEBUG_TUNER,
    'autoreload': _Config.AUTO_RELOAD,
    'xheaders': True
}

mysql_options = {  # TODO:mysql数据库设置
    'host': '127.0.0.1',
    'port': 3306,
    'db': 'host_server_db',
    'user': 'root',
    'password': '12345678'
}
# TODO: redis设置
redis_options = {
    'address': ('127.0.0.1', 6379),
    'minsize': 8,  # 连接池最小数量
    'maxsize': 16  # 连接池最大数量
}
