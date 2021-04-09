import socket

HOST = '143.198.234.58'  # The server's hostname or IP address
PORT = 1234        # The port used by the server

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    BUFFER_SIZE = 4096
    with open('50cent.jpg', 'rb') as file:
        while True:
            bytes_read = file.read(BUFFER_SIZE)
            if not bytes_read: # done
                break
            s.sendall(bytes_read)
        data = s.recv(1024)

print('Received', repr(data))