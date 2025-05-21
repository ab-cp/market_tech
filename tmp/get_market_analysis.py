# Import necessary libraries
import yfinance as yf
import pandas as pd
from IPython.display import display

# Function to get financial statements
def get_financial_statements(ticker):
    stock = yf.Ticker(ticker)
    
    # Get balance sheet
    balance_sheet = stock.balance_sheet
    #balance_sheet.columns =   # Add column title
    
    # Get income statement
    income_statement = stock.financials
    #income_statement.columns =   # Add column title
    
    # Get cash flow statement
    cash_flow = stock.cashflow
    #cash_flow.columns =   # Add column title
    
    return balance_sheet, income_statement, cash_flow

# Function to calculate financial ratios
def calculate_financial_ratios(ticker):
    stock = yf.Ticker(ticker)
    
    # Get latest financial data
    balance_sheet = stock.balance_sheet
    income_statement = stock.financials
    cash_flow = stock.cashflow
    
    # Calculate some basic financial ratios
    # Current Ratio = Current Assets / Current Liabilities
    current_ratio = balance_sheet.loc['Total Current Assets'][0] / balance_sheet.loc['Total Current Liabilities'][0]

    # Debt to Equity Ratio = Total Liabilities / Shareholder Equity
    debt_to_equity_ratio = balance_sheet.loc['Total Liab'][0] / balance_sheet.loc['Total Stockholder Equity'][0]

    # Return on Assets (ROA) = Net Income / Total Assets
    roa = income_statement.loc['Net Income'][0] / balance_sheet.loc['Total Assets'][0]

    # Return on Equity (ROE) = Net Income / Shareholder Equity
    roe = income_statement.loc['Net Income'][0] / balance_sheet.loc['Total Stockholder Equity'][0]

    # Free Cash Flow = Operating Cash Flow - Capital Expenditures
    free_cash_flow = cash_flow.loc['Total Cash From Operating Activities'][0] - cash_flow.loc['Capital Expenditures'][0]

    # Create a DataFrame for financial ratios
    ratios = pd.DataFrame({
        'Financial Metric': ['Current Ratio', 'Debt to Equity Ratio', 'Return on Assets (ROA)', 'Return on Equity (ROE)', 'Free Cash Flow'],
        ticker: [current_ratio, debt_to_equity_ratio, roa, roe, free_cash_flow]
    }).set_index('Financial Metric')
    
    return ratios

# Define ticker symbols
ticker_symbols = ['AAPL', 'NVDA', 'MCD']

# Initialize lists to store financial statements and ratios
balance_sheets = {}
income_statements = {}
cash_flows = {}
ratios_list = []

# Iterate over each ticker and store financial statements and ratios
for ticker in ticker_symbols:
    balance_sheet, income_statement, cash_flow = get_financial_statements(ticker)
    ratios = calculate_financial_ratios(ticker)
    
    balance_sheets.append(balance_sheet)
    income_statements.append(income_statement)
    cash_flows.append(cash_flow)
    ratios_list.append(ratios)

# Concatenate financial statements and ratios into single DataFrames
all_balance_sheets = pd.concat(balance_sheets, axis=1)
all_income_statements = pd.concat(income_statements, axis=1)
all_cash_flows = pd.concat(cash_flows, axis=1)
all_ratios = pd.concat(ratios_list, axis=1)

# Display the financial statements and ratios
display(all_balance_sheets)
display(all_income_statements)
display(all_cash_flows)
display(all_ratios)
