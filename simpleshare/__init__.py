# simpleshare
from .cli import cli_main


# defaults
PORT = 8139
MCASTGROUP = '239.0.0.68'


def cli():
    cli_main(PORT, MCASTGROUP)
