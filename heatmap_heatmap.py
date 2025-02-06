import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

st.set_page_config(layout="wide")

def main():
    st.title("Heatmap Dashboard")

    # Load data
    data_url = "https://raw.githubusercontent.com/SpartanKurt051/BFM/main/Heatmap.csv"
    df = pd.read_csv(data_url)

    # Create heatmap
    fig, ax = plt.subplots()
    sns.heatmap(df.set_index('Company').T, annot=True, ax=ax, cmap="YlGnBu")
    ax.set_title('Company Weights Heatmap')

    # Display heatmap in Streamlit
    st.pyplot(fig)

if __name__ == "__main__":
    main()
