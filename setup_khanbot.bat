@echo off
setlocal enabledelayedexpansion

:: Check WSL status
wsl --status > nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo Installing WSL...
    wsl --install -d Ubuntu --no-launch
    echo WSL installation complete. A system restart may be required.
) else (
    echo WSL already installed, checking Ubuntu...
    wsl -l -v | findstr "Ubuntu" > nul
    if %ERRORLEVEL% NEQ 0 (
        echo Installing Ubuntu on WSL...
        wsl --install -d Ubuntu --no-launch
    )
)

:: Check for existing conda
where conda > nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo Installing Miniconda...
    curl -O https://repo.anaconda.com/miniconda/Miniconda3-latest-Windows-x86_64.exe
    start /wait "" Miniconda3-latest-Windows-x86_64.exe /InstallationType=JustMe /RegisterPython=0 /S /D=%UserProfile%\Miniconda3
    del Miniconda3-latest-Windows-x86_64.exe
)

:: Setup/update conda environment
call conda env list | findstr "khanbot" > nul
if %ERRORLEVEL% NEQ 0 (
    echo Creating new khanbot environment...
    call conda env create -f environment.yml
) else (
    echo Updating existing khanbot environment...
    call conda env update -f environment.yml
)

echo Setup complete! KhanBot is ready to use.
