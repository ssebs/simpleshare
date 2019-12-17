@echo off

IF "%1%"=="" (
    echo "Building Simpleshare..."
    .\venv\Scripts\activate.bat
    pyinstaller simpleshare\__main__.py --clean -F -n simpleshare.exe
    echo "Built files are in .\dist\"
) 
