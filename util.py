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
