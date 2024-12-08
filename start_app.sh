#!/bin/bash

# Initialize conda in this shell, adjust path if different
source /opt/anaconda3/etc/profile.d/conda.sh

# Start backend
conda activate backend-api
uvicorn backend-api.main:app --reload &
BACKEND_PID=$!

# Wait a bit for backend to start
sleep 3

# Start dashboard
conda activate dashboard
make run &
DASHBOARD_PID=$!

# Wait a bit for dashboard to start
sleep 10

# Open the dashboard in the default browser
open http://127.0.0.1:8501

# Keep the script alive as long as the dashboard runs, or until user quits
wait $DASHBOARD_PID

# When user closes dashboard or kills it, also kill backend
kill $BACKEND_PID