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

#PROTOCOL MSGs
P2P_CHAT_PY_PROTOCOL_HI = 'ChatPy_Hi'
P2P_CHAT_PY_PROTOCOL_HI_ACK = 'ChatPy_Hi_Ack'
P2P_CHAT_PY_PROTOCOL_BYE = 'ChatPy_Bye'
P2P_CHAT_PY_PROTOCOL_BYE_ACK = 'ChatPy_Bye_Ack'
P2P_CHAT_PY_PROTOCOL_UPDATE = 'ChatPy_Update'
P2P_CHAT_PY_PROTOCOL_UPDATE_ACK = 'ChatPy_Update_Ack'
P2P_CHAT_PY_PROTOCOL_CONN = 'ChatPy_Conn'
P2P_CHAT_PY_PROTOCOL_CONN_ACK = 'ChatPy_Conn_Ack'
P2P_CHAT_PY_PROTOCOL_DIS = 'ChatPy_Dis'
P2P_CHAT_PY_PROTOCOL_DIS_ACK = 'ChatPy_Dis_Ack'
P2P_CHAT_PY_PROTOCOL_MSG = 'ChatPy_Msg'

#MACROS
MAX_MSG_SAVED = 20 


#We parse the info to be able to connect to the p2p_server
name = sys.argv[1]
our_port = int(sys.argv[2])
p2p_server_addr = sys.argv[3]
p2p_server_port = int(sys.argv[4])


#To connect with our server 
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.connect((p2p_server_addr,p2p_server_port))

#To bind our listen port
ours_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ours_server.setblocking(0)
ours_server.bind(('',our_port))
ours_server.listen(5)

#To track all readable ways 
ways_to_rd = [sys.stdin,server,ours_server]

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
    server.sendall(pickle.dumps([P2P_CHAT_PY_PROTOCOL_BYE,[name,our_port]]))
    time.sleep(1)
    logs.close()
    server.close()
    ours_server.close()
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
    print('\t/help\t\tTo consult the commands and guides for using the chat')
    print('\t/quit\t\tTo exit, it close all connections')
    print('\t/timeup\t\tTo get the time you have connected in the chat')
    print('\t/stats\t\tTo get statistics about your activity in the chat')
    print('\t/update\t\tTo update your peer list')
    print('\t/showpeers\tTo show your peers table')        
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


#To get time up in the multichat
def timeup_cmd(name,time_init):
    os.system('clear')
    print('Hi '+name+' !\n\n')
    time_b = datetime.datetime.now()
    print('You have '+str(time_b - time_init)+' time in the chat n.n\n\n\n')
    input("Press Enter to continue...")
    os.system('clear')

#To get our stats :)
def stats_cmd(name,msg_sent,msg_rcv,cmd_used,time_init,len_msg_history):

    os.system('clear')
    print('Hi '+name+' !\n\n')
    time_b = datetime.datetime.now()
    print('Your stats in the multichat:\n')
    print('1.\t Msg sent     : '+str(msg_sent))
    print('2.\t Msg rcv      : '+str(msg_rcv))
    print('3.\t Commands used: '+str(cmd_used))
    print('4.\t msg_History  : '+str(len_msg_history))
    print('5.\t Time up      : '+str(time_b -time_init)+'\n\n')  
    
    input("Press Enter to continue...")
    os.system('clear')

def print_peer_table(name, peer_list):
    os.system('clear')
    print('Hi '+name+' !\n\n')
    print('\t\t-- Peer table --\n')
    for peer in peer_list:
        print('+ Name: '+peer[0]+' | Ip: '+str(peer[1])+' | Port: '+peer[2]+' | Id_peer: '+str(peer[3]))
    input("\n\n\nPress Enter to continue...")
    os.system('clear')

def print_conn_table(name, active_conn):
    os.system('clear')
    print('Hi '+name+' !\n\n')
    print('\t\t-- Active connections table --\n')
    for peer in active_conn:
        print('+ Name: '+peer[0]+' | Ip: '+str(peer[1])+' | Port: '+peer[2]+' | Id_peer: '+str(peer[3]))
    input("\n\n\nPress Enter to continue...")
    os.system('clear')

def get_peer_element(peer_list, my_peer_id):

    for peer in peer_list:
        if peer[3] is my_id_peer:
            return peer

def getPeerId(msg):

    return int(msg.split(' ')[1])

def is_already_Connected(active_conn, id_peer):

    for conn in active_conn:
        if conn[3] is id_peer:
            return True

    return False

if __name__ == "__main__":

    #Check argv's
    if len(sys.argv) != 5:
        print('Error: usage: ./' + sys.argv[0] + ' <username> <your_listen_port> <IP_P2P_server> <Port>')
        sys.exit(0)
    else:
        #Let's to prepare the CTRL + C signal to handle it and be able  to close the connection
        signal.signal(signal.SIGINT, signal_handler)

        #Track time up in the multichat 
        time_init = datetime.datetime.now()

        #To track stats
        proto_msg_sent = 0
        proto_msg_rcv = 0
        msg_sent = 0
        msg_rcv = 0
        cmd_used = 0

        #Track all msg
        msg_history = []

        #Peer list
        peer_list = []
        my_id_peer = 0

        #Active_conn
        active_conn = []

        #Say Hi to p2p2 server
        print('Connecting to p2p server...')
        time.sleep(2)
        server.sendall(pickle.dumps([P2P_CHAT_PY_PROTOCOL_HI,[name,our_port]]))
        proto_msg_sent += 1

        #Main loop
        while True:
            events_rd,events_wr,events_excp = select.select(ways_to_rd,[],[])

            for event in events_rd:
                if event is server:
                    data = pickle.loads(server.recv(1024))
                    if data:
                        if data[0] == P2P_CHAT_PY_PROTOCOL_HI_ACK:
                            #We got the peer_list
                            peer_list = data[1]
                            my_id_peer = data[2]
                            now = datetime.datetime.now()
                            os.system('clear')
                            msg_history.append('['+now.strftime('%H:%M:%S')+'] The list of peers was received correctly, '+str(len(peer_list))+' total active peers')
                            print_msgs(msg_history)

                        elif data[0] == P2P_CHAT_PY_PROTOCOL_BYE_ACK:
                            
                            logs.close()
                            server.close()
                            ours_server.close()
                            #Cerrar con lod demas chats

                            now = datetime.datetime.now()
                            msg_history.append('['+now.strftime('%H:%M:%S')+'] Closing all connections ...')
                            print_msgs(msg_history)
                            print('\n\nGoodbye '+name+'!\n')
                            input("Press Enter to continue...")
                            sys.exit(0)

                        elif data[0] == P2P_CHAT_PY_PROTOCOL_UPDATE_ACK:
                            #We updated the peer_list
                            peer_list = data[1]
                            now = datetime.datetime.now()
                            os.system('clear')
                            msg_history.append('['+now.strftime('%H:%M:%S')+'] The list of peers was updated correctly, '+str(len(peer_list))+' total active peers')
                            print_msgs(msg_history)
                            
                    else:
                        logs.close()
                        server.close()
                        ours_server.close()
                        print('Goodbye!\n')

                elif event is ours_server:
                    #Accept user to chat with him
                    conn, addr = ours_server.accept()
                    conn.setblocking(0)
                    ways_to_rd.append(conn)

                # Stdin event
                elif event is sys.stdin:
                    msg = input()

                    if is_command(msg,'/quit'):
                        #To quit the multichat
                        os.system('clear')
                        server.sendall(pickle.dumps([P2P_CHAT_PY_PROTOCOL_BYE,[name,our_port],my_id_peer]))  

                    elif is_command(msg, '/update'):
                        #Request update to p2p2 server
                        cmd_used +=1 
                        proto_msg_sent += 1
                        os.system('clear')
                        server.sendall(pickle.dumps([P2P_CHAT_PY_PROTOCOL_UPDATE,[name,our_port],my_id_peer]))
                        proto_msg_sent += 1

                    elif is_command(msg,'/help'):
                        #To print help msg
                        cmd_used +=1 
                        print_help(name)
                        print_msgs(msg_history)

                    elif is_command(msg,'/conn'):
                        #To connect with someone
                        cmd_used +=1 
                        proto_msg_sent += 1

                        id_to_conn = getPeerId(msg)
                        if not is_already_Connected(id_to_conn):

                            try:
                                peer_to_conn = get_peer_element(peer_list, id_to_conn)
                            except:
                                msg_history.append('['+now.strftime('%H:%M:%S')+'] Id_peer: '+peer_to_conn[0]+' not found ...')

                            msg_history.append('['+now.strftime('%H:%M:%S')+'] Connecting with '+peer_to_conn[0]+' ...')
                            
                            aux_peer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                            aux_peer.connect((peer_to_conn[2],peer_to_conn[1]))
                            
                            time.sleep(1)
                            aux_peer.sendall([P2P_CHAT_PY_PROTOCOL_CONN,get_peer_element(peer_list,my_id_peer))
        
                        else:
                            msg_history.append('['+now.strftime('%H:%M:%S')+'] Id_peer: '+str(peer_to_conn[3])+' already in use...')
                        print_msgs(msg_history)

                    elif is_command(msg,'/dis'):
                        #To disconnect with someone
                        cmd_used +=1 
                        proto_msg_sent += 1


                        print_msgs(msg_history)

                    elif is_command(msg,'/msg'):
                        #To communicate with some peers, or single one
                        # /msg [id1,id2] @msg
                        cmd_used +=1 
                        proto_msg_sent += 1

                        print_msgs(msg_history)

                    elif is_command(msg,'/showpeers'):
                        #To print peer's table
                        cmd_used +=1
                        print_peer_table(name, peer_list) 
                        print_msgs(msg_history)
                    
                    elif is_command(msg,'/showconn'):
                        #To print active connections table
                        cmd_used +=1
                        print_conn_table(name, active_conn) 
                        print_msgs(msg_history)

                    elif is_command(msg,'/timeup'):
                        #To print time up in the multichat 
                        cmd_used +=1
                        timeup_cmd(name,time_init)
                        print_msgs(msg_history)

                    elif is_command(msg,'/stats'):
                        #To print our stats in the multichat
                        cmd_used +=1
                        stats_cmd(name,msg_sent,msg_rcv,cmd_used,time_init,len(msg_history))
                        print_msgs(msg_history)
                    else:
                        now = datetime.datetime.now()
                        add_to_msgHistory(msg_history,'['+now.strftime('%H:%M:%S')+'] Tu: '+msg)
                        print_msgs(msg_history)
                        logs.write('['+now.strftime('%H:%M:%S')+'] Tu: '+msg+'\n')
                
                #To handle events from peers
                else:

                    for peer in ways_to_rd:
                        if peer is not server and peer is not ours_server and peer is not sys.stdin:
                            data= pickle.loads(peer.recv(1024))
                            if data:
                                if data[0] == P2P_CHAT_PY_PROTOCOL_CONN:
                                    active_conn.append(data[1])
                                    peer.sendall(pickle.dumps(P2P_CHAT_PY_PROTOCOL_CONN_ACK,get_peer_element(peer_list,my_id_peer)))
                                    
                                elif data[0] == P2P_CHAT_PY_PROTOCOL_CONN_ACK:

                                elif data[0] == P2P_CHAT_PY_PROTOCOL_DIS:

                                elif data[0] == P2P_CHAT_PY_PROTOCOL_DIS_ACK:

                                elif data[0] == P2P_CHAT_PY_PROTOCOL_MSG:

                            else:
                                peer.close()
                                ways_to_rd.remove(peer)
                    


                        


        

        



