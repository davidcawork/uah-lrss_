#usr/bin/env python3

import socket
import sys


if __name__ == "__main__":
    #Check argv's
    if len(sys.argv) < 2:
        print('Error: usage: ./' + sys.argv[0] + ' <destination/IP> <Port>')
        exit()
    else:

        port = int(sys.argv[1])        
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        #Bind it
        s.bind(('',port))

        #Wait for our clients n.n 
        s.listen()
        connection,addr = s.accept()

        with connection:
            #I/O
            print('Client: ' + str(addr[0]) + '| Port: '+str(addr[1]))
            while True:
                #Recv time
                data = connection.recv(1024)
                if not data:
                    break
                #Reply client request
                connection.sendall(b'Ping : Reply (0)_______________')