import streamlit as st
import requests
import pdftotext
import pandas as pd
from io import BytesIO

def analyze_pdf(file_content: bytes, keywords: List[str]) -> bool:
    pdf = pdftotext.PDF(BytesIO(file_content))
    text = "\n\n".join(pdf).lower()

    for word in keywords:
        if word.lower() in text:
            return True
    return False

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
    matching_pdfs = []

    for pdf_url in pdf_urls:
        response = requests.get(pdf_url)
        if response.status_code == 200:
            if analyze_pdf(response.content, keywords):
                matching_pdfs.append(pdf_url)

    st.subheader("PDFs containing target keywords:")
    for pdf_url in matching_pdfs:
        st.write(pdf_url)
