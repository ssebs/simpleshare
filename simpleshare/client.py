# client.py

import socket
import struct


# # sample code to test multicast
def listener(mcgroup, port):
    # Look up multicast group address in name server and find out IP version
    addrinfo = socket.getaddrinfo(mcgroup, None)[0]
    s = socket.socket(addrinfo[0], socket.SOCK_DGRAM)

    # Allow multiple copies of this program on one machine
    # (not strictly needed)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(('', port))

    # aton instead of pton for Win suppt
    group_bin = socket.inet_aton(addrinfo[4][0])
    mreq = group_bin + struct.pack('=I', socket.INADDR_ANY)
    s.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

    # Loop, printing any data we receive
    while True:
        data, sender = s.recvfrom(1500)
        print(f"{str(sender[0])}:{data.decode('utf-8')}")
