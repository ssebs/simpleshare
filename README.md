# simpleshare
A local file sharing utility written in Python. Uses multicast UDP to share the files, and HTTP to transfer them.

## Goal:
- Single binary output
- Cross platform
- CLI
  - Args for the file / folder name
- GUI
  - DnD support. 
- Once file / folder is shared as server, client app on same network will be able to see that "someone" is sharing, and download the folder/files

## TODO:
- [ ] Structure program
    <!-- https://stackoverflow.com/questions/9382045/send-a-file-through-sockets-in-python -->
- Server
  - [ ] "Broadcast" (multicast) that you're sharing "x" file
  - [ ] Have server send files if requested to IP found.
  - [ ] CLI
  - [ ] GUI
    - [ ] DnD
- Client
  - [ ] Listen to see if anyone is sharing files
  - [ ] List available files / folders
  - [ ] Download files to specified folder
  - [ ] CLI
  - [ ] GUI
- [ ] Binary output
- [ ] Unit Tests

## Installation:
- Source:
  - Install Python 3
  - ```
    $ git clone https://github.com/ssebs/simpleshare
    $ cd simpleshare/
    $ python -m venv venv
    ```
  - Linux: 
    - `$ source ./venv/bin/activate`
  - Windows: 
    - `> .\venv\Scripts\activate.bat`
    ```
    $ pip install -r requirements.txt
    $ python run.py [<OPTIONS>] FILENAME
    ```
- Binary:
  - TBD, hopefully just download a binary for your platform

## Usage:
- CLI
  ```
  Usage: python simpleshare.py [<OPTION>] FILENAME

  Local file sharing utility. Can be used as server and as client. GUI available.
  
  Options:
  -s                   Server, use this option to serve the file/dir. (Default)
  -c                   Client, use this option to be a client.
  -f                   File type, serve a file.
  -d                   Directory type, serve a dir. (Defaults to .)
  
  -h, --help, --usage  Print this help message
  ```
- GUI
  - TBD, Double click the gui binary and follow the instructions.

## Building
- `$ pyinstaller run.py --clean -F`

## License
[MIT](./LICENSE) &copy; 2019 Sebastian Safari
