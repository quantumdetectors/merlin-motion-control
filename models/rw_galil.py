""" """
from kivy.clock import Clock, mainthread
from models.galil import MotionLink
from functools import partial
import threading
import time
from models.ping import ping

CLOCK_SPEED = 0.00001

class MotionLinkInterface():
    rp = '0'
    gatan_in = 1
    gatan_veto = 1
    speed = '0'
    speed_out = '0'
    mer_ip_address = '0.0.0.0'
    debug = bool()
    software_version = '0'
    software_title = '0'
    requested_position = '0'
    standby_position = '0'
    current_state = '0'
    is_connected = False
    _is_connected = False

    def __init__(self):
        self.ml = MotionLink()

    def initialize_poll_connection_thread(self):
        self.poll_connection_clock = Clock.schedule_interval(self.poll_connection_status, CLOCK_SPEED)

    def initialize_read_thread(self):
        self.read_clock = Clock.schedule_interval(self.read, 100*CLOCK_SPEED)

    def with_connection(fn):
        def wrapper(self,*args,**kwargs):
            if self.is_connected or self.debug:
                return fn(self, *args, **kwargs)
        return wrapper

    def poll_connection_status(self, *args):
        if not self.is_connected and not self.debug:
            self.ml.connect()
        self.is_connected = self.ml.connected
        if self.is_connected:
            self.set_requested_position()
            self.set_standby_position()
        self._is_connected = self.is_connected

    def thread_function(self):
        Clock.schedule_interval(self.read, 100*CLOCK_SPEED)

    def read(self, *args):
        if self.is_connected or self.debug:
            self.rp = self.ml.read_rp()
            self.gatan_in = self.ml.get_gatan_in()
            self.gatan_veto = self.ml.get_gatan_veto()
            self.current_state = self.ml.read_merstat()

    def update_ml(self):
        self.ml.speed = self.speed
        self.ml.speed_out = self.speed_out
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
    def set_standby_position(self):
        self.ml.set_standby_position(self.standby_position)

    @with_connection
    def move(self, arg):
        self.ml.move(arg)

    @with_connection
    def stop(self):
        self.ml.stop()

    @with_connection
    def standby(self):
        self.ml.standby()
