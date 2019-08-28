#!/usr/bin/env python3
import kivy
kivy.require("1.11.1")

from kivy.app import App
from kivy.uix.pagelayout import PageLayout


class PageLayoutApp(App):

    def build(self):
        return PageLayout()

pagelayout = PageLayoutApp()
pagelayout.run()
