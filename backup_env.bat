@echo off
setlocal enabledelayedexpansion

:: Create backup directory with timestamp
set "TIMESTAMP=%date:~10,4%%date:~4,2%%date:~7,2%_%time:~0,2%%time:~3,2%%time:~6,2%"
set "BACKUP_DIR=%USERPROFILE%\KhanBot_Backups\%TIMESTAMP%"
mkdir "%BACKUP_DIR%" 2>nul

:: Check if WSL is installed and backup Ubuntu if it exists
wsl -l -v | findstr "Ubuntu" > nul
if %ERRORLEVEL% EQU 0 (
    echo WSL Ubuntu found, creating backup...
    wsl --export Ubuntu "%BACKUP_DIR%\ubuntu_backup.tar"
)

:: Check for existing conda environment
conda env list | findstr "khanbot" > nul
if %ERRORLEVEL% EQU 0 (
    echo Existing khanbot conda environment found, creating backup...
    conda activate khanbot
    conda env export > "%BACKUP_DIR%\khanbot_environment.yml"
    conda deactivate
)

:: Save backup location for potential recovery
echo %BACKUP_DIR% > "%~dp0\last_backup.txt"

echo Backup complete at %BACKUP_DIR%