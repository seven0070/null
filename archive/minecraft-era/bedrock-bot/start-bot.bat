@echo off
REM Atlas Bedrock Bot — one-click starter for Windows.
REM Double-click this file. It checks Node, installs dependencies once, then joins
REM Sanath's Null Universe world (jensen-planting.tun.ply.gg:5650) as Atlas.
REM Keep this window open while the bot is playing; close it to stop the bot.
cd /d "%~dp0"

where node >nul 2>&1
if errorlevel 1 (
  echo Node.js is not installed.
  echo Install the LTS version from https://nodejs.org/ then double-click this file again.
  pause
  exit /b 1
)

if not exist node_modules (
  echo Installing dependencies (first run only)...
  call npm install
  if errorlevel 1 (
    echo npm install failed. Check your internet connection and try again.
    pause
    exit /b 1
  )
)

echo Starting Atlas bot...
node bot.js
echo.
echo Bot stopped (exit code %errorlevel%).
pause
