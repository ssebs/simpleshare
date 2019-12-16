# cli.py - parse the cli flags
import sys
import socket
from os import path
from threading import Thread
import time

from .util import is_port_open
from .server import broadcast_info, wait_for_replies, send_file
from .client import reply_if_server_available, recv_file


# TODO: https://docs.python.org/3/library/argparse.html


def cli_main(PORT, MCASTGROUP):
    flags = parse_flags()
    # print(flags)
    # flag defaults: {"ServeType": "file", "isServer": True, "filename": "..."}

    if flags["isServer"]:
        if not path.exists(flags["filename"]):
            raise Exception(f"File does not exist at {flags['filename']}")
        # Check if another server is running
        pass

        # Send "broadcast" every 5 secs, this is the name of it, and what port
        #  to send your replies to.
        broadcast_thread = Thread(target=broadcast_info, args=(
            flags["ip"], MCASTGROUP, flags["filename"], PORT, PORT+1))
        broadcast_thread.daemon = True
        broadcast_thread.start()

        # listen to replies, see if they want the file while the broadcast
        # is active.
        # #TODO: Make this stop when the bcast thread stops...
        while broadcast_thread.is_alive():
            reply = wait_for_replies(flags["ip"], flags["filename"], PORT+1)
            req_fn = reply.split(":")[1]
            # print(f"reply: {req_fn}")
            send_file(flags["ip"], flags["filename"], PORT+2)

        broadcast_thread.join()
    else:
        server_ip = reply_if_server_available(MCASTGROUP, PORT)
        time.sleep(0.5)
        print("Where would you like to put the new file? (incl. the name)")
        newpath = input("> ")
        recv_file(server_ip, PORT+2, newpath)
# cli_main


# parse flag vars
allowed_options = ["-s", "-c", "-f", "-d", "-ip", "-h", "--help", "--usage"]
help_message = """Usage: python simpleshare.py [OPTION] FILENAME

Local file sharing utility. Can be used as server and as client.
  GUI will be available. Make sure FILENAME is the last argument!

Options:
 -s                   Server, use this option to serve the file/dir. (Default)
 -c                   Client, use this option to be a client.
 -f                   File type, serve a file.
 -d                   Directory type, serve a dir. (Defaults to .)
 -ip                  Your local IP address you want to use. (-ip "1.2.3.4")

 -h, --help, --usage  Print this help message
"""


def parse_flags():
    flags = {"ServeType": "dir", "isServer": True,
             "filename": "./test.txt", "ip": None}

    if len(sys.argv) < 2:
        print(help_message)
        raise Exception("Not enough parameters")

    for i, flag in enumerate(sys.argv[1:]):
        if flag.startswith("-"):
            if flag not in allowed_options:
                print(help_message)
                raise Exception("Flag does not exist.")

            if flag == "-s":
                flags["isServer"] = True
            elif flag == "-c":
                flags["isServer"] = False
            elif flag == "-f":
                flags["ServeType"] = "file"
            elif flag == "-d":
                flags["ServeType"] = "dir"
            elif flag.startswith("-ip"):
                flags["ip"] = sys.argv[1:][i+1]
                continue
            elif flag == "-h" or flag == "--help" or flag == "--usage":
                print(help_message)
                exit(0)
        else:
            flags["filename"] = flag.strip()

    # if flags["isServer"] or True:
    if flags["isServer"]:
        if flags["ip"] is None:
            flags["ip"] = get_my_ip()
        try:
            socket.inet_aton(flags["ip"])
        except socket.error:
            flags["ip"] = get_my_ip()

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
