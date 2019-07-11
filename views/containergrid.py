from kivy.uix.gridlayout import GridLayout
from kivy.properties import StringProperty, BooleanProperty
from views.actionbuttons import ActionButtons
from views.statusfields import StatusFields
from views.labels import Labels
from models.galil import MotionLink
from kivy.clock import Clock


class ContainerGrid(GridLayout):
    rp = StringProperty('1000')


    def __init__(self, **kwargs):
        super(ContainerGrid, self).__init__(**kwargs)
        Clock.schedule_interval(self.update_status_fields, 0.1)
        self.ml = MotionLink()
        self.ml.debug = True

    def update_status_fields(self, *args):
        self.rp = self.ml.read_rp()
