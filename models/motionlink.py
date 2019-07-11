import gclib

ADDRESS = '192.168.0.155 --direct -s ALL'

class MotionLink():
    def _execute(self,command):
        try:
            g = gclib.py()
            g.GOpen(ADDRESS)
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
