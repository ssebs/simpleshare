# cli.py - parse the cli flags
import sys
import socket

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

allowed_options = ["-s", "-c", "-f", "-d", "-ip", "-h", "--help", "--usage"]


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

# TODO: https://docs.python.org/3/library/argparse.html


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
