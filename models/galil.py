#!/usr/bin/env python3
from models.verify_ip import is_valid_ipv4_address
import gclib
import random

class MotionLink():
    ip_address = ''
    debug = False
    last_debug_pos = 0
    state = 0
    def _execute(self,command):
        if not self.debug:
            try:
                g = gclib.py()
                if is_valid_ipv4_address(self.ip_address):
                    g.GOpen("".join([ip_address, ' --direct -s ALL']))
                else:
                    raise AttributeError("Invalid IP address. ", v, " is not a valid IPv4 address.")
                g.timeout = 5000
                val = g.GCommand(command)
                g.timeout = 5000
                return val
            except gclib.GclibError as e:
                print('Unexpected GclibError:', e)
            finally:
                g.GClose()
        else:
            # Move in
            if command == 'merin=1':
                self.state = 1
            elif command == 'DCX=100000;STX;merstat=3':
                self.state = 2
            elif command == 'merin=0':
                self.state = 0
            elif command == 'RP':
                if self.state == 1:
                    debug_pos = self.last_debug_pos+200
                    self.last_debug_pos = debug_pos
                    return str(debug_pos)
                elif self.state == 2:
                    return str(self.last_debug_pos)
                elif self.state == 0:
                    if self.last_debug_pos==0:
                        return '0'
                    else:
                        debug_pos = self.last_debug_pos-200
                        self.last_debug_pos = debug_pos
                        return str(debug_pos)

    def move(self, cmd):
        val = self._execute('merin={}'.format(cmd))
        return val

    def stop(self):
        val = self._execute('DCX=100000;STX;merstat=3')
        return val

    def read_rp(self):
        val = self._execute('RP')
        return val
