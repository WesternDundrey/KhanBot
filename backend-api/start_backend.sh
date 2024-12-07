#!/bin/bash
conda activate backend-api

# Start the backend API on port 8000
cd ../backend-api
uvicorn main:app --reload