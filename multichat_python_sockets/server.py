#usr/bin/env python3

import socket
import sys
import pickle
import select

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

        sockets_rd = [s]

        while True:
            events_rd,events_wr,events_excp = select.select( sockets_rd,[],[])

            for event in events_rd:

                if event == s:
                    #Add user into multichat :)
                    conn, addr = s.accept()
                    conn.setblocking(0)
                    sockets_rd.append(conn)
                else:
                    for sock_to_rcv in sockets_rd:
                        if sock_to_rcv != s and sock_to_rcv is event:
                            data = sock_to_rcv.recv(4096)
                            if data:
                                for sock_to_send in sockets_rd:
                                    if sock_to_send is not sock_to_rcv and sock_to_send is not s :
                                        sock_to_send.sendall(data)
                                        
                            else:
                                sock_to_rcv.close()
                                sockets_rd.remove(sock_to_rcv)
            

