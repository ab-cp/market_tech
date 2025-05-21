import yfinance as yf
import pandas as pd
import numpy as np
from yahoo_fin import stock_info as si
from scipy import stats
import datetime

# Function to get the list of S&P 500 tickers
def get_sp500_tickers():
    # Retrieve the list of S&P 500 companies from Yahoo Finance
    sp500 = si.tickers_sp500()
    for st in sp500:
        print(st)
    print('Done with sp500')
    return sp500

# Function to fetch stock data and calculate metrics
def fetch_stock_data(tickers):
    data = []
    
    for ticker in tickers:
        try:
            # Fetch stock data
            stock = yf.Ticker(ticker)
            hist = stock.history(period="1y")
            
            # Current stock price
            current_price = hist['Close'][-1]
            
            # 52 week high and low
            fifty_two_week_high = hist['High'].max()
            fifty_two_week_low = hist['Low'].min()
            
            # Support and Resistance estimation
            support = fifty_two_week_low
            resistance = fifty_two_week_high
            
            # Beta calculation (requires comparison to S&P 500 index)
            sp500 = yf.Ticker("^GSPC")
            sp500_hist = sp500.history(period="1y")['Close']
            stock_hist = hist['Close']
            beta = calculate_beta(stock_hist, sp500_hist)
            
            # Sharpe Ratio calculation
            sharpe_ratio = calculate_sharpe_ratio(stock_hist)
            
            # Append the data for the current stock
            data.append([ticker, current_price, fifty_two_week_high, fifty_two_week_low, support, resistance, beta, sharpe_ratio])
        
        except Exception as e:
            print(f"Error fetching data for {ticker}: {e}")
    
    return data

# Function to calculate Beta
def calculate_beta(stock_hist, sp500_hist):
    # Align data and calculate daily returns
    stock_returns = stock_hist.pct_change().dropna()
    sp500_returns = sp500_hist.pct_change().dropna()

    # Perform linear regression (stock vs S&P 500)
    beta, alpha, r_value, p_value, std_err = stats.linregress(sp500_returns, stock_returns)
    return beta

# Function to calculate Sharpe Ratio
def calculate_sharpe_ratio(stock_hist, risk_free_rate=0.02):
    # Calculate daily returns
    stock_returns = stock_hist.pct_change().dropna()
    
    # Calculate average daily return and standard deviation
    avg_return = stock_returns.mean()
    std_dev = stock_returns.std()
    
    # Sharpe ratio formula: (Mean return - Risk-free rate) / Standard deviation of returns
    sharpe_ratio = (avg_return - risk_free_rate / 252) / std_dev
    return sharpe_ratio

# Function to save the data into CSV
def save_to_csv(data, filename="sp500_stock_data.csv"):
    df = pd.DataFrame(data, columns=[
        'Ticker', 'Current Price', '52 Week High', '52 Week Low', 'Support', 'Resistance', 'Beta', 'Sharpe Ratio'
    ])
    df.to_csv(filename, index=False)
    print(f"Data saved to {filename}")

# Main function to fetch and process data
def main():
    tickers = get_sp500_tickers()
    print(f"Fetching data for {len(tickers)} S&P 500 stocks...")
    
    stock_data = fetch_stock_data(tickers)
    save_to_csv(stock_data)

if __name__ == "__main__":
    main()
