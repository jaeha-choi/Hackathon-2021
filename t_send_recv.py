import socket

HOST = '143.198.234.58'
PORT = 1234
BUFFER_SIZE = 4096

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    conn, addr = s.accept()
    with conn:
        print('Connected by', addr)
        with open('robin_sus.PNG', 'wb') as file:
            while True:
                data = conn.recv(BUFFER_SIZE)
                file.write(data)
                if not data: # done
                    break
                conn.send(b'data recieved')