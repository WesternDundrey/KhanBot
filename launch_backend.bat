@echo off
call conda activate khanbot || (
    echo Failed to activate conda environment
    pause
    exit /b 1
)
cd backend-api || (
    echo Failed to change directory
    pause
    exit /b 1
)
echo Starting Backend API...
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
pause