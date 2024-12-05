@echo off
echo Installing all dependencies from both environment files...

:: Activate conda environment
call conda activate khanbot || (
    echo Conda environment 'khanbot' not found. Creating it...
    call conda create -n khanbot python=3.10 -y
    call conda activate khanbot
)

echo Installing backend-api dependencies...
cd backend-api
call conda env update -n khanbot --file environment.yml
pip install -r requirements.txt 2>nul

echo Installing dashboard dependencies...
cd ../dashboard
call conda env update -n khanbot --file environment_conda.yml
pip install -r requirements.txt 2>nul

echo Installation complete. Use 'conda activate khanbot' to use the environment.
pause