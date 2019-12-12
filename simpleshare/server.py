# server.py

import socket
import struct
import time

PORT = 8139
MCASTGROUP = '225.0.0.250'
TTL = 1  # Increase to reach other networks


def server():
    addrinfo = socket.getaddrinfo(MCASTGROUP, None)[0]

    s = socket.socket(addrinfo[0], socket.SOCK_DGRAM)

    # Set Time-to-live (optional)
    ttl_bin = struct.pack('@i', TTL)
    s.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, ttl_bin)

    while True:
        data = b"test"
        s.sendto(data, (addrinfo[4][0], PORT))
        print("Sending data...")
        time.sleep(1)
