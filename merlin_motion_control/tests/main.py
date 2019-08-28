#!/usr/bin/env python3
import kivy
kivy.require('1.11.1') # replace with your current kivy version !

from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.event import EventDispatcher
import gclib

class MyApp(App):
    cmd = 0
    g = gclib.py()
    def __init__(self,**kwargs):
        super(MyApp, self).__init__(**kwargs)
        try:
            a = self.g.GOpen('192.168.0.150 --direct -s ALL')
            print(a)
            self.g.timeout = 5000
            print('TP', self.g.GCommand('TP'))
            print('RP', self.g.GCommand('RP'))
        except gclib.GclibError as e:
            print('Unexpected GclibError:', e)
        finally:
            self.g.GClose()
    def build(self):
        print('here2')
        btn = Button()
        btn.bind(on_press = lambda x:self.move())
        return btn

    def move(self):
        if self.cmd == 0:
            self.cmd = 1
        elif self.cmd == 1:
            self.cmd = 0
        else:
            self.cmd = 0
        print('Value is', self.cmd)
        self.g.GCommand('merin={}'.format(self.cmd))
        #except gclib.GclibError as e:
        #    print('Expected GclibError:', e)
        #finally:
        #    self.g.GClose()

    def __del__(self):
            self.g.GClose()

if __name__ == '__main__':
    MyApp().run()
