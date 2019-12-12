# cli.py - parse the cli flags
import sys

help_message = """Usage: python simpleshare.py [<OPTION>] FILENAME

Local file sharing utility. Can be used as server and as client. GUI available.

Options:
 -s                   Server, use this option to serve the file/dir.
 -c                   Client, use this option to be a client.
 -f                   File type, serve a file.
 -d                   Directory type, serve a dir.

 -h, --help, --usage  Print this help message
"""

allowed_options = ["-s", "-c", "-f", "-d", "-h", "--help", "--usage"]


def parse_flags():
    flags = {"ServeType": "file", "isServer": True, "filename": None}

    if len(sys.argv) < 2:
        print(help_message)
        raise Exception("Not enough parameters")

    for flag in sys.argv[1:]:
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
            elif flag == "-h" or flag == "--help" or flag == "--usage":
                print(help_message)
                exit(0)
        else:
            flags["filename"] = flag.strip()

    return flags
