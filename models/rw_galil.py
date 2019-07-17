""" """
from kivy.clock import Clock, mainthread
from models.galil import MotionLink
from functools import partial
import threading
import time
from tests.ping import ping

is_connected = False
ip_address = '0.0.0.0'
CLOCK_SPEED = 0.00001


class Thread_A(threading.Thread):

        def __init__(self, name):
            threading.Thread.__init__(self)
            self.name = name

        def run(self):
            global ip_address
            Clock.schedule_interval(self.attempt_connection, CLOCK_SPEED)

        def attempt_connection(self,chk_ml,*args):
            global is_connected
            global ip_address
            is_connected = ping(ip_address)



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
    requested_position = '0'
    current_state = '0'
    global is_connected
    global ip_address

    def __init__(self):
        Clock.schedule_interval(self.poll_connection_status, CLOCK_SPEED)
        threading.Thread(target=self.thread_function).start()
        self.threadA = Thread_A("Connection verification")
        self.threadA.start()
        self.ml = MotionLink()
        self.is_connected = is_connected
        self._is_connected = False

    def with_connection(fn):
        def wrapper(self,*args,**kwargs):
            if self.is_connected:
                return fn(self, *args, **kwargs)
        return wrapper

    @mainthread
    def poll_connection_status(self, *args):
        global is_connected
        self.is_connected = is_connected
        if self.is_connected:
            self.set_requested_position()
        self._is_connected = self.is_connected

    def thread_function(self):
        Clock.schedule_interval(self.read, 100*CLOCK_SPEED)

    def read(self, *args):
        if self.is_connected:
            self.rp = self.ml.read_rp()
            self.gatan_in = self.ml.get_gatan_in()
            self.gatan_veto = self.ml.get_gatan_veto()
            self.current_state = self.ml.read_merstat()

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
    def set_requested_position(self):
        self.ml.set_requested_position(self.requested_position)

    @with_connection
    def move(self, arg):
        self.ml.move(arg)

    @with_connection
    def stop(self):
        self.ml.stop()
