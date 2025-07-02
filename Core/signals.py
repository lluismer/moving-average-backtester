def generate_signals(data, short_window, long_window):
    # Calculate moving averages and add a column with the moving average
        data[f'MA_{short_window}'] = data['Close'].rolling(window=short_window).mean()
        data[f'MA_{long_window}'] = data['Close'].rolling(window=long_window).mean()
        
        # Generate signals
        data['Signal'] = 0
        data['Position'] = 0
        
        # Buy signal: When short MA crosses above long MA
        # Where the short_window moving average is above the long window one you change the Signal of that row to 1
        data.loc[data[f'MA_{short_window}'] > data[f'MA_{long_window}'], 'Signal'] = 1
        
        # Sell signal: When short MA crosses below long MA
        # Where the short_window moving average is below the long window one you change the Signal of that row to -1

        data.loc[data[f'MA_{short_window}'] < data[f'MA_{long_window}'], 'Signal'] = -1
        
        # See how the signals change
        data['Position'] = data['Signal'].diff().fillna(0)
        
        # Mark entry/exit points
        data['Entry'] = data['Position'] == 2  # From -1 to 1 (or 0 to 1)
        data['Exit'] = data['Position'] == -2   # From 1 to -1 (or 1 to 0)
        
        return data