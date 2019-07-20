"""Class for adding functionality to Settings modal window."""
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.modalview import ModalView
from kivy.properties import StringProperty, BooleanProperty, ListProperty, ObjectProperty
from kivy.clock import Clock, mainthread
from models.rw_galil import MotionLinkInterface
import copy
from time import sleep
import datetime
import threading
import time

class TestWindow(ModalView):
    """Add functionality to Settings modal window."""

    cycles = StringProperty('200')
    cycle = StringProperty('Default')
    delay = StringProperty('10.0')
    speed = StringProperty('20000')
    speed_out = StringProperty('20000')
    requested_position = StringProperty('180000')
    total_test_time_label = StringProperty('Default')
    time_remaining_label = StringProperty('Default')
    time_estimate_label = StringProperty('Estimated time')
    total_test_time = 0
    time_remaining = 0
    new_time_estimate = 0
    clock_rate = 1
    running = False
    new_time = 0

    def __init__(self, instance, ml_interface, **kwargs):
        """Initialize Settings modal window of main interface.

        Pull software version, title, ip address, speed, and speed out from
          MotionLink object.
        Deepcopy of MotionLink object to pass onto set_values().
        """
        super(TestWindow, self).__init__(**kwargs)
        self.ml_interface = ml_interface
        self.instance = instance
        self.cycles = '200'
        self.delay = '10.0'
        self.speed = str(self.ml_interface.speed)
        self.speed_out = str(self.ml_interface.speed_out)
        self.requested_position = str(self.ml_interface.requested_position)
        self.update_fields()

    def cycle_test(self):
        thrB = threading.Thread(target=self.start_cycle_test)
        thrB.start()

    def start_cycle_test(self):
        self.running = True
        self.new_time = 0
        self.cycles = str(int(float(self.cycles)))
        self.delay = str(float(self.delay))
        thrA = threading.Thread(target=self.schedule_updater)
        thrA.start()
        self.cycle = '0'
        for cycle in range(int(self.cycles)):
            start_time = time.time()
            if self.running:
                # Move in
                self.cycle = str(int(float(self.cycle))+1)
                print(self.cycle)
                self.instance.move_in()
                while not 'Inserted' in self.instance.current_state:
                    sleep(1)
                sleep(float(self.delay))
                self.instance.move_out()
                while not 'Retracted' in self.instance.current_state:
                    sleep(1)
                sleep(float(self.delay))
                elapsed_time = time.time() - start_time
                #if self.new_time_estimate != time_remaining:
                if self.new_time == 0:
                    self.new_time_estimate = float(elapsed_time)
                    time_new = int(float(self.new_time_estimate*(int(float(self.cycles))-int(float(self.cycle)))))
                    time_total = int(float(self.new_time_estimate*int(float(self.cycles))))
                    self.time_remaining = datetime.timedelta(seconds=time_new)
                    self.total_test_time = datetime.timedelta(seconds=time_total)
                    self.time_remaining_label = str(self.time_remaining)
                    self.total_test_time_label = str(self.total_test_time)
                    time_estimate_label = 'Total time'
                    self.new_time = 1


            else:
                break
        thrA.join()

    def schedule_updater(self):
        Clock.schedule_interval(self.update_time_remaining,self.clock_rate)

    @mainthread
    def abort(self):
        self.running = False

    @mainthread
    def update_fields(self):
        # Calculate time required
        self.speed = str(self.ml_interface.speed)
        self.speed_out = str(self.ml_interface.speed_out)
        self.requested_position = str(self.ml_interface.requested_position)
        if self.new_time == 1:
            time_per_cycle = self.new_time_estimate
        else:
            time_per_move_in = float(self.requested_position)/float(self.speed)
            time_per_move_out = float(self.requested_position)/float(self.speed_out)
            time_per_cycle = time_per_move_in + time_per_move_out + 2*float(self.delay)
        total_time = int(int(float(self.cycles))*time_per_cycle)
        self.total_test_time = datetime.timedelta(seconds=total_time)
        self.total_test_time_label = str(self.total_test_time)
        self.time_remaining = self.total_test_time
        self.time_remaining_label = str(self.time_remaining)


    @mainthread
    def update_time_remaining(self,*args):
        self.time_remaining = self.time_remaining - datetime.timedelta(seconds=self.clock_rate)
        if self.time_remaining <= datetime.timedelta(seconds=0):
            self.time_remaining_label = str(datetime.timedelta(seconds=0))
        else:
            self.time_remaining_label = str(self.time_remaining)
