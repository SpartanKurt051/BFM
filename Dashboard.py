import streamlit as st
import pandas as pd
import yfinance as yf
import requests
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression, Ridge, Lasso
from sklearn.metrics import mean_squared_error
import plotly.express as px
from sklearn.preprocessing import StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline

st.set_page_config(layout="wide") # Make the content fit the entire screen

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
            debt_to_equity = (balance_sheet.loc["Total Debt"].get(date.strftime("%Y-%m-%d"), None) / balance_sheet.loc["Total Equity"].get(date.strftime("%Y-%m-%d"), None)) if ("Total Debt" in balance_sheet.index and "Total Equity" in balance_sheet.index) else None
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
    hist = hist[hist.index <= '2025-01-25']  # Limit data till 25th January 2025
    hist.reset_index(inplace=True)
    hist['Year'] = hist['Date'].dt.year
    hist['Month'] = hist['Date'].dt.month
    hist['Day'] = hist['Date'].dt.day
    hist['Sales'] = hist['Close']  # Assuming 'Close' prices as 'Sales'
    return hist

# Data cleaning and transformation
def clean_transform_data(data):
    # Handle missing values
    data = data.dropna()

    # Remove duplicates
    data = data.drop_duplicates()

    # Correct data types
    data['Year'] = data['Year'].astype(int)
    data['Month'] = data['Month'].astype(int)
    data['Day'] = data['Day'].astype(int)
    data['Sales'] = data['Sales'].astype(float)

    # Normalize numerical features
    numerical_features = data.columns.difference(['Date'])
    numerical_transformer = StandardScaler()

    # Combine transformations
    preprocessor = ColumnTransformer(
        transformers=[
            ('num', numerical_transformer, numerical_features)
        ])

    return preprocessor.fit_transform(data)

# Improved prediction model using ensemble methods
def predict_sales(data):
    data = clean_transform_data(data)
    X = data[:, :-1]  # All columns except the last one
    y = data[:, -1]  # Last column is the target

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Trying different models
    models = {
        'Linear Regression': LinearRegression(),
        'Ridge Regression': Ridge(alpha=1.0),
        'Lasso Regression': Lasso(alpha=0.1)
    }
    
    best_model = None
    best_mse = float('inf')
    
    for name, model in models.items():
        model.fit(X_train, y_train)
        predictions = model.predict(X_test)
        mse = mean_squared_error(y_test, predictions)
        if mse < best_mse:
            best_mse = mse
            best_model = model
    
    # Predict sales for 26th January 2025
    next_day = pd.DataFrame({
        'Year': [2025],
        'Month': [1],
        'Day': [26],
        'Sales': [0]  # Placeholder value for Sales
    })
    next_day = clean_transform_data(next_day)
    next_day_sales = best_model.predict(next_day)[0]
    
    return best_model, best_mse, next_day_sales

# Plot sales predictions
def plot_predictions(model, data, year):
    data_filtered = data[data['Year'] == year]
    fig = px.line(data_filtered, x='Date', y='Sales', title=f'Daily Sales Prediction for {year}')
    fig.add_scatter(x=data_filtered['Date'], y=model.predict(data_filtered[data_filtered.columns.difference(['Date', 'Sales'])]), mode='lines', name='Predicted Sales')
    fig.update_layout(hovermode='x unified')
    st.plotly_chart(fig)

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

col1, col2, col3 = st.columns([3, 1.5, 1.5])

# First column: Sales Prediction, Year-wise Filter, and Data Display
with col1:
    st.subheader("Sales Prediction")
    sales_data = load_sales_data(ticker)
    model, mse, next_day_sales = predict_sales(sales_data)
    st.write(f"Predicted Sales for 26th Jan 2025: {next_day_sales}")
    
    st.subheader("Year-wise Filter")
    year_filter = st.selectbox("Select Year", [2020, 2021, 2022, 2023, 2024, 2025])
    plot_predictions(model, sales_data, year_filter)
    
    st.subheader("Sales Data")
    filtered_data = sales_data[sales_data['Year'] == year_filter]
    st.dataframe(filtered_data, height=200)

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
