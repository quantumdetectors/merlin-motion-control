#!/usr/bin/env python3
from models.verify_ip import is_valid_ipv4_address
import gclib
import random

class MotionLink():
    software_version = ''
    software_title = ''
    ip_address = ''
    mer_ip_address = ''
    speed = ''
    speed_out = ''
    merspeed = '20000'
    merspeec = '20000'
    requested_position = ''
    standby_position = ''
    current_state = ''
    debug = False
    last_debug_pos = 0
    state = 0
    connected = False
    g = gclib.py()

    def connect(self):
        try:
            self.g.GOpen('{} --direct -s ALL'.format(self.mer_ip_address))
            self.g.timeout = 1000
            self.connected = True
        except gclib.GclibError as e:
            print('Could not establish a connection:', e)
            self.connected = False
        except Exception:
            self.connected = False
        finally:
            self.g.GClose()

    def _execute(self,command):
        if not self.debug:
            try:
                self.g.GOpen('{} --direct -s ALL'.format(self.mer_ip_address))
                self.g.timeout = 5000
                val = self.g.GCommand(command)
                self.g.timeout = 5000
                self.connected = True
                return val
            except gclib.GclibError as e:
                print('Disconnecting device due to unexpected GclibError:', e)
                self.connected = False
                return '0'
            except Exception:
                print('Untreated exception in Galil class. Device disconnected.')
                self.connected = False
                return '0'
            finally:
                self.g.GClose()
        else:
            # Move in
            if command == 'merin=1':
                self.state = 1
            elif command == 'merin=2':
                self.state = 2
            elif command == 'merin=0':
                self.state = 0
            elif command == 'merin=3':
                self.state = 3
            elif command == 'RP':
                if self.state == 1:
                    if int(float(self.requested_position)) > int(float(self.last_debug_pos)):
                        self.current_state = 2
                        debug_pos = self.last_debug_pos+722
                        self.last_debug_pos = debug_pos
                    else:
                        self.current_state = 1
                        debug_pos = self.last_debug_pos
                    return str(debug_pos)
                elif self.state == 2:
                    self.current_state = 3
                    return str(self.last_debug_pos)
                elif self.state == 0:
                    if self.last_debug_pos==0:
                        self.current_state = 0
                        return '0'
                    else:
                        self.current_state = 2
                        debug_pos = self.last_debug_pos-722
                        self.last_debug_pos = debug_pos
                        return str(debug_pos)
                elif self.state == 3:
                    if int(float(self.standby_position)) > int(float(self.last_debug_pos)):
                        self.current_state = 2
                        debug_pos = self.last_debug_pos+722
                        self.last_debug_pos = debug_pos
                    else:
                        self.current_state = 4
                        debug_pos = self.last_debug_pos
                    return str(debug_pos)
            elif command == 'MG @IN[1]':
                return random.randint(0,1)
            elif command == 'MG @OUT[1]':
                return random.randint(0,1)
            elif command.split('=')[0] == 'merspeed':
                cmd = command.split('=')
                if cmd[1] == '?':
                    return str(self.merspeed)
                else:
                    self.merspeed = cmd[1]
                    print('g:', command)
            elif command.split('=')[0] == 'merspeec':
                cmd = command.split('=')
                if cmd[1] == '?':
                    return str(self.merspeec)
                else:
                    self.merspeec = cmd[1]
                    print('g:', command)
            elif command.split('=')[0] == 'req_pos':
                print('g: Request position set to', command.split('=')[1] )
            elif command == 'merstat=?':
                return self.current_state
            elif command.split('=')[0] == 'stdbypos':
                print('g: Standby position set to', command.split('=')[1] )


    def move(self, cmd):
        val = self._execute('merin={}'.format(cmd))
        return val

    def stop(self):
        val = self._execute('merin=2')
        return val

    def standby(self):
        val = self._execute('merin=3')
        return val

    def read_rp(self):
        val = self._execute('RP')
        return val

    def read_merstat(self):
        val = self._execute('merstat=?')
        return val

    def set_requested_position(self,cmd):
        if self.debug:
            self.requested_position = cmd
        val = self._execute('req_pos={}'.format(cmd))
        return val

    def set_standby_position(self,cmd):
        if self.debug:
            self.standby_position = cmd
        val = self._execute('stdbypos={}'.format(cmd))
        return val

    def get_gatan_in(self):
        if self.debug:
            return 0
        return 0 if float(self._execute('MG @IN[1]')) else 1

    def get_gatan_on(self):
        if self.debug:
            return 0
        on_state = self._execute('MG @IN[2]')
        return 1 if float(on_state) else 0

    def get_gatan_veto(self):
        if self.debug:
            return 0
        return int(float(self._execute('MG @OUT[1]')))

    def set_speed(self, speed):
        self._execute('merspeed={speed}'.format(speed=speed))

    def set_speed_out(self, speed_out):
        self._execute('merspeec={speed_out}'.format(speed_out=speed_out))

    def get_speed(self):
        return str(int(float(self._execute('merspeed=?'))))

    def get_speed_out(self):
        return str(int(float(self._execute('merspeec=?'))))

    def set_values(self):
        if self.speed.isdigit() and (int(self.speed) > 40000 or int(self.speed) < 1):
            print('Speed must be an integer between 1 and 40000')
            self.speed = self.get_speed()
        else:
            self.set_speed(self.speed)
        if self.speed_out.isdigit() and (int(self.speed_out) > 40000 or int(self.speed_out) < 1):
            print('Speed Out must be an integer between 1 and 40000')
            self.speed_out = self.get_speed_out()
        else:
            self.set_speed_out(self.speed_out)
        if is_valid_ipv4_address(self.ip_address):
            print('IP address:',self.ip_address)
            self.mer_ip_address = self.ip_address
        else:
            #print("Invalid IP address.", self.ip_address, "is not a valid IPv4 address.")
            self.ip_address = self.mer_ip_address
            #print(self.mer_ip_address)
