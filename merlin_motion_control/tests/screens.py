from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from screen1 import MenuScreen
from screen2 import SettingsScreen
from kivy.lang import Builder

kv = Builder.load_file('test.kv')

class MenuScreen(Screen):
    def __init__(self,  **kwargs):
        """Initialize class.

        On start this class can be initialized by adding fields underneath the
        super method. The super method must not be changed since that is likely to
        impact the functionality of the Kivy framework.
        """
        super(MenuScreen, self).__init__(**kwargs)

class SettingsScreen(Screen):
    def __init__(self,  **kwargs):
        """Initialize class.

        On start this class can be initialized by adding fields underneath the
        super method. The super method must not be changed since that is likely to
        impact the functionality of the Kivy framework.
        """
        super(SettingsScreen, self).__init__(**kwargs)


class MyOwnApp(App):
    def __init__(self, **kwargs):
        """Initialize class.

        On start this class can be initialized by adding fields underneath the
        super method. The super method must not be changed since that is likely to
        impact the functionality of the Kivy framework.
        """
        super(MyOwnApp, self).__init__(**kwargs)
        self.sm = ScreenManager()
        self.sm.add_widget(MenuScreen(name='menu'))
        self.sm.add_widget(SettingsScreen(name='settings'))

    def build(self):
        return kv

if __name__ == '__main__':
    MyOwnApp().run()
