@echo off
cd /d %~dp0

call venv\Scripts\activate

REM run server
python -m restaurant.run
pause