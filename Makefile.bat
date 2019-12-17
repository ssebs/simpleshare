@echo off

IF "%1%"=="" (
    echo "Building Simpleshare..."
    .\venv\Scripts\activate.bat
    pyinstaller simpleshare.py --clean -F -n simpleshare-cli
    echo "Built files are in .\dist\"
) 
