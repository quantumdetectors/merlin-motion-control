"""Class called directly by Merlin_Motion_Control.py for launching the app.

Class reads instructions on the appearance of the app from views/merlinmotioncontrol.kv.
"""

from views.containergrid import ContainerGrid
from kivy.app import App
import kivy
import config

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

    def build(self):
        """Return a layout."""
        return ContainerGrid(settings=config.load_user_settings())
