import kivy
kivy.require("1.11.1")
from kivy.app import App
import config
from views.containergrid import ContainerGrid


class MerlinMotionControlApp(App):

    def __init__(self, **kwargs):
        super(MerlinMotionControlApp, self).__init__(**kwargs)

    def build(self):
        return ContainerGrid(settings=config.load_user_settings())


if __name__ == '__main__':
    MerlinMotionControlApp().run()
