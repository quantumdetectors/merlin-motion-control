"""Class for adding functionality to Settings modal window."""
from kivy.uix.gridlayout import GridLayout
from kivy.uix.modalview import ModalView
from kivy.properties import StringProperty, BooleanProperty, ListProperty
from kivy.clock import Clock
from models.galil import MotionLink
import copy
from time import sleep


class SettingsWindow(ModalView):
    """Add functionality to Settings modal window."""

    software_version = StringProperty('Def')
    software_title = StringProperty('Def')
    ip_address = StringProperty('Def')
    speed = StringProperty('Def')
    speed_out = StringProperty('Def')
    standby_position = StringProperty('Def')
    requested_position = StringProperty('Def')

    def __init__(self, ml_object, main_screen, **kwargs):
        """Initialize Settings modal window of main interface.

        Pull software version, title, ip address, speed, and speed out from
          MotionLink object.
        Deepcopy of MotionLink object to pass onto set_values().
        """

        super(SettingsWindow, self).__init__(**kwargs)
        self.software_version = str(ml_object.software_version)
        self.software_title = str(ml_object.software_title)
        self.ip_address = str(ml_object.mer_ip_address)
        self.speed = str(ml_object.speed)
        self.speed_out = str(ml_object.speed_out)
        self.standby_position = str(ml_object.standby_position)
        self.requested_position = str(ml_object.requested_position)
        self.ml = ml_object
        self.main = main_screen
        
        self.set_values()

    def set_values(self):
        """Update values of MotionLink object when called.

        After MotionLink object has been updated, update own values based on
          the current ones of the MotionLink object.
        """

        # Hard coded value for maximum/minimum speed for insertion/retraction
        self.max_speed = 20000
        self.min_speed = 40000
        
        
        self.ml.mer_ip_address = self.ip_address

        # Now if you try to set speed over a maximum through the settings window
        # it will setting back to the hard codded value (CETA collision prevention)
        if int(self.speed) > self.max_speed:
            self.ml.speed = str(self.max_speed)
        else :
            self.ml.speed = self.speed
            
        # Now if you try to set speed under a minimum through the settings window
        # it will set it back to the hard codded value  (CETA collision prevention)
        if int(self.speed_out) < self.min_speed:
            self.ml.speed_out = str(self.min_speed)
        else :
            self.ml.speed_out = self.speed_out

        self.ml.standby_position = self.standby_position
        self.ml.requested_position = self.requested_position
        self.ml.update_ml()
        self.ml.write()
        self.ip_address = self.ml.mer_ip_address
        self.speed = str(self.ml.speed)
        self.speed_out = str(self.ml.speed_out)
        self.standby_position = str(self.ml.standby_position)
        self.requested_position = str(self.ml.requested_position)   
        self.main.set_requested_position()
        self.main.set_standby_position()

    def update_fields(self):
        self.ip_address = self.ml.mer_ip_address
        self.speed = str(self.ml.speed)
        self.speed_out = str(self.ml.speed_out)
        self.standby_position = str(self.ml.standby_position)
        self.requested_position = str(self.ml.requested_position)
