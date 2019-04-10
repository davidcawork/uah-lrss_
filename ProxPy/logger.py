#usr/bin/env python3

import socket
import sys
import os
import pickle
import datetime
import time 

#Note: 
#
#
#
#   For more info: github.com/davidcawork

#Global Vars
BUFFER_SIZE = 1024*5


#To get our socket UDP, where we will hear logs from ProxPy
def get_our_socket(port = '8010'):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.bind(('',port))
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        return s
    except:
        new_port = randint(8000, 9000)
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.bind(('',new_port))
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        return s

#To create log dir and get fd 
def create_logs(name,current_time):
    isLogDirCreate = False
    path = os.getcwd()
    list_dir = os.listdir(path)
    LogDir = 'logs'
    for files in list_dir:
        if files == LogDir:
            try:
                isLogDirCreate = True
                log_file=open(path +'/'+LogDir+'/log_'+name+'_'+current_time.strftime('%Y-%m-%d')+'.log','a+')
            except:
                print('Error: cannot create log files: '+path +'/'+LogDir+'/log_'+
                name+'_'+current_time.strftime('%Y-%m-%d')+'.log')
    
    if not isLogDirCreate:
        os.mkdir(path+'/'+LogDir)
        try:
            log_file=open(path +'/'+LogDir+'/log_'+name+'_'+current_time.strftime('%Y-%m-%d')+'.log','a+')
        except:
            print('Error: cannot create log files: '+path +'/'+LogDir+'/log_'
            +name+'_'+current_time.strftime('%Y-%m-%d')+'.log')
    
    return log_file

#To log incoming data
def logger(file_to_log, data):
    current_time = datetime.datetime.now()
    try:
        if data[1] == 'REQUEST':
            file_to_log.write('['+(datetime.datetime.now()).strftime('%H:%M:%S')+'] '+ 'REQUEST\n' )
        elif data[1] == 'REPLY':
            file_to_log.write('['+(datetime.datetime.now()).strftime('%H:%M:%S')+'] '+ 'REPLY\n')
    except:
        file_to_log.close()
        exit(-1)



if __name__ == "__main__":
    #Check argv's
    if len(sys.argv) != 2:
        print('Error: Usage: pyhton3 ' + sys.argv[0] + ' <Port>')
        exit(0)
    else:
        #Just create a socket, and bind it
        our_port = int(sys.argv[1])
        name = 'ProxPy'        
        s = get_our_socket(our_port)

        #To create log dir and get fd 
        current_time = datetime.datetime.now()
        logs = create_logs(name,current_time)


        try:          
            while True:
                #Wait for logs :))
                data_b,addr = s.recvfrom(BUFFER_SIZE)

                #Recover the list with pickle
                data = pickle.loads(data_b)

                if data:

                    if data[0] == 'DATA':
                        logger(logs, data)

                    elif data[0] == 'FIN':
                        #Only for SSOO releases the bind made to the port
                        s.close()
                        break
                else:
                    break
                

        except KeyboardInterrupt:
            #Only for SSOO releases the bind made to the port
            s.close()
