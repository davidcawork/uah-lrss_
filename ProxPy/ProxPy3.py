#/usr/bin/env python3
import socket           
import sys
import os
import select
import time
import datetime
import signal
import pickle
from random import *

#Note: 
#
#
#
#   For more info: github.com/davidcawork

#Global vars
VERSION_MAJOR_NUMBER = 1
VERSION_MINOR_NUMBER = 0
DEBUG_LEVEL_MAX = 3
DEBUG_LEVEL_NORMAL = 2
DEBUG_LEVEL_LOW = 1
MSG_PROXPY_INACTIVE = '[ProxPy] ProxPy inactive ...'
MSG_PROXPY_HI = '[ProxPy] Welcome to ProxPy CLI'
MSG_PROXPY_BYE = '[ProxPy] Turning off ProxPy ....'
MSG_PROXPY_VERSION = '[ProxPy] Current version is: ProxPy v'+ str(VERSION_MAJOR_NUMBER) + '.' + str(VERSION_MINOR_NUMBER)
MSG_PROXPY_NEW_INPUT_CONN = '[ProxPy] New input connection from: '
MSG_PROXPY_LOG_DATA = '[ProxPy] Log data'
MSG_PROXPY_LOG_BYE = '[ProxPy] Bye!'
MSG_PROXPY_LOG_REQ = '[ProxPy] Log data: Request'
MSG_PROXPY_LOG_RPLY = '[ProxPy] Log data: Reply'
ERROR_BAD_ARGVS_FROM_USER = '[ProxPy] Error, incorrect arguments: '
ERROR_TO_RCV_FROM_NAV = '[ProxPy] Error, cannot recover the request from: '
ERROR_TO_RCV_FROM_SW =  '[ProxPy] Error, cannot recover the server reply from: '
ERROR_TO_SEND_REQUEST = '[ProxPy] Error, cannot send the request to the server, connecting again...'
ERROR_TO_CONN_WITH_SW = '[ProxPy] Error, cannot connect with Server: '
ERROR_TO_CLOSE_INPUT_CONN = '[ProxPy] Error, cannot close the input connections: '
ERROR_TO_CLOSE_OUTPUT_CONN = '[ProxPy] Error, cannot close the output connections: '
ERROR_TO_CLOSE_CONN = '[ProxPy] Error, cannot close the connections: '
ERROR_TO_BIND_OUR_PORT = '[ProxPy] Error, our listening port is already in use, instead we use port: '
ERROR_TO_PREPARE_REQUEST= '[ProxPy] Error, cannot prepare the request: '
ERROR_TO_REPLY_NAV = '[ProxPy] Error, cannot process the request: '
ERROR_TO_LOG_REQUEST = '[ProxPy] Error, cannot log the request'
ERROR_TO_LOG_REPLY = '[ProxPy] Error, cannot log the reply'

#MACROS (str)
CRLF = '\r\n'  #Carriage return AND line feed
WSP = ' '
NSP = ''
COLON = ':'

#MACROS (byte)
CRLF_B = b'\r\n'  #Carriage return AND line feed
WSP_B = b' '
NSP_B = b''
COLON_B = b':'

#To get our socket TCP, where we will hear connections from web navigators
def get_our_socket(port):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setblocking(0)
        s.bind(('',port))
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.listen(5)
        return s
    except:
        new_port = randint(8000, 9000)
        print(get_str_time_ProxPy()+ERROR_TO_BIND_OUR_PORT+ str(new_port))
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setblocking(0)
        s.bind(('',new_port))
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.listen(5)
        return s

#Aux func to know if one item is in one list
def is_in_the_list(list_, element):

    if list_.count(element):
        return True

    return False

#To get ProxPy str time format
def get_str_time_ProxPy():
    return ('['+(datetime.datetime.now()).strftime('%H:%M:%S')+'] ')

#To parse all incoming HTTP request
def http_request_parser(data):

    #Request dic
    request = { 'method': '-', 'version': '-', 'uri': '-', 'header_count': 0, 'headers_list': [], 'body': '-'}
    
    http_request_parser_line(request, data.split(CRLF)[0])
    http_request_parser_headers(request,data.split(CRLF)[1:])
    http_request_parser_body(request, data.split(CRLF)[request['header_count'] + 1 :])

    return request

#To handle bad argvs
def bad_argvs_handler():
    print( get_str_time_ProxPy() + ERROR_BAD_ARGVS_FROM_USER +  '\n\n\t Usage: python3 ' + 
                sys.argv[0] + ' <Port> .... \n\n\n For more help you can chek: python3 '+ sys.argv[0] + ' -h\n')

#To parse all incoming HTTP request(Just first line)
def http_request_parser_line(request, data):

    request['method'] = data.split(WSP)[0]
    request['uri'] = data.split(WSP)[1]
    request['version'] = data.split(WSP)[2]

#To parse all incoming HTTP request(headers)
def http_request_parser_headers(request,data):

    for items in data:
        if items == NSP:
            break
        else:    
            request['headers_list'].append([items.split(COLON)[0], (items.split(COLON + WSP)[1]).strip()])
            request['header_count'] += 1 


#To parse all incoming HTTP request(To get the body)
def http_request_parser_body(request, data):

    if data[0] is NSP:
        request['body'] = '-'
    else:
        request['body'] = data[0]

#To get host from request
def get_host_from_header_list(list_):
    
    for item in list_:
        if item[0] == 'Host':
            return item[1]

#To get a conn with WS
def get_conn_to_server(output_conn_request_reply, request):
    #Lo parametrizaremos en el futuro
    port = 80
      
    sock_aux = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock_aux.connect((socket.gethostbyname(get_host_from_header_list(request['headers_list'])),port))
    except:
        print( get_str_time_ProxPy() + ERROR_TO_CONN_WITH_SW + get_host_from_header_list(request['headers_list'])+':'+str(port))

    output_conn_request_reply.append([sock_aux,socket.gethostbyname(get_host_from_header_list(request['headers_list'])),[request],[]])

    return sock_aux

#To update socket descriptor
def update_socket_output_conn(output_conn_request_reply,ip,sock):

    for item in output_conn_request_reply:
        if item[1] == ip:
            item[0] = sock
            break


#Returns True if we have a conn | False if we havent
def is_already_conn_sw(output_conn_request_reply, ip_addr, sock_to_rcv = 'default'):

    for conns in output_conn_request_reply:
        if conns[1] == ip_addr and conns[0] == sock_to_rcv:
            return True

    return False

#To append a request to active conn | return socket descriptor
def append_request(conn_request,ip_addr, request_to_append ):

    for conns in conn_request:
        if conns[1] == ip_addr:
            conns[2].append(request_to_append)
            return conns[0]

#To append a request to input_conn_request_reply list           
def add_to_input_conn_request(input_conn_request_reply, sock_to_rcv, request):

    if not is_already_conn_sw(input_conn_request_reply, sock_to_rcv.getsockname()[0], sock_to_rcv):
        input_conn_request_reply.append([sock_to_rcv, sock_to_rcv.getsockname()[0],[request],[]])
    else:
        append_request(input_conn_request_reply, sock_to_rcv.getsockname()[0],request)

#To send a request to server web 
def send_request_to_sw(host_uri, request, output_conn_request_reply):
    #Var aux
    pet = b''

    #We have to re-create the request
    #Add first line 
    pet += WSP_B.join([(request['method']).encode(),(request['uri']).encode(),(request['version']).encode()]) + CRLF_B

    #Add headers (Here we can add 'if' to change some header )
    for item in request['headers_list']:
        if item[0] == 'Connection':
            pet += item[0].encode() + b': '+ b'Close' + CRLF_B
        elif item[0] == 'Upgrade-Insecure-Requests':
            pass
        else:
            pet += item[0].encode() + b': '+item[1].encode() + CRLF_B 

    #Fin headers
    pet += CRLF_B

    #Add Body 
    if request['body'] is not '-':
        pet += (request['body']).encode()
    
    #Fin request
    pet += CRLF_B


    #Send it
    try:
        host_uri.sendall(pet)
    except:
        print(get_str_time_ProxPy()+ ERROR_TO_SEND_REQUEST)
        host_uri = get_conn_to_server(output_conn_request_reply, request)
        host_uri.sendall(pet)


#To get the socket where we will send the reply
def get_input_socket_from_request(list_intput, request):

    #HTTP replys in order
    for item in input_conn_request_reply:
        if item[2][0] == request:
            return item[0]

#To get the socket where we will send the request 
def get_output_socket_from_request(list_out, ip):

    for item in list_out:
        if item[1] == ip:
            return item[0]


#To get the request associate with a socket
def get_request_from_output_conn(output_conn_request_reply, sock_to_rcv):

    #HTTP replys in order
    for item in output_conn_request_reply:
        if item[0] == sock_to_rcv:
            return item[2][0]

#To remove a conn from list 
def remove_conn(list_to_rm, socket_to_rm):

    try:
        for item in list_to_rm:
            if item[0] == socket_to_rm:
                list_to_rm.remove(item)
    except:
        print( get_str_time_ProxPy() + ERROR_TO_CLOSE_CONN +' Value conn list '+str(list_to_rm))


# To close al connections (Web navigators and SW)
def close_all_conn(sockets_rd, input_conn, output_conn):
    
    try:    
        for sck_in in input_conn:
            sck_in.close()
        input_conn.clear()
    except:
        print( get_str_time_ProxPy() + ERROR_TO_CLOSE_INPUT_CONN +' Value input conn list '+str(input_conn))
    try:
        for sck_out in output_conn:
            sck_out.close()
        output_conn.clear()
    except:
        print( get_str_time_ProxPy() + ERROR_TO_CLOSE_OUTPUT_CONN +' Value output conn list '+str(output_conn))
    try:
        for sck in sockets_rd:
            sck.close()
        sockets_rd.clear()
    except:
        print( get_str_time_ProxPy() + ERROR_TO_CLOSE_CONN +' Value conn list '+str(sockets_rd))

#Welcome msg
def welcome():
    sys.stdout.flush()
    os.system('clear')
    print(get_str_time_ProxPy() + MSG_PROXPY_HI +'\n' +get_str_time_ProxPy()+ MSG_PROXPY_VERSION)

#Handler CTRL+C
def signal_handler(sig, frame):
    print( '\n\n\n'+get_str_time_ProxPy() + MSG_PROXPY_BYE)
    #Close al connections (Web navigators and SW) and exit
    close_all_conn(sockets_rd, input_conn, output_conn)
    sys.exit(0)

#To get UDP sockets desc.
def get_logger_socket():
    return socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

#To send to our logger  request info 
def send_to_logger_request(logger, logger_id, ip_client, ip_dest_, port_client,request):
    try:
        # Our pkt : [DATA, REQ/RPLY, [method, version, server(url), server(ip), client(ip), client(port)]]
        logger.sendto(pickle.dumps([MSG_PROXPY_LOG_DATA, MSG_PROXPY_LOG_REQ,[request['method'], request['version'], get_host_from_header_list(request['headers_list']), ip_dest_,ip_client, port_client]]), (logger_id[0],logger_id[1]))
    except:
        print( get_str_time_ProxPy() + ERROR_TO_LOG_REQUEST )

#Init argparse
def init_argvs():

    parser = argparse.ArgumentParser(description="Welcome to ProxPy's help page", epilog='For more help you can check my github page:  github.com/davidcawork')
    parser.add_argument('-p','--port',metavar='Port',type= int,default=8080,help='Provide an integer that will be our listen port (default = 8080)')
    parser.add_argument('-d','--debug',metavar='Debug',type= int,default=3,help='Provide an integer that will be our debug level')
    parser.add_argument('-t','--timeout',metavar='Timeout',type= int,default=300,help='Provide an integer that will be our debug level')
    parser.add_argument('-b','--buffer',type= int,default=1024*10,help='Provide an integer that will be our buffer size(Bytes)')
    parser.add_argument('-c','--max_conn',type= int,default=8,help='Provide an integer that will be max client conn avaible with ProxPy')
    parser.add_argument('-fs','--filter_server',type= str,default="",help='Provide an [url/IP] that will be ban it to our clients')
    parser.add_argument('-fc','--filter_client',type= str,default="",help='Provide an IP that will be ban it from ProxPy')

    return parser

#To prepare and parse all argvs
def prepare_argvs(parser,proxy_port,proxy_timeout,debug_mode,max_client_conn,BUFFER_SIZE,list_filter_server,list_filter_client):

    my_args = parser.parse_args()

    proxy_port= my_args.port
    proxy_timeout=my_args.timeout
    debug_mode=my_args.debug
    BUFFER_SIZE=my_args.buffer
    max_client_conn=my_args.max_conn
    list_filter_server.append(my_args.filter_server)
    list_filter_client.append(my_args.filter_client)

if __name__ == "__main__":

    #Check argv's and init args parser
    if len(sys.argv) > 2:
	    bad_argvs_handler()
	    exit(0)
    
    else:

        # --- Say welcome to ProxPy and print current version ---
        welcome()

        # --- Vars ----
        parser = init_argvs()
        proxy_port = 8080
        proxy_timeout = 300.0
        list_filter_server = []
        list_filter_client = []
        max_client_conn = 8
        debug_mode = 1
        BUFFER_SIZE = 1024*1000
        logger_id = ['localhost', 8010]

        #To parse argvs 
        prepare_argvs(parser,proxy_port,proxy_timeout,debug_mode,max_client_conn,BUFFER_SIZE,list_filter_server,list_filter_client)
        print("Port: "+str(proxy_port)+" | Debug: "+str(debug_mode)+" | Buffer: "+str(BUFFER_SIZE)+" | Max_conn: "+str(max_client_conn)+
        " | Filter_s: "+str(list_filter_server)+" | Filter_c: "+ str(list_filter_client))

        #Let's to prepare the CTRL + C signal to handle it and be able  to show the statistics before it comes out
        signal.signal(signal.SIGINT, signal_handler)

	    # --- Prepare our TCP socket where we will hear connections from web navigators ---
        our_proxy_socket = get_our_socket(proxy_port)

        # --- Prepare our udp socket where w'ill log every single pet ---
        logger = get_logger_socket()


        #Sockets to read
        sockets_rd = [our_proxy_socket]

        #To save 
        #Input connections
        input_conn = []
        input_conn_request_reply = []

        #Output connections 
        output_conn = []
        output_conn_request_reply = []
        
        #We'ill store the request like this : [ [sockets_descriptor, str_host, [current_request_1, current_request_2] ] ]

        # We can exit by CTRL+C signal :)
        while True:
            try:
	    		# The optional timeout argument specifies a time-out as a floating point number in seconds.
                events_rd,events_wr,events_excp = select.select( sockets_rd,[],[], proxy_timeout)

            except KeyboardInterrupt:
                print( '\n\n\n'+get_str_time_ProxPy() + MSG_PROXPY_BYE)
                #Close al connections (Web navigators and SW) and exit
                close_all_conn(sockets_rd, input_conn, output_conn)
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
                                data = sock_to_rcv.recv(BUFFER_SIZE)
                                if debug_mode:
                                    print("{}".format(data.decode('utf-8')))
                            except:
                                print( get_str_time_ProxPy() + ERROR_TO_RCV_FROM_NAV + sock_to_rcv.getsockname()[0]+':'+ str(sock_to_rcv.getsockname()[1]))
                                pass
                                
                            if data:
                                #Parse the request
                                try:
                                    request = http_request_parser(data.decode('utf-8'))
                                except:
                                    print( get_str_time_ProxPy() + ERROR_TO_RCV_FROM_NAV + ' \n\n'+str(data))
                                    break

                                #Process the request

                                #Filter
                                if request['method'] == 'GET' and get_host_from_header_list(request['headers_list']) != 'push.services.mozilla.com:443':
                                    try:   
                                        #Open connection to get uri
                                        host_uri = get_conn_to_server(output_conn_request_reply, request)

                                        #Add to input_conn_request_reply the request
                                        add_to_input_conn_request(input_conn_request_reply, sock_to_rcv, request)

                                        #Add to sockets_rd only if its necessary
                                        if not is_in_the_list(sockets_rd, host_uri):
                                            sockets_rd.append(host_uri)

                                        #Add to output_conn only if its necessary
                                        if not is_in_the_list(output_conn, host_uri):
                                            output_conn.append(host_uri)

                                        #Send the request and add to the list output_conn_request_reply, and log it
                                        send_to_logger_request(logger, logger_id, sock_to_rcv.getsockname()[0],socket.gethostbyname(get_host_from_header_list(request['headers_list'])), sock_to_rcv.getsockname()[1],request)
                                        send_request_to_sw(host_uri, request, output_conn_request_reply)

                                    except:
                                        print(get_str_time_ProxPy() + ERROR_TO_PREPARE_REQUEST + request['method'] + ' request to '+get_host_from_header_list(request['headers_list']))
                                        pass

                                    #Main handler request
                                    while True:
                                        try:
                                            #If host_uri sockets is closed, we try reconnect with the web server
                                            #Then we recv the reply to our request
                                            if host_uri._closed:
                                                host_uri = get_conn_to_server(output_conn_request_reply, request)
                                                data_rpl = host_uri.recv(BUFFER_SIZE)
                                            else:
                                                data_rpl = host_uri.recv(BUFFER_SIZE)

                                            if data_rpl:
                                                #If data is not b' ' we send it back to web navigator
                                                #logger.sendto(pickle.dumps(['DATA', 'REPLY','data']) , ('localhost',8010))
                                                sock_to_rcv.send(data_rpl)
                                            else:
                                                #When we have sent it the reply close the host_uri socket and remove from our list
                                                host_uri.close()
                                                sockets_rd.remove(host_uri)
                                                output_conn.remove(host_uri)
                                                remove_conn(output_conn_request_reply, host_uri)    
                                                break
                                        except:
                                            print(get_str_time_ProxPy() + ERROR_TO_REPLY_NAV + request['method'] + ' request to '+get_host_from_header_list(request['headers_list']))
                                            break

                            else:
                                #Only when we have rcv b' ' from web navigator, close the conn and remove the socket
                                # descriptor from our input list
                                sock_to_rcv.close()
                                sockets_rd.remove(sock_to_rcv)
                                input_conn.remove(sock_to_rcv)
                                remove_conn(input_conn_request_reply, sock_to_rcv)


            #Prepare timeout msg :)

            if not (events_rd or events_wr or events_excp):
                print( get_str_time_ProxPy() + MSG_PROXPY_INACTIVE )


                        




