import sys
import string
import gclib
import time


def main():
  g = gclib.py()

  try:
    print('gclib version:', g.GVersion())

    g.GOpen('192.168.0.154 --direct -s ALL')
    print(g.GInfo())
    g.timeout = 300000

    with open('dmc/merlin.dmc') as prog:
        lines = prog.read()
        out = []
        for l in lines.split('\n'):
            l = l.rstrip()
            #if not l:
            #    l += '\''
            if l:
                out.append(l + ';\r')

    #out.append('\\\r')
    print(out)
    # exit()

    g.GProgramDownload(''.join(out), '')
    print(' Uploaded program:\n%s' % g.GProgramUpload())
    g.GCommand('XQ')
    g.GCommand('BP')
    g.GSleep(20)

    print(g.GMessage())

    #g.GCommand('BP') #burn program
    #g.GSleep(10)
    #print g.GMessage()

  except gclib.GclibError as e:
    print('Unexpected GclibError:', e)

  finally:
    g.GClose()

  return


if __name__ == '__main__':
  main()
