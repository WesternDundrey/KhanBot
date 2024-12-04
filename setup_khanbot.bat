@echo off
echo Starting KhanBot Installation Process

REM Check if WSL is installed
wsl --status > nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo Installing WSL...
    wsl --install
    echo Please restart your computer after WSL installation and run this script again.
    pause
    exit
)

REM Install Ubuntu if not present
wsl -d Ubuntu > nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo Installing Ubuntu on WSL...
    wsl --install -d Ubuntu
)

REM Create and execute the WSL setup script
echo #!/bin/bash > wsl_setup.sh
echo sudo apt-get update >> wsl_setup.sh
echo sudo apt-get install -y python3-pip >> wsl_setup.sh
echo python3 -m venv khanbot_env >> wsl_setup.sh
echo source khanbot_env/bin/activate >> wsl_setup.sh
echo pip install -r requirements.txt >> wsl_setup.sh

REM Execute the setup in WSL
wsl bash wsl_setup.sh

REM Create the launcher script
echo #!/bin/bash > launch_khanbot.sh
echo source khanbot_env/bin/activate >> launch_khanbot.sh
echo cd %~dp0 >> launch_khanbot.sh
echo python3 khanbot_launcher.py >> launch_khanbot.sh

echo Installation complete. You can now run KhanBot using the Launch KhanBot shortcut.

REM Create a shortcut to launch KhanBot
echo Set oWS = WScript.CreateObject("WScript.Shell") > CreateShortcut.vbs
echo sLinkFile = "%USERPROFILE%\Desktop\Launch KhanBot.lnk" >> CreateShortcut.vbs
echo Set oLink = oWS.CreateShortcut(sLinkFile) >> CreateShortcut.vbs
echo oLink.TargetPath = "wsl" >> CreateShortcut.vbs
echo oLink.Arguments = "bash launch_khanbot.sh" >> CreateShortcut.vbs
echo oLink.WorkingDirectory = "%~dp0" >> CreateShortcut.vbs
echo oLink.Save >> CreateShortcut.vbs
cscript //nologo CreateShortcut.vbs
del CreateShortcut.vbs

pause
