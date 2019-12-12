# simpleshare
from .cli import parse_flags
from .server import server
from .client import client


def cli_main():
    flags = parse_flags()
    print(flags)
    # flag defaults: {"ServeType": "file", "isServer": True, "filename": "."}
    if flags["isServer"]:
        server()
    else:
        client()


def test():
    print("Welcome to simpleshare. This project is nowhere near done.")
