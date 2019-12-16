# run.py
from simpleshare import cli_main

if __name__ == "__main__":
    try:
        cli_main()
    except KeyboardInterrupt:
        exit(0)
