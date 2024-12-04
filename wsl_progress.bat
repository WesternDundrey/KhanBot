@echo off
setlocal EnableDelayedExpansion

:: Check WSL version and distribution
wsl --set-default-version 2 > nul
echo [WSL] Checking Ubuntu installation...

:: Wait for WSL to be fully available
:wait_loop
wsl -l -v | findstr "Ubuntu" > nul
if %ERRORLEVEL% NEQ 0 (
    echo [WSL] Waiting for Ubuntu to become available...
    timeout /t 2 > nul
    goto wait_loop
)

:: Initialize Ubuntu environment
echo [WSL] Initializing Ubuntu environment...
wsl --distribution Ubuntu -- bash -c "echo 'WSL environment initialized successfully'"

echo [WSL] Setup completed successfully
exit /b 0
