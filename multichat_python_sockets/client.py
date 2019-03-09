#/usr/bin/env python3
import socket
import sys
import os
import select
import pickle
import signal
import datetime

#Global vars
MAX_MSG_SAVED = 20 

#Handler CTRL+C - Close connection with server
def signal_handler(sig, frame):
    logs.close()
    s.close()
    print('Goodbye!\n')
    sys.exit(0)

#To log all msg 
def create_logs(name,current_time):
    isLogDirCreate = False
    path = os.getcwd()
    list_dir = os.listdir(path)
    LogDir = 'logs'
    for files in list_dir:
        if files == LogDir:
            try:
                isLogDirCreate = True
                log_file=open(path +'/'+LogDir+'/log_'+name+'_'+current_time.strftime('%Y-%m-%d')+'.txt','w')
            except:
                print('Error: cannot create log files: '+path +'/'+LogDir+'/log_'+
                name+'_'+current_time.strftime('%Y-%m-%d')+'.txt')
    
    if not isLogDirCreate:
        os.mkdir(path+'/'+LogDir)
        try:
            log_file=open(path +'/'+LogDir+'/log_'+name+'_'+current_time.strftime('%Y-%m-%d')+'.txt','w')
        except:
            print('Error: cannot create log files: '+path +'/'+LogDir+'/log_'
            +name+'_'+current_time.strftime('%Y-%m-%d')+'.txt')
    
    return log_file
    
def is_command(msg, str_cmd):
    return msg.count(str_cmd)

def print_help(name):
    sys.stdout.flush()
    os.system('clear')
    print('Hi '+name+' !\n\n')
    print('These are the commands that you can use:\n')
    print('\t/help\tTo consult the commands and guides for using the chat')
    print('\t/file\tto send a file to all multichat users, use:\n\t\t /file <path_to_file> <name_of_the_file>')
    print('\n\nFor more help you can check: https://github.com/davidcawork\n\n')
    input("Press Enter to continue...")
    os.system('clear')

def print_msgs(msg_history):
    sys.stdout.flush()
    os.system('clear')
    for msg in msg_history:
        print(msg)

def add_to_msgHistory(msg_history,msg):

    if len(msg_history) == MAX_MSG_SAVED:
        msg_history.pop(0)
    
    msg_history.append(msg)

if __name__ == "__main__":

    #Check argv's
    if len(sys.argv) != 4:
        print('Error: usage: ./' + sys.argv[0] + ' <username> <destination/IP> <Port>')
        sys.exit(0)
    else:
        #Let's to prepare the CTRL + C signal to handle it and be able  to show the statistics before it comes out
        signal.signal(signal.SIGINT, signal_handler)

        #We parse the info to be able to connect to the server
        name = sys.argv[1]
        host = sys.argv[2]
        port = int(sys.argv[3])

        #To connect with our server 
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((host,port))

        #Just for logs
        current_time = datetime.datetime.now()
        logs = create_logs(name,current_time)

        #Track all msg
        msg_history = []

        #Main loop
        while True:
            events_rd,events_wr,events_excp = select.select([sys.stdin,s],[],[])

            for event in events_rd:
                if event == s:
                    data = pickle.loads(s.recv(4096))
                    #keys_msg = list(sorted(data.keys()))

                    if data:
                        
                        if data[1] == 'msg':
                            if data[0] is not name:
                                now = datetime.datetime.now()
                                add_to_msgHistory(msg_history,'['+now.strftime('%H:%M:%S')+'] '+data[0]+': '+data[2])
                                print_msgs(msg_history)
                        elif data[1] == 'file':
                            print('Handle a file') 
                    else:
                        logs.close()
                        s.close()
                        print('Goodbye!\n')

                elif event == sys.stdin:
                    msg = input()

                    if is_command(msg,'/file'):  
                        print('XDDD')

                    elif is_command(msg,'/help'):
                        #To print help msg 
                        print_help(name)

                    else:
                        #To send a msg
                        s.sendall(pickle.dumps([name,'msg',msg]))
                        now = datetime.datetime.now()
                        add_to_msgHistory(msg_history,'['+now.strftime('%H:%M:%S')+'] Tu: '+msg)
                        print_msgs(msg_history)
                        logs.write('['+now.strftime('%H:%M:%S')+'] Tu: '+msg+'\n')
                        


        

        



