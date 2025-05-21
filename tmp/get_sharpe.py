# Install necessary libraries
import yfinance as yf
import pandas as pd
import numpy as np

def calculate_sharpe_ratio(tickers, start_date, end_date, risk_free_rate=0.01):
    # Download historical stock prices
    data = yf.download(tickers, start=start_date, end=end_date)['Adj Close']
    
    # Calculate daily returns
    daily_returns = data.pct_change().dropna()
    
    # Calculate the mean and standard deviation of daily returns
    mean_daily_returns = daily_returns.mean()
    std_daily_returns = daily_returns.std()
    
    # Calculate the annualized Sharpe ratio
    sharpe_ratios = (mean_daily_returns - risk_free_rate / 252) / std_daily_returns * np.sqrt(252)
    
    return sharpe_ratios

# Define parameters
tickers = ['AAPL', 'MSFT', 'GOOGL', 'AJG', 'MCK', 'SPY']  # Example tickers
start_date = '2021-07-01'
end_date = '2024-07-01'
risk_free_rate = 0.01  # Example risk-free rate (1%)

# Calculate Sharpe ratios
sharpe_ratios = calculate_sharpe_ratio(tickers, start_date, end_date, risk_free_rate)

#print(sharpe_ratios)

i = 0
for k in sharpe_ratios:
    print(tickers[i], round(k,2))
    i=i+1
