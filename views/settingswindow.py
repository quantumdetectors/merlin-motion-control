from kivy.uix.gridlayout import GridLayout
from kivy.uix.modalview import ModalView
from kivy.properties import StringProperty, BooleanProperty, ListProperty
from kivy.clock import Clock
from models.galil import MotionLink
import copy



class SettingsWindow(ModalView):
    software_version = StringProperty('Def')
    ip_address = StringProperty('Def')
    speed = StringProperty('Def')
    speed_out = StringProperty('Def')
    def __init__(self, ml_object, **kwargs):
        super(SettingsWindow, self).__init__(**kwargs)
        self.software_version = str(ml_object.software_version)
        self.ip_address = str(ml_object.ip_address)
        self.speed = str(ml_object.speed)
        self.speed_out = str(ml_object.speed_out)
        self.ml = copy.deepcopy(ml_object)

    def set_values(self):
        self.ml.software_version = self.software_version
        self.ml.ip_address = self.ip_address
        self.ml.speed = self.speed
        self.ml.speed_out = self.speed_out
        self.ml.set_values()
