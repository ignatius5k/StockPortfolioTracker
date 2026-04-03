# Portfolio Manager

A command-line stock & crypto portfolio simulator built in Python.

## Overview

Simulate buying and selling stocks and crypto across multiple trading days, track your portfolio value, and save your progress — all from the terminal. Start with $10,000 cash and see how your strategy holds up.

## Features

- Buy and sell stocks and crypto with real-time simulated prices
- Randomised ±5% daily price movement per symbol
- Edit holdings and cash balance manually
- Add custom symbols at any price
- Transaction history log
- Save and load your portfolio as JSON
- Daily portfolio summary with total value

## Default Symbols

| Symbol | Starting Price |
|--------|---------------|
| AAPL   | $240.00       |
| TSLA   | $340.00       |
| BTC    | $150,000.00   |
| ETH    | $5,600.00     |

## Getting Started
```bash
git clone https://github.com/ignatius5k/StockPortfolioTracker
cd portfolio-manager
python portfolio.py
```

No external dependencies — just the Python standard library.

## Usage

On launch you can create a new portfolio or load a saved one. From the portfolio menu:

| Key | Action           |
|-----|-----------------|
| B   | Buy             |
| S   | Sell            |
| H   | View holdings   |
| U   | Advance day (prices update) |
| M   | View market prices |
| R   | Portfolio summary |
| V   | View history    |
| E   | Edit a holding  |
| C   | Edit cash       |
| A   | Add new symbol  |
| F   | Save portfolio  |
| Q   | Quit to main menu |

## File Structure
```
portfolio-manager/
├── portfolio.py      # Main application
└── portfolio.json    # Auto-generated save file
```

## License

MIT
