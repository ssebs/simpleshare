# simpleshare
from threading import Thread

from .cli import parse_flags
from .util import is_port_open
from .server import sender, broadcast_info, wait_for_replies
from .client import listener

# defaults
PORT = 8139
MCASTGROUP = '239.0.0.68'


def cli_main():
    flags = parse_flags()
    print(flags)
    # flag defaults: {"ServeType": "file", "isServer": True, "filename": "."}
    if flags["isServer"]:
        # Check if another server is running
        pass

        # Send msg every 5 secs that you have a file to share, this is the name of it, and what port to send your replies to.
        broadcast_thread = Thread(target=broadcast_info, args=(
            flags["ip"], MCASTGROUP, flags["filename"], PORT))
        broadcast_thread.start()

        # listen to replies, see if they want the file
        while broadcast_thread.is_alive():
            foo = wait_for_replies(flags["ip"], flags["filename"], PORT+1)
            print(f"reply: {foo}")
            # send file

        # ## TEST
        # sender(flags["filename"])
    else:
        # ## TEST
        listener(MCASTGROUP, PORT)
# cli_main
