# util.py
import socket


def is_port_open(ip, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    result = sock.connect_ex((ip, port))
    if result == 0:
        sock.close()
        return True
    else:
        sock.close()
        return False

