@echo off
call conda activate khanbot || (
    echo Failed to activate conda environment
    pause
    exit /b 1
)
cd dashboard || (
    echo Failed to change directory
    pause
    exit /b 1
)
echo Starting Dashboard...
streamlit run main.py
pause