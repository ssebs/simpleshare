# simpleshare
A local file sharing utility written in Python. 

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
  - [ ] Listen to incoming conns on multicast 
  - [ ] Have server send files if requested to IP found.
  - [ ] CLI
  - [ ] GUI
    - [ ] DnD
- Client
  - [ ] Check subnet for existing conns on multicast
  - [ ] List available files / folders
  - [ ] Download files to specified folder
  - [ ] CLI
  - [ ] GUI
- [ ] Binary output
- [ ] Unit Tests

## Installation:
- tbd, hopefully just download a binary for your platform

## Usage:
- CLI
  ```
TBD.
  ```
- GUI
  - Double click the gui binary and follow the instructions.

## License
[MIT](./LICENSE) &copy; 2019 Sebastian Safari
