import pandas as pd
import matplotlib.pyplot as plt

# Load price data
price_df = pd.read_csv('data/amzn_raw.csv', parse_dates=['Date'])
price_df = price_df.sort_values('Date')

# Resample to weekly (using last close of the week)
weekly_prices = price_df.set_index('Date').resample('W').last().reset_index()

# Load trades log
tades_df = pd.read_csv('results/trades_log.csv', parse_dates=['Date'])

# Merge to get price for each trade (if not already present)
if 'Price' not in tades_df.columns or tades_df['Price'].isnull().any():
    tades_df = tades_df.merge(price_df[['Date', 'Adj Close']], on='Date', how='left')
    tades_df['Price'] = tades_df['Adj Close']

# Plot weekly prices
plt.figure(figsize=(14, 7))
plt.plot(weekly_prices['Date'], weekly_prices['Adj Close'], label='Weekly Adj Close', color='blue')

# Plot buy/sell signals
buy_trades = tades_df[tades_df['Action'] == 'BUY']
sell_trades = tades_df[tades_df['Action'] == 'SELL']

plt.scatter(buy_trades['Date'], buy_trades['Price'], marker='^', color='green', s=100, label='Buy Signal')
plt.scatter(sell_trades['Date'], sell_trades['Price'], marker='v', color='red', s=100, label='Sell Signal')

plt.title('Weekly Prices with Buy/Sell Signals')
plt.xlabel('Date')
plt.ylabel('Adj Close Price')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()
