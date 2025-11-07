# 🤖 Automated Trading Bot

![Python](https://img.shields.io/badge/python-3.9+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Status](https://img.shields.io/badge/status-active-success.svg)

Automated trading bot with configurable stop loss and take profit strategy. Targets 10% profit per trade on the most traded US stocks. AWS cloud deployment ready.

## 📋 Table of Contents

- [Features](#features)
- [How It Works](#how-it-works)
- [Architecture](#architecture)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [AWS Deployment](#aws-deployment)
- [Project Structure](#project-structure)
- [Safety & Risk Management](#safety--risk-management)
- [Contributing](#contributing)
- [License](#license)

## ✨ Features

- **Automated Stock Selection**: Identifies the most traded stock by volume in the US market
- **Stop Loss Protection**: Automatically exits positions at 10% loss to limit downside
- **Take Profit Strategy**: Secures profits at 10% gain per trade
- **Configurable Parameters**: All trading parameters can be easily modified
- **Profit Target Tracking**: Runs until cumulative profit target is reached
- **Comprehensive Logging**: Detailed logs of all trading activities
- **Paper Trading Support**: Test with Alpaca's paper trading before going live
- **AWS Ready**: Docker and deployment scripts included for cloud hosting

## 🔄 How It Works

1. **Initialization**: Bot starts with a configurable pot (default: $1000)
2. **Stock Selection**: Scans US market to find the most traded stock by volume
3. **Entry**: Buys maximum shares possible with available capital
4. **Monitoring**: Continuously checks price against stop loss and take profit levels
5. **Exit**: Sells when either stop loss (-10%) or take profit (+10%) is triggered
6. **Repeat**: Continues trading until profit target (default: $500) is reached

## 🏗️ Architecture

```
┌─────────────────┐
│  Trading Bot    │
│   (Python)      │
└────────┬────────┘
         │
         ├──> Alpaca API (Market Data & Orders)
         ├──> Configuration (config.py)
         ├──> Logging System
         └──> AWS CloudWatch (optional)
```

## 📦 Prerequisites

- Python 3.9 or higher
- Alpaca Trading Account ([Sign up here](https://alpaca.markets/))
- Alpaca API Key and Secret
- AWS Account (for cloud deployment, optional)

## 🚀 Installation

### Local Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/Gana310/automated-trading-bot.git
   cd automated-trading-bot
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Create .env file**
   ```bash
   cp .env.example .env
   ```

5. **Configure your API keys** (edit .env file)
   ```env
   ALPACA_API_KEY=your_api_key_here
   ALPACA_API_SECRET=your_secret_key_here
   ALPACA_BASE_URL=https://paper-api.alpaca.markets
   ```

## ⚙️ Configuration

Edit `config.py` to customize trading parameters:

```python
# Trading Parameters
INITIAL_POT = 1000.0          # Starting capital ($)
PROFIT_TARGET = 500.0         # Target profit ($)
STOP_LOSS_PCT = 0.10          # Stop loss (10%)
TAKE_PROFIT_PCT = 0.10        # Take profit (10%)

# Timing
CHECK_INTERVAL = 30           # Price check frequency (seconds)
TRADE_INTERVAL = 60           # Wait between trades (seconds)

# Risk Management
MAX_CONSECUTIVE_LOSSES = 3    # Pause after losses
MIN_STOCK_PRICE = 5.0         # Avoid penny stocks
MAX_STOCK_PRICE = 500.0       # Control position size
```

## 💻 Usage

### Run the Bot

```bash
python trading_bot.py
```

### Test Configuration

```bash
python config.py
```

### View Logs

```bash
tail -f trading_bot.log
```

## ☁️ AWS Deployment

For detailed AWS deployment instructions, see [AWS_DEPLOYMENT.md](AWS_DEPLOYMENT.md)

### Quick Deploy

```bash
# Build Docker image
docker build -t trading-bot .

# Run container
docker run -d --env-file .env trading-bot
```

## 📁 Project Structure

```
automated-trading-bot/
├── trading_bot.py          # Main trading bot logic
├── config.py               # Configuration settings
├── requirements.txt        # Python dependencies
├── Dockerfile             # Docker configuration
├── .env.example           # Example environment variables
├── .gitignore             # Git ignore rules
├── LICENSE                # MIT License
├── README.md              # This file
└── AWS_DEPLOYMENT.md      # AWS deployment guide
```

## 🛡️ Safety & Risk Management

### ⚠️ Important Disclaimers

- **Paper Trading First**: Always test with paper trading before using real money
- **Risk of Loss**: Trading involves risk of financial loss
- **No Guarantees**: Past performance does not guarantee future results
- **Your Responsibility**: You are responsible for all trading decisions
- **Not Financial Advice**: This software is for educational purposes

### 🔒 Security Best Practices

- Never commit API keys to version control
- Use environment variables for sensitive data
- Start with paper trading (default)
- Set appropriate position sizing limits
- Monitor bot activity regularly
- Use stop loss protection always

### 📊 Monitoring

- Check logs regularly: `trading_bot.log`
- Monitor Alpaca dashboard
- Set up AWS CloudWatch alarms (if deployed to AWS)
- Review trade history periodically

## 🤝 Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [Alpaca Markets](https://alpaca.markets/) for their excellent trading API
- Python trading community for inspiration

## 📞 Support

If you have questions or need help:

- Open an issue on GitHub
- Check existing issues for solutions
- Review Alpaca API documentation

---

**⚠️ Disclaimer**: This software is provided "as is" without warranty. Use at your own risk. Always test thoroughly with paper trading before using real money. The authors are not responsible for any financial losses.
