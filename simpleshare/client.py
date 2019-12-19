# client.py
import socket
import struct


def get_filename(mcgroup, port):
    print("Waiting for server...")
    # Look up multicast group address in name server and find out IP version
    addrinfo = socket.getaddrinfo(mcgroup, None)[0]
    s = socket.socket(addrinfo[0], socket.SOCK_DGRAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(('', port))

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

        return (ip, filename)
# get_filename


def reply(ip, port, filename):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.sendto(filename.encode("utf-8"), (ip, port))
# reply


def recv_file(ip, port, newpath):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((ip, port))
        data_out = b""
        while True:
            data = s.recv(1024)
            if not data:
                break
            data_out += data
        with open(newpath, "wb") as f:
            f.write(data_out)
# recv_file
