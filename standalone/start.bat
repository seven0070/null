@echo off
REM Null Universe — one click. No Minecraft, no installs, no accounts.
REM Needs Python 3 (https://www.python.org/downloads/). Then open http://localhost:8765
cd /d "%~dp0"

python server.py
if errorlevel 9009 (
  py server.py
  if errorlevel 9009 (
    echo Python 3 is not installed. Install it from https://www.python.org/downloads/ then double-click this file again.
    pause
    exit /b 1
  )
)
pause
