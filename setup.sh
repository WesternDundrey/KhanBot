#!/bin/bash

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${GREEN}Setting up KhanBot development environment...${NC}"

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Check for conda installation
if ! command_exists conda; then
    echo "Conda not found. Installing Miniconda..."
    
    # Download Miniconda installer
    if [[ "$OSTYPE" == "darwin"* ]]; then
        wget https://repo.anaconda.com/miniconda/Miniconda3-latest-MacOSX-x86_64.sh -O miniconda.sh
    else
        wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O miniconda.sh
    fi
    
    # Install Miniconda
    bash miniconda.sh -b -p $HOME/miniconda3
    rm miniconda.sh
    
    # Initialize conda
    eval "$($HOME/miniconda3/bin/conda shell.bash hook)"
    conda init
fi

# Create conda environments
echo "Creating conda environments..."

# Backend environment
conda env create -f backend-api/environment.yml

# Dashboard environment
conda env create -f dashboard/environment.yml

echo -e "${GREEN}Setup complete!${NC}"
echo "You can now activate the environments:"
echo "  conda activate backend-api"
echo "  conda activate dashboard"