import socket


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
def send_all_str(conn: socket.socket, msg: str, encoding: str = "utf-8") -> bool:
    try:
        b_msg = msg.encode(encoding=encoding)
        while b_msg:
            send_bytes = conn.send(b_msg)
            b_msg = b_msg[send_bytes:]
    except UnicodeError as err:
        print("Encoding error:", err)
        return False
    except:
        print("Unknown error in send_all_str")
        return False

    return True


def recv_all_str(conn: socket.socket, encoding: str = "utf-8", buff_size: int = 4096) -> (str, bool):
    string = ""
    try:
        data = conn.recv(buff_size)
        while data:
            string += data.decode(encoding)
            data = conn.recv(buff_size)
    except UnicodeError as err:
        print("Decoding error:", err)
        return string, False
    except:
        print("Unknown error in recv_all_str")
        return string, False

    return string, True


# Send as binary format
def send_all_bin(conn: socket.socket, file_n: str, buff_size: int = 4096) -> bool:
    try:
        with open(file_n, "rb") as file:
            while file:
                bytes_read = file.read(buff_size)
                conn.send(bytes_read)
    except ValueError as err:
        print("Encoding error:", err)
        return False
    except OSError as err:
        print("File error:", err)
    except:
        print("Unknown error in send_all_bin")
        return False

    return True


# Save as binary format
def recv_all_bin(conn: socket.socket, file_n: str, buff_size: int = 4096) -> bool:
    try:
        with open(file_n, "wb") as file:
            while file:
                data = conn.recv(buff_size)
                file.write(data)
    except ValueError as err:
        print("Encoding error:", err)
        return False
    except OSError as err:
        print("File error:", err)
    except:
        print("Unknown error in send_all_bin")
        return False

    return True
