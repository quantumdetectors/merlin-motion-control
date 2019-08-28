"""Class for adding functionality to the Info modal window."""
from kivy.uix.modalview import ModalView
from kivy.properties import StringProperty
from datetime import datetime


class InfoWindow(ModalView):
    """Add functionality to Info modal window."""

    copyright_date = StringProperty('Def')
    software_version = StringProperty('Def')
    software_title = StringProperty('Def')

    def __init__(self, ml_object, **kwargs):
        """Initialize an fields for the Info modal window.

        Update copyright_date with today's year.
        Pull software version from MotionLink object.
        Pull software title from Motionlink object.

        On start this class can be initialized by adding fields underneath
        the super method. The super method must not be changed since that is
        likely to impact the functionality of the Kivy framework.
        """
        super(InfoWindow, self).__init__(**kwargs)
        self.copyright_date = datetime.now().strftime('%Y')
        self.software_version = str(ml_object.software_version)
        self.software_title = str(ml_object.software_title)
