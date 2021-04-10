import os
import socket
import struct


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
    except:
        print("Unknown error in _recv_n_byte")
        return None
    return data


def send_str(conn: socket.socket, msg: str, encoding: str = "utf-8") -> bool:
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
        b_msg = struct.pack('!L', len(msg)) + msg.encode(encoding=encoding)
        while b_msg:
            sent_bytes = conn.send(b_msg)
            b_msg = b_msg[sent_bytes:]
    except UnicodeError as err:
        print("Encoding error:", err)
        return False
    except:
        print("Unknown error in send_str")
        return False

    return True


def recv_str(conn: socket.socket, encoding: str = "utf-8") -> (str, bool):
    """
    Receive text as string format
    :param conn: Connection socket
    :param encoding: Encoding to use for string
    :return: Tuple of received string and Boolean indicating the receive status.
    """
    string = ""
    try:
        pkg_len = _recv_n_byte(conn, 4)
        # This is inefficient as the size can get big very fast
        # end_idx = data.find(b']')
        # pkg_len = int(data[:pkg_len])

        # convert byte to unsigned long
        packet_size = struct.unpack('!L', pkg_len)[0]
        data = _recv_n_byte(conn, packet_size)
        string = data.decode(encoding)
    except UnicodeError as err:
        print("Decoding error:", err)
        return string, False
    except:
        print("Unknown error in recv_str")
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
            conn.send(b_msg)
            while file:
                bytes_read = file.read(buff_size)
                conn.send(bytes_read)
    except ValueError as err:
        print("Encoding error:", err)
        return False
    except OSError as err:
        print("File error:", err)
        return False
    except:
        print("Unknown error in send_bin")
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
        with open(file_n, "wb") as file:
            while file:
                data = _recv_n_byte(conn, packet_size)
                file.write(data)
    except ValueError as err:
        print("Encoding error:", err)
        return False
    except OSError as err:
        print("File error:", err)
        return False
    except:
        print("Unknown error in recv_bin")
        return False

    return True
