import kivy
kivy.require("1.11.1")
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
import config
from views.containergrid import ContainerGrid
from views.actionbuttons import ActionButtons
from views.statusfields import StatusFields
from views.labels import Labels

class MerlinMotionControlApp(App):

    title="Merlin Motion Control"
    version=config.software_version()

    def build(self):
        print("here")
        return ContainerGrid()

if __name__ == '__main__':
    MerlinMotionControlApp().run()
