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

# Create separate file uploaders for the featured domain and competitor domains.
featured_file = st.file_uploader("Upload a CSV file for Featured Domain:", type=['csv'])
comp_files = [st.file_uploader(f"Upload a CSV file for Competitor {i + 1} Domain:", type=['csv']) for i in range(4)]

# When the "Compare Rankings" button is clicked, process the uploaded files and generate the comparison table.
if st.button("Compare Rankings"):
    # Process the featured domain file and competitor domain files
    featured_df = process_csv(featured_file)
    comp_dfs = [process_csv(comp_file) for comp_file in comp_files if comp_file is not None]

    if featured_df is not None and len(comp_dfs) > 0:
        # Combine the featured domain DataFrame and competitor domain DataFrames.
        all_dfs = [featured_df] + comp_dfs
        combined_df = pd.concat(all_dfs, axis=0)

        # Calculate the average current position for each keyword, volume, and domain combination.
        combined_df = combined_df.groupby(['Keyword', 'Volume', 'Domain']).agg(Avg_Current_Position=('Current position', 'mean')).reset_index()

        # Pivot the DataFrame to display the average current position for each domain in separate columns.
        pivot_df = combined_df.pivot_table(index=['Keyword', 'Volume'], columns='Domain', values='Avg_Current_Position').reset_index()

        # Rename the pivot table columns to include the domain names.
        pivot_df.columns = ['Keyword', 'Volume'] + [col for col in pivot_df.columns if isinstance(col, str) and col != 'Keyword' and col != 'Volume']

        # Create a list of domain column names for the resulting DataFrame.
        domain_columns = [df['Domain'].iloc[0] for df in all_dfs]

        # Calculate the number of ranking domains for each keyword and volume with a value <50.
        pivot_df['# of Ranking Domains <50'] = pivot_df.iloc[:, 2:].apply(lambda x: (x < 50).sum(), axis=1)

        # Calculate the lowest ranking position for each keyword and volume.
        pivot_df['Lowest Ranking Position'] = pivot_df.iloc[:, 2:len(domain_columns) + 2].min(axis=1)

        # Determine if the featured domain has the lowest rank for each keyword and volume.
        featured_domain = domain_columns[0]
        pivot_df['Is the Featured Domain the lowest ranking keyword'] = pivot_df.apply(lambda x: x[featured_domain] == x['Lowest Ranking Position'], axis=1)
                 
        # Display the resulting pivot table.
        st.write(pivot_df)

        # Allow the user to export the pivot table as a CSV file.
        if st.button("Export to CSV"):
            pivot_df.to_csv("keyword_rankings_comparison.csv", index=False)
            st.markdown("[Download CSV](keyword_rankings_comparison.csv)")

        # Display the keywords and volumes where the featured domain is not the lowest-ranking.
        not_lowest_df = pivot_df[pivot_df['Is the Featured Domain the lowest ranking keyword'] == False].sort_values(by='Volume', ascending=False)
        st.subheader("Featured Domain not Lowest")
        st.write(not_lowest_df)

    else:
        st.write("Please upload the required CSV files.")
