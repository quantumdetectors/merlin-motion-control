#!/usr/bin/env python3
"""Connect to host on IP address specified in input_config.py."""

import socket
import sys
import os
from time import sleep
import json

from arthur.docstring_logger import to_stdout
import input_config

# Importing paths
CLIENT_IP = input_config.settings['client_ip']
HOST_IP = input_config.settings['host_ip']
ROOT_DIR = input_config.settings['root_dir']
OUTPUT_DIR = input_config.settings['output_dir']


@to_stdout
def establish_connection(host_ip=HOST_IP, host_port=6341):
    """Return a socket connected to a server with host_ip and host_port."""
    try:
        # Create a TCP/IP socket object.
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except socket.error as e:
        #  Failed to create socket.
        print('(client) Error:', e)
        return

    try:
        # Connect to socket.
        server_address = (host_ip, host_port)
        sock.connect(server_address)
    except socket.gaierror as e:
        # If getaddrinfo() and getnameinfo() methods of socket fails.
        print('(client) Error:', e)
        return
    except ConnectionRefusedError as e:
        # If peer prevents connection from being established.
        print('(client) Error:', e)
        return
    data = sock.recv(4096)
    print(data.decode())
    return sock


@to_stdout
def send_data(sock):
    """Send data to an open socket connected to a host waiting to receive."""
    print()
    while True:
        message = input('(client) Send to server: ')
        # Send data to server as a UTF-8 encoded byte string.
        sock.send(bytes(message, 'UTF-8'))
        # Receive above string back from server and print to stdout.
        if message != '':
            data = sock.recv(4096)
            print('(client) >>> ', data.decode(), '\n')
        else:
            # Stop sending messages if last message was empty.
            break
    print('\n', '(client) Closing connection')


@to_stdout
def close_connection(sock):
    """Close an open connection of a socket.socket() object."""
    sock.close()


@to_stdout
def main():
    """Enable feedback loop to server.py for debugging.

    1. Create socket.
    2. Connect socket to server with (host_ip, host_port).
    3. Send data to socket object.
        3.1 Receive data back from server.
        3.2 Break with empty message.
    4. Close connection.
    """
    host_ip = HOST_IP
    host_port = 6341
    sock = establish_connection(host_ip, host_port)
    if sock is not None:
        send_data(sock)
        close_connection(sock)
    return


if __name__ == "__main__":
    """To run locally, start test/server.py and then launch run_calibration."""
    main()
