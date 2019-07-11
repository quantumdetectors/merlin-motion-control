#!/usr/bin/env python3
import kivy
kivy.require("1.11.1")

from kivy.app import App
from kivy.uix.gridlayout import GridLayout


class GridLayoutApp(App):

    def build(self):
        return GridLayout()

gridlayout = GridLayoutApp()
gridlayout.run()
