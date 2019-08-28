#!/usr/bin/env python3

import socket
import sys, os


def main():
    s = socket.socket()
    host = ('', 6143)
    s.bind(host)

    close_connection = 'n'
    s.listen(1)
    client, addr = s.accept()
    print('(host) Received a connection from', addr)
    client.send(b'Connection established with server on localhost.')
    while close_connection != 'y':
        try:
            data = client.recv(4096)
            print('(host) Data received:', data.decode())
            if data.decode() != '':
                client.send(data)
            else: close_connection = 'y'
        except ConnectionResetError as e:
            print('(host) Error:', e)
            break
    print('\n', '(host) Closing connection')


    client.close()


if __name__ == "__main__":
    main()
