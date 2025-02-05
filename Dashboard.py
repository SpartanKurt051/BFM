# Load closing price data for prediction
def load_closing_price_data(ticker):
    stock = yf.Ticker(ticker)
    hist = stock.history(period="max")
    hist = hist[hist.index <= '2025-01-25']  # Limit data till 25th January 2025
    hist.reset_index(inplace=True)
    hist['Year'] = hist['Date'].dt.year
    hist['Month'] = hist['Date'].dt.month
    hist['Day'] = hist['Date'].dt.day
    hist['Closing Price'] = hist['Close']  # Assuming 'Close' prices as 'Closing Price'
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
    data['Closing Price'] = data['Closing Price'].astype(float)

    # Normalize numerical features
    numerical_features = ['Year', 'Month', 'Day', 'Closing Price']
    numerical_transformer = StandardScaler()

    # Combine transformations
    preprocessor = ColumnTransformer(
        transformers=[
            ('num', numerical_transformer, numerical_features)
        ])

    return preprocessor.fit_transform(data)

# Improved prediction model using ensemble methods
def predict_closing_prices(data):
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
    
    return best_model, best_mse

# Plot closing price predictions
def plot_predictions(model, data, year):
    data_filtered = data[data['Year'] == year]
    fig = px.line(data_filtered, x='Date', y='Closing Price', title=f'Daily Closing Price Prediction for {year}')
    fig.add_scatter(x=data_filtered['Date'], y=model.predict(data_filtered[['Year', 'Month', 'Day']]), mode='lines', name='Predicted Closing Price')
    fig.update_layout(hovermode='x unified')
    st.plotly_chart(fig)

# First column: Closing Price Prediction, Year-wise Filter, and Data Display
with col1:
    st.subheader("Closing Price Prediction")
    closing_price_data = load_closing_price_data(ticker)
    model, mse = predict_closing_prices(closing_price_data)
    
    st.subheader("Year-wise Filter")
    year_filter = st.selectbox("Select Year", [2020, 2021, 2022, 2023, 2024, 2025])
    plot_predictions(model, closing_price_data, year_filter)
    
    st.subheader("Closing Price Data")
    filtered_data = closing_price_data[closing_price_data['Year'] == year_filter]
    st.dataframe(filtered_data, height=200)
