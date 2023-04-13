import streamlit as st
import pandas as pd
import re
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
        # Initialize


st.title("Keyword Rankings Comparison")

featured_file = st.file_uploader("Upload a CSV file for Featured Domain:", type=['csv'])
comp1_file = st.file_uploader("Upload a CSV file for Competitor 1 Domain:", type=['csv'])
comp2_file = st.file_uploader("Upload a CSV file for Competitor 2 Domain:", type=['csv'])
comp3_file = st.file_uploader("Upload a CSV file for Competitor 3 Domain:", type=['csv'])
comp4_file = st.file_uploader("Upload a CSV file for Competitor 4 Domain:", type=['csv'])

if st.button("Compare Rankings"):
    featured_df = process_csv(featured_file, 'Featured Domain')
    comp1_df = process_csv(comp1_file, 'Competitor 1')
    comp2_df = process_csv(comp2_file, 'Competitor 2')
    comp3_df = process_csv(comp3_file, 'Competitor 3')
    comp4_df = process_csv(comp4_file, 'Competitor 4')

    if featured_df is not None and comp1_df is not None and comp2_df is not None and comp3_df is not None and comp4_df is not None:
        combined_df = pd.concat([featured_df, comp1_df, comp2_df, comp3_df, comp4_df], axis=0)
        combined_df = combined_df.groupby(['Keyword', 'Volume', 'Domain']).agg(Avg_Current_Position=('Featured Domain', 'mean')).reset_index()
        pivot_df = combined_df.pivot_table(index=['Keyword', 'Volume'], columns='Domain', values='Avg_Current_Position').reset_index()

        st.write(pivot_df)
    else:
        st.write("Please upload all required CSV files.")
