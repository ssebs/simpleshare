# simpleshare
from os import path
from threading import Thread
import time

from .cli import parse_flags
from .util import is_port_open
from .server import broadcast_info, wait_for_replies, send_file
from .client import reply_if_server_available, recv_file

# defaults
PORT = 8139
MCASTGROUP = '239.0.0.68'


def cli_main():
    flags = parse_flags()
    # print(flags)
    # flag defaults: {"ServeType": "file", "isServer": True, "filename": "."}

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
            print(f"reply: {req_fn}")
            send_file(flags["ip"], flags["filename"], PORT+2)

        broadcast_thread.join()
    else:
        server_ip = reply_if_server_available(MCASTGROUP, PORT)
        time.sleep(0.5)
        print("Where would you like to put the new file? (incl. the name)")
        newpath = input("> ")
        recv_file(server_ip, PORT+2, newpath)
# cli_main
