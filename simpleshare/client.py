# client.py
import socket
import struct


def reply_if_server_available(mcgroup, port):
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

    ip = ""
    filename = ""
    port = -1
    while True:
        data = s.recv(1500)
        if data is None:
            continue
        str_data = data.decode('utf-8').split(",")
        # print(str_data)
        ip = str_data[0].split(":")[1].strip()
        filename = str_data[1].split(":")[1].strip()
        port = int(str_data[2].split(":")[1].strip())

        # todo: check if in VLI mode or GUI mode
        ans = input(f"Do you want to download {filename}? ")
        if ans.lower().startswith("y"):
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            # print(filename.encode("utf-8"), (ip, port))
            s.sendto(filename.encode("utf-8"), (ip, port))
            return ip
# reply_if_server_available


def recv_file(ip, port, newpath):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((ip, port))
        s.send(b'Test?')
        data = s.recv(1024)
        # data = s.recv(1024).decode('utf-8')
        # print(data)
        with open(newpath, "wb") as f:
            f.write(data)
# recv_file

# # sample code to test multicast
# def listener(mcgroup, port):
#     print("Waiting for server...")
#     # Look up multicast group address in name server and find out IP version
#     addrinfo = socket.getaddrinfo(mcgroup, None)[0]
#     s = socket.socket(addrinfo[0], socket.SOCK_DGRAM)

#     # Allow multiple copies of this program on one machine
#     # (not strictly needed)
#     s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
#     s.bind(('', port))

#     # aton instead of pton for Win suppt
#     group_bin = socket.inet_aton(addrinfo[4][0])
#     mreq = group_bin + struct.pack('=I', socket.INADDR_ANY)
#     s.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

#     # Loop, printing any data we receive
#     while True:
#         data = s.recv(1500)
#         print(data.decode('utf-8'))


# # CLI TEST to reply to server
"""
import socket
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.sendto(b"Test", ("10.0.0.251", 8140))


"""
