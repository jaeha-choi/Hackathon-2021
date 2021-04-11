import logging as log
import socket
import time
import uuid

from utility import util
from utility.util import Command
from utility.util import ExitCode

# Terminate connection if empty packet is being sent for TERMINATE_TH sec
TERMINATE_TH = 30
log.basicConfig(format='%(asctime)s - %(levelname)s: %(message)s',
                level=log.DEBUG, datefmt='%m/%d/%Y %I:%M:%S %p')


class Server:

    def __init__(self, ip: str, port: int):
        # TODO: Validate IP addr/port
        self.ip = ip
        self.port = port
        self.clients = {}  # uuid : (pub_ip, port, priv_ip, priv_port)
        self.err_cnt = 0

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((self.ip, self.port))
        self.socket.listen()
        self.socket.settimeout(30)

    def add(self, uid: uuid.UUID, pub_ip: str, priv_ip: str, port: int, priv_port: int):
        self.clients[uid] = (pub_ip, port, priv_ip, priv_port)

    def load_clients(self):
        pass

    def data_relay(self, sender_ip: str, sender_port: int, receiver_ip: str, receiver_port: int) -> bool:
        # TODO: Consider creating a hole punching method

        pass

    def close(self):
        self.socket.close()

    def listen(self):
        conn, addr = self.socket.accept()
        while self.err_cnt <= TERMINATE_TH:
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
                        self.add(uid, addr[0], addr[1], priv_addr[0], priv_addr[1])
                        util.send_str(conn, ExitCode.SUCCESS)
                        log.info("ADD command done")

                    elif command == str(Command.EXIT):
                        # Receive exit command
                        # Receive close connection packet
                        util.send_str(conn, "Closing connection.")
                        uid, _ = util.recv_str(conn)
                        conn.close()
                        # Remove from online users
                        del self.clients[uid]
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
                            log.info("File successfully saved")
                            util.send_str(conn, ExitCode.SUCCESS)
                        else:
                            log.error("File not saved")
                            util.send_str(conn, ExitCode.FAIL_GENERAL)
                        log.info("TRANSFER command done")
                    elif command == str(Command.RELAY):
                        # Get dest uid
                        uid, _ = util.recv_str(conn)
                        if uid in self.clients:
                            # UUID found in dict
                            sender = self.clients[uid]  # (pub_ip, port, priv_ip, priv_port)
                            receiver = self.clients[uid]  # (pub_ip, port, priv_ip, priv_port)
                            # Consider relaying both pub/priv as the paper suggests
                            if sender[0] == receiver[0]:
                                # If public address is the same, try LAN (would usually work)
                                status = self.data_relay(sender[2], sender[3], receiver[2], receiver[3])
                            else:
                                status = self.data_relay(sender[0], sender[1], receiver[0], receiver[1])

                        else:
                            # UUID not found in dict
                            pass
                    self.err_cnt = 0

            except Exception as err1:
                log.error("Unknown Error at listen", err1)
        if self.err_cnt > TERMINATE_TH:
            # If error exceeds TERMINATE_TH threshold, close connection.
            conn.close()
            self.err_cnt = 0
            log.warning("Closing connection due to timeout.")


if __name__ == '__main__':
    serv = Server("", 1234)
    try:
        serv.listen()
    except KeyboardInterrupt:
        log.error("Keyboard Interrupt")
        serv.close()
