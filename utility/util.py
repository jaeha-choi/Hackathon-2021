import logging as log
import os
import socket
import struct
from enum import Enum
from typing import Any

log.basicConfig(format='%(asctime)s - %(levelname)s: %(message)s',
                level=log.DEBUG, datefmt='%m/%d/%Y %I:%M:%S %p')


class Command(Enum):
    def __str__(self):
        return str(self.value)

    ADD = "ADD"
    EXIT = "EXT"
    HEARTBEAT = "HRB"
    TRANSFER = "TRF"
    RELAY = "REL"
    DATA_RELAY = "DRL"


class ExitCode(Enum):
    def __str__(self):
        return str(self.value)

    SUCCESS = 0
    FAIL_GENERAL = 1
    CONTINUE = 2
    NO_UUID_MATCH = 3


# def exec_res(function: Callable, *args: tuple[Any, ...]) -> None:
#     res = function(args[0][0], args[0][1]) if len(args) else function()
#     print("Function \033[96m%s\033[0m returned code: %s" % (str(function.__name__), res.name))


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
        log.debug("IP address [%s] is not valid." % ip_addr)
        return 1
    if not (1 <= port <= 65535):
        log.debug("Port number [%s] is not valid." % port)
        return 2
    log.debug("IP address [%s] and port number [%s] is valid." % ip_addr, port)
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
        log.error("Unknown error in _recv_n_byte [%s]" % err)
        return False
    log.debug("Received [%s] bytes." % packet_size)
    return data


def _get_pkt_size(conn: socket.socket) -> int:
    """
    Get the packet size by unpacking first four bytes of the data
    :param conn: Connection socket
    :return: Size of a single file, string. -1 if no packet received.
    """
    # Receive first four bytes
    b_pkt_len = _recv_n_byte(conn, 4)
    if b_pkt_len is None:
        log.debug("Byte packet length: None")
        return -1
    # convert byte to unsigned long
    lng = struct.unpack('!L', b_pkt_len)[0]
    log.debug("Byte packet length: [%s]." % lng)
    return lng


def passthroughs(send_conn: socket.socket, recv_conn: socket.socket) -> bool:
    """
    Get file from sender and pass it to the receiver.
    Both connection must be alive
    :param send_conn: Sender socket
    :param recv_conn: Receiver socket
    :return: True if successfully passed a file, False if not.
    """
    total_received = 0
    try:
        # Get first four bytes to get packet size
        packet_size = _get_pkt_size(send_conn)
        if packet_size == -1:
            return False
        # Server sends length of bytes to expect to the receiver
        recv_conn.sendall(struct.pack('!L', packet_size))
        while total_received < packet_size:
            packet = send_conn.recv(packet_size - total_received)
            if not packet:
                return False
            total_received += len(packet)
            recv_conn.sendall(packet)
    except UnicodeError as err:
        log.error("Encoding error: [%s]" % err)
        return False
    except Exception as err:
        log.error("Unknown error in passthroughs: [%s]" % err)
        return False
    # TODO: add print log
    return True


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
        conn.sendall(b_msg)
        # while b_msg:
        #     sent_bytes = conn.send(b_msg)
        #     b_msg = b_msg[sent_bytes:]
    except UnicodeError as err:
        log.error("Encoding error: [%s]" % err)
        return False
    except Exception as err:
        log.error("Unknown error in send_str: [%s]" % err)
        return False
    log.debug("Sent string [%s]. Packet size: [%s]." % (msg, len(msg)))
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
        packet_size = _get_pkt_size(conn)
        if packet_size == -1:
            return string, False
        data = _recv_n_byte(conn, packet_size)
        string = data.decode(encoding)
    except UnicodeError as err:
        log.error("Decoding error: [%s]" % err)
        return string, False
    except Exception as err:
        log.error("Unknown error in recv_str: [%s]" % err)
        return string, False
    log.debug("Received string [%s]. Packet size: [%s]." % (string, packet_size))
    return string, True


def send_bin(conn: socket.socket, file_n: str, buff_size: int = 4096) -> bool:
    """
    Send file as binary format. Could return error if folder
    permission is incorrect, path does not exist, etc.
    :param conn: Connection socket
    :param file_n: File name to save as
    :param buff_size: Size of a buffer
    :return: True if successfully sent, False otherwise.
    """
    try:
        with open(file_n, "rb") as file:
            b_msg = struct.pack('!L', os.path.getsize(file_n))
            conn.send(b_msg)
            while True:
                bytes_read = file.read(buff_size)
                if not bytes_read:
                    # eof
                    break
                conn.send(bytes_read)
    except ValueError as err:
        log.error("Encoding error: [%s]" % err)
        return False
    except OSError as err:
        log.error("File error: [%s]" % err)
        return False
    except Exception as err:
        log.error("Unknown error in send_bin: [%s]" % err)
        return False
    log.debug("Sent file [%s]." % file_n)
    return True


def recv_bin(conn: socket.socket, file_n: str) -> bool:
    """
    Receive file as binary format
    :param conn: Connection socket
    :param file_n: File name to save as
    :return: True if successfully received, False otherwise.
    """
    try:
        packet_size = _get_pkt_size(conn)
        if packet_size == -1:
            return False
        with open(file_n, "wb") as file:
            data = _recv_n_byte(conn, packet_size)
            file.write(data)
    except ValueError as err:
        log.error("Encoding error: [%s]" % err)
        return False
    except OSError as err:
        log.error("File error: [%s]" % err)
        return False
    except Exception as err:
        log.error("Unknown error in recv_bin: [%s]" % err)
        return False
    log.debug("Received file [%s]. Size: [%s]." % (file_n, packet_size))
    return True
