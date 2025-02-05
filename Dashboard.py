import streamlit as st
import pandas as pd
import yfinance as yf
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
#Create a ticker-dropdown
'''
import streamlit as st
import yfinance as yf
import pandas as pd

def fetch_stock_data(ticker):
    """Fetch historical stock data from 2020 to 2025-01-25 on a daily basis."""
    df = yf.download(ticker, start="2020-01-01", end="2025-01-25")
    return df

def fetch_fundamental_data(ticker):
    """Fetch fundamental company data for sales prediction on a daily basis."""
    stock = yf.Ticker(ticker)
    info = stock.info
    financials = stock.financials
    balance_sheet = stock.balance_sheet
    cashflow = stock.cashflow
    
    # Extract relevant financial data on a daily basis
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

'''
import streamlit as st
import pandas as pd
import yfinance as yf
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error

# Load CSS file
def load_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Load CSS
load_css("styles.css")

# Define functions to fetch data
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
            debt_to_equity = (balance_sheet.loc["Total Debt"].get(date.strftime("%Y-%m-%d"), None) / balance_sheet.loc["Total Equity"].get(date.strftime("%Y-%m-%d"), None)) if "Total Debt" in balance_sheet.index and "Total Equity" in balance_sheet.index else None
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

# Define companies and their tickers
companies = {
    "Adani Energy": "ADANIGREEN.NS",
    "Tata Power": "TATAPOWER.NS",
    "Jsw Energy": "JSWENERGY.NS",
    "NTPC": "NTPC.NS",
    "Power Grid Corp": "POWERGRID.NS",
    "NHPC": "NHPC.NS"
}

# Streamlit UI
st.markdown("# Stock Market Dashboard")

# Sidebar for page navigation
pages = ["Home", "Performance", "Analysis"]
page = st.sidebar.selectbox("Select a page", pages)

if page == "Home":
    st.markdown("## Home")
    st.sidebar.markdown("### Select Company")
    company = st.sidebar.selectbox("Choose a company", list(companies.keys()))
    ticker = companies[company]

    st.markdown('<div style="border: 1px solid black; padding: 10px;">', unsafe_allow_html=True)
    st.markdown(f"### {company} Stock Data")
    df_stock = fetch_stock_data(ticker)
    st.dataframe(df_stock.tail(10))
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<div style="border: 1px solid black; padding: 10px;">', unsafe_allow_html=True)
    st.markdown(f"### {company} Financial Data")
    df_fundamental = fetch_fundamental_data(ticker)
    st.dataframe(df_fundamental)
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("Data fetched successfully! Use this for further analysis and prediction.")
    
elif page == "Performance":
    st.markdown('<div style="border: 1px solid black; padding: 10px;">', unsafe_allow_html=True)
    st.markdown("## Performance of Index")
    st.markdown("### Holding Analysis")
    st.markdown("### Equity Share Allocation")
    st.markdown("### Advanced Ratios")
    st.markdown('</div>', unsafe_allow_html=True)
    # Add your charts and analysis here

elif page == "Analysis":
    st.markdown('<div style="border: 1px solid black; padding: 10px;">', unsafe_allow_html=True)
    st.markdown("## Index Graph")
    st.markdown("### Search Prediction")
    st.markdown("### Buy/Sell")
    st.markdown("### Live Stock")
    st.markdown("### Year-wise Filter")
    st.markdown("### ML Table")
    st.markdown('</div>', unsafe_allow_html=True)
    # Add your analysis and tables here
