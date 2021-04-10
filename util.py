import os
import socket
import struct


# Return 0 for valid, 1 for invalid ip address, 2 for invalid port
def validate(ip_addr: str, port: int):
    try:
        socket.inet_aton(ip_addr)
    except socket.error:
        return 1
    if not (1 <= port <= 65535):
        return 2
    return 0


# Return True if msg was sent, False if encountered an error.
def send_str(conn: socket.socket, msg: str, encoding: str = "utf-8") -> bool:
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


# Private function to receive n amount of bytes
def _recv_n_byte(conn: socket.socket, packet_size: int):
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


def recv_str(conn: socket.socket, encoding: str = "utf-8") -> (str, bool):
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


# Send as binary format
def send_bin(conn: socket.socket, file_n: str, buff_size: int = 4096) -> bool:
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
    except:
        print("Unknown error in send_bin")
        return False

    return True


# Save as binary format
def recv_bin(conn: socket.socket, file_n: str) -> bool:
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
    except:
        print("Unknown error in recv_bin")
        return False

    return True
