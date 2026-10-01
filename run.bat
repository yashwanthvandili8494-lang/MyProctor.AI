@echo off
echo ========================================================
echo        Starting MyProctor.ai Proctoring System
echo ========================================================
echo.

cd /d "%~dp0"

if not exist ".venv\Scripts\python.exe" (
    echo [ERROR] Virtual environment not found.
    pause
    exit /b 1
)

echo Starting application at http://localhost:5000 ...
start http://localhost:5000
.venv\Scripts\python.exe app.py
pause
