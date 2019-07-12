from kivy.uix.gridlayout import GridLayout
from kivy.properties import StringProperty, BooleanProperty, ListProperty
from views.actionbuttons import ActionButtons
from views.statusfields import StatusFields
from views.labels import Labels
from models.galil import MotionLink
from kivy.clock import Clock


class ContainerGrid(GridLayout):
    rp = StringProperty('1000')
    last_cycle_rp = StringProperty('Default')
    block_movement = BooleanProperty(False)
    movement_blocked = StringProperty('Default')
    requested_position = StringProperty('0')
    current_state = StringProperty('Default')
    requested_state = StringProperty('Default')
    gatan_in = StringProperty('Default')
    gatan_veto = StringProperty('Default')
    _is_connected = BooleanProperty('False')
    connection_status = StringProperty('Disconnected')


    def __init__(self, settings, **kwargs):
        super(ContainerGrid, self).__init__(**kwargs)
        Clock.schedule_interval(self.update_status_fields, 0.1)
        self.settings = settings
        self.ml = MotionLink()
        self.ml.debug = True
        self.ml.ip_address = self.settings["ip_address"]
        self.ml.speed = self.settings["speed"]
        self.ml.speed_out = self.settings["speed_out"]

    def move_in(self):
        if self.current_state is not 'Stopped':
            self.requested_state = 'Inserted'
            if not self.block_movement:
                self.ml.move(1)

    def move_out(self):
        self.requested_state = 'Retracted'
        self.ml.move(0)

    def stop(self):
        self.requested_state = 'Stopped'
        self.ml.stop()

    def update_status_fields(self, *args):
        self.rp = self.ml.read_rp()
        if self.requested_position > self.settings["max_position"]:
            self.requested_position = self.settings["max_position"]

        if not self.block_movement and int(self.rp) > int(self.requested_position):
            self.ml.stop()
            self.block_movement = True
        elif self.block_movement and int(self.rp) < int(self.requested_position):
            self.block_movement = False


        if self.requested_state is 'Stopped':
            self.current_state = self.requested_state
        elif self.rp is self.last_cycle_rp and int(self.rp) > 0:
            self.current_state = 'Inserted'
        elif self.rp is self.last_cycle_rp and int(self.rp) > 0 and self.block_movement == 1:
            self.current_state = 'Fully Inserted'
        elif self.rp is not self.last_cycle_rp:
            self.current_state = 'Moving'
        elif self.rp is self.last_cycle_rp and int(self.rp) == 0:
            self.current_state = 'Retracted'

        if self.block_movement:
            self.movement_blocked = 'Yes'
        else:
            self.movement_blocked = 'No'

        if not self._is_connected:
            self.connection_status = 'Disconnected'
        elif self._is_connected:
            self.connection_status = 'Connection established'
        # Called last
        self.last_cycle_rp = self.rp
