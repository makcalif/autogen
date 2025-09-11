import yfinance as yf

# Download historical data for Amazon (AMZN) from 1995-01-01 to 2005-12-31
amzn = yf.download('AMZN', start='1995-01-01', end='2005-12-31')
amzn.to_csv('amzn_raw.csv')

# Download historical data for eBay (EBAY) from 1995-01-01 to 2005-12-31
ebay = yf.download('EBAY', start='1995-01-01', end='2005-12-31')
ebay.to_csv('ebay_raw.csv')

print('Data downloaded and saved as amzn_raw.csv and ebay_raw.csv')
