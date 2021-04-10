import socket
import uuid

import util
from util import Command
from util import ExitCode


class Server:
    def __init__(self):
        self.ip = ""
        self.port = 1234
        self.clients = {}

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((self.ip, self.port))
        self.socket.listen()

    def add(self, uid: uuid.UUID, pub_ip: str, priv_ip: str, port: int):
        self.clients[uid] = (pub_ip, port, priv_ip)

    def load_clients(self):
        pass

    def listen(self):
        conn, addr = self.socket.accept()
        while True:
            try:
                command, _ = util.recv_str(conn)
                if command == str(Command.ADD):
                    # Receive add user command
                    # Receive uuid
                    uid, _ = util.recv_str(conn)
                    # Receive private address and port
                    priv_addr, _ = util.recv_str(conn)
                    self.add(uid, addr[0], addr[1], priv_addr[0])
                    util.send_str(conn, ExitCode.SUCCESS)
                    print("ADD command done")  # Debug

                elif command == str(Command.EXIT):
                    # Receive exit command
                    # Receive close connection packet
                    util.send_str(conn, "Closing connection.")
                    conn.close()
                    print("EXIT command done")  # Debug
                    break

                elif command == str(Command.HEARTBEAT):
                    # Receive heartbeat command
                    # Receive keep-alive packet
                    # hrs, _ = util.recv_str(conn)
                    util.send_str(conn, ExitCode.SUCCESS)
                    print("KEEP-ALIVE command done")  # Debug

                elif command == str(Command.TRANSFER):
                    # Receive transfer command
                    # Receive file name used for saving
                    file_n, _ = util.recv_str(conn)
                    # If file is received
                    if util.recv_bin(conn, file_n):
                        # print("File successfully saved")
                        util.send_str(conn, ExitCode.SUCCESS)
                    else:
                        # print("File not saved")
                        util.send_str(conn, ExitCode.FAIL_GENERAL)
                    print("TRANSFER command done")  # Debug

            except Exception as err:
                print("Unknown Error at listen", err)


if __name__ == '__main__':
    serv = Server()
    serv.listen()
