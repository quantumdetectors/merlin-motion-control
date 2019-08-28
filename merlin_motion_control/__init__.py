# -*- coding: utf-8 -*-
"""
Quantum Detectors Merlin Motion Control
"""

def main():
    from .views.interface import MerlinMotionControlApp
    from . import config

    MerlinMotionControlApp().run()