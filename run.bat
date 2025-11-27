@echo off
cd /d %~dp0
call python -m venv venv
call venv\Scripts\activate
call pip install -r .\requirements.txt

REM init db



REM run server
python -m restaurant.index
pause