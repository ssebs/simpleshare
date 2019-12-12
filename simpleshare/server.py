# server.py

import socket
import struct
import time

PORT = 8139
MCASTGROUP = '224.0.1.68'
TTL = 2  # Increase to reach other networks


def sender():
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
