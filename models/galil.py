#!/usr/bin/env python3
from models.verify_ip import is_valid_ipv4_address
import gclib
import random

class MotionLink():
    software_version = ''
    ip_address = ''
    speed = ''
    speed_out = ''
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
                    debug_pos = self.last_debug_pos+722
                    self.last_debug_pos = debug_pos
                    return str(debug_pos)
                elif self.state == 2:
                    return str(self.last_debug_pos)
                elif self.state == 0:
                    if self.last_debug_pos==0:
                        return '0'
                    else:
                        debug_pos = self.last_debug_pos-722
                        self.last_debug_pos = debug_pos
                        return str(debug_pos)
            elif command == 'MG @IN[1]':
                return random.randint(0,1)
            elif command == 'MG @OUT[1]':
                return random.randint(0,1)
            elif command[0] == 'm' and command[7] == 'd':
                print(command)


    def move(self, cmd):
        val = self._execute('merin={}'.format(cmd))
        return val

    def stop(self):
        val = self._execute('DCX=100000;STX;merstat=3')
        return val

    def read_rp(self):
        val = self._execute('RP')
        return val

    def get_gatan_in(self):
        if self.debug:
            if self._execute('MG @IN[1]') == 1:
                return 0
            else:
                return 1
        return 0 if float(self._execute('MG @IN[1]')) else 1

    def get_gatan_veto(self):
        if self.debug:
            return self._execute('MG @OUT[1]')
        return int(float(self._execute('MG @OUT[1]')))

    def set_speed(self, speed):
        self._execute('merspeed={speed}'.format(speed=speed))

    def set_speed(self, speed_out):
        self._execute('merspeec={speed_out}'.format(speed_out=speed_out))

    def set_values(self):
        if self.speed > '40000' or self.speed < '1':
            print('Speed must be an integer between 1 and 40000')
        else:
            self.set_speed(self.speed)
        if self.speed_out > '40000' or self.speed_out < '1':
            print('Speed Out must be an integer between 1 and 40000')
        else:
            self.set_speed_out(self.speed_out)
