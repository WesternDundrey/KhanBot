# KhanBot

KhanBot is a comprehensive cryptocurrency trading automation platform that combines strategy configuration, backtesting capabilities, and performance analysis in a user-friendly interface.

## Features

KhanBot provides powerful trading capabilities through its modular architecture:

### Strategy Configuration
Configure multiple trading strategies including:
- PMM Simple and Dynamic Market Making
- Grid Strike Trading
- Bollinger Bands
- MACD with Bollinger Bands
- SuperTrend Trading
- D-Man Maker V2

### Advanced Backtesting
Test your strategies with historical data using our robust backtesting engine that provides:
- Detailed performance metrics
- Visual analysis tools
- Risk assessment calculations
- Trade execution simulation

### Performance Analysis
Monitor and analyze your trading performance with:
- Real-time performance tracking
- Detailed metrics visualization
- PnL analysis
- Risk management insights

## Installation

### Prerequisites
- Python 3.10 or higher
- Git
- Windows OS (for executable version)

### Quick Start
1. Download the KhanBot executable from the latest release
2. Run `KhanBot.exe` to launch the application
3. Access the dashboard through your web browser at `http://localhost:8501`

### Development Setup
1. Clone the repository:
```bash
git clone https://github.com/WesternDundrey/KhanBot.git
cd KhanBot
```

2. Create and activate a conda environment:
```bash
conda create -n khanbot python=3.10
conda activate khanbot
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Launch the application:
```bash
python main.py
```

## Project Structure

KhanBot is organized into two main components:

### Backend API
- Located in `/backend-api`
- Handles trading logic and data processing
- Manages bot configurations and execution

### Dashboard
- Located in `/dashboard`
- Provides the user interface
- Handles visualization and configuration

## Configuration

Strategy configurations are stored in YAML format in the `/backend-api/bots/conf/controllers` directory. Each strategy can be configured through the web interface or by directly editing the configuration files.

## Usage

1. Launch KhanBot through the executable or development environment
2. Navigate to the web interface
3. Select or create a trading strategy
4. Configure your strategy parameters
5. Run backtests to validate performance
6. Deploy your strategy when ready

## Development

### Building from Source
To build the executable:
```bash
pyinstaller khanbot_launcher.spec
```

### Contributing
1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to your fork
5. Submit a pull request

## Support

For support and questions, please create an issue in the GitHub repository or contact the development team.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
