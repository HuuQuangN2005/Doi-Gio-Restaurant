@echo off
cd /d %~dp0
call C:\Users\Admin\AppData\Local\Programs\Python\Python312\python.exe -m venv venv
call venv\Scripts\activate
call pip install -r .\requirements.txt

REM init db
python -m restaurant.database.sql.models.product
python -m restaurant.database.sql.models.user
python -m restaurant.database.sql.models.order

REM run server
python -m restaurant.run
pause