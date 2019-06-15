import os

# TODO：静态变量及各服务器参数设置
# TODO:Debug开关
DEBUG_TUNER = True
# TODO:Xsrf保护开关
XSRF_PROECT_TUNER = True
# TODO:默认服务器监听端口
DEFAULT_SERVER_PORT = 8000
# TODO:cookie加密密钥
COOKIE_SECRET = 'bZJc2sWbQLKos6GkHn/VB9oXwQt8S0R0kRvJ5/xJ89E='
# TODO:工程根目录
CURRENT_PATH = os.path.dirname(__name__)
# TODO:是否缓存高访问频率页面
SAVE_CACHE = True
# TODO:session有效期 单位：秒
SESSION_VALIDITY_PERIOD = 86400
# TODO:html页面缓存有效期 单位：秒
PAGE_CACHE_VALIDITY_PERIOD = 3600
# TODO:服务器变更自动重载开关
AUTO_RELOAD = False
# TODO:session功能开关
SESSION_TUNER = True
# TODO:用户登录数限制
LOGIN_LIMIT = False
# TODO:使用mako模板语言
USING_MAKO = True
# TODO:未登录跳转地址
LOGIN_REDIRECT = '/'
