#/usr/bin/env python3
import socket           
import sys
import os
import select
import pickle
import signal
import datetime
import math
import time 


#Note: We declare here the server descriptor and the log file to be "global variables"
#      and that these can be accessed by the CTRL + C handler and the connection 
#      can be closed correctly(the log file too). This can be done with POO in a cleaner way
#      but I do not have enough time to do it, it is as future improvement for the holidays :) ,
#      let's say that this is the version: ChatPy v1.0
#
#   For more info: github.com/davidcawork

#Global vars
MAX_MSG_SAVED = 20 
CHUNCK_SIZE = 256

#We parse the info to be able to connect to the server
name = sys.argv[1]
host = sys.argv[2]
port = int(sys.argv[3])

#To connect with our server 
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((host,port))

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

#Just for logs
current_time = datetime.datetime.now()
logs = create_logs(name,current_time)


#Handler CTRL+C - Close connection with server
def signal_handler(sig, frame):
    logs.close()
    s.close()
    print('\n\nGoodbye!\n')
    sys.exit(0)

#to get cmd written
def is_command(msg, str_cmd):
    return msg.count(str_cmd)

#To print /help cmd
def print_help(name):
    sys.stdout.flush()
    os.system('clear')
    print('Hi '+name+' !\n\n')
    print('These are the commands that you can use:\n')
    print('\t/help\tTo consult the commands and guides for using the chat')
    print('\t/file\tTo send a file to all multichat users\n\t\tUse: /file <name_of_the_file>')
    print('\t/quit\tTo exit the multichat')
    print('\t/timeup\tTo get the time you have connected in the chat')
    print('\t/stats\tTo get statistics about your activity in the chat')        
    print('\n\nFor more help you can check: https://github.com/davidcawork\n\n')
    
    input("Press Enter to continue...")
    os.system('clear')

#To print msg_history
def print_msgs(msg_history):
    sys.stdout.flush()
    os.system('clear')
    for msg in msg_history:
        print(msg)

#To manege msg's
def add_to_msgHistory(msg_history,msg):

    if len(msg_history) == MAX_MSG_SAVED:
        msg_history.pop(0)
    
    msg_history.append(msg)

#To get the file name
def file_split(line):

    return (line.split(' '))[1]

#To get time up in the multichat
def timeup_cmd(name,time_init):
    os.system('clear')
    print('Hi '+name+' !\n\n')
    time_b = datetime.datetime.now()
    print('You have '+str(time_b - time_init)+' time in the chat n.n\n\n\n')
    input("Press Enter to continue...")
    os.system('clear')

#To get our stats :)
def stats_cmd(name,msg_sent,msg_rcv,files_sent,files_rcv,cmd_used,time_init,len_msg_history):

    os.system('clear')
    print('Hi '+name+' !\n\n')
    time_b = datetime.datetime.now()
    print('Your stats in the multichat:\n')
    print('1.\t Msg sent     : '+str(msg_sent))
    print('2.\t Msg rcv      : '+str(msg_rcv))
    print('3.\t Files sent   : '+str(files_sent))
    print('4.\t Files rcv    : '+str(files_rcv))
    print('5.\t Commands used: '+str(cmd_used))
    print('6.\t msg_History  : '+str(len_msg_history))
    print('7.\t Time up      : '+str(time_b -time_init)+'\n\n')  
    
    input("Press Enter to continue...")
    os.system('clear')


if __name__ == "__main__":

    #Check argv's
    if len(sys.argv) != 4:
        print('Error: usage: ./' + sys.argv[0] + ' <username> <destination/IP> <Port>')
        sys.exit(0)
    else:
        #Let's to prepare the CTRL + C signal to handle it and be able  to close the connection
        signal.signal(signal.SIGINT, signal_handler)

        #Track time up in the multichat 
        time_init = datetime.datetime.now()

        #To track stats
        msg_sent = 0
        msg_rcv = 0
        files_sent = 0
        files_rcv = 0
        cmd_used = 0

        #Track all msg
        msg_history = []

        #Main loop
        while True:
            events_rd,events_wr,events_excp = select.select([sys.stdin,s],[],[])

            for event in events_rd:
                if event == s:
                    data = pickle.loads(s.recv(512))
                    #keys_msg = list(sorted(data.keys()))

                    if data:
                        
                        if data[1] == 'msg':
                            if data[0] is not name:
                                msg_rcv +=1
                                now = datetime.datetime.now()
                                add_to_msgHistory(msg_history,'['+now.strftime('%H:%M:%S')+'] '+data[0]+': '+data[2])
                                print_msgs(msg_history)
                                logs.write('['+now.strftime('%H:%M:%S')+'] '+data[0]+': '+data[2])
                        elif data[1] == 'file':
                            files_rcv += 1
                            now = datetime.datetime.now()
                            print('['+now.strftime('%H:%M:%S')+'] Downloading '+data[2]+' file from '+data[0]+' ('+str(data[3])+' bytes)')
                            #time.sleep(2)
                            
                            with open(data[2], "wb") as f:        
                                chunk = s.recv(CHUNCK_SIZE)
                                #while chunk[2] is not 'fin':
                                for chunck in range(0,data[3]):
                                    f.write(chunk)
                                    chunk = s.recv(CHUNCK_SIZE)
                                    if not chunk:
                                        break
                            now = datetime.datetime.now()
                            print('['+now.strftime('%H:%M:%S')+'] It has already been downloaded :)')
                    else:
                        logs.close()
                        s.close()
                        print('Goodbye!\n')

                # Stdin event
                elif event == sys.stdin:
                    msg = input()

                    if is_command(msg,'/file'):
                        #To send a file  
                        files_sent +=1
                        cmd_used +=1
                        name_file = file_split(msg)
                        chuncks = math.ceil(float(os.path.getsize(os.getcwd()+'/'+name_file))/CHUNCK_SIZE)
                        s.sendall(pickle.dumps([name,'file',name_file,chuncks]))
                        now = datetime.datetime.now()
                        print('['+now.strftime('%H:%M:%S')+'] Sharing '+name_file+' with all the users of the multichat...')
                        time.sleep(4)
                        
                        with open(name_file, 'rb') as f:
                            for line in f:
                                s.sendall(line)

                    elif is_command(msg,'/quit'):
                        #To quit the multichat
                        s.close()
                        logs.close()
                        os.system('clear')
                        print('\n\nGoodbye!\n')
                        sys.exit(0)       
                   
                    elif is_command(msg,'/help'):
                        #To print help msg
                        cmd_used +=1 
                        print_help(name)
                        print_msgs(msg_history)

                    elif is_command(msg,'/timeup'):
                        #To print time up in the multichat 
                        cmd_used +=1
                        timeup_cmd(name,time_init)
                        print_msgs(msg_history)

                    elif is_command(msg,'/stats'):
                        #To print our stats in the multichat
                        cmd_used +=1
                        stats_cmd(name,msg_sent,msg_rcv,files_sent,files_rcv,cmd_used,time_init,len(msg_history))
                        print_msgs(msg_history)
                    else:
                        #To send a msg
                        msg_sent+=1
                        s.sendall(pickle.dumps([name,'msg',msg]))
                        now = datetime.datetime.now()
                        add_to_msgHistory(msg_history,'['+now.strftime('%H:%M:%S')+'] Tu: '+msg)
                        print_msgs(msg_history)
                        logs.write('['+now.strftime('%H:%M:%S')+'] Tu: '+msg+'\n')
                        


        

        



