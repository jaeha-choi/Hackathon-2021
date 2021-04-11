import socket
import uuid

from utility import util
from utility.util import Command
from utility.util import ExitCode


class Client:
    def __init__(self, server_ip: str, server_port: int, uid: uuid.UUID = uuid.uuid4()):
        # Communication/relay server
        self.server_ip = server_ip
        self.server_port = server_port
        self.server_conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # p2p connection
        self.client_ip = ""
        self.client_port = 1234
        self.client_conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # self.conn.settimeout(5)
        # self.conn.bind((self.SERVER, self.PORT))
        # TODO: Consider using UUIDv5
        self.uuid = uid

    def _send_command(self, command: Command) -> bool:
        return util.send_str(self.server_conn, str(command))

    def _get_result(self) -> ExitCode:
        return ExitCode(int(util.recv_str(self.server_conn)[0]))

    def connect(self) -> ExitCode:
        # self.socket.listen()
        self.server_conn.connect((self.server_ip, self.server_port))
        print('Connected to', self.server_ip, 'on', str(self.server_port))
        return self.send_heartbeat()
        # return con, adr

    def close(self):
        self._send_command(Command.EXIT)
        util.send_str(self.server_conn, str(self.uuid))
        self.server_conn.close()

    def send_uuid(self) -> ExitCode:
        # Send ADD(add) command
        self._send_command(Command.ADD)
        # Send uuid
        util.send_str(self.server_conn, str(self.uuid))

        info = self.server_conn.getsockname()
        # Send priv_ip
        util.send_str(self.server_conn, info[0])
        # Send priv_port
        util.send_str(self.server_conn, str(info[1]))
        return self._get_result()

    def send_heartbeat(self) -> ExitCode:
        self._send_command(Command.HEARTBEAT)
        # util.send_str(self.conn, "Keep-alive")
        return self._get_result()

    def send_clip(self, recv_uid: str, content: str) -> ExitCode:
        pass

    def send_file_relay(self, recv_uid: str, file_n: str, server_save_n: str) -> ExitCode:
        pass

    def send_file(self, file_n: str, server_save_n: str) -> ExitCode:
        self._send_command(Command.TRANSFER)
        # Send file name to use for saving on server-side
        util.send_str(self.server_conn, server_save_n)
        # Send file
        util.send_bin(self.server_conn, file_n)
        return self._get_result()

    def recv_data(self):
        pass

    def get_user(self, uid: str):
        pass


if __name__ == '__main__':
    client = Client('', 1234)
    client.connect()
    client.send_uuid()
    # util.exec_res(client.send_file, ("./test/cat.png", "dog.png"))
    # util.exec_res(client.send_file, ("./test/cat2.JPG", "stars.JPG"))
    # util.exec_res(client.send_heartbeat)
