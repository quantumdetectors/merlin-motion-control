"""Add functionality for main window.

Bind button functionality between interface and MotionLink options.
Update status fields.
"""
from kivy.uix.floatlayout import FloatLayout
from kivy.properties import StringProperty, BooleanProperty, ListProperty, AliasProperty, NumericProperty
from kivy.uix.label import Label
from kivy.clock import Clock, mainthread
from views.settingswindow import SettingsWindow
from views.infowindow import InfoWindow
from views.testwindow import TestWindow
from views.actionbuttons import ActionButtons
from views.statusfields import StatusFields
from views.labels import Labels
from models.rw_galil import MotionLinkInterface
import threading
import time
import os
CLOCK_SPEED = 0.000001


class ContainerGrid(FloatLayout):
    """Add layout and functionality to the main app window."""

    rp = StringProperty('0')
    _rp = StringProperty('Default')
    requested_position = StringProperty('0')
    standby_position = StringProperty('0')
    current_state = StringProperty('Default')
    requested_state = StringProperty('Default')
    gatan_in = StringProperty('Default')
    gatan_veto = StringProperty('Default')
    gatan_in_msg = StringProperty('Default')
    gatan_veto_msg = StringProperty('Default')
    _is_connected = BooleanProperty('False')
    connection_status = StringProperty('Disconnected')
    state = NumericProperty(0)
    interlocked = 0
    inserted = 0
    debug = False
    ml_interface = MotionLinkInterface()

    def disable_window(self):
        return True if self.connection_status == 'Disconnected' else False
    def disable_standby(self):
        state = int(float(self.ml_interface.current_state))
        return True if state == 4 and self.requested_state != 'Default' else False
    def disable_move_in(self):
        state = int(float(self.ml_interface.current_state))
        return  True if state == 1 and self.requested_state != 'Default' else False
    def disable_move_out(self):
        state = int(float(self.ml_interface.current_state))
        return True if state == 0 else False
    def disable_stop(self):
        state = int(float(self.ml_interface.current_state))
        return False if state == 2 else True

    window_disabled = AliasProperty(disable_window, bind=['connection_status'])
    button_standby_disabled = AliasProperty(disable_standby, bind=['current_state'])
    button_move_in_disabled = AliasProperty(disable_move_in, bind=['current_state'])
    button_move_out_disabled = AliasProperty(disable_move_out, bind=['current_state'])
    button_stop_disabled = AliasProperty(disable_stop, bind=['current_state'])

    def __init__(self, settings, **kwargs):
        """Initialize layout.

        Create MotionLink object and initialize it with values from config.py.
        Initialize settings and info windows.

        The super method must not be changed since that is likely to
        impact the functionality of the Kivy framework.
        """
        super(ContainerGrid, self).__init__(**kwargs)
        Clock.schedule_interval(self.update_status_fields, 100*CLOCK_SPEED)
        self.settings = settings
        self.ml_interface.debug = self.debug
        self.ml_interface.software_version = str(self.settings["software_version"])
        self.ml_interface.software_title = self.settings["title"]
        self.ml_interface.mer_ip_address = self.settings["ip_address"]
        self.ml_interface.speed = str(self.settings["speed"])
        self.ml_interface.speed_out = str(self.settings["speed_out"])
        self.standby_position = str(
            self.settings["standby_position"]
        )
        self.requested_position = str(
            self.settings["default_requested_position"]
        )
        self.ml_interface.standby_position = self.standby_position
        self.ml_interface.requested_position = self.requested_position
        self.title = self.ml_interface.software_title
        self.settingsWindow = SettingsWindow(ml_object=self.ml_interface)
        self.infoWindow = InfoWindow(ml_object=self.ml_interface)
        self.testWindow = TestWindow(self, ml_interface=self.ml_interface)
        self.ml_interface.update_ml()
        self.ml_interface.write()
        self.set_requested_position()
        self.set_standby_position()

    def standby(self):
        """Call move to standby."""
        print('Containergrid',self.standby_position)
        print('ML',self.ml_interface.standby_position)
        self.ml_interface.standby()
        self.requested_state = 'Standby'

    def move_in(self):
        """Call move in function on the MotionLink object."""
        self.requested_state = 'Inserted'
        self.ml_interface.move(1)


    def move_out(self):
        """Call move in function on the MotionLink object."""
        self.requested_state = 'Retracted'
        self.ml_interface.move(0)

    def stop(self):
        """Call stop function on the MotionLink object."""
        self.requested_state = 'Stopped'
        self.ml_interface.stop()

    def set_requested_position(self):
        self.ml_interface.requested_position = self.requested_position
        self.ml_interface.set_requested_position()

    def set_standby_position(self):
        self.ml_interface.standby_position = self.standby_position
        self.ml_interface.set_standby_position()

    def update_status_fields(self, *args):
        """Call read_rp on the MotionLink object and update status fields.

        Method called by clock set in __init__.

        Set status fields depending on the change in position between each
          clock cycle.

        requested_position: Set by the user through settings.json or by
          by textinput when the app is running.

        rp: Relative Position. Related to number of pulses sent to the
            controller of the MotionLink stepper motor. 3200 pulses
            equals 1 mm on the linear stage.

        requested_state/
        current_state:   'Stopped' if Stop button is pressed
                         'Moving' if rp in last cycle (_rp) != rp from current
                         'Inserted' if _rp == rp and rp > 0
                         'Max Insertion' if rp >= max_position set in .env file
                         'Retracted' if rp == 0 and rp == _rp

        connection_status: 'Connection established' if _is_connected is True.
                           'Disconnected' if _is_conneceted is False.

        gatan_in_msg: 'Yes' if get_gatan_in() on MotionLink object is True.
                      'No' if False.

        gatan_veto_msg: 'In' if get_gatan_veto() call to MotionLink
                          object is True.
                        'No' if False.

        """


        self.connection_status = 'Connection established' if self.ml_interface.is_connected else 'Disconnected'
        self.requested_position = self.ml_interface.requested_position

        self.rp = self.ml_interface.rp


        if self.requested_position is '':
            self.requested_position = '0'

        if int(self.requested_position) > self.settings["max_position"]:
            self.requested_position = str(self.settings["max_position"])

        if int(self.rp) >= int(self.requested_position) and self.inserted == 0:
            self.inserted = 1

        state = int(float(self.ml_interface.current_state))
        self.current_state = 'Standby' if state == 4 else ('Stopped'if state == 3 else ('Moving' if state == 2 else ('Inserted' if state == 1 else 'Retracted')))
        self.gatan_in_msg = 'Yes' if self.ml_interface.gatan_in else 'No'
        self.gatan_veto_msg = 'Yes' if self.ml_interface.gatan_veto else 'No'

        # Called last
        self._rp = self.rp

    def settingswindow(self):
        """Open Settings window."""
        self.settingsWindow.open()

    def infowindow(self):
        """Open Info window."""
        self.infoWindow.open()


    def testwindow(self):
        """Open Info window."""
        self.testWindow.open()
