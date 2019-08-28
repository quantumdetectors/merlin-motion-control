import platform    # For getting the operating system name
import subprocess  # For executing a shell command
import os

def ping(host):
    """
    Returns True if host (str) responds to a ping request.
    Remember that a host may not respond to a ping (ICMP) request even if the host name is valid.
    """

    # Option for the number of packets as a function of
    param = '-n' if platform.system().lower()=='windows' else '-c'
    timeout = '-w' if platform.system().lower()=='windows' else '-W'

    # Building the command. Ex: "ping -c 1 google.com"
    command = ['ping', param, '1', timeout, '10', '-t 1', host]

    return subprocess.call(command, stdout=open(os.devnull, 'wb')) == 0
