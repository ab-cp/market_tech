import requests
import pandas as pd
import matplotlib.pyplot as plt

# Set up the API key and endpoint (replace 'YOUR_API_KEY' with your actual BEA API key)
api_key = 'YC055F424-4A82-42FA-A418-6C5D788FA1B0'
url = 'https://apps.bea.gov/api/data/'

# Define the parameters for the API request
params = {
    'UserID': api_key,
    'method': 'GetData',
    'datasetname': 'NIPA',
    'TableName': 'T20304',  # This table contains consumer spending data
    'Frequency': 'Q',  # Quarterly data
    'Year': 'ALL',  # Retrieve all available years
    'ResultFormat': 'json'
}

# Make the API request
response = requests.get(url, params=params)
data = response.json()

# Process the data
df = pd.DataFrame(data['BEAAPI']['Results']['Data'])
df['TimePeriod'] = pd.to_datetime(df['TimePeriod'])
df['DataValue'] = pd.to_numeric(df['DataValue'])

# Filter for consumer spending data
consumer_spending = df[df['LineDescription'] == 'Personal consumption expenditures']

# Plot the data
plt.figure(figsize=(10, 6))
plt.plot(consumer_spending['TimePeriod'], consumer_spending['DataValue'], label='Consumer Spending')
plt.title('Time Series of Consumer Spending in the USA')
plt.xlabel('Year')
plt.ylabel('Spending (in billions of dollars)')
plt.legend()
plt.grid(True)
plt.show()
