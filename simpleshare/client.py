# client.py

import socket
import struct

PORT = 8139
MCASTGROUP = '225.0.0.250'
TTL = 1  # Increase to reach other networks


def client():
    # Look up multicast group address in name server and find out IP version
    addrinfo = socket.getaddrinfo(MCASTGROUP, None)[0]

    # Create a socket
    s = socket.socket(addrinfo[0], socket.SOCK_DGRAM)

    # Allow multiple copies of this program on one machine
    # (not strictly needed)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    # Bind it to the port
    s.bind(('', PORT))

    # aton instead of pton for Win suppt
    group_bin = socket.inet_aton(addrinfo[4][0])
    mreq = group_bin + struct.pack('=I', socket.INADDR_ANY)
    s.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

    # Loop, printing any data we receive
    while True:
        data, sender = s.recvfrom(1500)
        while data[-1:] == '\0':
            data = data[:-1]  # Strip trailing \0's
        print(str(sender) + '  ' + repr(data))
