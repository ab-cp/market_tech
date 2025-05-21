import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

def calculate_pivot_points(df):
    """Calculate pivot points and support/resistance levels."""
    pivot_points = pd.DataFrame(index=df.index)
    pivot_points['Pivot Point'] = (df['High'] + df['Low'] + df['Close']) / 3
    pivot_points['Support Level 1'] = 2 * pivot_points['Pivot Point'] - df['High']
    pivot_points['Support Level 2'] = pivot_points['Pivot Point'] - (df['High'] - df['Low'])
    pivot_points['Resistance Level 1'] = 2 * pivot_points['Pivot Point'] - df['Low']
    pivot_points['Resistance Level 2'] = pivot_points['Pivot Point'] + (df['High'] - df['Low'])
    return pivot_points.round(2)  # Round to 2 decimal points

def get_stock_data(ticker, period='1mo'):
    """Fetch stock data for a given ticker and period."""
    stock = yf.Ticker(ticker)
    hist = stock.history(period=period)
    return hist

def calculate_for_stocks(tickers, period='1mo'):
    """Calculate pivot points and support/resistance levels for a list of stocks."""
    results = {}
    for ticker in tickers:
        df = get_stock_data(ticker, period)
        pivot_points = calculate_pivot_points(df)
        results[ticker] = pivot_points
    return results

def plot_pivot_points(results):
    """Plot pivot points and support/resistance levels for multiple stocks."""
    plt.figure(figsize=(14, 8))

    for ticker, pivot_points in results.items():
        pivot_points['Pivot Point'].plot(label=f'{ticker} Pivot Point')
        pivot_points['Support Level 1'].plot(label=f'{ticker} Support Level 1')
        pivot_points['Support Level 2'].plot(label=f'{ticker} Support Level 2')
        pivot_points['Resistance Level 1'].plot(label=f'{ticker} Resistance Level 1')
        pivot_points['Resistance Level 2'].plot(label=f'{ticker} Resistance Level 2')

    plt.title('Pivot Points and Support/Resistance Levels')
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.legend()
    plt.grid(True)
    plt.show()

# List of stock tickers
tickers = ['AAPL', 'MSFT', 'GOOGL']

# Period (e.g., '1mo', '3mo', '1y', etc.)
period = '1mo'

# Calculate pivot points and support/resistance levels
results = calculate_for_stocks(tickers, period)

# Display results
for ticker, pivot_points in results.items():
    print(f"Results for {ticker}:")
    print(pivot_points)
    print()

# Plot the pivot points and support/resistance levels
plot_pivot_points(results)
