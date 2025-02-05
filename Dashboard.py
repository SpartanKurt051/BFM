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
import plotly.express as px

# Set page configuration (optional)
st.set_page_config(
    page_title="Multi-Page Dashboard",
    page_icon=":bar_chart:",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Multi-page navigation using a sidebar selectbox
page = st.sidebar.selectbox("Select Page", ["Dashboard", "Page 2", "Page 3"])

if page == "Dashboard":
    st.title("Dashboard - Page 1")
    
    # Divide the page vertically into two columns (left and right)
    left_col, right_col = st.columns(2)
    
    # LEFT HALF: Four horizontal sections
    with left_col:
        # Section 1: Index Graph with search prediction, buy/sell, live stock
        with st.container():
            st.subheader("Index Graph & Live Data")
            # Placeholder for the index graph (replace with your chart code)
            dummy_graph = px.line(x=[1, 2, 3, 4], y=[10, 15, 13, 17], title="Index Graph")
            st.plotly_chart(dummy_graph, use_container_width=True)
            st.write("Search Prediction, Buy/Sell Signals, Live Stock Data go here.")
        
        st.markdown("---")  # Horizontal separator
        
        # Section 2: Year-wise filter
        with st.container():
            st.subheader("Year-wise Filter")
            # A selectbox to choose a year (you can expand this to a range or slider as needed)
            year = st.selectbox("Select Year", [2020, 2021, 2022, 2023, 2024, 2025])
            st.write(f"Data filtered for the year: {year}")
        
        st.markdown("---")  # Horizontal separator
        
        # Section 3: ML Table
        with st.container():
            st.subheader("ML Table")
            # Dummy table data; replace with your ML model output table
            ml_data = pd.DataFrame({
                "Metric": ["Accuracy", "Precision", "Recall"],
                "Value": [0.85, 0.80, 0.78]
            })
            st.dataframe(ml_data)
        
        st.markdown("---")  # Horizontal separator
        
        # Section 4: Additional Dropdown
        with st.container():
            st.subheader("Additional Options")
            option = st.selectbox("Select an Option", ["Option 1", "Option 2", "Option 3"])
            st.write(f"You selected: {option}")
    
    # RIGHT HALF: About & Performance Charts
    with right_col:
        st.header("About & Performance")
        
        # About section
        with st.container():
            st.subheader("About")
            st.write("This dashboard provides an analysis of the index performance along with detailed metrics such as Holding Analysis, Equity Share Allocation, and Advanced Ratios.")
        
        st.markdown("---")
        
        # Performance charts section
        with st.container():
            st.subheader("Performance of Index")
            
            # Holding Analysis Pie Chart
            st.write("**Holding Analysis**")
            holding_data = pd.DataFrame({
                "Holding": ["Institutional", "Retail", "Foreign"],
                "Value": [40, 35, 25]
            })
            holding_chart = px.pie(holding_data, values="Value", names="Holding", title="Holding Analysis")
            st.plotly_chart(holding_chart, use_container_width=True)
            
            st.markdown("---")
            
            # Equity Share Allocation Pie Chart
            st.write("**Equity Share Allocation**")
            equity_data = pd.DataFrame({
                "Category": ["Large Cap", "Mid Cap", "Small Cap"],
                "Value": [50, 30, 20]
            })
            equity_chart = px.pie(equity_data, values="Value", names="Category", title="Equity Share Allocation")
            st.plotly_chart(equity_chart, use_container_width=True)
            
            st.markdown("---")
            
            # Advanced Ratios Pie Chart
            st.write("**Advanced Ratios**")
            ratio_data = pd.DataFrame({
                "Ratio": ["P/E", "P/B", "PEG"],
                "Value": [15, 2, 1.2]
            })
            ratio_chart = px.pie(ratio_data, values="Value", names="Ratio", title="Advanced Ratios")
            st.plotly_chart(ratio_chart, use_container_width=True)
    
elif page == "Page 2":
    st.title("Dashboard - Page 2")
    st.write("Content for Page 2 goes here.")
    
elif page == "Page 3":
    st.title("Dashboard - Page 3")
    st.write("Content for Page 3 goes here.")
