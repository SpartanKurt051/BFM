import pandas as pd
import streamlit as st
import plotly.express as px

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
    
    # Plot the actual and predicted opening prices
    fig = px.line(data, x='Date', y=['Actual Price', 'Predicted Price'],
                  labels={'value': 'Price', 'variable': 'Type'},
                  title=f'{company_name} - Actual vs Predicted Opening Prices')
    
    # Use Streamlit to display the plot
    st.plotly_chart(fig)

# Streamlit application
st.title('Company Opening Prices Dashboard')

# Add a dropdown to select a company
selected_company = st.selectbox('Select a company', list(companies.keys()))

if selected_company:
    file_name = companies[selected_company]
    st.header(selected_company)
    plot_actual_vs_predicted(selected_company, file_name)
