#!/bin/bash

echo "KhanBot Dependency Checker and Launcher"
echo "======================================="

# Function to check if a command exists
check_command() {
    if ! command -v $1 &> /dev/null; then
        echo "❌ $1 is not installed"
        return 1
    else
        echo "✅ $1 found"
        return 0
    fi
}

# Check for essential commands
echo "Checking system requirements..."
check_command conda || { echo "Please install conda first"; exit 1; }
check_command pip || { echo "Please install pip first"; exit 1; }

# Activate or create conda environment
echo "Setting up conda environment..."
if ! conda env list | grep -q "khanbot"; then
    echo "Creating new khanbot environment..."
    conda env create -f environment.yml || { echo "Failed to create conda environment"; exit 1; }
fi

# Activate conda environment
eval "$(conda shell.bash hook)"
conda activate khanbot || { echo "Failed to activate conda environment"; exit 1; }

# Install backend dependencies
echo "Installing backend dependencies..."
cd backend-api
pip install -r requirements.txt || { echo "Failed to install backend dependencies"; exit 1; }
cd ..

# Install dashboard dependencies
echo "Installing dashboard dependencies..."
cd dashboard
pip install -r requirements.txt || { echo "Failed to install dashboard dependencies"; exit 1; }
cd ..

# Make sure launch scripts are executable
chmod +x launch_backend.sh launch_dashboard.sh

echo "All dependencies installed successfully!"
echo "Starting KhanBot..."

# Start backend
./launch_backend.sh &

# Wait for backend to initialize
echo "Waiting for backend to start..."
sleep 5

# Start dashboard
./launch_dashboard.sh &

echo "KhanBot services are starting..."
echo "Backend API will be available at: http://localhost:8000"
echo "Dashboard will be available at: http://localhost:8501"