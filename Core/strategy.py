import pandas as pd

def run_strategy(signals, initial_capital):
    #Create dataframe with same row labels as signals

    portfolio = pd.DataFrame(index=signals.index)
    portfolio['Price'] = signals['Close']
    portfolio['Holdings'] = 0
    portfolio['Cash'] = initial_capital
    portfolio['Total'] = initial_capital
    portfolio['Returns'] = 0.0
    portfolio['Strategy_Returns'] = 0.0
    
    # Current position state
    position = 0  # 0 = no position, 1 = long
    cash = initial_capital
    holdings = 0
    trades = []
    
    for i, (date, row) in enumerate(signals.iterrows()):
        price = row['Close']
        signal = row['Signal']
        
        # Buy signal (enter long position)
        if signal == 1 and position == 0:
            shares_to_buy = cash // price
            if shares_to_buy > 0:
                holdings = shares_to_buy
                cash -= shares_to_buy * price
                position = 1
                
                # Record trade
                trades.append({
                    'Date': date,
                    'Type': 'BUY',
                    'Price': price,
                    'Shares': shares_to_buy,
                    'Value': shares_to_buy * price
                })
        
        # Sell signal (exit long position)
        elif signal == -1 and position == 1:
            if holdings > 0:
                cash += holdings * price
                
                # Record trade
                trades.append({
                    'Date': date,
                    'Type': 'SELL',
                    'Price': price,
                    'Shares': holdings,
                    'Value': holdings * price
                })
                
                holdings = 0
                position = 0
        
        # Update portfolio values
        portfolio.loc[date, 'Holdings'] = holdings
        portfolio.loc[date, 'Cash'] = cash
        portfolio.loc[date, 'Total'] = cash + holdings * price
        
        # Calculate returns
        if i > 0:
            prev_total = portfolio.iloc[i-1]['Total']
            portfolio.loc[date, 'Strategy_Returns'] = (portfolio.loc[date, 'Total'] - prev_total) / prev_total
            portfolio.loc[date, 'Returns'] = (price - signals.iloc[i-1]['Close']) / signals.iloc[i-1]['Close']
    
    return portfolio, trades