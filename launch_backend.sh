#!/bin/bash
echo "Starting Backend API..."

# Activate conda environment
eval "$(conda shell.bash hook)"
conda activate khanbot

cd backend-api
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000