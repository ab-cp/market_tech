import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def get_stock_metrics(ticker, start_date="2015-01-01", end_date="2023-01-01", risk_free_rate=0.02):
    """
    Calculate financial metrics for a given stock ticker.

    Parameters:
        ticker (str): Stock ticker symbol
        start_date (str): Start date for historical data (format: 'YYYY-MM-DD')
        end_date (str): End date for historical data (format: 'YYYY-MM-DD')
        risk_free_rate (float): Risk-free rate for Sharpe Ratio calculation (default: 2%)

    Returns:
        dict: A dictionary containing Beta, P/E Ratio, Sharpe Ratio, MACD, and other metrics
    """
    # Download historical stock data
    stock_data = yf.download(ticker, start=start_date, end=end_date)
    if stock_data.empty:
        return {"error": "No data found for the ticker"}

    # Download S&P 500 data as a market benchmark for Beta calculation
    sp500 = yf.download('^GSPC', start=start_date, end=end_date)

    # Daily returns for stock and market
    stock_data['Daily Return'] = stock_data['Adj Close'].pct_change()
    sp500['Daily Return'] = sp500['Adj Close'].pct_change()

    # Calculate Beta
    covariance = stock_data['Daily Return'].cov(sp500['Daily Return'])
    variance = sp500['Daily Return'].var()
    beta = covariance / variance

    # P/E Ratio (requires forward PE data)
    stock_info = yf.Ticker(ticker).info
    pe_ratio = stock_info.get('trailingPE', 'N/A')  # Get P/E Ratio (trailing)

    # Sharpe Ratio
    mean_daily_return = stock_data['Daily Return'].mean()
    std_dev = stock_data['Daily Return'].std()
    sharpe_ratio = (mean_daily_return - risk_free_rate / 252) / std_dev

    # MACD (Moving Average Convergence Divergence)
    short_ema = stock_data['Adj Close'].ewm(span=12, adjust=False).mean()
    long_ema = stock_data['Adj Close'].ewm(span=26, adjust=False).mean()
    macd = short_ema - long_ema
    signal = macd.ewm(span=9, adjust=False).mean()

    # Add MACD to DataFrame for visualization
    stock_data['MACD'] = macd
    stock_data['Signal'] = signal

    # Plot MACD
    plt.figure(figsize=(10, 5))
    plt.plot(stock_data.index, macd, label='MACD', color='blue')
    plt.plot(stock_data.index, signal, label='Signal Line', color='red')
    plt.title(f'MACD for {ticker}')
    plt.legend()
    plt.show()
    # Plot MACD and save to a file
    output_file = f"{ticker}.png"  # Change to 'aapl.jpg' if you prefer a JPG file
    plt.figure(figsize=(10, 5))
    plt.plot(stock_data.index, macd, label='MACD', color='blue')
    plt.plot(stock_data.index, signal, label='Signal Line', color='red')
    plt.title(f'MACD for {ticker}')
    plt.legend()
    plt.savefig(output_file, format='png')  # Save the figure
    plt.close()  # Close the figure to avoid displaying it in interactive environments
    print(f"MACD plot saved as {output_file}")


    # Output dictionary
    metrics = {
        "Ticker": ticker,
        "Beta": beta,
        "P/E Ratio": pe_ratio,
        "Sharpe Ratio": sharpe_ratio,
        "MACD (last value)": macd.iloc[-1],
        "Signal Line (last value)": signal.iloc[-1]
    }
    return metrics


# Example usage
ticker = "AAPL"  # Replace with your desired ticker
metrics = get_stock_metrics(ticker)
print(metrics)


