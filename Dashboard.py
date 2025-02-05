import streamlit as st
import pandas as pd
import yfinance as yf
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
import streamlit as st
import pandas as pd
import yfinance as yf
import requests

import streamlit as st
import pandas as pd
import yfinance as yf
import requests

def load_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Load CSS
load_css("styles.css")

def fetch_stock_data(ticker):
    df = yf.download(ticker, start="2020-01-01", end="2025-01-25")
    return df

def fetch_fundamental_data(ticker):
    stock = yf.Ticker(ticker)
    info = stock.info
    financials = stock.financials
    balance_sheet = stock.balance_sheet
    cashflow = stock.cashflow
    
    dates = pd.date_range(start="2020-01-01", end="2025-01-25", freq='D')
    fundamental_data = []
    
    for date in dates:
        try:
            total_revenue = financials.loc["Total Revenue"].get(date.strftime("%Y-%m-%d"), None) if "Total Revenue" in financials.index else None
            debt_to_equity = balance_sheet.loc["Total Debt"].get(date.strftime("%Y-%m-%d"), None) / balance_sheet.loc["Total Equity"].get(date.strftime("%Y-%m-%d"), None) if "Total Debt" in balance_sheet.index and "Total Equity" in balance_sheet.index else None
            net_cashflow = cashflow.loc["Total Cash From Operating Activities"].get(date.strftime("%Y-%m-%d"), None) if "Total Cash From Operating Activities" in cashflow.index else None
        except Exception:
            total_revenue, debt_to_equity, net_cashflow = None, None, None
        
        data = {
            "Date": date,
            "Market Cap": info.get("marketCap"),
            "Enterprise Value": info.get("enterpriseValue"),
            "P/E Ratio": info.get("trailingPE"),
            "Debt-to-Equity Ratio": debt_to_equity,
            "Total Revenue": total_revenue,
            "Net Cash Flow": net_cashflow
        }
        fundamental_data.append(data)
    
    return pd.DataFrame(fundamental_data)

def fetch_live_news(api_key, query):
    url = f'https://newsapi.org/v2/everything?q={query}&sortBy=publishedAt&apiKey={api_key}'
    response = requests.get(url)
    news_data = response.json()
    return news_data['articles'] if 'articles' in news_data else []

# Energy companies and their ticker symbols
companies = {
    "Adani Energy": "ADANIGREEN.NS",
    "Tata Power": "TATAPOWER.NS",
    "Jsw Energy": "JSWENERGY.NS",
    "NTPC": "NTPC.NS",
    "Power Grid Corp": "POWERGRID.NS",
    "NHPC": "NHPC.NS"
}

st.title("Stock Market Dashboard")
st.sidebar.header("Select Company")

company = st.sidebar.selectbox("Choose a company", list(companies.keys()))
ticker = companies[company]

col1, col2 = st.columns(2)

# First column: Selected Company's About and Performance
with col1:
    st.subheader(f"About {company}")
    st.write("Company information goes here...")

    st.subheader(f"{company} Performance")
    df_stock = fetch_stock_data(ticker)
    st.dataframe(df_stock.tail(10))

# Second column: Live NEWS and EPS, PE, IPO KPI
news_api_key = "31739ed855eb4759908a898ab99a43e7"
query = company

with col2:
    st.subheader("Live News")
    news_articles = fetch_live_news(news_api_key, query)
    news_text = ""
    for article in news_articles:
        news_text += f"**{article['title']}**\n\n{article['description']}\n\n[Read more]({article['url']})\n\n\n"
    st.text_area("Live News", news_text, height=300)

    st.subheader(f"{company} EPS, PE, IPO KPI")
    df_fundamental = fetch_fundamental_data(ticker)
    st.dataframe(df_fundamental)

st.write("Data fetched successfully! Use this for further analysis and prediction.")
