import streamlit as st
import pandas as pd
import yfinance as yf
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_absolute_error, mean_squared_error
import plotly.graph_objects as go
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout

st.set_page_config(layout="wide") # Make the content fit the entire screen

def load_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Load CSS
load_css("styles.css")

def fetch_stock_data(ticker):
    df = yf.download(ticker, start="2020-01-01", end="2025-01-25")
    return df

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

def create_sequences(data, seq_length=60):
    X, y = [], []
    for i in range(len(data) - seq_length):
        X.append(data[i:i + seq_length])
        y.append(data[i + seq_length])
    return np.array(X), np.array(y)

def train_lstm_model(data):
    scaler = MinMaxScaler(feature_range=(0, 1))
    data_scaled = scaler.fit_transform(data[['Sales']])

    train_size = int(len(data_scaled) * 0.8)
    train_data, test_data = data_scaled[:train_size], data_scaled[train_size:]

    X_train, y_train = create_sequences(train_data)
    X_test, y_test = create_sequences(test_data)

    X_train = X_train.reshape((X_train.shape[0], X_train.shape[1], 1))
    X_test = X_test.reshape((X_test.shape[0], X_test.shape[1], 1))

    model = Sequential([
        LSTM(50, return_sequences=True, input_shape=(X_train.shape[1], 1)),
        Dropout(0.2),
        LSTM(50, return_sequences=False),
        Dropout(0.2),
        Dense(25),
        Dense(1)
    ])

    model.compile(optimizer="adam", loss="mean_squared_error")
    model.fit(X_train, y_train, epochs=20, batch_size=32, validation_data=(X_test, y_test))

    return model, scaler, X_test, y_test

def plot_predictions(actual_prices, predictions):
    fig_pred = go.Figure()
    fig_pred.add_trace(go.Scatter(y=actual_prices.flatten(), mode="lines", name="Actual Price"))
    fig_pred.add_trace(go.Scatter(y=predictions.flatten(), mode="lines", name="Predicted Price", line=dict(color="red")))
    fig_pred.update_layout(title="Stock Price Prediction", xaxis_title="Days", yaxis_title="Price (₹)", template="plotly_dark")
    st.plotly_chart(fig_pred)

def main():
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

    with col1:
        st.subheader("Sales Prediction")
        sales_data = load_sales_data(ticker)
        model, scaler, X_test, y_test = train_lstm_model(sales_data)

        predictions = model.predict(X_test)
        predictions = scaler.inverse_transform(predictions)
        actual_prices = scaler.inverse_transform(y_test.reshape(-1, 1))

        plot_predictions(actual_prices, predictions)

        mae = mean_absolute_error(actual_prices, predictions)
        rmse = np.sqrt(mean_squared_error(actual_prices, predictions))
        error_percentage = (mae / np.mean(actual_prices)) * 100

        st.subheader("Prediction Error Metrics")
        st.write(f"*Mean Absolute Error (MAE):* {mae:.2f}")
        st.write(f"*Root Mean Squared Error (RMSE):* {rmse:.2f}")
        st.write(f"*Error Percentage:* {error_percentage:.2f}%")

if __name__ == "__main__":
    main()
