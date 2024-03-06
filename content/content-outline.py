import streamlit as st
import requests
import base64
import json
from openai import OpenAI

# Streamlit interface for keyword, credentials, and description input
st.title("Content Generator using Data For SEO API")
keyword = st.text_input("Enter a keyword", "")
description = st.text_area("Enter a description for the article", "")

# Inputs for user credentials
dataforseo_login = st.text_input("Enter your DataForSEO Login", "")
dataforseo_password = st.text_input("Enter your DataForSEO Password", "", type="password")
openai_api_key = st.text_input("Enter your OpenAI API Key", "", type="password")

# Modified function to generate content using OpenAI with added description parameter
def generate_content(keyword, serp_data, api_key, description):
    client = OpenAI(api_key=api_key)

    # Initialize lists
    titles = []
    paa_questions = []

    # Extract titles and People Also Ask questions
    items = serp_data['tasks'][0]['result'][0]['items']
    for item in items:
        if item.get('type') == 'organic':
            title = item.get('title')
            if title:
                titles.append(title)
        elif item.get('type') == 'people_also_ask':
            for paa_item in item.get('items', []):
                question = paa_item.get('title')
                if question:
                    paa_questions.append(question)

    # Limit to first 5 elements
    titles = titles[:5]
    paa_questions = paa_questions[:5]

    # Creating a message string with extracted titles and questions
    titles_str = ", ".join(titles) if titles else "No titles available"
    paa_str = ", ".join(paa_questions) if paa_questions else "No questions available"

    # Include the 'description' in the system message
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": f"Create an informative and comprehensive article about '{keyword}'. Begin with an introduction that provides a clear overview of the topic based on this goal of the outline: {description}. Weave in SEO keywords identified in the titles if you think they make sense to the overarching topic: {titles_str}. Include answers to the '{paa_str}' at the bottom of the article. Use complete sentences with bulleted thoughts for the body of the article."
            }
        ],
    max_tokens=3500
    )

    generated_content = response.choices[0].message.content

    return generated_content, titles, paa_questions

# Button to trigger the Data for SEO API call, generate content, and display results
if st.button("Generate Data For SEO"):
    if not keyword or not dataforseo_login or not dataforseo_password or not openai_api_key or not description:
        st.warning("Please enter all required information.")
    else:
        serp_data = fetch_serp_data(keyword, dataforseo_login, dataforseo_password)
        if serp_data:
            generated_content, titles, paa_questions = generate_content(keyword, serp_data, openai_api_key, description)
            
            st.subheader("Data Used for Content Generation")
            st.write("### Title Tags:")
            for title in titles:
                st.text(title)
            
            st.write("### People Also Ask Questions:")
            for question in paa_questions:
                st.text(question)

            st.subheader("Generated Content")
            st.markdown(generated_content, unsafe_allow_html=True)
