import pandas as pd
import yfinance as yf

# Function to get the current stock price
def get_stock_price(symbol):
    stock = yf.Ticker(symbol)
    return stock.history(period='1d')['Close'][0]

# URL of the Wikipedia page
url = 'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'

# Read the tables on the Wikipedia page
tables = pd.read_html(url)

# Check if tables were found
if tables:
    # The table we want is the first one
    df = tables[0]

    # Filter the rows where the GICS Sector is 'Information Technology'
    it_stocks = df[df['GICS Sector'] == 'Information Technology']

    # Add a new column for the current stock price
    it_stocks['Current Price'] = it_stocks['Symbol'].apply(get_stock_price)

    # Print the stock tickers
    print(it_stocks['Symbol'].tolist())
else:
    print("No tables found on the page.")

