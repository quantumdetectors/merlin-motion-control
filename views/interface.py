"""Class called directly by Merlin_Motion_Control.py for launching the app.

Class reads instructions on the appearance of the app from views/merlinmotioncontrol.kv.
"""

from views.screens.main.mainscreen import MainScreen
from kivy.app import App
import kivy
import config

# Separate kv files
from kivy.lang import Builder
from views.modals.settings import settingswindow
#from views.modals.settings.settingswindow import SettingsWindow
from views.modals.info import infowindow
from views.modals.test import testwindow
#from views.modals.info.infowindow import InfoWindow
#from views.screens.main.mainscreen import MainScreen
#from views.screens.main.actionbuttons import ActionButtons
#from views.screens.main.labels import Labels
#from views.screens.main.statusfields import StatusFields
from views.screens.main import mainscreen
from views.static import styles

kivy.require("1.11.1")


class MerlinMotionControlApp(App):
    """Main class inheriting the App class of Kivy and is responsible for building the GUI."""

    def __init__(self, **kwargs):
        """Initialize class.

        On start this class can be initialized by adding fields underneath the
        super method. The super method must not be changed since that is likely to
        impact the functionality of the Kivy framework.
        """
        super(MerlinMotionControlApp, self).__init__(**kwargs)
        Builder.load_file(styles.__file__.split('.py')[0]+'.kv')
        Builder.load_file(settingswindow.__file__.split('.py')[0]+'.kv')
        Builder.load_file(infowindow.__file__.split('.py')[0]+'.kv')
        Builder.load_file(testwindow.__file__.split('.py')[0]+'.kv')
        Builder.load_file(mainscreen.__file__.split('.py')[0]+'.kv')

    def build(self):
        """Return a layout."""
        return MainScreen(settings=config.load_user_settings())
