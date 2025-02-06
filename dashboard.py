import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

# Define the companies and their CSV file names
companies = {
    "Adani Energy": "Adani Energy_opening_price_data_with_predictions.csv",
    "Tata Power": "Tata Power_opening_price_data_with_predictions.csv",
    "Jsw Energy": "Jsw Energy_opening_price_data_with_predictions.csv",
    "NTPC": "NTPC_opening_price_data_with_predictions.csv",
    "Power Grid Corp": "Power Grid Corp_opening_price_data_with_predictions.csv",
    "NHPC": "NHPC_opening_price_data_with_predictions.csv"
}

def plot_actual_vs_predicted(company_name, file_name):
    # Load the data
    data = pd.read_csv(file_name)
    
    # Set the date as the index for plotting
    data['Date'] = pd.to_datetime(data['Date']).dt.tz_localize(None)
    data.set_index('Date', inplace=True)
    
    # Plot the actual and predicted opening prices
    plt.figure(figsize=(14, 7))
    plt.plot(data['Actual Price'], label='Actual Price')
    plt.plot(data['Predicted Price'], label='Predicted Price', linestyle='--')
    plt.title(f'{company_name} - Actual vs Predicted Opening Prices')
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.legend()
    plt.grid(True)
    
    # Use Streamlit to display the plot
    st.pyplot(plt)

# Streamlit application
st.title('Company Opening Prices Dashboard')

# Plot graphs for all companies
for company_name, file_name in companies.items():
    st.header(company_name)
    plot_actual_vs_predicted(company_name, file_name)
