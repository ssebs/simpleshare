@echo off

IF "%1%"=="" (
    REM no param set
    echo "You must define a specific target. (cli, gui)"
) ELSE IF "%1%"=="cli" (
    REM build cli
    echo "Building CLI..."
    .\venv\Scripts\activate.bat
    pyinstaller run.py --clean -F -n simpleshare-cli
) ELSE IF "%1%"=="gui" (
    REM build gui
    echo "Building GUI..."
)
