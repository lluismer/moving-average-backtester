import matplotlib.pyplot as plt

def plot_results(signals, portfolio, ticker, metrics, short_window, long_window, initial_capital, save_path=None):
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(16, 12))
    fig.suptitle(f'{ticker} Moving Average Crossover Strategy Backtest', fontsize=16, fontweight='bold')
    
    # Plot 1: Price and Moving Averages with Signals
    ax1.plot(signals.index, signals['Close'], label='Close Price', linewidth=1, alpha=0.8)
    ax1.plot(signals.index, signals[f'MA_{short_window}'], 
            label=f'{short_window}-day MA', linewidth=1.5)
    ax1.plot(signals.index, signals[f'MA_{long_window}'], 
            label=f'{long_window}-day MA', linewidth=1.5)
    
    # Mark buy/sell signals
    buy_signals = signals[signals['Entry']]
    sell_signals = signals[signals['Exit']]
    
    ax1.scatter(buy_signals.index, buy_signals['Close'], 
                color='green', marker='^', s=100, label='Buy Signal', zorder=5)
    ax1.scatter(sell_signals.index, sell_signals['Close'], 
                color='red', marker='v', s=100, label='Sell Signal', zorder=5)
    
    ax1.set_title('Price Chart with Trading Signals')
    ax1.set_ylabel('Price ($)')
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    
    # Plot 2: Portfolio Value vs Buy & Hold
    buy_hold_value = initial_capital * (portfolio['Price'] / portfolio['Price'].iloc[0])
    
    ax2.plot(portfolio.index, portfolio['Total'], 
            label='Strategy Portfolio', linewidth=2, color='blue')
    ax2.plot(portfolio.index, buy_hold_value, 
            label='Buy & Hold', linewidth=2, color='gray', linestyle='--')
    
    ax2.set_title('Portfolio Value Comparison')
    ax2.set_ylabel('Portfolio Value ($)')
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    
    # Format y-axis as currency
    ax2.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x:,.0f}'))
    
    # Plot 3: Drawdown
    daily_returns = portfolio['Strategy_Returns'].dropna()
    cumulative = (1 + daily_returns).cumprod()
    running_max = cumulative.expanding().max()
    drawdown = (cumulative - running_max) / running_max * 100
    
    ax3.fill_between(drawdown.index, drawdown, 0, color='red', alpha=0.3)
    ax3.plot(drawdown.index, drawdown, color='red', linewidth=1)
    ax3.set_title('Strategy Drawdown')
    ax3.set_ylabel('Drawdown (%)')
    ax3.grid(True, alpha=0.3)
    
    # Plot 4: Performance Metrics Table
    ax4.axis('off')
    metrics_text = []
    for key, value in metrics.items():
        metrics_text.append(f"{key}: {value}")
    
    ax4.text(0.1, 0.9, '\n'.join(metrics_text), transform=ax4.transAxes, 
            fontsize=11, verticalalignment='top', fontfamily='monospace',
            bbox=dict(boxstyle='round', facecolor='lightgray', alpha=0.8))
    ax4.set_title('Performance Metrics')
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"Chart saved to {save_path}")
    
    plt.show()