#usr/bin/env python3

import socket
import sys

if __name__ == "__main__":

    if len(sys.argv) < 3 or len(sys.argv) > 3:
        print('Error: usage: ./' + sys.argv[0] + ' <destination/IP> <Port>')
        exit()
    else:
        host = sys.argv[1]
        port = int(sys.argv[2])
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((host,port))
        s.sendall(b'HOLAAA :p')
        data = s.recv(1024)

        print('Recibido: ' + str(repr(data)))

