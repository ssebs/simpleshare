# run.py
from simpleshare import cli

if __name__ == "__main__":
    try:
        cli()
    except KeyboardInterrupt:
        exit(0)
