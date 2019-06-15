from Handlers.BaseHandlers import BaseHandler
from pymysql.err import *
import json


class IndexHandler(BaseHandler):
    """用户主页"""

    @BaseHandler.require_login
    async def get(self):
        await self.send('index.html')
        pass


class LoginHandler(BaseHandler):
    """用户登录页面"""

    @BaseHandler.require_no_login
    async def get(self):
        await self.send('login.html')
        pass

    @BaseHandler.require_no_login
    @BaseHandler.use_database
    async def post(self):
        user_email = self.json_args.get('user_email')
        user_pwd = self.json_args.get('user_pwd')
        if all((user_pwd, user_email)):  # 判断参数是否缺失
            try:
                async with self.con.cursor() as cur:
                    sql = 'select user_name,user_pwd from user_info_tb where user_email = "%s"'
                    await cur.execute(
                        sql % user_email
                    )
                    res = await cur.fetchone()
            except Exception as e:
                print(e)
                await self.finish(json.dumps({'err_code': '400', 'err_msg': '数据库错误'}))
                return
            if res[1] == user_pwd:
                await self.Session.set('user_name', res[0], True)
                await self.finish(json.dumps({'err_code': '200', 'err_msg': 'ok'}))
                return
            else:  # 若密码错误
                await self.finish(json.dumps({'err_code': '400', 'err_msg': '账号密码错误'}))
                return
            await self.finish(json.dumps({'err_code': '400', 'err_msg': '未知错误'}))
        else:  # 若参数缺失
            await self.finish(json.dumps({'err_code': '400', 'err_msg': '参数缺失'}))


class RegisterHandler(BaseHandler):
    """用户注册界面"""

    async def get(self):
        await self.send('register.html')
        pass

    @BaseHandler.use_database
    async def post(self):
        user_name = self.json_args.get('user_name')
        user_pwd = self.json_args.get('user_pwd')
        user_email = self.json_args.get('user_email')
        if all((user_email, user_name, user_pwd)):  # 检查参数是否缺失
            try:
                sql = 'insert into user_info_tb(user_name, user_email, user_pwd) values ("%s","%s","%s")'
                async with self.con.cursor() as cur:
                    await cur.execute(
                        sql % (user_name, user_email, user_pwd)
                    )
                    await self.con.commit()  # 提交sql语句
                await self.finish(json.dumps({'err_code': '200', 'err_msg': 'ok'}))
            except IntegrityError:
                await self.finish(json.dumps({'err_code': '420', 'err_msg': '用户已存在'}))
        else:  # 参数缺失返回错误信息
            await self.finish(json.dumps({'err_code': '400', 'err_msg': '参数缺失'}))


class get_stat(BaseHandler):
    """获取设备状态api接口"""

    @BaseHandler.require_login
    async def post(self):
        ws = self.application.devices['main_devices'].bind(self)
        await ws.write_message(json.dumps({'type': 'get_stat'}))


class change_stat(BaseHandler):
    """切换设备状态api接口"""

    @BaseHandler.require_login
    async def post(self):
        stat = self.json_args.get('stat')
        ws = self.application.devices['main_devices'].bind(self)
        await ws.write_message(json.dumps({'type': 'change_stat', 'stat': stat}))


