# -*- coding: utf-8 -*-
"""
Quantum Detectors Merlin Motion Control
"""
# Import the resources (icons, etc.) for Kivy early:
import os.path as path
from kivy.resources import resource_add_path
resource_add_path(path.dirname(__file__))

def main():
    from .views.interface import MerlinMotionControlApp
    from . import config

    MerlinMotionControlApp().run()