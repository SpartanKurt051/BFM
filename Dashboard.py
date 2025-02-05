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

# Streamlit UI with horizontal split
st.markdown('<div class="horizontal-container">', unsafe_allow_html=True)

# Left division (Blank Container)
st.markdown('<div class="left-box">', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# Right division (Placeholder)
st.markdown('<div class="right-box blue-box">', unsafe_allow_html=True)
st.markdown('<div class="placeholder">ABOUT, PERFORMANCE OF INDEX ( HOLDING ANALYSIS, EQUITY SHARE ALLOCATION, ADVANCED RATIOS ) PIE CHARTS</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)
