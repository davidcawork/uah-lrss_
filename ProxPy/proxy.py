#/usr/bin/env python3
import socket           
import sys
import os
import select


#Note: 
#
#
#
#   For more info: github.com/davidcawork

#Global vars
MSG_PROXPY_INACTIVE = '[ProxPy] Proxy inactive ...'



if __name__ == "__main__":
    #Check argv's
    if len(sys.argv) < 2:
	    print('Error: usage: ./' + sys.argv[0] + ' <Port>')
	    exit(0)
    
    else:

        #Vars
        pet = b''
        proxy_port = int(sys.argv[1])
        proxy_timeout = 300.0
	
	    #Prepare our socket
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setblocking(0)
        s.bind(('',proxy_port))
        s.listen(5)

        # To prepare csic request
        host=socket.gethostbyname('www.csic.es')
        request = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        request.connect((host,80))
        #request.sendall(b'GET / HTTP/1.1\r\nHost: www.csic.es\r\nUser-Agent: Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:66.0) Gecko/20100101 Firefox/66.0\r\nAccept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8\r\nAccept-Language: en-US,en;q=0.5\r\nAccept-Encoding: gzip, deflate\r\nConnection: keep-alive\r\nUpgrade-Insecure-Requests: 1\r\n\r\n')
        
        #pet = request.recv(1000000000)
        #pet += request.recv(1000000000)
        #pet += request.recv(1000000000)
        #pet += request.recv(1000000000)
        #pet += request.recv(1000000000)
        #pet += request.recv(1000000000)
        #pet += request.recv(1000000000)
        #pet += request.recv(1000000000)
        #print(str(pet))
        #Sockets to read
        sockets_rd = [s,request]

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
                if event == s:
                	#Accept input conn from web navigator
                    conn, addr = s.accept()
                    conn.setblocking(0)
                    sockets_rd.append(conn)
                else:
            	    #Handle other conn
                    for sock_to_rcv in sockets_rd:
                        if sock_to_rcv != s and sock_to_rcv is event:
                            if sock_to_rcv != request:
                                data = sock_to_rcv.recv(1024*1000)
                                print("{}".format(data.decode('utf-8')))
                                if data:
                                    #print('ENviando datossss......')
                                    request.sendall(data)
                                else:
                                    sock_to_rcv.close()
                                    sockets_rd.remove(sock_to_rcv)
                            else:
                                try:
                                    sockets_rd[2].sendall(request.recv(1024*1000))
                                except:
                                    print("Error al hacer reply :) \n\n\n ")
                                
                                    
                                
                                			
                
                
            



	    
