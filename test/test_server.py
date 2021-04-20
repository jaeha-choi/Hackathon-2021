import socket

HOST = ''
PORT = 1234
BUFFER_SIZE = 4096

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((HOST, PORT))
    s.listen()
    conn, addr = s.accept()
    try:
        with conn:
            while True:
                by = b''
                data = conn.recv(BUFFER_SIZE)
                if not data:
                    break
                by += data
                print(by)
    except KeyboardInterrupt:
        conn.close()
        print("Keyboard Interrupt")
