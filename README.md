# KhanBot

KhanBot is a custom trading bot platform with a FastAPI backend and Streamlit dashboard.

## Features

- FastAPI backend for trading logic and data management
- Streamlit dashboard for monitoring and control
- Support for multiple trading strategies
- Real-time performance monitoring
- Configuration management through web interface

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/khanbot.git
cd khanbot
```

2. Create and activate conda environment for backend:
```bash
cd backend-api
conda env create -f environment.yml
conda activate backend-api
```

3. Create and activate conda environment for dashboard:
```bash
cd ../dashboard
conda env create -f environment.yml
conda activate dashboard
```

## Usage

Run the launcher:
```bash
python launcher.py
```

Or use the executable:
```bash
./dist/khanbot
```

## Development

1. Backend API (FastAPI):
   - Located in `backend-api/`
   - Run with `uvicorn main:app --reload`

2. Dashboard (Streamlit):
   - Located in `dashboard/`
   - Run with `make run`

## License

[MIT License](LICENSE)

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.