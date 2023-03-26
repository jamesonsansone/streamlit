import os
import pandas as pd
import openai
import streamlit as st

# Function to generate description using OpenAI API
def generate_description(keyword):
    openai.api_key = os.getenv("OPENAI_API_KEY")
    prompt = f"Write a short, NLP-friendly description of the keyword: {keyword}"

    response = openai.Completion.create(
        engine="davinci-codex",
        prompt=prompt,
        max_tokens=50,
        n=1,
        stop=None,
        temperature=0.7,
    )

    description = response.choices[0].text.strip()
    return description

st.title("Featured Snippet Optimization Tool")

# Input field for OpenAI API key
api_key = st.text_input("Enter your OpenAI API key:")
if api_key:
    os.environ["OPENAI_API_KEY"] = api_key

uploaded_file = st.file_uploader("Upload a CSV file containing keywords:", type=['csv'])

if uploaded_file is not None and api_key:
    keywords_df = pd.read_csv(uploaded_file)

    if st.button("Generate Descriptions"):
        st.write("Generating NLP-friendly descriptions for your keywords...")

        descriptions = []

        for keyword in keywords_df['Keyword']:
            description = generate_description(keyword)
            descriptions.append(description)

        keywords_df['description'] = descriptions

        st.write(keywords_df)

        st.download_button(
            label="Download CSV with Descriptions",
            data=keywords_df.to_csv(index=False).encode('utf-8'),
            file_name="keywords_with_descriptions.csv",
            mime="text/csv",
        )
