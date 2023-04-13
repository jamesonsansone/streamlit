import streamlit as st
import pandas as pd
import re
import tldextract
from urllib.parse import urlparse

# Function to extract domain from URL
def extract_domain(url):
    if not url or not isinstance(url, str):
        return None
    parsed_uri = urlparse(url)
    domain = tldextract.extract(parsed_uri.netloc).domain
    return domain

# Function to process input CSVs
def process_csv(uploaded_file, domain_col_name):
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        df = df[['Keyword', 'Volume', 'KD', 'Current position', 'Current URL']]
        df['Domain'] = df['Current URL'].apply(extract_domain)
        df = df.rename(columns={'Current position': domain_col_name})
        return df
    else:
        return None

st.title("Keyword Rankings Comparison")

featured_file = st.file_uploader("Upload a CSV file for Featured Domain:", type=['csv'])

# Use a list to store competitor file uploaders
competitor_files = []
for i in range(1, 5):  # Change the range to add more competitors
    competitor_file = st.file_uploader(f"Upload a CSV file for Competitor {i} Domain:", type=['csv'])
    competitor_files.append(competitor_file)

if st.button("Compare Rankings"):
    featured_df = process_csv(featured_file, 'Featured Domain')
    
    if featured_df is not None:
        # Initialize the combined_df with featured_df
        combined_df = featured_df

        # Process and concatenate each competitor file
        for i, comp_file in enumerate(competitor_files, start=1):
            comp_df = process_csv(comp_file, f'Competitor {i}')
            
            if comp_df is not None:
                combined_df = pd.concat([combined_df, comp_df], axis=0)

        combined_df = combined_df.groupby(['Keyword', 'Volume', 'Domain']).agg(Avg_Current_Position=('Featured Domain', 'mean')).reset_index()
        pivot_df = combined_df.pivot_table(index=['Keyword', 'Volume'], columns='Domain', values='Avg_Current_Position').reset_index()

        st.write(pivot_df)
    else:
        st.write("Please upload the required CSV file for Featured Domain.")
