# simpleshare
A local file sharing utility written in Python. Uses multicast UDP to share the files, and HTTP to transfer them.

## Goal:
- Single binary output
- Cross platform
- CLI
  - Args for the file name
- GUI
  - DnD support. 
- Once file is shared as server, client app on same network will be able to see that "someone" is sharing, and download the file.
- Folder support

## TODO:
- [ ] Structure program
    <!-- https://stackoverflow.com/questions/9382045/send-a-file-through-sockets-in-python -->
- Server
  - [x] "Broadcast" (multicast) that you're sharing "x" file
  - [ ] Have server send files if requested to IP found.
  - [.] CLI
  - [ ] GUI
    - [ ] DnD
- Client
  - [x] Listen to see if anyone is sharing files
  - [x] List available files
  - [ ] Download files to specified folder
  - [.] CLI
  - [ ] GUI
- [ ] Make this work with 1 file, 1 client
- [ ] Make this work with 1 file, 2 clients
- [ ] Make this work with 1 dir, 1 client
- [ ] Make this work with 1 dir, 2 clients
- [ ] Make this work with 2 files (2 servers), 1 client
- [ ] Make this work with 2 files (2 servers), 2 client
- [x] Binary output
- [ ] Refactor + document
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
    (venv) $ pip install -r requirements.txt
    (venv) $ python run.py [<OPTIONS>] FILENAME
    ```
- Binary:
  - TBD, just download a binary for your platform

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
- `(venv) $ pyinstaller run.py --clean -F`

## License
[MIT](./LICENSE) &copy; 2019 Sebastian Safari
