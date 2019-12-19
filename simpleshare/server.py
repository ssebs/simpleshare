# server.py

import socket
import struct
import time


def broadcast_info(my_ip, mcastip, fn, port, dport):
    print("Broadcasting.")
    tries = 10

    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    ttl_bin = struct.pack('@i', 20)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, ttl_bin)
    s.bind((my_ip, port))

    for t in range(tries):
        data = (
            f"ip: {str(my_ip)}, filename: {fn}, dataport: {dport}"
        ).encode("utf-8")
        s.sendto(data, (mcastip, port))
        print("Sending broadcast... " + str(tries-t) + " tries left.")
        time.sleep(1)
    print("Broadcast done")
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
        c, addr = s.accept()

        print(f"Sending {filename} to {addr[0]}")
        c.send(file_bin.read())
        c.close()
# send_file
