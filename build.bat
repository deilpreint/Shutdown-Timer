@echo off
pip install -r requirements.txt pyinstaller
pyinstaller --onefile --windowed --collect-all customtkinter --name ShutdownTimer --paths src src\main.py
echo.
echo Готово: dist\ShutdownTimer.exe
pause
