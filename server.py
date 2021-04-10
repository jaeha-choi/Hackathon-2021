import socket
import uuid

import util


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

    def load_clients(self):
        pass

    def listen(self):
        try:

            conn, addr = self.socket.accept()
            data, _ = util.recv_all_str(conn)
            string_return = "address:\t" + str(addr) + "\ndata:\t" + data
            print("Public address:\t", addr)
            print("Private address:\t", data)
            util.send_all_str(conn, string_return)
            print("Sent to client")
            file_n, _ = util.recv_all_str(conn)
            if util.recv_all_bin(conn, file_n):
                print("File successfully saved")
                util.send_all_str(conn, "File successfully saved")
            else:
                print("File not saved")
                util.send_all_str(conn, "File not saved")
            print()
            # conn.close()
            # self.socket.close()
        except Exception as err:
            print(err)
            # self.socket.close()


if __name__ == '__main__':
    # print("Nothing here yet")
    serv = Server()
    while True:
        serv.listen()
