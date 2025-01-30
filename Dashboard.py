import streamlit as st
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
st.write("Hello World")


import streamlit as st
import pandas as pd

st.title('Reliance Industries Stock Data')
df = pd.read_csv('reliance_stock_data.csv')
st.dataframe(df)


