# Plot opening prices throughout the year
def plot_buying_decision(company_name, data):
    fig = go.Figure()

    # Ensure 'Opening Price' column exists
    if 'Opening Price' not in data.columns:
        st.error("Opening Price column is missing in the data.")
        return

    # Compare each day's opening price with the previous day's price
    colors = ['red' if data['Opening Price'].iloc[i] < data['Opening Price'].iloc[i - 1] else 'green' for i in range(1, len(data))]
    colors.insert(0, 'red')  # Initial day color

    # Add trace for opening prices with color based on comparison
    fig.add_trace(go.Scatter(x=data['Date'], y=data['Opening Price'], mode='lines+markers', name='Opening Price',
                             marker=dict(color=colors)))

    # Update layout with titles and labels
    fig.update_layout(
        title=f'{company_name} - Buying & Selling Decision',
        xaxis_title='Date',
        yaxis_title='Opening Price',
        hovermode='x unified'
    )

    # Use Streamlit to display the plot
    st.plotly_chart(fig)

# Main function
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

    # Fetch EPS, PE Ratio, IPO Price, High, Low, Open, Close, KPI
    eps_pe_ipo_kpi = fetch_eps_pe_ipo_kpi(ticker)
    
    col1, col2 = st.columns(2)
    
    with col1:
        csv_data = load_nifty_energy_csv()
        fig = go.Figure(data=[go.Scatter(x=csv_data['Date'], y=csv_data['Open'], mode='lines', name='Open')])
        fig.update_layout(title='NIFTY ENERGY Index - Open Prices', xaxis_title='Date', yaxis_title='Open Price')
        st.plotly_chart(fig)
        
        st.subheader("Historical Stock Data of NIFTY ENERGY Index")
        st.write(csv_data)
        
    with col2:
        st.subheader("About Nifty Energy Index")
        nift_energy_info = """
        The Nifty Energy Index is designed to reflect the behavior and performance of the companies that represent the petroleum, gas and power sector in India. The Nifty Energy Index comprises of[...]

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
        
        st.subheader("NIFTYENERGY_Performance CSV")
        csv_url = "https://github.com/SpartanKurt051/BFM/raw/main/NIFTYENERGY_Performance.csv"
        df = pd.read_csv(csv_url)
        st.write(df)
    
    col1, col2, col3 = st.columns([4, 2.5, 2.5])
    
    with col1:
        # Display key financial metrics in horizontal format next to the title
        metrics_html = (
            f"<div style='float: right; color: goldenrod; white-space: nowrap; animation: scroll-left 10s linear infinite; font-size: 20px;'>"
            f"<span>EPS:</span> <span>{eps_pe_ipo_kpi['EPS']}</span> &nbsp;&nbsp;"
            f"<span>PE Ratio:</span> <span>{eps_pe_ipo_kpi['PE Ratio']}</span> &nbsp;&nbsp;"
            f"<span>IPO Date:</span> <span>{eps_pe_ipo_kpi['IPO Date']}</span> &nbsp;&nbsp;"
            f"<span>IPO Price:</span> <span>{eps_pe_ipo_kpi['IPO Price']}</span> &nbsp;&nbsp;"
            f"<span>High:</span> <span>{eps_pe_ipo_kpi['High']}</span> &nbsp;&nbsp;"
            f"<span>Low:</span> <span>{eps_pe_ipo_kpi['Low']}</span> &nbsp;&nbsp;"
            f"<span>Open:</span> <span>{eps_pe_ipo_kpi['Open']}</span> &nbsp;&nbsp;"
            f"<span>Close:</span> <span>{eps_pe_ipo_kpi['Previous Close']}</span> &nbsp;&nbsp;"
            f"<span>KPI:</span> <span>{eps_pe_ipo_kpi['KPI']}</span>"
            f"</div>"
        )
        st.markdown(metrics_html, unsafe_allow_html=True)
        st.markdown(
            """
            <style>
            @keyframes scroll-left {
                0% { transform: translateX(100%); }
                100% { transform: translateX(-100%); }
            }
            </style>
            """,
            unsafe_allow_html=True
        )

        st.subheader("Opening Price Prediction")

        current_price = fetch_current_stock_price(ticker)
        st.markdown(f"<h4 style='color: green;'>Current Stock Price: ₹{current_price:.2f}</h4>", unsafe_allow_html=True)

        opening_price_data = load_opening_price_data(ticker)
        plot_actual_vs_predicted(company, f"{company}_opening_price_data_with_predictions.csv")

        year = st.selectbox("Select Year", [2020, 2021, 2022, 2023, 2024, 2025])
        st.subheader("Opening Price Data")
        filtered_data = opening_price_data[opening_price_data['Year'] == year]
        st.dataframe(filtered_data, height=200)
        
    with col2:
        st.subheader(f"About {company}")
        company_info = fetch_company_info(ticker)
        st.text_area("Company Information", company_info, height=150)

        df_stock = fetch_stock_data(ticker)
        year_data = df_stock[df_stock.index.year == year]
        
        st.subheader("Company Weightage Heatmap")

        data_url = "https://raw.githubusercontent.com/SpartanKurt051/BFM/main/Heatmap.csv"
        df = pd.read_csv(data_url)
        df.columns = df.columns.str.strip()
        df.set_index('Company', inplace=True)

        num_companies = df.shape[0]
        num_cols = 5
        num_rows = int(np.ceil(num_companies / num_cols))

        padded_weights = np.pad(df['Weight'].values, (0, num_rows * num cols - num_companies), mode='constant', constant values=np.nan)
        padded_companies = np.pad(df.index.values, (0, num rows * num cols - num companies), mode='constant', constant values='')

        heatmap_data = padded_weights.reshape(num_rows, num cols)
        hovertext = np.array([f"{company}<br>Weight: {weight:.2f}<br>Rank: {rank+1}" for rank, (company, weight) in enumerate(zip(padded_companies, padded_weights))]).reshape(num_rows, num cols)

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
            yaxis=dict(showticklabels(False),
            height=501,
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
