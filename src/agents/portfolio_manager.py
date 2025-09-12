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

    def execute_trades(self, risk_assessment, trade_date, trade_price=None):
        # Expect risk_assessment to include the trading signals
        trades = []
        signals = risk_assessment.get('signals', [])
        for signal in signals:
            price = trade_price if trade_price is not None else signal.get('price', 100.0)
            trade = {
                'Date': trade_date.strftime('%Y-%m-%d'),
                'Symbol': signal.get('symbol', 'AMZN'),
                'Action': signal.get('action', 'BUY'),
                'Quantity': signal.get('quantity', 10),
                'Price': price,
                'Reasoning': str(risk_assessment)
            }
            self.log_trade(trade)
            trades.append(trade)
        return {"trades": trades}

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
