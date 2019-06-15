import RPi.GPIO as gpio
import websocket
import json
import time


class Devices(websocket.WebSocketApp):
    stat = False
    s_id = 'main_devices'

    def __init__(self, *args, **kwargs):
        super(Devices, self).__init__(on_message=self.on_message, *args, **kwargs)
        self.gpio = gpio
        self.gpio.setmode(gpio.BCM)
        gpio.setwarnings(False)
        self.gpio.setup(17, gpio.OUT)
        self.gpio.output(17, self.stat)

    def on_message(self, msg):
        data = json.loads(msg)
        print(data)
        if data['type'] == 'get_stat':
            self.send(json.dumps({'type': 'stat', 'stat': '1' if self.stat else '0'}))
        elif data['type'] == 'change_stat':
            if data['stat'] == 'on':
                try:
                    self.stat = True
                    self.gpio.output(17, self.stat)
                except Exception:
                    self.stat = not self.stat
                    self.send(json.dumps({'type': 'res', 'stat': '1' if self.stat else '0'}))
                finally:
                    self.send(json.dumps({'type': 'res', 'stat': '1' if self.stat else '0'}))
            elif data['stat'] == 'off':
                try:
                    self.stat = False
                    self.gpio.output(17, self.stat)
                except Exception:
                    self.stat = not self.stat
                    self.send(json.dumps({'type': 'res', 'stat': '1' if self.stat else '0'}))
                finally:
                    self.send(json.dumps({'type': 'res', 'stat': '1' if self.stat else '0'}))

    def on_error(self, error):
        print(error)




if __name__ == '__main__':
    websocket.enableTrace(True)
    while True:
        ws = Devices('ws://192.168.31.44:8000/websocket?session_id=' + Devices.s_id)
        ws.run_forever()
        print('连接失败或断开，在一秒后尝试重连')
        time.sleep(1)  # 若断开或未成功连接则在一秒后尝试重连
