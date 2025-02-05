import streamlit as st
import pandas as pd
import yfinance as yf
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
#Create a ticker-dropdown

# Load CSS file
import streamlit as st

# Load CSS file
def load_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Load CSS
load_css("styles.css")

# Streamlit UI with a big box covering the entire page
st.markdown('<div class="big-box">', unsafe_allow_html=True)
st.markdown('Big Box Content', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)
