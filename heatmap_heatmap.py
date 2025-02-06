import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

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

    # Generate a grid layout for the heatmap
    num_companies = df.shape[0]
    num_cols = 5  # Define the number of columns in the "periodic table"
    num_rows = (num_companies // num_cols) + 1

    fig, ax = plt.subplots(figsize=(15, 8))
    heatmap_data = df['Weight'].values.reshape(num_rows, num_cols)

    sns.heatmap(heatmap_data, annot=df.index.values.reshape(num_rows, num_cols),
                fmt='', cmap="YlGnBu", cbar_kws={'label': 'Weightage'}, linewidths=.5, ax=ax)

    ax.set_title('Company Weightage Heatmap')

    # Display heatmap in Streamlit
    st.pyplot(fig)

if __name__ == "__main__":
    main()
