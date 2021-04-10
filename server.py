import logging as log
import socket
import time
import uuid

from utility import util
from utility.util import Command
from utility.util import ExitCode

# Terminate connection if empty packet is being sent for TERMINATE_TH sec
TERMINATE_TH = 30


class Server:

    def __init__(self, ip: str, port: int):
        self.ip = ip
        self.port = port
        self.clients = {}
        self.err_cnt = 0

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((self.ip, self.port))
        self.socket.listen()

    def add(self, uid: uuid.UUID, pub_ip: str, priv_ip: str, port: int):
        self.clients[uid] = (pub_ip, port, priv_ip)

    def load_clients(self):
        pass

    def listen(self):
        conn, addr = self.socket.accept()
        while self.err_cnt < TERMINATE_TH:
            try:
                command, res = util.recv_str(conn)
                if not res:
                    # If empty packet is being sent
                    # or if there's an error
                    self.err_cnt += 1
                    time.sleep(1)
                else:
                    if command == str(Command.ADD):
                        # Receive add user command
                        # Receive uuid
                        uid, _ = util.recv_str(conn)
                        # Receive private address and port
                        priv_addr, _ = util.recv_str(conn)
                        self.add(uid, addr[0], addr[1], priv_addr[0])
                        util.send_str(conn, ExitCode.SUCCESS)
                        log.info("ADD command done")

                    elif command == str(Command.EXIT):
                        # Receive exit command
                        # Receive close connection packet
                        util.send_str(conn, "Closing connection.")
                        conn.close()
                        log.info("EXIT command done")
                        break

                    elif command == str(Command.HEARTBEAT):
                        # Receive heartbeat command
                        # Receive keep-alive packet
                        # hrs, _ = util.recv_str(conn)
                        util.send_str(conn, ExitCode.SUCCESS)
                        log.info("KEEP-ALIVE command done")

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
                        log.info("TRANSFER command done")

            except Exception as err:
                log.error("Unknown Error at listen", err)
        # If error exceeds TERMINATE_TH threshold, close connection.
        conn.close()
        self.err_cnt = 0
        log.warning("Closing connection due to errors.")


if __name__ == '__main__':
    serv = Server("", 1234)
    serv.listen()
