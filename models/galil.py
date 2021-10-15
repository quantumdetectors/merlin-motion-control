#!/usr/bin/env python3
from models.verify_ip import is_valid_ipv4_address
import json
import gclib
import random

class MotionLink():
    software_version = ''
    software_title = ''
    ip_address = ''
    mer_ip_address = ''
    speed = ''
    speed_out = ''
    merspeed = '7500'
    merspeec = '20000'
    requested_position = ''
    standby_position = ''
    current_state = ''
    debug = False
    last_debug_pos = 0
    state = 0
    connected = False
    g = gclib.py()
    disconnect = 0
    
    with open('settings.json') as settings:
        data = json.load(settings)
        i_type = data['interlock_type']
    

    def connect(self):
        try:
            self.g.GOpen('{} -s ALL'.format(self.mer_ip_address))
            self.g.timeout = 1000
            self.g.disconnect = 0
            self.connected = True
        except gclib.GclibError as e:
            print('Could not establish a connection:', e)
            #self.g.disconnect += 1
            #if self.g.disconnect > 30: os.system("shutdown /r /t 30")
            #print(self.g.disconnect)
            self.connected = False
        except Exception:
            self.connected = False
        finally:
            self.g.GClose()

    def _execute(self,command):
        if not self.debug:
            try:
                self.g.GOpen('{} -s ALL'.format(self.mer_ip_address))
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

    def interlock_type_data(self):                            #creation of dictionary for interlock types
        inter=self.i_type
        interlock = {
            0: ['Override',"MG @OUT[0]","MG @OUT[0]"],
            1: ['Pneumatic',"MG @IN[1]","MG @IN[2]"],      #format is [name, cameraIn logic, CameraOn logic]      
            2: ['RJ45',"MG @IN[3]","MG @IN[4]" ]         
            
        }   
         
        return interlock.get(inter, "Invalid selection")       #invalid selection would be printed if not selected correctly

    def get_camera_in(self):
        if self.debug:
            return 0
        
        inter=(self.interlock_type_data())           #getting interlock data from the selected i_type
        cmd=inter[1]                                #verbose; selecting correct interlock data, camera in             
        in_state = int(float(self._execute(cmd)))   #int float required to sanitise the format
        
        return 0 if in_state else 1                      #In state determined by signal attributed to camera in being high this would be better reflected as camera retracted, this is therefore inverted 


    def get_camera_on(self):
        if self.debug:
            return 0
        
        inter=(self.interlock_type_data())           #getting interlock data from the selected i_type
        cmd=inter[2]                                #verbose; selecting correct interlock data, camera on
        on_state = int(float(self._execute(cmd)))

        return 1 if on_state else 0              #if the on_state is high then return that the camera is on

    def get_camera_veto(self):
        if self.debug:
            return 0
        CameraOn = self.get_camera_on()
        CameraIn = self.get_camera_in()
        
        if CameraOn == 1 and CameraIn == 0:
           CameraVeto = 0
        else:
            CameraVeto = 1

        one = self._execute("MG @IN[1]")
        four = self._execute("MG @IN[4]")
        zero = self._execute("MG @OUT[0]")

        
        print(zero, one)

        return CameraVeto


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
