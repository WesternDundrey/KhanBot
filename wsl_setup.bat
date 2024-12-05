@echo off
setlocal enabledelayedexpansion

echo Checking WSL environment...

REM Check if WSL is installed
wsl --status > nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo WSL is not installed. Installing WSL...
    wsl --install -d Ubuntu
    echo Please restart your computer and run this script again.
    pause
    exit /b 1
)

REM Check if Ubuntu is installed
wsl -d Ubuntu -e echo "Testing Ubuntu" > nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo Ubuntu not found. Installing Ubuntu...
    wsl --install -d Ubuntu
    echo Please wait for Ubuntu installation to complete...
    timeout /t 30 /nobreak
)

REM Initialize WSL environment
echo Setting up WSL environment...
wsl -d Ubuntu -e bash -c "
    # Update package list
    sudo apt-get update
    
    # Install required packages
    sudo apt-get install -y python3-pip python3-dev
    
    # Install Miniconda if not present
    if [ ! -d ~/miniconda3 ]; then
        echo 'Installing Miniconda...'
        curl -sL https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -o miniconda.sh
        bash miniconda.sh -b -p $HOME/miniconda3
        rm miniconda.sh
    fi
    
    # Initialize conda
    source ~/miniconda3/etc/profile.d/conda.sh
    
    # Create conda environment if it doesn't exist
    if ! conda env list | grep -q 'khanbot'; then
        echo 'Creating khanbot environment...'
        conda env create -f environment.yml
    fi
"

echo WSL environment setup complete.
echo You can now run launch_khanbot.bat to start the services.
pause