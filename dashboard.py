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
    data.set_index('Date', inplace=True)
    
    # Calculate the error percentage for January 24, 2025
    specific_date = pd.Timestamp('2025-01-24')
    if specific_date in data.index:
        actual_price = data.loc[specific_date, 'Actual Price']
        predicted_price = data.loc[specific_date, 'Predicted Price']
        error_percentage = abs((actual_price - predicted_price) / actual_price) * 100
        error_text = f"Error percentage as on January 24, 2025: {error_percentage:.2f}%"
    else:
        error_text = "No data for January 24, 2025"
    
    # Create the figure
    fig = go.Figure()
    
    # Add actual price trace
    fig.add_trace(go.Scatter(x=data.index, y=data['Actual Price'], mode='lines', name='Actual Price', line=dict(color='blue')))
    
    # Add predicted price trace
    fig.add_trace(go.Scatter(x=data.index, y=data['Predicted Price'], mode='lines', name='Predicted Price', line=dict(color='red', dash='dash')))
    
    # Update layout with titles and labels
    fig.update_layout(
        title=f'{company_name} - Actual vs Predicted Opening Prices',
        xaxis_title='Date',
        yaxis_title='Price',
        hovermode='x unified'
    )
    
    # Update hover information
    fig.update_traces(
        hovertemplate='<b>Date</b>: %{x|%d/%m/%Y}<br><b>Actual Price</b>: %{y}<br><b>Predicted Price</b>: %{customdata:.2f}<extra></extra>',
        customdata=data['Predicted Price']
    )
    
    # Use Streamlit to display the plot and error percentage
    st.plotly_chart(fig)
    st.write(error_text)

# Streamlit application
st.title('Company Opening Prices Dashboard')

# Add a dropdown to select a company
selected_company = st.selectbox('Select a company', list(companies.keys()))

if selected_company:
    file_name = companies[selected_company]
    st.header(selected_company)
    plot_actual_vs_predicted(selected_company, file_name)
