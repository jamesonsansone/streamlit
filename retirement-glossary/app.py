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
                "content": "You are an advanced content generation assistant specialized in creating structured, SEO-optimized articles. Your responses should be formal, authoritative, and informative. Each response should be well-organized with a clear introduction, followed by logically structured sections with headings and subheadings focused on the main keyword. Include relevant keywords and related SEO queries naturally throughout the text. Ensure the content is suitable for a broad audience seeking information online. Generate an article with Markdown formatted headings. Use '#' for main titles (h1) and '##' for subtitles (h2)."
            },
            {
                "role": "user",
                "content": f"Write an informative and comprehensive article about '{keyword}'. The article should include an introduction to the topic, a detailed breakdown, and incorporate related SEO queries within the text. The headlines and subheadings should focus on the main keyword. Keep the text between 750 to 1500 characters. Include Markdown-formatted headings."
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
