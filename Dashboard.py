import streamlit as st
import pandas as pd
import yfinance as yf
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
#Create a ticker-dropdown

import streamlit as st
import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt

# Load CSS file
def load_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Load CSS
load_css("styles.css")

# Streamlit UI with two graphs side by side
st.markdown('<div class="container_primary">', unsafe_allow_html=True)

# Left graph
col1, col2 = st.columns(2)

with col1:
    st.markdown('<div class="left-box">', unsafe_allow_html=True)
    # Placeholder data for the left graph
    data_left = pd.Series([1, 3, 2, 4, 5])
    fig_left, ax_left = plt.subplots()
    ax_left.plot(data_left)
    st.pyplot(fig_left)
    st.markdown('</div>', unsafe_allow_html=True)

# Right graph
with col2:
    st.markdown('<div class="right-box">', unsafe_allow_html=True)
    # Placeholder data for the right graph
    data_right = pd.Series([5, 4, 3, 2, 1])
    fig_right, ax_right = plt.subplots()
    ax_right.plot(data_right)
    st.pyplot(fig_right)
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)
