import yfinance as yf
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout
import numpy as np

# Define the companies and their tickers
companies = {
    "Adani Energy": "ADANIGREEN.NS",
    "Tata Power": "TATAPOWER.NS",
    "Jsw Energy": "JSWENERGY.NS",
    "NTPC": "NTPC.NS",
    "Power Grid Corp": "POWERGRID.NS",
    "NHPC": "NHPC.NS"
}

# Fetch and save opening price data
def fetch_and_save_opening_price_data(ticker, company_name):
    stock = yf.Ticker(ticker)
    hist = stock.history(start="2020-01-01", end="2025-01-26")
    hist.reset_index(inplace=True)
    hist['Opening Price'] = hist['Open']
    hist = hist[['Date', 'Opening Price']]
    hist.to_csv(f'{company_name}_opening_price_data.csv', index=False)

# Normalize Data
def normalize_data(data):
    scaler = MinMaxScaler(feature_range=(0, 1))
    data_scaled = scaler.fit_transform(data[['Opening Price']])
    return data_scaled, scaler

# Create Sequences for LSTM
def create_sequences(data, seq_length=60):
    X, y = [], []
    for i in range(len(data) - seq_length):
        X.append(data[i:i + seq_length])
        y.append(data[i + seq_length])
    return np.array(X), np.array(y)

# Build and Train LSTM Model
def build_and_train_lstm_model(X_train, y_train, X_test, y_test):
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
    return model

# Make Predictions
def make_predictions(model, X_test, scaler):
    predictions = model.predict(X_test)
    predictions = scaler.inverse_transform(predictions)
    return predictions

# Add predicted prices to CSV
def add_predicted_prices_to_csv(company_name):
    data = pd.read_csv(f'{company_name}_opening_price_data.csv')
    data_scaled, scaler = normalize_data(data)
    train_size = int(len(data_scaled) * 0.8)
    train_data, test_data = data_scaled[:train_size], data_scaled[train_size:]
    X_train, y_train = create_sequences(train_data)
    X_test, y_test = create_sequences(test_data)
    
    model = build_and_train_lstm_model(X_train, y_train, X_test, y_test)
    predictions = make_predictions(model, X_test, scaler)
    
    data['Predicted Price'] = np.nan
    data.loc[len(data) - len(predictions):, 'Predicted Price'] = predictions.flatten()
    data.to_csv(f'{company_name}_opening_price_data_with_predictions.csv', index=False)

# Process each company
for company_name, ticker in companies.items():
    fetch_and_save_opening_price_data(ticker, company_name)
    add_predicted_prices_to_csv(company_name)

# Note: Use Git commands to commit and push the files to the GitHub repository.
