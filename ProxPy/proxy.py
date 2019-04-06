#/usr/bin/env python3
import socket           
import sys
import os
import select
import time
import datetime

#Note: 
#
#
#
#   For more info: github.com/davidcawork

#Global vars
MSG_PROXPY_INACTIVE = '[ProxPy] Proxy inactive ...'
ERROR_TO_RCV_FROM_NAV = '[ProxPy] Error to recover the request from: '






#To get our socket TCP, where we will hear connections from web navigators
def get_our_socket(port):

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setblocking(0)
    s.bind(('',port))
    s.listen(5)
    return s

#Aux func to know if one item is in one list
def is_in_the_list(list_, element):

    for items in list_:
        if list_.count(element):
            return True

    return False

#To get ProxPy str time format
def get_str_time_ProxPy():
    return ('['+(datetime.datetime.now()).strftime('%H:%M:%S')+'] ')

#To get the Host from request
def get_host_from_request(data):

    for lines in  data.split('\r\n'):
        if line.count('Host: '):
            return line.split('Host: ')[0]

#To get the Resource from request
def get_resource_from_request(data):

    for lines in  data.split('\r\n'):
        if line.count('GET '):
            return line.split('Host: ')[0]


if __name__ == "__main__":

    #Check argv's
    if len(sys.argv) != 3:
	    print('Error: usage: ./' + sys.argv[0] + ' <Port>')
	    exit(0)
    
    else:

        # --- Vars ----
        proxy_port = int(sys.argv[1])
        proxy_timeout = 300.0
        debug_mode = bool(sys.argv[2])

	    #Prepare our TCP socket where we will hear connections from web navigators
        our_proxy_socket = get_our_socket(proxy_port)

        #Prepare our udp socket where w'ill log every single pet.
        # 


        #Sockets to read
        sockets_rd = [our_proxy_socket]

        #To save 
        #Input connections
        input_conn = []

        #Output connections 
        output_conn = []

        
        # We can exit by CTRL+C signal
        while True:
            try:

	    		# The optional timeout argument specifies a time-out as a floating point number in seconds.
                events_rd,events_wr,events_excp = select.select( sockets_rd,[],[])

            except KeyboardInterrupt:
                print('\n\n\nShutdown ProxPy....')
                for sock in sockets_rd:
                    sock.close()
                sys.exit(0)

            for event in events_rd:

                if event == our_proxy_socket:

                	#Accept input conn from web navigator
                    conn, addr = our_proxy_socket.accept()
                    conn.setblocking(0)
                    sockets_rd.append(conn)
                    input_conn.append(conn)

                else:
            	    #Handle other conn
                    for sock_to_rcv in sockets_rd:
                        #To manage request from web nav. connections 
                        if sock_to_rcv != our_proxy_socket and sock_to_rcv is event and is_in_the_list(input_conn,sock_to_rcv):
                
                            #Recover request from Web nav
                            try:
                                data = sock_to_rcv.recv(1024*1000)
                                if debug_mode:
                                    print("{}".format(data.decode('utf-8')))
                            except:
                                print( get_str_time_ProxPy() + ERROR_TO_RCV_FROM_NAV + sock_to_rcv.getsockname()[0]+':'+sock_to_rcv.getsockname()[1])
                            
                            if data:
                                #Parse the request
                                host = get_host_from_request(str(data))
                                content = get_resource_from_request(str(data))

                                # 
                            else:
                                sock_to_rcv.close()
                                sockets_rd.remove(sock_to_rcv)
                                input_conn.remove(sock_to_rcv)


                        elif sock_to_rcv != our_proxy_socket and sock_to_rcv is event and is_in_the_list(output_conn,sock_to_rcv):

                            try:
                                sockets_rd[2].sendall(request.recv(1024*1000))
                            except:
                                print("[2] Error al hacer reply\n\n\n")
