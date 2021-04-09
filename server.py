import socket
import uuid


class Server:
    def __init__(self):
        self.ip = "127.0.0.1"
        self.port = 28383
        self.clients = {}

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((self.ip, self.port))

    def add(self, uid: uuid.UUID, ip_addr: str, port: int):
        self.clients[uid] = (ip_addr, port)


if __name__ == '__main__':
    print("Nothing here yet")
