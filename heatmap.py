import streamlit as st
import pandas as pd
import yfinance as yf
import seaborn as sns
import matplotlib.pyplot as plt

st.set_page_config(layout="wide")

# List of top 10 companies in NIFTY Energy index
companies = {
    "Adani Green Energy": "ADANIGREEN.NS",
    "Tata Power": "TATAPOWER.NS",
    "Jsw Energy": "JSWENERGY.NS",
    "NTPC": "NTPC.NS",
    "Power Grid Corp": "POWERGRID.NS",
    "NHPC": "NHPC.NS",
    "Reliance Industries": "RELIANCE.NS",
    "Oil and Natural Gas Corp": "ONGC.NS",
    "GAIL India": "GAIL.NS",
    "Indian Oil Corp": "IOC.NS"
}

@st.cache_data
def fetch_stock_data(ticker):
    data = yf.download(ticker, start="2022-01-01", end="2023-01-01")
    if data.empty:
        return pd.Series(dtype='float64')
    return data['Close']

def main():
    st.title("🔍 NIFTY Energy Top 10 Companies Heatmap")

    # Fetch data for each company
    stock_data = {}
    for company, ticker in companies.items():
        stock_data[company] = fetch_stock_data(ticker)

    # Filter out empty series
    stock_data = {k: v for k, v in stock_data.items() if not v.empty}

    # Create a DataFrame with the closing prices of the stocks
    if stock_data:
        df = pd.DataFrame(stock_data)
        df = df.pct_change().corr()

        # Plot the heatmap
        fig, ax = plt.subplots(figsize=(10, 8))
        sns.heatmap(df, annot=True, cmap='coolwarm', ax=ax)
        plt.tight_layout()  # Ensure the plot fits into the figure area

        st.pyplot(fig)
    else:
        st.write("No data available to display the heatmap.")

if __name__ == "__main__":
    main()
