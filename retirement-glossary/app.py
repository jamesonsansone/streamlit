import streamlit as st
from openai import OpenAI

# Initialize the OpenAI client with the API key from Streamlit secrets
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

def generate_content(keyword):
    """
    Generate content based on the given keyword.
    """
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": "You are a content generation assistant, expert in creating SEO-optimized articles with a focus on SEO. Your client is a FinTech 401(k) retirement benefit provider needing your help to write content for a new retirement glossary. Articles should be structured, authoritative similar to a glossary set of terms. Use Markdown for formatting, with '#' for main titles and '##' for subtitles. Ensure articles are concise, engaging, and no more than 1500 characters. Do not include conclusion paragraphs."
            },
            {
                "role": "user",
                "content": f"Write an informative and comprehensive article about '{keyword}'. The article should include an introduction to the topic, a detailed breakdown, and incorporate related SEO queries within the text. The headlines and subheadings should focus on content semantically related to '{keyword}'. Write content in a way that matches natural language processing. Keep the text between 750 to 1500 characters. Include Markdown-formatted headings. The first heading should be 'What is '{keyword}''"
            }
        ]
    )
    return response.choices[0].message.content

# Streamlit interface
st.title("Retirement Glossary Generator")

# User input for keyword
keyword = st.text_input("Enter a Keyword", "")

# Button to generate content
if st.button("Generate Content"):
    with st.spinner("Generating content..."):
        generated_content = generate_content(keyword)
        st.markdown(generated_content, unsafe_allow_html=True)
