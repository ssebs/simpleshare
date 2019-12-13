# client.py

import socket
import struct


# # sample code to test multicast
def listener(mcgroup, port):
    print("Waiting for server...")
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
        print(data.decode('utf-8'))

# # CLI TEST
"""
import socket
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.sendto(b"Test", ("10.0.0.251", 8140))


"""