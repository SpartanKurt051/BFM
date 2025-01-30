import streamlit as st
st.write("Hello World")


import streamlit as st
import pandas as pd

st.title('Reliance Industries Stock Data')
df = pd.read_csv('reliance_stock_data.csv')
st.dataframe(df)
