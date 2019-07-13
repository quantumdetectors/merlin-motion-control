import kivy
kivy.require("1.11.1")
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
import config
from views.containergrid import ContainerGrid
from views.actionbuttons import ActionButtons
from views.statusfields import StatusFields
from views.labels import Labels
from kivy.properties import StringProperty, BooleanProperty, ListProperty


class MerlinMotionControlApp(App):

    title="Merlin Motion Control"
    settings = dict()
    def __init__(self, **kwargs):
        super(MerlinMotionControlApp, self).__init__(**kwargs)
        try:
            self.settings = config.load_user_settings()
        except AttributeError as e:
            print(e.__class__, "".join(e.args))
        except FileNotFoundError as e:
            print(e.__class__, "".join(e.args))
            self.settings = {
                "ip_address":config.default_ip(),
                "default_requested_position":config.default_requested_position(),
                "speed":config.default_speed(),
                "speed_out":config.default_speed_out()
            }
            print("Default settings are:")
            for k,v in self.settings.items():
                print(k,v)
        self.settings["max_position"] = config.max_position()
        self.settings["software_version"] = config.software_version()
        self.settings["title"] = self.title

    def build(self):
        return ContainerGrid(settings=self.settings)


if __name__ == '__main__':
    MerlinMotionControlApp().run()
