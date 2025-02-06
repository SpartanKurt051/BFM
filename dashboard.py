import pandas as pd
import streamlit as st
import plotly.graph_objects as go

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
    
    # Create the figure
    fig = go.Figure()
    
    # Add actual price trace
    fig.add_trace(go.Scatter(x=data['Date'], y=data['Actual Price'], mode='lines', name='Actual Price', line=dict(color='blue')))
    
    # Add predicted price trace
    fig.add_trace(go.Scatter(x=data['Date'], y=data['Predicted Price'], mode='lines', name='Predicted Price', line=dict(color='red', dash='dash')))
    
    # Update layout with titles and labels
    fig.update_layout(
        title=f'{company_name} - Actual vs Predicted Opening Prices',
        xaxis_title='Date',
        yaxis_title='Price',
        hovermode='x unified'
    )
    
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
