# simpleshare
from threading import Thread

from .cli import parse_flags
from .util import is_port_open
from .server import broadcast_info, wait_for_replies
from .client import reply_if_server_available

# defaults
PORT = 8139
MCASTGROUP = '239.0.0.68'


def cli_main():
    flags = parse_flags()
    # print(flags)
    # flag defaults: {"ServeType": "file", "isServer": True, "filename": "."}
    if flags["isServer"]:
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
            foo = wait_for_replies(flags["ip"], flags["filename"], PORT+1)
            print(f"reply: {foo}")
            broadcast_thread.join()
            # send file

        # ## TEST
        # sender(flags["filename"])
    else:
        reply_if_server_available(MCASTGROUP, PORT)
        print("replied!")
        # ## TEST
        # listener(MCASTGROUP, PORT)
# cli_main
