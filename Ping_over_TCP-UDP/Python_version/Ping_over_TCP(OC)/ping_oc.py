#usr/bin/env python3

import socket
import sys
import signal
from datetime import datetime, date, time, timedelta
import time

#GLobal var.
shouldSend = True
lista_tm = ()
num_pck_sent = 0
num_pck_rcv = 0
aux_timer = 0.0


#Stats info
def stats():
    print('\n--- '+sys.argv[1]+' ping statistics ---\n')
    print(str(num_pck_sent)+' packets transmitted, '+str(num_pck_rcv)+' received, '+str(100*((num_pck_sent-num_pck_rcv)/num_pck_sent))+'% packet loss, time average {:.4f} (ms)\n\n'.format(aux_timer/num_pck_sent))

#Handler CTRL+C
def signal_handler(sig, frame):
    shouldSend = False
    stats()
    sys.exit(0)


if __name__ == "__main__":

    #Check argv's
    if len(sys.argv) != 3:
        print('Error: usage: ./' + sys.argv[0] + ' <destination/IP> <Port>')
        sys.exit(0)
    else:
        #Let's to prepare the CTRL + C signal to handle it and be able  to show the statistics before it comes out
        signal.signal(signal.SIGINT, signal_handler)

        #We parse the info to be able to connect to the server
        num_seq = 0
        host = sys.argv[1]
        port = int(sys.argv[2]) 
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        s.connect((host,port))

        #First ping
        (server_addr, server_port) = s.getpeername()
        print('\nPING '+ sys.argv[1] +' ('+ str(server_addr) +') with '+ str(sys.getsizeof('Ping : Request (8)'))+' bytes of data.')

        while shouldSend:
            
            #Just send each 2 sec
            time.sleep(2)
            t_init = time.time()
            
            #Send time
            s.sendall(b'Ping : Request (8)\n')
            num_pck_sent += 1

            #Recv time 
            data = s.recv(1024)
            num_seq +=1
            num_pck_rcv += 1

            #Track rtt
            t_fin = time.time()
            aux_timer +=(1000*(t_fin - t_init))
            
            #I/0 
            print(str(sys.getsizeof(data))+' bytes from '+ sys.argv[1] +' ('+str(server_addr)+'): num_seq='+str(num_seq)+' time={:.4f} ms'.format(1000*(t_fin - t_init)))

