import streamlit as st
import pandas as pd
import yfinance as yf
import plotly.graph_objects as go

st.set_page_config(layout="wide")

def load_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Load CSS
load_css("styles.css")

@st.cache_data
def fetch_nifty_energy_data():
    ticker = "^NSEI"  # Replace with the correct ticker for NIFTY ENERGY if different
    stock_data = yf.download(ticker, start="2020-01-01", end="2025-01-24")
    return stock_data

def main():
    st.title("📈 Stock Market Dashboard")
    
    # Sidebar
    st.sidebar.header("Select Company")
    companies = {
        "Adani Green Energy": "ADANIGREEN.NS",
        "Tata Power": "TATAPOWER.NS",
        "Jsw Energy": "JSWENERGY.NS",
        "NTPC": "NTPC.NS",
        "Power Grid Corp": "POWERGRID.NS",
        "NHPC": "NHPC.NS"
    }
    company = st.sidebar.selectbox("Choose a company", list(companies.keys()))
    ticker = companies[company]

    # Page filter
    st.sidebar.header("Select Page")
    page = st.sidebar.selectbox("Choose a page", ["Page 1", "Page 2"])
    
    if page == "Page 1":
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Historical Stock Data of NIFTY ENERGY Index")
            nifty_energy_data = fetch_nifty_energy_data()
            st.write(nifty_energy_data)
        
        with col2:
            st.subheader("About Nifty Energy Index")
            nift_energy_info = """
            The Nifty Energy Index is designed to reflect the behavior and performance of the companies that represent the petroleum, gas and power sector in India. The Nifty Energy Index comprises of 10 stocks from the energy sector listed on the National Stock Exchange (NSE).

            The base date of the Nifty Energy Index is April 01, 2005 and base value is 1000.

            Here are some of the major constituents of the Nifty Energy Index:
            - Reliance Industries Ltd.
            - Indian Oil Corporation Ltd.
            - NTPC Ltd.
            - Power Grid Corporation of India Ltd.
            - Bharat Petroleum Corporation Ltd.
            - GAIL (India) Ltd.
            - Oil and Natural Gas Corporation Ltd.
            - Tata Power Company Ltd.
            - Adani Transmission Ltd.
            - Adani Green Energy Ltd.
            """
            st.text_area("Nifty Energy Index Information", nift_energy_info, height=150)
            
            # Display NIFTYENERGY_Performance CSV file from the repository
            st.subheader("NIFTYENERGY_Performance CSV")
            csv_url = "https://github.com/SpartanKurt051/BFM/raw/main/NIFTYENERGY_Performance.csv"
            df = pd.read_csv(csv_url)
            st.write(df)
    
    if page == "Page 2":
        col1, col2, col3 = st.columns([4, 2.5, 2.5])
    
        with col1:
            st.subheader("Opening Price Prediction")
            # Dummy data and implementation for opening price prediction
            st.write("Opening price prediction data will be here.")
        
        with col2:
            st.subheader(f"About {company}")
            # Dummy data and implementation for company information
            st.write("Company information will be here.")
        
        with col3:
            st.subheader("Live News")
            # Dummy data and implementation for live news
            st.write("Live news will be here.")

if __name__ == "__main__":
    main()
