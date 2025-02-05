import streamlit as st
import pandas as pd
import yfinance as yf
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
#Create a ticker-dropdown
import streamlit as st
import yfinance as yf
import pandas as pd

def fetch_stock_data(ticker):
    """Fetch historical stock data."""
    df = yf.download(ticker, start="2021-01-01", end="2025-01-25")
    return df

def fetch_fundamental_data(ticker):
    """Fetch fundamental company data for sales prediction."""
    stock = yf.Ticker(ticker)
    info = stock.info
    financials = stock.financials
    
    # Extract relevant financial data
    data = {
        "Market Cap": info.get("marketCap"),
        "Enterprise Value": info.get("enterpriseValue"),
        "P/E Ratio": info.get("trailingPE"),
        "Debt-to-Equity Ratio": info.get("debtToEquity"),
        "Total Revenue (Latest)": financials.loc["Total Revenue"].iloc[0] if "Total Revenue" in financials.index else None
    }
    
    return pd.DataFrame([data])

# Energy companies and their ticker symbols
companies = {
    "Adani Energy": "ADANIGREEN.NS",
    "Tata Power": "TATAPOWER.NS",
    "Jsw Energy": "JSWENERGY.NS",
    "NTPC": "NTPC.NS",
    "Power Grid Corp": "POWERGRID.NS",
    "NHPC": "NHPC.NS"
}

# Streamlit UI
st.title("Stock Market Dashboard")
st.sidebar.header("Select Company")

# Dropdown for company selection
company = st.sidebar.selectbox("Choose a company", list(companies.keys()))
ticker = companies[company]

# Fetch and display stock data
st.subheader(f"{company} Stock Data")
df_stock = fetch_stock_data(ticker)
st.dataframe(df_stock.tail(10))  # Show last 10 records

# Fetch and display fundamental data
st.subheader(f"{company} Financial Data")
df_fundamental = fetch_fundamental_data(ticker)
st.dataframe(df_fundamental)

st.write("Data fetched successfully! Use this for further analysis and prediction.")
