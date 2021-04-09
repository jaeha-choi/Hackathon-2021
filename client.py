import socket
import uuid
import util
import time

def gen_uuid():
        return uuid.uuid4()

class Client:
    def __init__(self, server_ip, port):
        self.SERVER = server_ip
        self.PORT = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.settimeout(5)
        self.socket.bind((self.SERVER, self.PORT))
        self.uuid = gen_uuid()

    def connect_to_server(self):
        self.socket.listen(2)
        con, adr = self.socket.accept()
        print('Connected to', self.SERVER, 'on', str(self.PORT))
        return con, adr

    def send_uuid(self):
        con, adr = self.connect_to_server()
        con.sendall(bytes(self.uuid))
        data = con.recv()
        
    def send_data(self, file_name: str):
        with open(file_name, 'r') as file:
            
        pass

    def recv_data(self):
        pass

    def get_user(self, con):
        pass

if __name__ == '__main__':
    client = Client('localhost', 28383)
    client.connect_to_server()
    client.send_uuid() 