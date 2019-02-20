#usr/bin/env python3

import socket
import sys
import signal
from datetime import datetime, date, time, timedelta
import time

#GLobal var.
shouldSend = True
lista_tm = []
num_pck = 0

def sumarlista(lista_tm):
    sum = 0

    for i in lista_tm:
        sum += lista_tm
    return sum

def stats():
    print('\n--- '+sys.argv[1]+' ping statistics ---\n')
    print(str(num_pck)+' packets transmitted, '+str(num_pck)+' received, 0.0% packet loss, time average  (s)\n\n')

def signal_handler(sig, frame):
    shouldSend = False
    stats()
    sys.exit(0)

def stats_ping(dic_time, num_seq, server , host ,total_time):
    print('\n--- '+sys.argv[1]+' ping statistics ---\n')
    print(str(num_seq)+' packets transmitted, %d received, %0.3f%c packet loss, total time %0.2f (s)')
if __name__ == "__main__":

    if len(sys.argv) < 3 or len(sys.argv) > 3:
        print('Error: usage: ./' + sys.argv[0] + ' <destination/IP> <Port>')
        sys.exit(0)
    else:
        signal.signal(signal.SIGINT, signal_handler)

        num_seq = 0

        host = sys.argv[1]
        port = int(sys.argv[2]) 
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        server_addr = socket.gethostbyname(host)
        print('\nPING '+ sys.argv[1] +' ('+ str(server_addr) +') with '+ str(sys.getsizeof('Ping : Request (8)'))+' bytes of data.')
        while shouldSend:
            time.sleep(2)
            t_init = time.time()
            s.sendto(b'Ping : Request (8)\n', (host,port))
            data = s.recvfrom(1024)
            t_fin = time.time()
            num_seq += 1
            lista_tm.append(1000*(t_fin - t_init))
            num_pck += 1
            print(str(sys.getsizeof(data))+' bytes from '+ sys.argv[1] +' ('+str(server_addr)+'): num_seq='+str(num_seq)+' time={:.4f}ms'.format(1000*(t_fin - t_init)))

