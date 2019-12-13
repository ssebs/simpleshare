# simpleshare
import asyncio

from .cli import parse_flags
from .util import is_port_open
from .server import sender, broadcast_info
from .client import listener

# defaults
PORT = 8139
MCASTGROUP = '239.0.0.68'


async def cli_main():
    flags = parse_flags()
    print(flags)
    # flag defaults: {"ServeType": "file", "isServer": True, "filename": "."}
    if flags["isServer"]:
        # Check if another server is running
        pass

        # Send msg every 5 secs that you have a file to share, this is the name of it, and what port to send your replies to.
        task_broadcast = asyncio.create_task(
            broadcast_info(flags["ip"], MCASTGROUP, flags["filename"], PORT))

        # listen to replies, see if they want the file
        pass
        # send file
        pass

        await task_broadcast

        # ## TEST
        # sender(flags["filename"])
    else:
        # ## TEST
        listener(MCASTGROUP, PORT)


def test():
    print("Welcome to simpleshare. This project is nowhere near done.")
