import streamlit as st
import pandas as pd
import yfinance as yf
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
#Create a ticker-dropdown
companies = {
    "Adani Energy": "ADANIGREEN.NS",
    "Tata Power": "TATAPOWER.NS",
    "Jsw Energy": "JSWENERGY.NS",
    "NTPC": "NTPC.NS",
    "Power Grid Corp": "POWERGRID.NS",
    "NHPC": "NHPC.NS"
}

# Dropdown menu for selecting company
company = st.selectbox('Select a company', list(companies.keys()))

# Load the selected company's data
ticker = companies[company]
df = yf.download(ticker, start="2021-01-01", end="2025-01-25")

# Display the data
st.subheader(f'{company} Stock Data')
st.dataframe(df)
