from kivy.uix.screenmanager import ScreenManager, Screen

class SettingsScreen(Screen):
    def __init__(self,  **kwargs):
        """Initialize class.

        On start this class can be initialized by adding fields underneath the
        super method. The super method must not be changed since that is likely to
        impact the functionality of the Kivy framework.
        """
        super(SettingsScreen, self).__init__(**kwargs)
