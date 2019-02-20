 #usr/bin/env python3

import socket
import sys


#usr/bin/env python3

import socket
import sys


if __name__ == "__main__":

    if len(sys.argv) < 2:
        print('Error: usage: ./' + sys.argv[0] + ' <destination/IP> <Port>')
        exit()
    else:
        port = int(sys.argv[1])        
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind(('127.0.0.1',port))
        s.listen()
        conn,addr = s.accept()
        with conn:
            print('Cliente: ' + str(addr[0]) + '| Port: '+str(addr[1]))
            while True:
                data = conn.recv(1024)
                if not data:
                    break
                conn.sendall(b'Ping : Reply (0)_______________')