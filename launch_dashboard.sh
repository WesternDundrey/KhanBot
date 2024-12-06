#!/bin/bash
echo "Starting Dashboard..."

# Activate conda environment
eval "$(conda shell.bash hook)"
conda activate khanbot

cd dashboard
streamlit run main.py