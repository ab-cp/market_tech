# Install necessary libraries
import yfinance as yf
import pandas as pd
import numpy as np
import json


def calculate_sharpe_ratio(tickers, start_date, end_date, risk_free_rate=0.01):
    sharpe_ratios = {}
    for ticker in tickers:
        try:
            # Adjust tickers that contain periods
            adjusted_ticker = ticker.replace('.', '-')
            
            # Download historical stock prices
            data = yf.download(adjusted_ticker, start=start_date, end=end_date,progress=False)['Adj Close']
            
            if data.empty:
                print(f"No data found for {ticker}")
                continue
            
            # Calculate daily returns
            daily_returns = data.pct_change().dropna()
            
            # Calculate the mean and standard deviation of daily returns
            mean_daily_returns = daily_returns.mean()
            std_daily_returns = daily_returns.std()
            
            # Calculate the annualized Sharpe ratio
            sharpe_ratio = (mean_daily_returns * 252 - risk_free_rate) / (std_daily_returns * np.sqrt(252))
            sharpe_ratios[ticker] = round(sharpe_ratio,3)
            print(ticker, sharpe_ratio)            
        except Exception as e:
            print(f"Error processing {ticker}: {e}")
    
    return sharpe_ratios


def get_sp500_stocks():
    # Wikipedia page URL that contains the S&P 500 list
    url = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
    
    # Scraping the table containing the S&P 500 list
    tables = pd.read_html(url)
    
    # The first table on the page contains the S&P 500 companies
    sp500_table = tables[0]
    print(sp500_table)

    tick_list = sp500_table['Symbol']    
    # Get the stock symbols and company names
    sp500_stocks = sp500_table[['Symbol', 'Security']]
    
    return sp500_stocks, tick_list

# Get the list of S&P 500 stocks
stocks, my_tickers = get_sp500_stocks()

tickers = my_tickers.to_list()

# Print confirmation
start_date = '2021-07-01'
end_date = '2024-08-01'
risk_free_rate = 0.01  # Example risk-free rate (1%)

# Calculate Sharpe ratios
sharpe_ratios = calculate_sharpe_ratio(tickers, start_date, end_date, risk_free_rate)

# Convert the Sharpe ratios to a DataFrame for easier saving
sharpe_df = pd.DataFrame(list(sharpe_ratios.items()), columns=['Ticker', 'Sharpe Ratio'])

# Save the DataFrame to a CSV file
sharpe_df.to_csv('sharpe_ratios.csv', index=False)
print("Sharpe ratios saved to sharpe_ratios.csv")

# Save the Sharpe ratios to a JSON file
with open('sharpe_ratios.json', 'w') as f:
    json.dump(sharpe_ratios, f, indent=4)

#print("Sharpe ratios saved to sharpe_ratios.json")

''' 
i = 0
for k in sharpe_ratios.keys():
    print(k, round(sharpe_ratios[k],2))
    #print(tickers[i],k[tickers[i]])
    #print(tickers[i], round(k,2))
    #i=i+1

tickers = stocks[0]
cnt = 0
for t in tickers:
    cnt = cnt + 1
print(cnt)
'''