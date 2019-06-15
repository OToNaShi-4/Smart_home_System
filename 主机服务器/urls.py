from Handlers.BaseHandlers import *
from Handlers.Handler import *
from Handlers.DevicesHandler import *
import os

urls = [
    (r'/', IndexHandler),
    (r'/login', LoginHandler),
    (r'/register', RegisterHandler),
    (r'/websocket', ClientHandelr),
    (r'/api/get_stat', get_stat),
    (r'/api/change_stat', change_stat),
    (r"/(.*)", BaseStaticFileHandler,
     dict(path=os.path.join(os.path.dirname(__file__), "Templates")))
]
