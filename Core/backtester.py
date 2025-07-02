from .data_loader import fetch_data
from .signals import generate_signals
from .strategy import run_strategy
from .performance import calculate_performance
from .plotter import plot_results

class MovingAverageCrossoverBacktester:
    """
    Controller class for the Moving Average Crossover Backtesting workflow.
    """

    def __init__(self, ticker: str, start_date: str, end_date: str,
                 short_window: int = 20, long_window: int = 50,
                 initial_capital: float = 100000):
        self.ticker = ticker.upper()
        self.start_date = start_date
        self.end_date = end_date
        self.short_window = short_window
        self.long_window = long_window
        self.initial_capital = initial_capital

        self.data = None
        self.signals = None
        self.portfolio = None
        self.trades = []
        self.metrics = {}

    def run_backtest(self, save_plot_path: str = None):
        print("=" * 60)
        print(f"MOVING AVERAGE CROSSOVER BACKTEST - {self.ticker}")
        print("=" * 60)
        print(f"Strategy: {self.short_window}-day MA vs {self.long_window}-day MA")
        print(f"Period: {self.start_date} to {self.end_date}")
        print(f"Initial Capital: ${self.initial_capital:,.2f}")
        print("-" * 60)

        # Step 1: Fetch data
        print("Fetching data...")
        self.data = fetch_data(self.ticker, self.start_date, self.end_date)

        # Step 2: Generate signals
        print("Generating trading signals...")
        self.signals = generate_signals(self.data, self.short_window, self.long_window)

        # Step 3: Run strategy and backtest
        print("Running strategy simulation...")
        self.portfolio, self.trades = run_strategy(self.signals, self.initial_capital)

        # Step 4: Calculate performance metrics
        print("Calculating performance metrics...")
        self.metrics = calculate_performance(self.portfolio, self.trades, self.initial_capital)

        # Step 5: Plot results
        print("Plotting results...")
        plot_results(self.signals, self.portfolio, self.ticker, self.metrics,
                     self.short_window, self.long_window, self.initial_capital,
                     save_path=save_plot_path)

        # Summary
        print("\nBACKTEST RESULTS")
        print("-" * 30)
        for key, value in self.metrics.items():
            print(f"{key:<25}: {value}")

        print(f"\nTotal Trades Executed: {len(self.trades)}")
        print(f"Data Points Analyzed: {len(self.data)}")

        return self
    

