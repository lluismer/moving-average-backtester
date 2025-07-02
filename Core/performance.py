import numpy as np


def calculate_performance(portfolio, trades, initial_capital):
    
    # Basic performance
    total_return = (portfolio['Total'].iloc[-1] - initial_capital) / initial_capital
    
    # Annualized returns
    days = len(portfolio)
    years = days / 252  # Approximate trading days per year
    annualized_return = (1 + total_return) ** (1/years) - 1
    
    # Volatility
    daily_returns = portfolio['Strategy_Returns'].dropna()
    volatility = daily_returns.std() * np.sqrt(252)  # Annualized
    
    # Sharpe ratio (assuming 2% risk-free rate)
    risk_free_rate = 0.02
    sharpe_ratio = (annualized_return - risk_free_rate) / volatility if volatility > 0 else 0
    
    # Maximum drawdown
    cumulative = (1 + daily_returns).cumprod()
    running_max = cumulative.expanding().max()
    drawdown = (cumulative - running_max) / running_max
    max_drawdown = drawdown.min()
    
    # Buy and hold comparison
    buy_hold_return = (portfolio['Price'].iloc[-1] - portfolio['Price'].iloc[0]) / portfolio['Price'].iloc[0]
    buy_hold_annualized = (1 + buy_hold_return) ** (1/years) - 1
    
    # Win rate
    if len(trades) >= 2:
        trade_pairs = []
        for i in range(0, len(trades)-1, 2):
            if i+1 < len(trades) and trades[i]['Type'] == 'BUY' and trades[i+1]['Type'] == 'SELL':
                profit = trades[i+1]['Value'] - trades[i]['Value']
                trade_pairs.append(profit)
        
        winning_trades = len([p for p in trade_pairs if p > 0])
        total_trades = len(trade_pairs)
        win_rate = winning_trades / total_trades if total_trades > 0 else 0
    else:
        win_rate = 0
        total_trades = 0
    
    metrics = {
        'Total Return': f"{total_return:.2%}",
        'Annualized Return': f"{annualized_return:.2%}",
        'Volatility': f"{volatility:.2%}",
        'Sharpe Ratio': f"{sharpe_ratio:.2f}",
        'Max Drawdown': f"{max_drawdown:.2%}",
        'Buy & Hold Return': f"{buy_hold_return:.2%}",
        'Buy & Hold Annualized': f"{buy_hold_annualized:.2%}",
        'Total Trades': total_trades,
        'Win Rate': f"{win_rate:.2%}",
        'Final Portfolio Value': f"${portfolio['Total'].iloc[-1]:,.2f}"
    }
    
    return metrics