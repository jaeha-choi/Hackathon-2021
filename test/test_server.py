import socket

HOST = ''
PORT = 1234
BUFFER_SIZE = 4096

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    conn, addr = s.accept()
    try:
        with conn:
            by = b''
            while True:
                data = conn.recv(BUFFER_SIZE)
                if not data:
                    break
                by += data
                print(by)
    except KeyboardInterrupt:
        conn.close()
        print("Keyboard Interrupt")
