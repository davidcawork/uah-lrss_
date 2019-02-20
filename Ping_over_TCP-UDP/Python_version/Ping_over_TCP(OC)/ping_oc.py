#usr/bin/env python3

import socket
import sys
import signal
from datetime import datetime, date, time, timedelta
import time

shouldSend = True

def signal_handler(sig, frame):
    shouldSend = False
    sys.exit(0)

if __name__ == "__main__":

    if len(sys.argv) < 3 or len(sys.argv) > 3:
        print('Error: usage: ./' + sys.argv[0] + ' <destination/IP> <Port>')
        sys.exit(0)
    else:
        signal.signal(signal.SIGINT, signal_handler)

        num_seq = 0

        host = sys.argv[1]
        port = int(sys.argv[2]) 
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((host,port))
        (server_addr, server_port) = s.getpeername()
        print('\nPING '+ sys.argv[1] +' ('+ str(server_addr) +') with '+ str(sys.getsizeof('Ping : Request (8)'))+' bytes of data.')
        while shouldSend:
            time.sleep(2)
            t_init = time.time()
            s.sendall(b'Ping : Request (8)\n')
            data = s.recv(1024)
            t_fin = time.time()
            num_seq +=1
            print(str(sys.getsizeof(data))+' bytes from '+ sys.argv[1] +' ('+str(server_addr)+'): num_seq='+str(num_seq)+' time={:.4f}ms'.format(1000*(t_fin - t_init)))

