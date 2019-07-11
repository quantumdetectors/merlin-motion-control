#!/usr/bin/env python3
from time import sleep
import gclib

def main():
  g = gclib.py()
  g.GOpen('192.168.0.150 --direct -s ALL')
  g.timeout = 5000

  try:
    print('TP', g.GCommand('TP'))
    print('RP', g.GCommand('RP'))
    pos = 0
    speed = input('Speed in, default 20000:')
    speedout = input('Speed out, default 20000:')
    if len(speed)==0 or int(speed) < 1000:
        print('Speed too low, setting speed = 20000')
        speed = 20000
    elif int(speed) > 60000:
        print('Speed too high, setting speed = 20000')
        speed = 20000
    if len(speedout)==0 or int(speedout) < 1000:
        print('Speed out too low, setting speed out = 20000')
        speedout = 20000
    elif int(speedout) > 60000:
        print('Speed out too high, setting speed out = 20000')
        speedout = 20000
    print(g.GCommand('merspeed={speed}'.format(int(speed))))
    print(g.GCommand('merspeec={speedout}'.format(int(speedout))))
    cmd = 0
    while cmd=='0' or cmd=='1' or cmd=='2':
        cmd = int(input('0-move out, 1-move in, 2-stop'))
        print(g.GCommand('merin={cmd}'.format(cmd)))
        t = 5000
        print('Sleeping for', t, 'ms.')
        sleep(t)
  except gclib.GclibError as e:
    print('Unexpected GclibError:', e)

  finally:
    g.GClose()

  return


if __name__ == '__main__':
    main()
