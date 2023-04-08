import streamlit as st
import requests
import fitz  # PyMuPDF
import pandas as pd
from io import BytesIO
from typing import List

def analyze_pdf(file_content: bytes, keywords: List[str]) -> dict:
    with BytesIO(file_content) as f:
        doc = fitz.open(stream=f)
        text = "\n\n".join(page.get_text("text").lower() for page in doc)

    keyword_counts = {}
    for word in keywords:
        count = text.lower().count(word.lower())
        keyword_counts[word] = count

    return keyword_counts

st.title('PDF Keyword Scanner')

uploaded_file = st.file_uploader("Upload a CSV file with PDF URLs", type="csv")

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    pdf_urls = df['pdf_url'].tolist()

keywords_input = st.text_input(
    label="Enter comma-separated keywords",
    value="example, keyword"
)

if keywords_input:
    keywords = [k.strip() for k in keywords_input.split(',')]

if uploaded_file and keywords_input:
    for keyword in keywords:
        df[keyword] = 0

    for idx, pdf_url in enumerate(pdf_urls):
        response = requests.get(pdf_url)
        if response.status_code == 200:
            keyword_counts = analyze_pdf(response.content, keywords)
            for keyword, count in keyword_counts.items():
                df.at[idx, keyword] = count

    st.subheader("PDFs with target keyword counts:")
    st.write(df)
