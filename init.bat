@echo off
cd /d %~dp0
call C:\Users\Admin\AppData\Local\Programs\Python\Python312\python.exe -m venv venv
call venv\Scripts\activate
call pip install -r .\requirements.txt

REM init db
python -m restaurant.models.sql

REM init data
python -m restaurant.data.data

REM run server
python -m restaurant.run
pause