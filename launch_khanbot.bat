@echo off
REM launch_backend.bat
wsl -e bash -ic "cd %~dp0 && ./wsl_backend.sh"

@echo off
REM launch_dashboard.bat
wsl -e bash -ic "cd %~dp0 && ./wsl_dashboard.sh"

@echo off
REM launch_khanbot.bat
echo Starting KhanBot Services...

REM Check WSL status
echo Checking WSL...
wsl --status > nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo WSL is not running or not installed properly
    echo Please run setup_khanbot.bat first
    pause
    exit /b 1
)

REM Start backend service
echo Starting Backend API in WSL...
start "KhanBot Backend" cmd /c "launch_backend.bat"

REM Wait for backend to initialize
echo Waiting for backend to initialize...
timeout /t 10 /nobreak

REM Start dashboard service
echo Starting Dashboard in WSL...
start "KhanBot Dashboard" cmd /c "launch_dashboard.bat"

echo KhanBot services are starting...
echo Backend API will be available at: http://localhost:8000
echo Dashboard will be available at: http://localhost:8501