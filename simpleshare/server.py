# server.py

import socket
import struct
import time


def broadcast_info(my_ip, mcastip, fn, port):
    print("Broadcasting.")
    # 24 & 5 for 2 mins
    tries = 15
    delay = 1

    # addrinfo = socket.getaddrinfo(mcastip, None)[0]
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    ttl_bin = struct.pack('@i', 2)
    s.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, ttl_bin)

    for t in range(tries):  # run for 2 mins ( delay*tries=x, x/60=ans )
        data = (
            f"ip: {str(my_ip)}, filename: {fn}, dataport: {port+1}"
        ).encode("utf-8")
        s.sendto(data, (mcastip, port))
        print("Sending data... " + str(tries-t) + " tries left.")
        time.sleep(delay)
# broadcast_info


def wait_for_replies(my_ip, fn, port):
    print(f"{my_ip} {fn} {port}")
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.bind((my_ip, port))

        # Wait for a reply & send the info
        while True:
            data, addr = s.recvfrom(1024)
            return f"{addr}:" + str(data.decode("utf-8"))
# wait_for_replies

# sample code to test multicast


# def sender(mcgroup, port, fn):
#     s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#     ttl_bin = struct.pack('@i', 2)
#     s.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, ttl_bin)

#     while True:
#         data = fn.encode("utf-8")
#         s.sendto(data, (mcgroup, port))
#         print("Sending data...")
#         time.sleep(1)
