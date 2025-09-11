import pandas as pd
import os

class PerformanceMonitorAgent:
    def __init__(self, trades_log_path='results/trades_log.csv'):
        self.trades_log_path = trades_log_path

    def log_weekly_results(self):
        # Log summary of trades for the week
        if os.path.exists(self.trades_log_path):
            trades = pd.read_csv(self.trades_log_path)
            print(f"Total trades so far: {len(trades)}")
            print(trades.tail())
        else:
            print("No trades logged yet.")
