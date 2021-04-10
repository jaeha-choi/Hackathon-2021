import socket
import time

import util

HOST = '143.198.234.58'  # The server's hostname or IP address
PORT = 1234  # The port used by the server

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    addr = s.getsockname()
    util.send_all_str(s, str(addr))
    time.sleep(1)
    print(util.recv_all_str(s)[0])
    util.send_all_str(s, "test.png")
    time.sleep(1)
    util.send_all_bin(s, "./test/cat.png")
    print(util.recv_all_str(s)[0])
    # with open('50cent.jpg', 'rb') as file:
    #     while True:
    #         bytes_read = file.read(BUFFER_SIZE)
    #         if not bytes_read: # done
    #             break
    #         s.sendall(bytes_read)
    #     data = s.recv(1024)

# print('Received', repr(data))
