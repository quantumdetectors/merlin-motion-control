"""Class for updating the status fields of the main interface."""
from kivy.uix.gridlayout import GridLayout


class StatusFields(GridLayout):
    """Add functionality for the status fields of the main interface."""

    def __init__(self, **kwargs):
        """Initialize class.

        On start this class can be initialized by adding fields underneath
        the super method. The super method must not be changed since that is
        likely to impact the functionality of the Kivy framework.
        """

        super(StatusFields, self).__init__(**kwargs)
        #self.ids['conn_stat'].background_color=(1,0,0,1)
