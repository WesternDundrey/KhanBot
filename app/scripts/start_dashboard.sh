#!/bin/bash
# Activate the dashboard env
source /opt/anaconda3/etc/profile.d/conda.sh
conda activate dashboard

# Start Streamlit dashboard on port 8501 by default
cd ../dashboard
make run