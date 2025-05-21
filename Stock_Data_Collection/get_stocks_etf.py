import requests
import pandas as pd
from bs4 import BeautifulSoup
'''
The following code doesnt seem to work
for the ETF.

'''
def get_etf_holdings(etf_ticker):
    url = f"https://finance.yahoo.com/quote/{etf_ticker}/holdings?p={etf_ticker}"
    
    # Send a GET request to the URL
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Find the holdings table by its unique attributes
    tables = soup.find_all("table")
    
    # Parse the table into a DataFrame
    holdings_df = pd.read_html(str(tables))[0]
    
    return holdings_df

# Get the list of holdings for VGT
vgt_holdings = get_etf_holdings("VGT")

# Save to CSV file
vgt_holdings.to_csv('vgt_holdings.csv', index=False)

# Save to JSON file
vgt_holdings.to_json('vgt_holdings.json', orient='records', lines=True)

# Print confirmation
print("Data saved to 'vgt_holdings.csv' and 'vgt_holdings.json'.")
