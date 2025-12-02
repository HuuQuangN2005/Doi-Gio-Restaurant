@echo off
cd /d %~dp0
call python -m venv venv
call venv\Scripts\activate
call pip install -r .\requirements.txt

REM init db
python -m restaurant.models.product
python -m restaurant.models.user
python -m restaurant.models.order

REM run server
python -m restaurant.index
pause