# KhanBot Desktop

A desktop application for KhanBot trading platform.

## Prerequisites

Before running KhanBot, please ensure you have the following installed:

1. **Docker Desktop**
   - Download from [https://www.docker.com/products/docker-desktop](https://www.docker.com/products/docker-desktop)
   - Make sure Docker is running before starting KhanBot

2. **Conda**
   - Download from [https://docs.conda.io/en/latest/miniconda.html](https://docs.conda.io/en/latest/miniconda.html)
   - Required for running Python services

## Installation

1. Install Docker Desktop and start it
2. Set up the conda environments:
```bash
# Backend API environment
conda env create -f backend-api/environment.yml

# Dashboard environment
conda env create -f dashboard/environment.yml
```

3. Install application dependencies:
```bash
npm install
```

## Running KhanBot

1. Ensure Docker Desktop is running
2. Start the application:
```bash
npm start
```

## Troubleshooting

If you encounter any issues:

1. Make sure Docker Desktop is running
2. Check that both conda environments are properly installed
3. Verify that ports 8000 and 8501 are not in use
4. Check the application logs for specific error messages