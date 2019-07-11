#!/usr/bin/env python3
from models.verify_ip import is_valid_ipv4_address
import gclib

class MotionLink():
    ip_address = ''
    def _execute(self,command):
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

    def move(self, cmd):
        val = self._execute('merin={}'.format(cmd))
        return val

    def stop(self):
        val = self._execute('DCX=100000;STX;merstat=3')
        return val

    def read_rp(self):
        val = self._execute('RP')
        return val
