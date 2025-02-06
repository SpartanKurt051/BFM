import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

st.set_page_config(layout="wide")

def main():
    st.title("Company Weightage Heatmap")

    # Load data
    data_url = "https://raw.githubusercontent.com/SpartanKurt051/BFM/main/Heatmap.csv"
    df = pd.read_csv(data_url)

    # Strip any leading/trailing spaces from column names
    df.columns = df.columns.str.strip()

    # Set the 'Company' column as index
    df.set_index('Company', inplace=True)

    # Create heatmap
    fig, ax = plt.subplots(figsize=(10, 8))
    sns.heatmap(df, annot=True, cmap="YlGnBu", ax=ax)
    ax.set_title('Company Weightage Heatmap')

    # Display heatmap in Streamlit
    st.pyplot(fig)

if __name__ == "__main__":
    main()
