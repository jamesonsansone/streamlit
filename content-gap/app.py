import streamlit as st
import pandas as pd
import tldextract
from urllib.parse import urlparse

# This function takes a URL string as input and extracts the domain from it.
def extract_domain(url):
    if not url or not isinstance(url, str):
        return None
    parsed_uri = urlparse(url)
    domain = tldextract.extract(parsed_uri.netloc).domain
    return domain

# This function processes the uploaded CSV file by extracting domains and adding a new 'Domain' column.
def process_csv(uploaded_file):
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        df['Domain'] = df['Current URL'].apply(extract_domain)
        return df
    else:
        return None

# Set the title of the Streamlit app.
st.title("Keyword Rankings Comparison")

# Create file uploaders for the featured domain and competitor domains.
file_uploaders = [st.file_uploader(f"Upload a CSV file for Domain {i + 1}:", type=['csv']) for i in range(5)]

# When the "Compare Rankings" button is clicked, process the uploaded files and generate the comparison table.
if st.button("Compare Rankings"):
    # Process the uploaded files and filter out any None values
    dfs = [process_csv(file) for file in file_uploaders if file is not None]

    if len(dfs) > 0:
        # Combine all DataFrames into one DataFrame
        combined_df = pd.concat(dfs, axis=0)

        # Calculate the average current position for each keyword, volume, and domain combination.
        combined_df = combined_df.groupby(['Keyword', 'Volume', 'Domain']).agg(Avg_Current_Position=('Current position', 'mean')).reset_index()
        
        # Pivot the DataFrame to display the average current position for each domain in separate columns.
        pivot_df = combined_df.pivot_table(index=['Keyword', 'Volume'], columns='Domain', values='Avg_Current_Position').reset_index()

        # Rename the pivot table columns to include the domain names.
        pivot_df.columns = ['Keyword', 'Volume'] + [col for col in pivot_df.columns if isinstance(col, str) and col != 'Keyword' and col != 'Volume']

        # Display the resulting pivot table.
        st.write(pivot_df)

        # Allow the user to export the pivot table as a CSV file.
        if st.button("Export to CSV"):
            pivot_df.to_csv("keyword_rankings_comparison.csv", index=False)
            st.markdown("[Download CSV](keyword_rankings_comparison.csv)")
    else:
        st.write("Please upload the required CSV files.")
