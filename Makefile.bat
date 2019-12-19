@echo off

IF "%1%"=="" (
    echo "Building Simpleshare..."
    .\venv\Scripts\activate
    pyinstaller simpleshare\__main__.py --clean -F -n simpleshare.exe  --noconsole --icon=simpleshare\img\simpleshare_logo.ico
    echo "Built files are in .\dist\"
) 
