# -*- coding: utf-8 -*-
"""
Galil Motion Control Interface
"""
from typing import Optional
import logging
log = logging.getLogger(__name__)

from .verify_ip import is_valid_ipv4_address
import gclib
import random

class MotionLink(object):
    """
    """

    def __init__(self):
        self.software_version: str = ''  
        self.software_title: str = ''
        self.ip_address: str = ''
        self.mer_ip_address: str = ''
        self.speed: str = ''
        self.speed_out: str = ''
        self._debug: bool = False
        self.connected: bool = False
        self.g = gclib.py()

    @property
    def debug(self) -> bool:
        """
        Whether the MotionLink is running in debug (i.e. emulator) mode.
        """
        return self._debug

    @debug.setter
    def debug(self, value: bool) -> None:
        self._debug = bool(value)
        # Dynamically add in debugging attributes so they don't clutter the namespace
        # if unused.
        if self._debug is True:
            self._d_requested_pos = ''
            self._d_standby_pos = ''
            self._d_current_state = ''

            self._d_merspeed = '20000'
            self._d_merspeec = '20000'
            self._d_last_pos = 0
            self._d_state = 0


    def connect(self) -> None:
        try:
            self.g.GOpen('{} --direct -s ALL'.format(self.mer_ip_address))
            self.g.timeout = 1000
            self.connected = True
        except gclib.GclibError as e:
            log.info(f'Could not establish a connection: {e}')
            self.connected = False
        except Exception:
            self.connected = False
        finally:
            self.g.GClose()


    def _execute(self, command: str) -> Optional[str]:
        if self.debug:
            self._execute_debug(command)
            return
        
        try:
            self.g.GOpen(f'{self.mer_ip_address} --direct -s ALL')
            self.g.timeout = 5000
            val = self.g.GCommand(command)
            self.g.timeout = 5000
            self.connected = True
            return val
        except gclib.GclibError as e:
            log.info(f'Disconnecting device due to unexpected GclibError: {e}')
            self.connected = False
            return '0'
        except:
            log.info('Unhandled exception in Galil class. Device disconnected.')
            self.connected = False
            return '0'
        finally:
            self.g.GClose()


    def _execute_debug(self, command: str) -> Optional[str]:
        """
        As per `MotionLink._execute` but when run in emulator mode.
        """
        if command == 'merin=1': # Move in
            self._d_state = 1
        elif command == 'merin=2': # Stop
            self._d_state = 2
        elif command == 'merin=0': # Move out
            self._d_state = 0
        elif command == 'merin=3': # Standy
            self._d_state = 3
        elif command == 'RP':
            if self._d_state == 1:
                if int(float(self._d_requested_pos)) > int(float(self._d_last_pos)):
                    self._d_current_state = 2
                    debug_pos = self._d_last_pos+722
                    self._d_last_pos = debug_pos
                else:
                    self._d_current_state = 1
                    debug_pos = self._d_last_pos
                return str(debug_pos)
            elif self._d_state == 2:
                self._d_current_state = 3
                return str(self._d_last_pos)
            elif self._d_state == 0:
                if self._d_last_pos==0:
                    self._d_current_state = 0
                    return '0'
                else:
                    self._d_current_state = 2
                    debug_pos = self._d_last_pos-722
                    self._d_last_pos = debug_pos
                    return str(debug_pos)
            elif self._d_state == 3:
                if int(float(self._d_standby_pos)) > int(float(self._d_last_pos)):
                    self._d_current_state = 2
                    debug_pos = self._d_last_pos+722
                    self._d_last_pos = debug_pos
                else:
                    self._d_current_state = 4
                    debug_pos = self._d_last_pos
                return str(debug_pos)
        elif command == 'MG @IN[1]':
            return random.randint(0,1)
        elif command == 'MG @OUT[1]':
            return random.randint(0,1)
        elif command.split('=')[0] == 'merspeed':
            cmd = command.split('=')
            if cmd[1] == '?':
                return str(self._d_merspeed)
            else:
                self._d_merspeed = cmd[1]
                log.info(f'g: {command}')
        elif command.split('=')[0] == 'merspeec':
            cmd = command.split('=')
            if cmd[1] == '?':
                return str(self._d_merspeec)
            else:
                self._d_merspeec = cmd[1]
                log.info(f'g: {command}')
        elif command.split('=')[0] == 'req_pos':
            log.info(f'g: Request position set to {command.split("=")[1]}')
        elif command == 'merstat=?':
            return self._d_current_state
        elif command.split('=')[0] == 'stdbypos':
            log.info(f'g: Standby position set to {command.split("=")[1]}')
        # TODO: should have a default return?


    def move(self, cmd) -> str:
        val = self._execute(f'merin={cmd}')
        return val

    def stop(self) -> str:
        val = self._execute('merin=2')
        return val

    def standby(self) -> str:
        val = self._execute('merin=3')
        return val

    def read_rp(self) -> str:
        val = self._execute('RP')
        return val

    def read_merstat(self) -> str:
        val = self._execute('merstat=?')
        return val

    def set_requested_position(self, cmd: str) -> str:
        val = self._execute(f'req_pos={cmd}')
        return val

    def set_standby_position(self, cmd: str) -> str:
        val = self._execute(f'stdbypos={cmd}')
        return val

    def get_gatan_in(self) -> int:
        return 0 if float(self._execute('MG @IN[1]')) else 1

    def get_gatan_veto(self) -> int:
        return int(float(self._execute('MG @OUT[1]')))

    def set_speed(self, speed: int) -> None:
        self._execute(f'merspeed={speed}')

    def set_speed_out(self, speed_out: int) -> None:
        self._execute(f'merspeec={speed_out}')

    def get_speed(self) -> str:
        return str(int(float(self._execute('merspeed=?'))))

    def get_speed_out(self) -> str:
        return str(int(float(self._execute('merspeec=?'))))

    def validate_values(self) -> None:
        if self.speed.isdigit() and (int(self.speed) > 40000 or int(self.speed) < 1):
            log.info('Speed must be an integer between 1 and 40000')
            self.speed = self.get_speed()
        else:
            self.set_speed(self.speed)
        if self.speed_out.isdigit() and (int(self.speed_out) > 40000 or int(self.speed_out) < 1):
            log.info('Speed Out must be an integer between 1 and 40000')
            self.speed_out = self.get_speed_out()
        else:
            self.set_speed_out(self.speed_out)
        if is_valid_ipv4_address(self.ip_address):
            log.info(f'IP address: {self.ip_address} is valid.')
            self.mer_ip_address = self.ip_address
        else:
            log.info(f'Invalid IPv4 address: {self.ip_address}')
            self.ip_address = self.mer_ip_address


