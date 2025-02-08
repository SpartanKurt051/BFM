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

# New function to fetch data from the CSV file
@st.cache_data
def load_nifty_energy_csv():
    url = "https://github.com/SpartanKurt051/BFM/raw/main/NIFTYENERGY_stock.csv"
    data = pd.read_csv(url)
    data = data.rename(columns=lambda x: x.strip())  # Strip any whitespace or special characters
    data['Date'] = pd.to_datetime(data['Date'])
    return data

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

            # Load data from CSV and create a graph
            csv_data = load_nifty_energy_csv()
            fig = go.Figure(data=[go.Scatter(x=csv_data['Date'], y=csv_data['Open'], mode='lines', name='Open')])
            fig.update_layout(title='NIFTY ENERGY Index - Open Prices', xaxis_title='Date', yaxis_title='Open Price')
            st.plotly_chart(fig)
        
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

            # Fetch current stock price
            current_price = fetch_current_stock_price(ticker)
            st.markdown(f"<h4 style='color: green;'>Current Stock Price: ₹{current_price:.2f}</h4>", unsafe_allow_html=True)

            # Perform prediction on page load
            opening_price_data = load_opening_price_data(ticker)
            
            # Plot the predictions
            plot_actual_vs_predicted(company, f"{company}_opening_price_data_with_predictions.csv")

            year = st.selectbox("Select Year", [2020, 2021, 2022, 2023, 2024, 2025])

            st.subheader("Opening Price Data")
            filtered_data = opening_price_data[opening_price_data['Year'] == year]
            st.dataframe(filtered_data, height=200)  # Decrease height of the opening price data chart

        with col2:
            st.subheader(f"About {company}")
            company_info = fetch_company_info(ticker)
            st.text_area("Company Information", company_info, height=150)

            df_stock = fetch_stock_data(ticker)
            year_data = df_stock[df_stock.index.year == year]
            
            st.subheader("Company Weightage Heatmap")

            # Load heatmap data
            data_url = "https://raw.githubusercontent.com/SpartanKurt051/BFM/main/Heatmap.csv"
            df = pd.read_csv(data_url)

            # Strip any leading/trailing spaces from column names
            df.columns = df.columns.str.strip()

            # Set the 'Company' column as index
            df.set_index('Company', inplace=True)

            # Generate a grid layout for the heatmap
            num_companies = df.shape[0]
            num_cols = 5  # Define the number of columns in the "periodic table"
            num_rows = int(np.ceil(num_companies / num_cols))

            # Pad the data to fit into the grid layout
            padded_weights = np.pad(df['Weight'].values, (0, num_rows * num_cols - num_companies), mode='constant', constant_values=np.nan)
            padded_companies = np.pad(df.index.values, (0, num_rows * num_cols - num_companies), mode='constant', constant_values='')

            # Create interactive heatmap using Plotly
            heatmap_data = padded_weights.reshape(num_rows, num_cols)
            hovertext = np.array([f"{company}<br>Weight: {weight:.2f}<br>Rank: {rank+1}" for rank, (company, weight) in enumerate(zip(padded_companies, padded_weights))]).reshape(num_rows, num_cols)

            fig = go.Figure(data=go.Heatmap(
                z=heatmap_data,
                text=hovertext,
                hoverinfo='text',
                colorscale='YlOrBr',
                showscale=True,
                colorbar=dict(title='Weightage(in %)')
            ))

            fig.update_layout(
                title='Company Weightage Heatmap',
                xaxis=dict(showticklabels=False),
                yaxis=dict(showticklabels=False),
                height=501,# Increase height of the heatmap
            )

            st.plotly_chart(fig)

        with col3:
            st.subheader("Live News")
            news_api_key = "31739ed855eb4759908a898ab99a43e7"
            query = company
            news_articles = fetch_live_news(news_api_key, query)
            news_text = ""
            for article in news_articles:
                news_text += f"{article['title']}: {article['description']}\n\n"
            st.text_area("Live News", news_text, height=150)

            st.subheader("Buying & Selling Decision")
            plot_buying_decision(company, filtered_data)

if __name__ == "__main__":
    main()
