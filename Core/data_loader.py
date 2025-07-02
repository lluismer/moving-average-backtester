import yfinance as yf
import pandas as pd

def fetch_data(ticker, start_date, end_date):
    try:
        print(f"Fetching data for {ticker} from {start_date} to {end_date}...")
        stock = yf.Ticker(ticker)
        data = stock.history(start=start_date, end=end_date)
        
        if data.empty:
            raise ValueError(f"No data found for ticker {ticker}")
        
        # Clean and prepare data
        data = data[['Open', 'High', 'Low', 'Close', 'Volume']].copy()
        data.dropna(inplace=True)
        
        print(f"Successfully fetched {len(data)} trading days of data")
        return data
        
    except Exception as e:
        print(f"Error fetching data: {e}")
        raise