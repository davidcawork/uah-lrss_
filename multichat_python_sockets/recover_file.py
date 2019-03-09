import socket


HOST = '192.168.1.214'
PORT = 5000
CHUNK_SIZE = 5 * 1024
FILE = "example2.txt"

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))

    with open(FILE, "wb") as f:        
        chunk = s.recv(CHUNK_SIZE)

        while chunk:
            f.write(chunk)
            chunk = s.recv(CHUNK_SIZE)