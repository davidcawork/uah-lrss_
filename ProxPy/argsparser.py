import argparse
import sys



parser = argparse.ArgumentParser(description="Welcome to ProxPy's help page", epilog='For more help you can check my github page:  github.com/davidcawork')
parser.add_argument('-p','--port',metavar='Port',type= int,default=8080,help='Provide an integer that will be our listen port (default = 8080)')
parser.add_argument('-d','--debug',metavar='Debug',type= int,default=3,help='Provide an integer that will be our debug level')
parser.add_argument('-b','--buffer',type= int,default=1024*10,help='Provide an integer that will be our buffer size(Bytes)')
parser.add_argument('-c','--max_conn',type= int,default=8,help='Provide an integer that will be max client conn avaible with ProxPy')
parser.add_argument('-fs','--filter_server',type= str,default="",help='Provide an [url/IP] that will be ban it to our clients')
parser.add_argument('-fc','--filter_client',type= str,default="",help='Provide an IP that will be ban it from ProxPy')

my_args = parser.parse_args()

port= my_args.port
debug=my_args.debug
buffer=my_args.buffer
max_conn=my_args.max_conn
filter_server=my_args.filter_server
filter_client=my_args.filter_client


print("Port: "+str(port)+" | Debug: "+str(debug)
+" | Buffer: "+str(buffer)+" | Max_conn: "+str(max_conn)+" | Filter_s: "+str(filter_server)+" | Filter_c: "+ str(filter_client))


print(str(len(sys.argv)))
print(str(len(vars(my_args))))