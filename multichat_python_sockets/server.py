#usr/bin/env python3

import socket
import sys
import pickle
import select
import os

#To print all clients connected
def print_conn(sock_addr_port):
    
    os.system('clear')
    for clients in sock_addr_port:
        print('Client: ' + str(clients[1]) + '| Port: '+str(clients[2]))

#To remove from list when some client goes out 
def remove_client_from_list(sock_addr_port,sock_to_remove):

    for clients in sock_addr_port:
        if clients[0] is sock_to_remove:
            sock_addr_port.remove(clients)


if __name__ == "__main__":
    #Check argv's
    if len(sys.argv) < 2:
        print('Error: usage: ./' + sys.argv[0] + ' <Port>')
        exit()
    else:

        port = int(sys.argv[1])        
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setblocking(0)
        s.bind(('',port))
        s.listen(5)

        #Sockets to read
        sockets_rd = [s]

        #Just for track all conn
        sock_addr_port = []

        while True:
            try:
                events_rd,events_wr,events_excp = select.select( sockets_rd,[],[])
            except KeyboardInterrupt:
                print('\n\n\nShutdown....')
                for sock in sockets_rd:
                    sock.close()
                sys.exit(0)

            for event in events_rd:

                if event == s:
                    #Add user into multichat :)
                    conn, addr = s.accept()
                    sock_addr_port.append([conn,addr[0],addr[1]])
                    conn.setblocking(0)
                    sockets_rd.append(conn)
                else:
                    #Handle other conn
                    for sock_to_rcv in sockets_rd:
                        if sock_to_rcv != s and sock_to_rcv is event:
                            data = sock_to_rcv.recv(4096)
                            if data:
                                for sock_to_send in sockets_rd:
                                    if sock_to_send is not sock_to_rcv and sock_to_send is not s :
                                        sock_to_send.sendall(data)
                                        
                            else:
                                #Remove one client
                                sock_to_rcv.close()
                                sockets_rd.remove(sock_to_rcv)
                                remove_client_from_list(sock_addr_port,sock_to_rcv)
                
                #Print al active conn
                print_conn(sock_addr_port)
            

