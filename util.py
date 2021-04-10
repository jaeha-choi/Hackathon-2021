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
def send_all_str(conn: socket, msg: str, encoding: str = "utf-8") -> bool:
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
