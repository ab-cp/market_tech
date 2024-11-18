import pandas as pd

def get_sp500_stocks():
    # Wikipedia page URL that contains the S&P 500 list
    url = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
    
    # Scraping the table containing the S&P 500 list
    tables = pd.read_html(url)
    
    # The first table on the page contains the S&P 500 companies
    sp500_table = tables[0]
    
    # Get the stock symbols and company names
    sp500_stocks = sp500_table[['Symbol', 'Security']]
    
    return sp500_stocks

# Get the list of S&P 500 stocks
stocks = get_sp500_stocks()

# Save to CSV file
stocks.to_csv('sp500_stocks.csv', index=False)

# Save to JSON file
stocks.to_json('sp500_stocks.json', orient='records', lines=True)

# Print confirmation
print("Data saved to 'sp500_stocks.csv' and 'sp500_stocks.json'.")
