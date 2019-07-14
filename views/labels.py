"""Class for adding functionality to the labels of the main interface."""
from kivy.uix.gridlayout import GridLayout


class Labels(GridLayout):
    """Add functionality for the labels of the main interface."""

    def __init__(self, **kwargs):
        """Initialize class.

        On start this class can be initialized by adding fields underneath
        the super method. The super method must not be changed since that is
        likely to impact the functionality of the Kivy framework.
        """
        super(Labels, self).__init__(**kwargs)
