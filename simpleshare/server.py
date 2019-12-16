# server.py

import socket
import struct
import time


def broadcast_info(my_ip, mcastip, fn, port, dport):
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
            f"ip: {str(my_ip)}, filename: {fn}, dataport: {dport}"
        ).encode("utf-8")
        s.sendto(data, (mcastip, port))
        print("Sending data... " + str(tries-t) + " tries left.")
        time.sleep(delay)
# broadcast_info


def wait_for_replies(my_ip, fn, port):
    # print(f"{my_ip} {fn} {port}")
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.bind((my_ip, port))

        # Wait for a reply & send the info
        while True:
            data, addr = s.recvfrom(1024)
            return f"{addr[0]}: " + str(data.decode("utf-8"))
# wait_for_replies


def send_file(my_ip, filename, port):
    file_bin = open(filename, "rb")
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('', port))
        s.listen(1)
        print("Waiting for conn")
        print(my_ip)
        print(port)
        c, addr = s.accept()
        while True:
            print("Connection from: " + str(addr))
            c.send(file_bin.read())
            c.close()
            break
# send_file
