"""Add functionality for main window.

Bind button functionality between interface and MotionLink options.
Update status fields.
"""
from kivy.uix.floatlayout import FloatLayout
from kivy.properties import StringProperty, BooleanProperty, ListProperty
from kivy.uix.label import Label
from kivy.clock import Clock, mainthread
from views.settingswindow import SettingsWindow
from views.infowindow import InfoWindow
from views.actionbuttons import ActionButtons
from views.statusfields import StatusFields
from views.labels import Labels
from models.rw_galil import MotionLinkInterface
import threading
import time
CLOCK_SPEED = 0.000001


class ContainerGrid(FloatLayout):
    """Add layout and functionality to the main app window."""

    rp = StringProperty('0')
    _rp = StringProperty('Default')
    requested_position = StringProperty('0')
    current_state = StringProperty('Default')
    requested_state = StringProperty('Default')
    gatan_in = StringProperty('Default')
    gatan_veto = StringProperty('Default')
    gatan_in_msg = StringProperty('Default')
    gatan_veto_msg = StringProperty('Default')
    _is_connected = BooleanProperty('False')
    connection_status = StringProperty('Disconnected')
    interlocked = 0
    inserted = 0

    def __init__(self, settings, **kwargs):
        """Initialize layout.

        Create MotionLink object and initialize it with values from config.py.
        Initialize settings and info windows.

        The super method must not be changed since that is likely to
        impact the functionality of the Kivy framework.
        """
        super(ContainerGrid, self).__init__(**kwargs)
        Clock.schedule_interval(self.update_status_fields, CLOCK_SPEED)
        self.settings = settings
        self.ml_interface = MotionLinkInterface()
        self.ml_interface.debug = False
        self.ml_interface.software_version = self.settings["software_version"]
        self.ml_interface.software_title = self.settings["title"]
        self.ml_interface.mer_ip_address = self.settings["ip_address"]
        self.ml_interface.speed = self.settings["speed"]
        self.ml_interface.speed_out = self.settings["speed_out"]
        self.requested_position = str(
            self.settings["default_requested_position"]
        )
        self.title = self.ml_interface.software_title
        self.settingsWindow = SettingsWindow(ml_object=self.ml_interface)
        self.infoWindow = InfoWindow(ml_object=self.ml_interface)
        self.ml_interface.update_ml()
        self.ml_interface.write()


    def move_in(self):
        """Call move in function on the MotionLink object."""
        if self.inserted == 0:
        #if self.current_state is not 'Stopped':
            self.ml_interface.move(1)
            self.requested_state = 'Inserted'


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
        self.rp = self.ml_interface.rp

        if self.requested_position is '':
            self.requested_position = '0'

        if int(self.requested_position) > self.settings["max_position"]:
            self.requested_position = str(self.settings["max_position"])

        if int(self.rp) >= int(self.requested_position) and self.inserted == 0:
            self.ml_interface.stop()
            self.inserted = 1

        if self.requested_state is 'Stopped':
            self.current_state = self.requested_state
        elif self.rp is self._rp and int(self.rp) >= \
                self.settings["max_position"]:
            self.current_state = 'Max Insertion'
        elif self.rp is self._rp and int(self.rp) > 0:
            self.current_state = 'Inserted'
        elif self.rp is not self._rp:
            self.current_state = 'Moving'
        elif self.rp is self._rp and int(self.rp) == 0:
            self.current_state = 'Retracted'
            self.inserted = 0


        self.connection_status = 'Connection established' if self.ml_interface.is_connected else 'Disconnected'
        self.gatan_in_msg = 'Yes' if self.ml_interface.gatan_in else 'No'
        self.gatan_veto_msg = 'Yes' if self.ml_interface.gatan_veto else 'No'

        # Called last
        self._rp = self.rp
        #self.rp = str(int(float(self.rp)/3200)) # In units of mm

    def settingswindow(self):
        """Open Settings window."""
        self.settingsWindow.open()

    def infowindow(self):
        """Open Info window."""
        self.infoWindow.open()
