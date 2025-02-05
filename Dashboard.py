import streamlit as st
import pandas as pd
import yfinance as yf
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
#Create a ticker-dropdown


# Load CSS file
def load_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Load CSS
load_css("styles.css")

# Streamlit UI with two vertical parts

# Left division
st.markdown('<span class="left-box">Left Box Content</span>', unsafe_allow_html=True)

# Right division
st.markdown('<span class="right-box">Right Box Content</span>', unsafe_allow_html=True)


