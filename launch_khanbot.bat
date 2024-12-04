@echo off
echo Starting KhanBot Services...

REM Start backend in a new window
start "KhanBot Backend" cmd /c launch_backend.bat

REM Wait for backend to initialize
timeout /t 5 /nobreak

REM Start dashboard in a new window
start "KhanBot Dashboard" cmd /c launch_dashboard.bat

echo KhanBot services are starting...
echo Backend API will be available at: http://localhost:8000
echo Dashboard will be available at: http://localhost:8501