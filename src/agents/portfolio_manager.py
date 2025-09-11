import csv
import os
from datetime import datetime

class PortfolioManagerAgent:
    def __init__(self, trades_log_path='results/trades_log.csv'):
        self.trades_log_path = trades_log_path
        # Write header if file does not exist
        if not os.path.exists(self.trades_log_path):
            with open(self.trades_log_path, mode='w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(['Date', 'Symbol', 'Action', 'Quantity', 'Price', 'Reasoning'])

    def execute_trades(self, risk_assessment, trade_date):
        # Example: Simulate a trade for demonstration
        trade = {
            'Date': trade_date.strftime('%Y-%m-%d'),
            'Symbol': 'AMZN',
            'Action': 'BUY',
            'Quantity': 10,
            'Price': 100.0,
            'Reasoning': str(risk_assessment)
        }
        self.log_trade(trade)
        return {"trades": [trade]}

    def log_trade(self, trade):
        with open(self.trades_log_path, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([
                trade['Date'],
                trade['Symbol'],
                trade['Action'],
                trade['Quantity'],
                trade['Price'],
                trade['Reasoning']
            ])
