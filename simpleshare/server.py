# server.py

import socket
import struct
import time


async def broadcast_info(my_ip, mcastip, fn, port):
    print("Broadcasting.")
    # 24 & 5 for 2 mins
    tries = 2
    delay = 1
    
    addrinfo = socket.getaddrinfo(mcastip, None)[0]
    s = socket.socket(addrinfo[0], socket.SOCK_DGRAM)
    ttl_bin = struct.pack('@i', 2)
    s.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, ttl_bin)

    for t in range(tries):  # run for 2 mins ( delay*tries=x, x/60=ans )
        data = (f"ip: {str(my_ip)}, filename: " + fn).encode("utf-8")
        s.sendto(data, (addrinfo[4][0], port))
        print("Sending data... " + str(tries-t) + " tries left.")
        time.sleep(delay)
# broadcast_info


def wait_for_replies(fn):
        pass

# sample code to test multicast
def sender(mcgroup, port, fn):
    addrinfo = socket.getaddrinfo(mcgroup, None)[0]

    s = socket.socket(addrinfo[0], socket.SOCK_DGRAM)

    ttl_bin = struct.pack('@i', 2)
    s.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, ttl_bin)

    while True:
        data = fn.encode("utf-8")
        s.sendto(data, (addrinfo[4][0], port))
        print("Sending data...")
        time.sleep(1)
