#!/usr/bin/env python3
import kivy
kivy.require("1.11.1")

from kivy.app import App
from kivy.uix.floatlayout import FloatLayout


class FloatLayoutApp(App):

    def build(self):
        return FloatLayout()

floatlayout = FloatLayoutApp()
floatlayout.run()
