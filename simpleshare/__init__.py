# simpleshare
from .cli import parse_flags
from .server import server
from .client import client


def main():
    flags = parse_flags()
    print(flags)


def test():
    print("Welcome to simpleshare. This project is nowhere near done.")
