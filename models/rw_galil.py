from kivy.clock import Clock, mainthread
from models.galil import MotionLink
from functools import partial
import threading
import time

class MotionLinkInterface():
    rp = '0'
    gatan_in = 1
    gatan_veto = 1
    is_connected = False
    speed = '0'
    speed_out = '0'
    mer_ip_address = '0.0.0.0'
    debug = False
    software_version = '0'
    software_title = '0'

    def __init__(self):
        self.ml = MotionLink()
        threading.Thread(target=self.thread_function).start()

    def with_connection(fn):
        def wrapper(self,*args,**kwargs):
            if self.is_connected:
                return fn(self, *args, **kwargs)
        return wrapper

    def thread_function(self):
        Clock.schedule_interval(self.read, 0.01)


    def read(self, *args):
        self.is_connected = self.ml._connected
        if not self.is_connected:
            self.ml.connect()
        else:
            self.rp = self.ml.read_rp()
            self.gatan_in = self.ml.get_gatan_in()
            self.gatan_veto = self.ml.get_gatan_veto()

    @with_connection
    def write(self):
        self.ml.speed = self.speed
        self.ml.speed_out = self.speed_out
        self.ml.mer_ip_address = self.mer_ip_address
        self.ml.debug = self.debug
        self.ml.software_version = self.software_version
        self.ml.software_title = self.software_title
        self.ml.set_values()

    @with_connection
    def move(self, arg):
        self.ml.move(arg)

    @with_connection
    def stop(self):
        self.ml.stop()
