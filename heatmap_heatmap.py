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

    # Strip any leading/trailing spaces from column names
    df.columns = df.columns.str.strip()

    # Create a pivot table for heatmap
    df_pivot = df.pivot_table(index='Company', values='Weight')

    # Create heatmap
    fig, ax = plt.subplots(figsize=(10, 8))
    sns.heatmap(df_pivot, annot=True, ax=ax, cmap="YlGnBu", cbar_kws={'label': 'Weightage'})
    ax.set_title('Company Weightage Heatmap')

    # Display heatmap in Streamlit
    st.pyplot(fig)

if __name__ == "__main__":
    main()
