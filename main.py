from Core.backtester import MovingAverageCrossoverBacktester
import pandas as pd
import numpy as np

def single_stock_analysis():
    """Example: Single stock comprehensive analysis"""
    print("=== SINGLE STOCK ANALYSIS ===")
    
    backtester = MovingAverageCrossoverBacktester(
        ticker='AAPL',
        start_date='2020-01-01',
        end_date='2024-01-01',
        short_window=20,
        long_window=50,
        initial_capital=100000
    )
    

    backtester.run_backtest(save_plot_path='aapl_analysis.png')    
    return backtester

def multi_stock_comparison():
    """Example: Compare strategy across multiple stocks"""
    print("\n=== MULTI-STOCK COMPARISON ===")
    
    stocks = ['AAPL', 'MSFT', 'GOOGL', 'TSLA', 'SPY']
    results = []
    
    for ticker in stocks:
        print(f"\nAnalyzing {ticker}...")
        
        try:
            bt = MovingAverageCrossoverBacktester(
                ticker=ticker,
                start_date='2020-01-01',
                end_date='2024-01-01',
                short_window=20,
                long_window=50,
                initial_capital=100000
            )
            bt.run_backtest()
            
            total_return = (bt.portfolio['Total'].iloc[-1] - 100000) / 100000
            
            results.append({
                'Ticker': ticker,
                'Total_Return': total_return,
                'Final_Value': bt.portfolio['Total'].iloc[-1],
                'Trades': len(bt.trades)
            })
            
        except Exception as e:
            print(f"Error analyzing {ticker}: {e}")
            continue
    
    df = pd.DataFrame(results)
    df['Total_Return'] = df['Total_Return'].apply(lambda x: f"{x:.2%}")
    df['Final_Value'] = df['Final_Value'].apply(lambda x: f"${x:,.2f}")
    
    print("\nCOMPARISON RESULTS:")
    print(df.to_string(index=False))
    
    return df

def parameter_sensitivity_analysis():
    """Example: Test different MA window combinations"""
    print("\n=== PARAMETER SENSITIVITY ANALYSIS ===")
    
    short_windows = [10, 15, 20, 25]
    long_windows = [40, 50, 60]
    results = []
    
    for short in short_windows:
        for long in long_windows:
            if short >= long:
                continue
                
            print(f"Testing {short}/{long} MA combination...")
            
            try:
                bt = MovingAverageCrossoverBacktester(
                    ticker='SPY',
                    start_date='2020-01-01',
                    end_date='2024-01-01',
                    short_window=short,
                    long_window=long,
                    initial_capital=100000
                )
                bt.run_backtest()
                
                total_return = (bt.portfolio['Total'].iloc[-1] - 100000) / 100000
                daily_returns = bt.portfolio['Strategy_Returns'].dropna()
                volatility = daily_returns.std() * np.sqrt(252)
                sharpe = (total_return * 252/len(daily_returns) - 0.02) / volatility if volatility > 0 else 0
                
                results.append({
                    'Short_MA': short,
                    'Long_MA': long,
                    'Total_Return': total_return,
                    'Volatility': volatility,
                    'Sharpe_Ratio': sharpe,
                    'Trades': len(bt.trades)
                })
                
            except Exception as e:
                print(f"Error with {short}/{long}: {e}")
                continue
    
    df = pd.DataFrame(results)
    best_sharpe = df.loc[df['Sharpe_Ratio'].idxmax()]
    best_return = df.loc[df['Total_Return'].idxmax()]
    
    print(f"\nBest Sharpe Ratio: {best_sharpe['Short_MA']}/{best_sharpe['Long_MA']} MA")
    print(f"Sharpe: {best_sharpe['Sharpe_Ratio']:.3f}, Return: {best_sharpe['Total_Return']:.2%}")
    
    print(f"\nBest Total Return: {best_return['Short_MA']}/{best_return['Long_MA']} MA")
    print(f"Return: {best_return['Total_Return']:.2%}, Sharpe: {best_return['Sharpe_Ratio']:.3f}")
    
    return df

def sector_analysis():
    """Example: Analyze strategy performance across sectors"""
    print("\n=== SECTOR ANALYSIS ===")
    
    sectors = {
        'Technology': 'XLK',
        'Healthcare': 'XLV', 
        'Financial': 'XLF',
        'Energy': 'XLE',
        'Consumer Discretionary': 'XLY',
        'Utilities': 'XLU'
    }
    
    results = []
    
    for sector_name, ticker in sectors.items():
        print(f"\nAnalyzing {sector_name} ({ticker})...")
        
        try:
            bt = MovingAverageCrossoverBacktester(
                ticker=ticker,
                start_date='2020-01-01',
                end_date='2024-01-01',
                short_window=20,
                long_window=50,
                initial_capital=100000
            )
            bt.run_backtest()
            
            total_return = (bt.portfolio['Total'].iloc[-1] - 100000) / 100000
            daily_returns = bt.portfolio['Strategy_Returns'].dropna()
            
            cumulative = (1 + daily_returns).cumprod()
            running_max = cumulative.expanding().max()
            drawdown = (cumulative - running_max) / running_max
            max_drawdown = drawdown.min()
            
            results.append({
                'Sector': sector_name,
                'Ticker': ticker,
                'Total_Return': total_return,
                'Max_Drawdown': max_drawdown,
                'Trades': len(bt.trades),
                'Final_Value': bt.portfolio['Total'].iloc[-1]
            })
            
        except Exception as e:
            print(f"Error analyzing {sector_name}: {e}")
            continue
    
    df = pd.DataFrame(results)
    df = df.sort_values('Total_Return', ascending=False)
    
    print("\nSECTOR PERFORMANCE RANKING:")
    for _, row in df.iterrows():
        print(f"{row['Sector']:<25} {row['Total_Return']:>8.2%} {row['Max_Drawdown']:>8.2%} {row['Trades']:>6}")
    
    return df

def stress_test_analysis():
    """Example: Test strategy during market stress periods"""
    print("\n=== STRESS TEST ANALYSIS ===")
    
    stress_periods = [
        ('COVID Crash', '2020-02-01', '2020-04-30'),
        ('Recovery Period', '2020-05-01', '2021-12-31'),
        ('Rate Hike Period', '2022-01-01', '2023-12-31')
    ]
    
    results = []
    
    for period_name, start, end in stress_periods:
        print(f"\nTesting {period_name} ({start} to {end})...")
        
        try:
            bt = MovingAverageCrossoverBacktester(
                ticker='SPY',
                start_date=start,
                end_date=end,
                short_window=20,
                long_window=50,
                initial_capital=100000
            )
            bt.run_backtest()
            
            total_return = (bt.portfolio['Total'].iloc[-1] - 100000) / 100000
            days = len(bt.portfolio)
            buy_hold_return = (bt.portfolio['Price'].iloc[-1] - bt.portfolio['Price'].iloc[0]) / bt.portfolio['Price'].iloc[0]
            
            results.append({
                'Period': period_name,
                'Strategy_Return': total_return,
                'BuyHold_Return': buy_hold_return,
                'Outperformance': total_return - buy_hold_return,
                'Days': days,
                'Trades': len(bt.trades)
            })
            
        except Exception as e:
            print(f"Error in {period_name}: {e}")
            continue
    
    df = pd.DataFrame(results)
    print("\nSTRESS TEST RESULTS:")
    for _, row in df.iterrows():
        print(f"{row['Period']:<20} Strategy: {row['Strategy_Return']:>7.2%} "
              f"B&H: {row['BuyHold_Return']:>7.2%} Diff: {row['Outperformance']:>+7.2%}")
    
    return df

def main():
    print("MOVING AVERAGE CROSSOVER BACKTESTER - EXAMPLE USAGE")
    print("=" * 60)
    
    single_stock_analysis()
    multi_stock_comparison()
    parameter_sensitivity_analysis()
    sector_analysis()
    stress_test_analysis()

if __name__ == "__main__":
    main()