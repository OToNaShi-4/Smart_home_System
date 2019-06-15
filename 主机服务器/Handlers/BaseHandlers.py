import functools
import json
import time
from uuid import uuid4
from mako import lookup
from tornado import web
from _Config import *
from utils import Session


class BaseHandler(web.RequestHandler):
    """Handler 基类"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.look_up = lookup.TemplateLookup([self.get_template_path()], input_encoding='utf-8',
                                             output_encoding='utf-8')
        self.con = None
        self.time1 = time.time()

    async def prepare(self):
        """若接受到json数据则提前预处理，并自动将application/json添加到headre里"""
        if self.request.headers.get("Content-Type", "").startswith("application/json"):
            # 当请求头内有application/json时，解析请求中的json数据
            self.set_header("Content-Type", "application/json")
            self.json_args = json.loads(self.request.body)
        else:
            self.json_args = {}

    def render(self, template_name: str, **kwargs: any):
        """在每次渲染模板时把xsrf一并设置进去"""
        self.xsrf_token  # 若是使用render提供页面的话，添加xsrf——token
        if USING_MAKO:  # 使用mako渲染
            html = self.render_string(template_name, **kwargs)
            return self.finish(html)
        else:  # 使用tornado自带模板语言渲染
            super().render(template_name, **kwargs)

    async def send(self, template_name: str):
        """直接发送html文件"""
        self.xsrf_token  # 设置xsrf_token头
        with open(os.path.join(CURRENT_PATH, 'Templates/' + template_name), 'r') as f:
            data = f.read()
        await self.finish(data)

    def render_string(self, template_name: str, **kwargs: any) -> str or bytes:
        if USING_MAKO:
            """使用mako模板替代tornado自带的模板"""
            template = self.look_up.get_template(template_name)
            env_kwargs = dict(
                handler=self,
                request=self.request,
                current_user=self.current_user,
                locale=self.locale,
                _=self.locale.translate,
                static_url=self.static_url,
                xsrf_form_html=self.xsrf_form_html,
                reverse_url=self.application.reverse_url,
            )
            env_kwargs.update(kwargs)
            return template.render(**env_kwargs)
        else:
            """使用tornado自带模板语言"""
            return super().render_string(template_name, **kwargs)

    async def get_current_user(self) -> Session:
        """
        实例化session并获取用户session数据
        若不使用自带session实现请重写本方法
        """
        if not self.get_secure_cookie('session_id'):
            self.set_secure_cookie('session_id', uuid4().hex)
        self.Session = Session.Session(self)
        await self.Session.get_data()
        return self.Session.data

    @staticmethod
    def require_login(fun):
        """
        装饰器
        用于装饰需要登录的部分
        若不使用自带session实现请重写本装饰器
        """

        @functools.wraps(fun)
        async def wraper(self, *args, **kwargs):
            self.require_loin = True
            # 当用户以post请求访问时的处理
            if self.request.headers.get("Content-Type", "").startswith("application/json"):
                if not await self.get_current_user():
                    self.set_header('Content-Type', "application/json")
                    await self.finish(json.dumps({'err_code': 400, 'err_msg': '用户未登录'}))
                    return
            # 当用户以get请求访问时的处理
            else:
                if not await self.get_current_user():
                    self.redirect('/login')
                    return
            # 若用户已经登录
            await fun(self, *args, **kwargs)

        return wraper

    @staticmethod
    def require_no_login(fun):
        """用于装饰需要用户未登录的请求"""

        @functools.wraps(fun)
        async def wraper(self, *args, **kwargs):
            # 当用户以post请求访问时的处理
            if self.request.headers.get("Content-Type", "").startswith("application/json"):
                if await self.get_current_user():
                    self.set_header('Content-Type', "application/json")
                    await self.finish(json.dumps({'err_code': 400, 'err_msg': '用户已登录'}))
                    return
            # 当用户以get请求访问时的处理
            else:
                if await self.get_current_user():
                    self.redirect('/login')
                    return
            # 若用户未经登录
            await fun(self, *args, **kwargs)

        return wraper

    @staticmethod
    def use_database(fun):
        """装饰需要用到数据库的方法"""

        @functools.wraps(fun)
        async def warper(obj, *args, **kwargs):
            async with obj.db_pool.acquire() as obj.con:
                await fun(obj, *args, **kwargs)

        return warper

    @property
    def db_pool(self):
        return self.application.db_pool

    @property
    def redis(self):
        return self.application.redis


class BaseStaticFileHandler(web.StaticFileHandler):
    """静态文件处理"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 自动添加xsrf——token
        self.xsrf_token
