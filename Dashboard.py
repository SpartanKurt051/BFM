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
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
import matplotlib.pyplot as plt

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

def fetch_eps_pe_ipo_kpi(ticker):
    stock = yf.Ticker(ticker)
    info = stock.info
    data = {
        "EPS": info.get("trailingEps"),
        "PE Ratio": info.get("trailingPE"),
        "IPO Date": info.get("ipoDate"),
        "KPI": info.get("kpi")
    }
    return data

def fetch_company_info(ticker):
    stock = yf.Ticker(ticker)
    info = stock.info
    summary = info.get("longBusinessSummary", "No information available.")
    return summary

# Load sales data for prediction
def load_sales_data(ticker):
    stock = yf.Ticker(ticker)
    hist = stock.history(period="max")
    hist.reset_index(inplace=True)
    hist['Year'] = hist['Date'].dt.year
    hist['Sales'] = hist['Close']  # Assuming 'Close' prices as 'Sales'
    return hist[['Year', 'Sales']]

# Predict sales using Linear Regression
def predict_sales(data):
    X = data[['Year']]
    y = data['Sales']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    model = LinearRegression()
    model.fit(X_train, y_train)
    predictions = model.predict(X_test)
    mse = mean_squared_error(y_test, predictions)
    return model, predictions, mse, X_test, y_test

# Plot sales predictions
def plot_predictions(model, data):
    plt.figure(figsize=(10, 5))
    plt.scatter(data['Year'], data['Sales'], color='blue', label='Actual Sales')
    plt.plot(data['Year'], model.predict(data[['Year']]), color='red', label='Predicted Sales')
    plt.xlabel('Year')
    plt.ylabel('Sales')
    plt.title('Year-wise Sales Prediction')
    plt.legend()
    st.pyplot(plt)

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

col1, col2, col3 = st.columns([2, 2, 2])

# First column: Sales Prediction, Year-wise Filter, and Data Display
with col1:
    st.subheader("Sales Prediction")
    sales_data = load_sales_data(ticker)
    model, predictions, mse, X_test, y_test = predict_sales(sales_data)
    plot_predictions(model, sales_data)
    
    st.subheader("Year-wise Filter")
    year_filter = st.slider("Select Year", int(sales_data['Year'].min()), int(sales_data['Year'].max()), (int(sales_data['Year'].min()), int(sales_data['Year'].max())))
    filtered_data = sales_data[(sales_data['Year'] >= year_filter[0]) & (sales_data['Year'] <= year_filter[1])]
    st.write(filtered_data)
    
    st.subheader("Sales Data")
    st.dataframe(sales_data, height=200)

# Second column: Selected Company's About and Performance
with col2:
    st.subheader(f"About {company}")
    company_info = fetch_company_info(ticker)
    st.write(company_info)

    st.subheader(f"{company} Performance")
    df_stock = fetch_stock_data(ticker)
    st.dataframe(df_stock.tail(10))

# Third column: Live NEWS and EPS, PE, IPO KPI
news_api_key = "31739ed855eb4759908a898ab99a43e7"
query = company

with col3:
    st.subheader("Live News")
    news_articles = fetch_live_news(news_api_key, query)
    news_text = ""
    for article in news_articles:
        news_text += f"**{article['title']}**\n\n{article['description']}\n\n[Read more]({article['url']})\n\n\n"
    st.text_area("Live News", news_text, height=150)

    st.subheader(f"{company} EPS, PE, IPO KPI")
    eps_pe_ipo_kpi = fetch_eps_pe_ipo_kpi(ticker)
    kpi_info = f"**EPS**: {eps_pe_ipo_kpi['EPS']}  |  **PE Ratio**: {eps_pe_ipo_kpi['PE Ratio']}  |  **IPO Date**: {eps_pe_ipo_kpi['IPO Date']}  |  **KPI**: {eps_pe_ipo_kpi['KPI']}"
    st.write(kpi_info)

st.write("Data fetched successfully! Use this for further analysis and prediction.")
