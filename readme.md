# Moving Average Crossover Trading Strategy Backtester

A professional-grade Python backtesting framework for moving average crossover trading strategies. Built for quantitative finance applications with comprehensive performance analytics and visualization.

## 🎯 Strategy Overview

**Moving Average Crossover Strategy:**
- **BUY Signal**: When short-term MA crosses above long-term MA (Golden Cross)
- **SELL Signal**: When short-term MA crosses below long-term MA (Death Cross)
- **Position**: Long-only strategy with full capital allocation

## 🚀 Key Features

- **Real Market Data**: Fetches live historical data from Yahoo Finance
- **Professional Metrics**: Sharpe ratio, maximum drawdown, win rates, and more
- **Comprehensive Visualization**: Multi-panel charts with signals and performance
- **Trade Export**: CSV export of all trading activity
- **CLI Interface**: Command-line tool for quick backtests
- **Robust Error Handling**: Production-ready code with proper exception handling

## 📊 Performance Metrics Calculated

- Total & Annualized Returns
- Sharpe Ratio (risk-adjusted returns)
- Maximum Drawdown
- Volatility (annualized)
- Win Rate & Trade Count
- Buy & Hold Comparison

## 🛠️ Installation

```bash
# Clone the repository
git clone https://github.com/lluismer/moving-average-backtester
cd moving-average-backtester

# Install required packages
pip install yfinance pandas numpy matplotlib
```

## 📈 Quick Start

### Basic Usage (Python Script)

```python
from Core.backtester import MovingAverageCrossoverBacktester

# Initialize backtester
backtester = MovingAverageCrossoverBacktester(
    ticker='AAPL',
    start_date='2020-01-01',
    end_date='2024-01-01',
    short_window=20,  # 20-day MA
    long_window=50,   # 50-day MA
    initial_capital=100000
)

# Run backtest and display results
backtester.run_backtest(save_plot_path='')
```

### Command Line Interface

```bash
# Basic backtest
python main.py --ticker AAPL --start 2020-01-01 --end 2024-01-01

# Advanced usage with custom parameters
python ma_backtester.py \
  --ticker SPY \
  --start 2019-01-01 \
  --end 2023-12-31 \
  --short 10 \
  --long 30 \
  --capital 50000 \
  --save-chart results.png \
```

### CLI Options

| Parameter | Description | Default |
|-----------|-------------|---------|
| `--ticker` | Stock symbol | AAPL |
| `--start` | Start date (YYYY-MM-DD) | 2020-01-01 |
| `--end` | End date (YYYY-MM-DD) | 2024-01-01 |
| `--short` | Short MA window | 20 |
| `--long` | Long MA window | 50 |
| `--capital` | Initial capital | 100,000 |
| `--save-chart` | Save chart file path | None |

## 📊 Sample Results

### AAPL (2020-2024) - 20/50 MA Strategy

**Performance Metrics:**
- **Total Return**: 89.43%
- **Annualized Return**: 17.21%
- **Sharpe Ratio**: 1.34
- **Maximum Drawdown**: -12.8%
- **Win Rate**: 67.3%
- **Total Trades**: 52

**Strategy vs Buy & Hold:**
- Strategy: 89.43% (17.21% annualized)
- Buy & Hold: 156.73% (26.43% annualized)

*Note: This is illustrative data. Actual results will vary based on market conditions.*

## 🧮 Mathematical Foundation

### Signal Generation
```
Signal = 1 if MA_short(t) > MA_long(t)  # Buy
Signal = -1 if MA_short(t) < MA_long(t) # Sell
```

### Key Metrics Formulas

**Sharpe Ratio:**
```
Sharpe = (Annualized Return - Risk Free Rate) / Annualized Volatility
```

**Maximum Drawdown:**
```
Drawdown = (Peak Value - Current Value) / Peak Value
Max Drawdown = max(Drawdown_t for all t)
```

## ⚠️ Important Disclaimers

- **Past Performance ≠ Future Results**: Historical backtests do not guarantee future performance
- **No Transaction Costs**: This model excludes trading fees, slippage, and bid-ask spreads
- **Survivorship Bias**: Only analyzes stocks that exist for the full period
- **Educational Purpose**: This is for learning and research, not investment advice

## 🔄 Future Enhancements

- [ ] Multiple timeframe analysis
- [ ] Transaction cost modeling
- [ ] Risk management (stop-loss, position sizing)
- [ ] Alternative MA types (EMA, WMA)
- [ ] Multi-asset portfolio backtesting
- [ ] Machine learning signal enhancement

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

## 📞 Contact

- **Author**: Lluis Mercade
- **Email**: lluismergo@outlook.com
- **LinkedIn**: lmercade
- **GitHub**: lluismer
