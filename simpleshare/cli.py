# cli.py - parse the cli flags
import sys
import socket
import time
from os import path
from threading import Thread
import argparse

from simpleshare.util import is_port_open
from simpleshare.server import broadcast_info, wait_for_replies, send_file
from simpleshare.client import reply_if_server_available, recv_file


def cli_main(PORT, MCASTGROUP):
    flags = parse_flags()
    # flag defaults: {"type": "client", "filename": "...", "ip": "..."}

    if flags.type == "server":
        if not path.exists(flags.filename):
            raise Exception(f"File does not exist at {flags.filename}")
        # Check if another server is running
        pass

        print(f"Sharing {flags.filename} for 2 mins")

        def broadcast():
            broadcast_info(flags.ip, MCASTGROUP, flags.filename,
                           PORT, PORT+1)
        # broadcast

        def reply_n_send():
            reply = wait_for_replies(flags.ip, flags.filename,
                                     PORT+1)
            req_fn = reply.split(":")[1]
            send_file(flags.ip, flags.filename, PORT+2)
        # reply_n_send

        b_t = Thread(target=broadcast)
        b_t.start()

        r_t = Thread(target=reply_n_send)
        r_t.start()
    else:
        server_ip, filename = reply_if_server_available(MCASTGROUP, PORT)
        time.sleep(0.5)
        print("Where would you like to put the new file? (incl. the name)")
        newpath = input("> ")
        if newpath == "":
            newpath = filename
        recv_file(server_ip, PORT+2, newpath)
# cli_main


def parse_flags():
    help_message = "Local file sharing utility. Can be used as server and as \
        a client. Run this without any arguments to run GUI."
    parser = argparse.ArgumentParser(description=help_message)

    parser.add_argument("--type", action='store', default="client",
                        choices=["client", "server"],
                        help="Type, how do you want to use this tool",
                        dest="type")
    parser.add_argument("--ip", action='store', default="",
                        help="IP address, only used if you're the server",
                        dest="ip")
    parser.add_argument("FILENAME", action='store',
                        help="Name of the file you want to share, if running \
                            as the server.",
                        nargs="?")

    flags = parser.parse_args()

    if flags.type == "server":
        if not flags.FILENAME:
            parser.error("You must supply a filename if running as a server!")
        if flags.ip == "":
            flags.ip = get_my_ip()

    flags.filename = flags.FILENAME

    # print(flags)
    return flags
# parse_flags


def get_my_ip():
    my_ips = socket.gethostbyname_ex(socket.gethostname())[2]

    print("Pick an IP address from the list below:")
    for i, ip in enumerate(my_ips):
        print(f"{i+1}: {ip}")

    choice = input("> ")
    try:
        choice = int(choice)
    except Exception:
        print("Not a number")
        exit(1)

    if choice <= len(my_ips):
        return my_ips[choice - 1]

# get_my_ip
