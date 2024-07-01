@echo off

set "envpath=venv"

if not exist "%envpath%" (
    python -m venv %envpath%
    call "%envpath%\Scripts\activate.bat"
    pip install -r requirements.txt
)

call "%envpath%\Scripts\activate.bat"

python main.py -o
pause
