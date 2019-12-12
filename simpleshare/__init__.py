# simpleshare
from .cli import parse_flags
from .server import sender
from .client import listener


def cli_main():
    flags = parse_flags()
    print(flags)
    # flag defaults: {"ServeType": "file", "isServer": True, "filename": "."}
    if flags["isServer"]:
        sender()
    else:
        listener()


def test():
    print("Welcome to simpleshare. This project is nowhere near done.")
