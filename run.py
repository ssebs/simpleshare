# run.py
import asyncio
from simpleshare import test, cli_main

if __name__ == "__main__":
    # test()
    try:
        asyncio.run(cli_main())
    except KeyboardInterrupt:
        exit(0)
