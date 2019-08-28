import gclib
import kivy
kivy.require("1.11.1")

from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.widget import Widget
from kivy.clock import Clock
from kivy.properties import StringProperty, BooleanProperty


ADDRESS = '192.168.0.155 --direct -s ALL'


class MotionLink():
    def _execute(self,command):
        try:
            g = gclib.py()
            g.GOpen(ADDRESS)
            g.timeout = 5000
            val = g.GCommand(command)
            g.timeout = 5000
            return val
        except gclib.GclibError as e:
            print('Unexpected GclibError:', e)
        finally:
            g.GClose()

    def move(self, cmd):
        val = self._execute('merin={}'.format(cmd))
        return val

    def stop(self):
        val = self._execute('DCX=100000;STX;merstat=3')
        return val

    def read_rp(self):
        val = self._execute('RP')
        return val


class HBoxWidget(GridLayout):
    def __init__(self, **kwargs):
        super(HBoxWidget, self).__init__(**kwargs)


class VBoxWidget(GridLayout):
    def __init__(self, **kwargs):
        super(VBoxWidget, self).__init__(**kwargs)

class TBoxWidget(GridLayout):
    def __init__(self, **kwargs):
        super(TBoxWidget, self).__init__(**kwargs)

class ContainerBox(GridLayout):
    rp = StringProperty('Default')
    last_cycle_rp = StringProperty('Default')
    block_movement = BooleanProperty(False)
    movement_blocked = StringProperty('Default')
    max_insert = 50000
    requested_position = StringProperty(str(max_insert))
    current_state = StringProperty('Default')
    requested_state = StringProperty('Default')
    gatan_in = StringProperty('Default')
    gatan_veto = StringProperty('Default')
    _is_connected = BooleanProperty('False')
    connection_status = StringProperty('Disconnected')

    def __init__(self, **kwargs):
        super(ContainerBox, self).__init__(**kwargs)
        self.ml = MotionLink()
        Clock.schedule_interval(self.update_values, 0.1)

    def move_in(self):
        if self.current_state is not 'Stopped':
            self.requested_state = 'Inserted'
            if self.block_movement is False:
                self.ml.move(1)

    def move_out(self):
        self.requested_state = 'Retracted'
        self.ml.move(0)

    def stop(self):
        self.requested_state = 'Stopped'
        self.ml.stop()

    def update_values(self,*args):
        self.rp = self.ml.read_rp()
        print(self.requested_position)
        if int(self.requested_position) > self.max_insert:
            self.requested_position = str(self.max_insert)

        if self.block_movement is False and int(self.rp) > int(self.requested_position):
            self.ml.stop()
            self.block_movement = True
        elif self.block_movement is True and int(self.rp) < int(self.requested_position):
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

        if self.block_movement is True:
            self.movement_blocked = 'Yes'
        else:
            self.movement_blocked = 'No'

        if self._is_connected == False:
            self.connection_status = 'Disconnected'
        elif self_is_connected == True:
            self.connection_status = 'Connection established'


        # Called last
        self.last_cycle_rp = self.rp

class MyApp(App):
    title="Merlin Motion Control"
    version="v0.1"

    def build(self):
        return ContainerBox()

if __name__ == '__main__':
    MyApp().run()
