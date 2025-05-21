import yfinance as yf

# Here We are getting Facebook financial information
# We need to pass FB as argument for that
ticker = yf.Ticker("META")

# whole python dictionary is printed here
#print(ticker.info)
# display Company Sector
#print("Company Sector : ", ticker.info['sector'])
# display Price Earnings Ratio
#print("Price Earnings Ratio : ", ticker.info['trailingPE'])
# display Company Beta
#print("Company Beta : ", ticker.info['beta'])
keys = "META"
for key, value in ticker.info.items():
    print(key, ":", value)
    keys = keys + "," + key
print(keys)

