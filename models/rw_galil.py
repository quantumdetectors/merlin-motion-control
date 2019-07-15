from kivy.clock import Clock, mainthread
from models.galil import MotionLink
from functools import partial
import threading
import time

c = threading.Condition()
is_connected = False
ip_address = '0.0.0.0'
CLOCK_SPEED = 0.00001


class Thread_A(threading.Thread):
        def __init__(self, name):
            threading.Thread.__init__(self)
            self.name = name

        def run(self):
            ml = MotionLink()
            global is_connected
            global ip_address
            Clock.schedule_interval(partial(self.attempt_connection, ml), CLOCK_SPEED)

        def attempt_connection(self,chk_ml,*args):
            global is_connected
            global ip_address
            c.acquire()
            chk_ml.mer_ip_address = ip_address
            c.release()
            chk_ml.connect()
            c.acquire()
            is_connected = chk_ml._connected
            c.release()
            print(ip_address, 'is_connected=',str(is_connected))


class MotionLinkInterface():
    rp = '0'
    gatan_in = 1
    gatan_veto = 1
    #is_connected = False
    speed = '0'
    speed_out = '0'
    mer_ip_address = '0.0.0.0'
    debug = False
    software_version = '0'
    software_title = '0'
    global is_connected
    global ip_address

    def __init__(self):
        Clock.schedule_interval(self.poll_connection_status, CLOCK_SPEED)
        threading.Thread(target=self.thread_function).start()
        self.threadA = Thread_A("Connection verification")
        self.threadA.start()
        self.ml = MotionLink()
        self.is_connected = is_connected

    def with_connection(fn):
        def wrapper(self,*args,**kwargs):
            if self.is_connected:
                return fn(self, *args, **kwargs)
        return wrapper

    def poll_connection_status(self, *args):
        global is_connected
        self.is_connected = is_connected

    def thread_function(self):
        Clock.schedule_interval(self.read, 10*CLOCK_SPEED)

    def read(self, *args):
        if self.is_connected:
            self.rp = self.ml.read_rp()
            self.gatan_in = self.ml.get_gatan_in()
            self.gatan_veto = self.ml.get_gatan_veto()

    def update_ml(self):
        global ip_address
        self.ml.speed = self.speed
        self.ml.speed_out = self.speed_out
        ip_address = self.mer_ip_address
        self.ml.mer_ip_address = self.mer_ip_address
        self.ml.debug = self.debug
        self.ml.software_version = self.software_version
        self.ml.software_title = self.software_title

    @with_connection
    def write(self):
        self.ml.set_values()

    @with_connection
    def move(self, arg):
        self.ml.move(arg)

    @with_connection
    def stop(self):
        self.ml.stop()
