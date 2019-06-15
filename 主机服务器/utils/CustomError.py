class BaseError(Exception):
    error_info = None

    def __str__(self):
        return self.error_info


class MissingKeyError(BaseError):
    def __init__(self):
        super().__init__(self)
        self.error_info = '若需要储存到数据库内，con参数不可以为空'


class MissingSourseKeyError(BaseError):
    def __init__(self):
        super().__init__(self)
        self.error_info = '爬取模式若非full则必须提供sourse参数'


class CrawlerNoneDataError(BaseError):
    def __init__(self):
        super().__init__(self)
        self.error_info = '无法爬取数据，请检查url地址是否正确'


class DuplicateContentError(BaseError):
    def __init__(self):
        super().__init__(self)
        self.error_info = '数据库出现重复内容'


class RedisDeleteFaildError(BaseError):
    def __init__(self):
        super(RedisDeleteFaildError, self).__init__(self)
        self.error_info = 'Redis数据删除失败'


class NoneRedisPool(BaseError):
    def __init__(self):
        super(NoneRedisPool, self).__init__(self)
        self.error_info = '对象不存在Redis链接池'


class NoneMysqlPool(BaseError):
    def __init__(self):
        super(NoneRedisPool, self).__init__(self)
        self.error_info = '对象不存在Mysql链接池'
