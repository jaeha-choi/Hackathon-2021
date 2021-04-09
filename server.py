import socket
import uuid


class Server:
    def __init__(self):
        self.ip = ""
        self.port = 1234
        self.clients = {}

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((self.ip, self.port))
        self.socket.listen()

    def add(self, uid: uuid.UUID, ip_addr: str, port: int):
        self.clients[uid] = (ip_addr, port)

    def listen(self):
        try:

            conn, addr = self.socket.accept()
            data = conn.recv(4096)
            string_return = "address:\t" + str(addr) + "\ndata:\t" + str(data)
            # print("address:\t", addr)
            # print("data:\t", data)
            string_return = string_return.encode()
            conn.send(b'coconut')
            while string_return:
                bytes = conn.send(string_return)
                string_return = string_return[bytes:]
            print("sent")
            conn.close()
            self.socket.close()
        except:
            self.socket.close()


if __name__ == '__main__':
    # print("Nothing here yet")
    serv = Server()
    serv.listen()
