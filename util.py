import os
import socket
import struct
from enum import Enum
from typing import Any


class Command(Enum):
    def __str__(self):
        return str(self.value)

    ADD = "ADD"
    EXIT = "EXT"
    HEARTBEAT = "HRB"
    TRANSFER = "TRF"


class ExitCode(Enum):
    def __str__(self):
        return str(self.value)

    SUCCESS = 0
    FAIL_GENERAL = 1


def validate(ip_addr: str, port: int):
    """
    Validate IP address and port
    :param ip_addr: IP address to validate
    :param port: Port to validate
    :return: Return 0 for valid, 1 for invalid ip address, 2 for invalid port
    """
    try:
        socket.inet_aton(ip_addr)
    except socket.error:
        return 1
    if not (1 <= port <= 65535):
        return 2
    return 0


def _recv_n_byte(conn: socket.socket, packet_size: int):
    """
    Private function to receive n amount of bytes
    :param conn: Connection socket
    :param packet_size: Total size of a packet to receive
    :return: Received data in bytes. None if not all bytes were received.
    """
    data = b''
    try:
        while len(data) < packet_size:
            packet = conn.recv(packet_size - len(data))
            if not packet:
                return None
            data += packet
    except Exception as err:
        print("Unknown error in _recv_n_byte", err)
        return None
    return data


def send_str(conn: socket.socket, msg: Any, encoding: str = "utf-8") -> bool:
    """
    Send text as string format
    :param conn: Connection socket
    :param msg: String to send
    :param encoding: Encoding to use for the string
    :return: Return True if msg was sent, False otherwise.
    """
    try:
        # This is inefficient as the size can get big very fast
        # b_msg = b'%i]' % len(b_msg) + msg.encode(encoding=encoding)
        # Sends size of the file in first four bytes
        b_msg = struct.pack('!L', len(str(msg))) + str(msg).encode(encoding=encoding)
        # print("send_str:\tPacket size:", len(msg))  # Debug
        conn.sendall(b_msg)
        # while b_msg:
        #     sent_bytes = conn.send(b_msg)
        #     b_msg = b_msg[sent_bytes:]
    except UnicodeError as err:
        print("Encoding error:", err)
        return False
    except Exception as err:
        print("Unknown error in send_str", err)
        return False

    return True


def recv_str(conn: socket.socket, encoding: str = "utf-8") -> (str, bool):
    """
    Receive text as string format. If packet is not being sent, raises exception.
    :param conn: Connection socket
    :param encoding: Encoding to use for string
    :return: Tuple of received string and Boolean indicating the receive status.
    """
    string = ""
    try:
        # Check first four bytes for total packet size
        pkg_len = _recv_n_byte(conn, 4)
        # This is inefficient as the size can get big very fast
        # end_idx = data.find(b']')
        # pkg_len = int(data[:pkg_len])

        # convert byte to unsigned long
        packet_size = struct.unpack('!L', pkg_len)[0]
        # print("recv_str:\tPacket size:", packet_size)  # Debug
        data = _recv_n_byte(conn, packet_size)
        string = data.decode(encoding)
    except UnicodeError as err:
        print("Decoding error:", err)
        return string, False
    except Exception as err:
        print("Unknown error in recv_str", err)
        return string, False

    return string, True


def send_bin(conn: socket.socket, file_n: str, buff_size: int = 4096) -> bool:
    """
    Send file as binary format
    :param conn: Connection socket
    :param file_n: File name to save as
    :param buff_size: Size of a buffer
    :return: True if successfully sent, False otherwise.
    """
    try:
        with open(file_n, "rb") as file:
            b_msg = struct.pack('!L', os.path.getsize(file_n))
            # print("send_bin:\tPacket size:", os.path.getsize(file_n))  # Debug
            conn.send(b_msg)
            while True:
                bytes_read = file.read(buff_size)
                if not bytes_read:
                    # eof
                    break
                conn.send(bytes_read)

    except ValueError as err:
        print("Encoding error:", err)
        return False
    except OSError as err:
        print("File error:", err)
        return False
    except Exception as err:
        print("Unknown error in send_bin", err)
        return False

    return True


def recv_bin(conn: socket.socket, file_n: str) -> bool:
    """
    Receive file as binary format
    :param conn: Connection socket
    :param file_n: File name to save as
    :return: True if successfully received, False otherwise.
    """
    try:
        pkg_len = _recv_n_byte(conn, 4)
        packet_size = struct.unpack('!L', pkg_len)[0]
        # print("recv_bin:\tPacket size:", packet_size)  # Debug
        with open(file_n, "wb") as file:
            data = _recv_n_byte(conn, packet_size)
            file.write(data)
    except ValueError as err:
        print("Encoding error:", err)
        return False
    except OSError as err:
        print("File error:", err)
        return False
    except Exception as err:
        print("Unknown error in recv_bin", err)
        return False

    return True
