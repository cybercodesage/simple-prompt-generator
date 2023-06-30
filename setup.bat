@echo off

REM Check if the virtual environment directory exists
if not exist .\spggui (
    REM Create the virtual environment
    python -m venv spggui
)

REM Activate the virtual environment
call .\spggui\Scripts\activate.bat

REM Install the requirements
pip install -r requirements.txt

echo Virtual environment created and requirements installed.