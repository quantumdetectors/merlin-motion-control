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

    def __init__(self, **kwargs):
        super(MerlinMotionControlApp, self).__init__(**kwargs)

    def build(self):
        return ContainerGrid(settings=config.load_user_settings())


if __name__ == '__main__':
    MerlinMotionControlApp().run()
