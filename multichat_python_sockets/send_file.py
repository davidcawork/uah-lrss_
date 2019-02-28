import socket



PORT = 5000
CHUNK_SIZE = 5 * 1024
FILE = "example.txt"

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind(('', PORT))
    s.listen(1)
    conn, addr = s.accept()
    with conn:
        with open(FILE, 'rb') as f:
            conn.sendfile(f)