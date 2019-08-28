#!/usr/bin/env python3
import kivy
kivy.require("1.11.1")

from kivy.app import App
from kivy.uix.stacklayout import StackLayout


class StackLayoutApp(App):

    def build(self):
        return StackLayout()

stacklayout = StackLayoutApp()
stacklayout.run()
