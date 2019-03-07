#/usr/bin/env python3
import socket
import sys
import select
import pickle
import signal
from datetime import datetime, date, time, timedelta
import time


#Handler CTRL+C - Close connection with server
def signal_handler(sig, frame):
    shouldSend = False
    stats()
    sys.exit(0)

if __name__ == "__main__":

    #Check argv's
    if len(sys.argv) != 4:
        print('Error: usage: ./' + sys.argv[0] + '<username> <destination/IP> <Port>')
        sys.exit(0)
    else:
        #Let's to prepare the CTRL + C signal to handle it and be able  to show the statistics before it comes out
        signal.signal(signal.SIGINT, signal_handler)

        #We parse the info to be able to connect to the server
        name = sys.argv[1]
        host = sys.argv[2]
        port = int(sys.argv[3]) 
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((host,port))

        while True:
            events_rd,events_wr,events_excp = select.select([sys.stdin,s],[],[])

            for event in events_rd:
                if event == s:
                    data = s.recv(1024)
                    if data:
                        print("Hemos recibido: {}".format(data.decode('utf-8')))
                    else:
                        s.close()
                        print('Goodbye!\n')
                elif event == sys.stdin:
                        msg = input()
                        dic_msg = {name:msg}
                        pickle.dump()
                       
                        #b_msg = bytes(msg, 'utf-8')
                        s.sendall(obj)
                        print('[TIEMPO] Tu: '+msg+'\n')
        

        



