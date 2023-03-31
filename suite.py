import os
import pandas as pd
import openai
import streamlit as st



st.title("Featured Snippet Optimization Tool")

uploaded_file = st.file_uploader("Upload a CSV file containing keywords:", type=['csv'])

if uploaded_file is not None:
    keywords_df = pd.read_csv(uploaded_file)
   
   if st.button("Generate Descriptions"):
        st.write("Generating NLP-friendly descriptions for your keywords...")
        
        #function to clean up CSV
        columns_to_keep = ["Keyword", "Volume", "Current URL"]
        df_new = keywords_df[columns_to_keep]
        # Removed st.write(keywords_df) to stop displaying the results in a table

        st.download_button(
            label="Download CSV with Descriptions",
            data=df_new.to_csv(index=False).encode('utf-8'),
            file_name="keywords_with_two.csv",
            mime="text/csv",
        )
