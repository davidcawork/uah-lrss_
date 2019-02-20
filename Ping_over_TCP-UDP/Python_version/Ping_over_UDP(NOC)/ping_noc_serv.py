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
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.bind(('127.0.0.1',port))
                    
        while True:
            data,addr = s.recvfrom(1024)
            print('Cliente: ' + str(addr[0]) + '| Port: '+str(addr[1]))
            if not data:
                break
            s.sendto(b'Ping : Reply (0)_______________',(addr[0],addr[1]))