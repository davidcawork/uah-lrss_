 #usr/bin/env python3

import socket
import sys




if __name__ == "__main__":
    #Check argv's
    if len(sys.argv) < 2:
        print('Error: usage: ./' + sys.argv[0] + ' <destination/IP> <Port>')
        exit()
    else:
        #Just create a socket, and bind it
        port = int(sys.argv[1])        
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.bind(('',port))
                    
        while True:
            #Wait for data :))
            data,addr = s.recvfrom(1024)
            print('Client: ' + str(addr[0]) + '| Port: '+str(addr[1]))
            if not data:
                break
            #Reply our client
            s.sendto(b'Ping : Reply (0)_______________',(addr[0],addr[1]))