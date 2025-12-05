@echo off
REM Discord AI Bot - Auto-Restart Script (Windows)
REM Usage: Double-click run_bot.bat

title Discord AI Bot - Auto Restart
color 0A

echo.
echo ====================================
echo   Discord AI Bot - Auto Restart
echo ====================================
echo.

REM Check if venv exists
if not exist "venv\Scripts\activate.bat" (
    echo [ERROR] Virtual environment not found!
    echo Please create it first:
    echo    python -m venv venv
    echo.
    pause
    exit /b 1
)

REM Activate virtual environment
call venv\Scripts\activate.bat
echo [OK] Virtual environment activated
echo.

REM Check if .env exists
if not exist ".env" (
    echo [ERROR] .env file not found!
    echo Please create .env file with your tokens
    echo.
    pause
    exit /b 1
)

REM Check if bot.py exists
if not exist "bot.py" (
    echo [ERROR] bot.py not found!
    echo.
    pause
    exit /b 1
)

echo [OK] All files found
echo.
echo Starting bot...
echo Press Ctrl+C to stop
echo.

:restart
REM Run bot
python bot.py

REM Check exit code
if %ERRORLEVEL% EQU 0 (
    echo.
    echo [OK] Bot exited normally
    goto end
) else (
    echo.
    echo [ERROR] Bot crashed with exit code: %ERRORLEVEL%
    echo Restarting in 5 seconds...
    echo Press Ctrl+C to cancel
    timeout /t 5 /nobreak > nul
    goto restart
)

:end
echo.
echo Bot stopped
pause