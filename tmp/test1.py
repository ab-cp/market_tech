import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

# Function to download stock data and calculate MACD
def get_stock_data(symbol, start_date, end_date):
    # Download stock data
    stock_data = yf.download(symbol, start=start_date, end=end_date)
    
    # Calculate the MACD
    stock_data['EMA12'] = stock_data['Close'].ewm(span=12, adjust=False).mean()
    stock_data['EMA26'] = stock_data['Close'].ewm(span=26, adjust=False).mean()
    stock_data['MACD'] = stock_data['EMA12'] - stock_data['EMA26']
    stock_data['Signal Line'] = stock_data['MACD'].ewm(span=9, adjust=False).mean()
    
    return stock_data

# Function to plot the stock data and MACD
def plot_stock_data(stock_data):
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 10))
    
    # Plot the closing price
    ax1.plot(stock_data['Close'], label='Close Price')
    ax1.set_title('Close Price')
    ax1.set_ylabel('Price')
    ax1.legend()
    
    # Plot the MACD
    ax2.plot(stock_data['MACD'], label='MACD', color='g')
    ax2.plot(stock_data['Signal Line'], label='Signal Line', color='r')
    ax2.bar(stock_data.index, stock_data['MACD'] - stock_data['Signal Line'], label='MACD Histogram', color='b')
    ax2.set_title('MACD')
    ax2.set_ylabel('Value')
    ax2.legend()
    
    plt.show()

# Example usage
symbol = 'AAPL'
start_date = '2023-01-01'
end_date = '2023-12-31'
stock_data = get_stock_data(symbol, start_date, end_date)
plot_stock_data(stock_data)
