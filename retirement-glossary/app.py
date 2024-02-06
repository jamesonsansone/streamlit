import streamlit as st
import requests
import base64
import json
import pprint
from openai import OpenAI

# Streamlit interface for keyword input
st.title("Content generator using Data For SEO API")
keyword = st.text_input("Enter a keyword", "")

# Initialize the OpenAI client with the API key from Streamlit secrets
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# Function to fetch SERP data using DataForSEO API
def fetch_serp_data(keyword):
    login = st.secrets["DATAFORSEO_LOGIN"]
    password = st.secrets["DATAFORSEO_PASSWORD"]
    credentials = f"{login}:{password}"
    encoded_credentials = base64.b64encode(credentials.encode()).decode()

    headers = {
        "Authorization": f"Basic {encoded_credentials}",
        "Content-Type": "application/json"
    }

    task_post_data = json.dumps({
        0: {
            "language_code": "en",
            "location_code": 2840,
            "keyword": keyword,
            "calculate_rectangles": True
        }
    })

    # Corrected API Endpoint
    task_url = "https://api.dataforseo.com/v3/serp/google/organic/live/advanced"
    task_response = requests.post(task_url, headers=headers, data=task_post_data)

    if task_response.status_code == 200:
        task_response_data = task_response.json()
        return task_response_data
    else:
        st.error(f"Error creating task. Code: {task_response.status_code} Message: {task_response.text}")
        return None

# Function to generate content using OpenAI
def generate_content(keyword, serp_data):
    """
    Generate content based on the given keyword.
    """
    # Extract titles and People Also Ask questions
    titles = [item.get('title') for item in serp_data['tasks'][0]['result'][0]['items'] if item.get('type') == 'organic' and item.get('title')][:5]
    paa_questions = [item.get('title') for item in serp_data['tasks'][0]['result'][0]['items'] if item.get('type') == 'people_also_ask' and item.get('title')][:5]

    # Ensure there is data to join
    titles_str = ', '.join(titles) if titles else 'No titles available'
    paa_str = ', '.join(paa_questions) if paa_questions else 'No questions available'

    # Creating a message string with extracted titles and questions
    serp_info = f"Titles: {titles_str}. People Also Ask: {paa_str}."

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": "You are a content generation assistant, expert in creating SEO-optimized articles with a focus on SEO. Your client is a FinTech 401(k) retirement benefit provider needing your help to write content for a new retirement glossary. Articles should be structured, authoritative similar to a glossary set of terms. Use Markdown for formatting, with '#' for main titles and '##' for subtitles. Ensure articles are concise, engaging, and no more than 1500 characters. Do not include conclusion paragraphs."
            },
            {
                "role": "user",
                "content": f"Write an informative and comprehensive article about '{keyword}'. The article should include an introduction to the topic, a detailed breakdown, and incorporate related SEO queries within the text, including {serp_info}. The headlines and subheadings should focus on content semantically related to '{keyword}'. Write content in a way that matches natural language processing. Keep the text between 750 to 1500 characters. Include Markdown-formatted headings. The first heading should be 'What is '{keyword}''."
            }
        ]
    )

    generated_content = response.choices[0].message.content

    return generated_content, serp_info


# Button to trigger the Data for SEO API call, generate content and display results
if st.button("Generate Data For SEO"):
    if not keyword:
        st.warning("Please enter a keyword.")
    else:
        serp_data = fetch_serp_data(keyword)
        if serp_data:
            generated_content, serp_info = generate_content(keyword, serp_data)
            st.subheader("Data Used for Content Generation")
            st.text(serp_info)  # Display the SERP information
            st.subheader("Generated Content")
            st.markdown(generated_content, unsafe_allow_html=True)
