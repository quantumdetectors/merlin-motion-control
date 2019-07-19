"""Class for adding functionality to Settings modal window."""
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.modalview import ModalView
from kivy.properties import StringProperty, BooleanProperty, ListProperty, ObjectProperty
from kivy.clock import Clock
from models.rw_galil import MotionLinkInterface
import copy
from time import sleep
from datetime import datetime
import threading





class TestWindow(FloatLayout):
    """Add functionality to Settings modal window."""

    cycles = StringProperty('200')
    cycle = StringProperty('Default')
    delay = StringProperty('10.0')
    speed = StringProperty('20000')
    speed_out = StringProperty('20000')
    requested_position = StringProperty('180000')
    total_test_time_label = StringProperty('Default')
    time_remaining_label = StringProperty('Default')
    total_test_time = 0
    time_remaining = 0
    clock_rate = 1


    def __init__(self, instance, ml_interface, **kwargs):
        """Initialize Settings modal window of main interface.

        Pull software version, title, ip address, speed, and speed out from
          MotionLink object.
        Deepcopy of MotionLink object to pass onto set_values().
        """
        super(TestWindow, self).__init__(**kwargs)
        self.ml_interface = ml_interface
        self.instance = instance
        self.ml_interface.debug = True
        self.cycles = '200'
        self.delay = '10.0'
        self.speed = str(self.ml_interface.speed)
        self.speed_out = str(self.ml_interface.speed_out)
        self.requested_position = str(self.ml_interface.requested_position)


        def start_cycle_test(self):
            self.cycles = str(int(float(self.cycles)))
            self.delay = str(float(self.delay))
            thrA = threading.Timer(self.clock_rate, update_time_remaining)
            #Clock.schedule_interval(self.update_time_remaining,self.clock_rate)
            for cycle in range(int(self.cycles)):
                # Move in
                self.cycle = cycle
                self.instance.move_in()
                sleep(float(self.delay))
                self.instance.move_out()
                sleep(float(self.delay))


        def update_fields(self):
            # Calculate time required
            time_per_move_in = float(self.requested_position)/float(self.speed)
            time_per_move_out = float(self.requested_position)/float(self.speed_out)
            time_per_cycle = time_per_move_in + time_per_move_out + 2*float(self.delay)
            total_time = int(int(float(self.cycles))*time_per_cycle)
            self.total_test_time = datetime.timedelta(seconds=total_time)
            self.total_test_time_label = str(self.total_test_time)
            self.time_remaining = self.total_test_time
            self.time_remaining_label = str(self.time_remaining)



        def update_time_remaining(self):
            self.time_remaining = self.time_remaining - datetime.timedelta(seconds=self.clock_rate)
            self.time_remaining_label = str(self.time_remaining)
