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
    try:
        task_response = requests.post(task_url, headers=headers, data=task_post_data)
        if task_response.status_code == 200:
            task_response_data = task_response.json()
            print("API Response:", task_response_data)  # Consider logging this instead of printing in production
            return task_response_data
        else:
            st.error(f"Error creating task. Code: {task_response.status_code} Message: {task_response.text}")
            return None
    except requests.exceptions.RequestException as e:
        st.error("Failed to connect to DataForSEO API. Please try again later.")
        print(e)  # For debugging purposes; consider logging this in production
        return None
 
# Function to generate content using OpenAI
def generate_content(keyword, serp_data):
    """
    Generate content based on the given keyword.
    """
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
    serp_info = f"Titles: {titles_str}. People Also Ask: {paa_str}."

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": """You are a content generation assistant, expert in creating SEO-optimized article outlines with a focus on ranking in search results. Create a comprehensive blog post outline for a blog article titled '{keyword}', using a 2-level heading structure. Include a Frequently Asked questions section at the end of the article which answers the '{paa_str}' questions in paragraph form in an NLP-friendly way. Imagine you are Rand Fishkin writing an SEO content outline. Approach your content with these key elements:

1. **Accessible and Clear:** "Simplify complex 401(k) concepts. Break down financial terms into easy-to-understand language, making retirement planning accessible to all."
2. **Encouraging and Supportive:** "Motivate readers to take charge of their retirement planning with positive reinforcement and supportive guidance. Highlight success stories and easy wins."
3. **Friendly Expertise:** "Leverage your deep SEO and FinTech knowledge to guide readers like a trusted friend would, using layman’s terms and avoiding industry jargon."
4. **Informative and Reassuring:** "Provide thorough insights into retirement planning, reassuring readers with data-driven advice and answering common concerns with clarity."
5. **Solution-oriented:** "Focus on practical solutions to the readers' 401(k) queries. Offer step-by-step guides and actionable tips to navigate retirement planning challenges."
6. **Educational:** "Educate with intent. Use each article to build on the reader's knowledge, covering foundational concepts to advanced strategies in a structured format."
Use Markdown for formatting, with '#' for main titles and '##' for subtitles. Do not include conclusion paragraphs.  
"""
            },
            {
                "role": "user",
                "content": f"Create an informative and comprehensive article about '{keyword}'. Begin with an introduction that provides a clear overview of the topic. Weave in SEO keywords identified in the titles if you think they make sense to the overarching topic: {titles_str}. Include answers to the '{paa_str}' at the bottom of the article."

            }
        ],
    max_tokens = 3500
    )

    generated_content = response.choices[0].message.content

    return generated_content, titles, paa_questions


# Button to trigger the Data for SEO API call, generate content and display results
if st.button("Generate Data For SEO"):
    if not keyword:
        st.warning("Please enter a keyword.")
    else:
        serp_data = fetch_serp_data(keyword)
        if serp_data:
            generated_content, titles, paa_questions = generate_content(keyword, serp_data)
            
            st.subheader("Data Used for Content Generation")
            st.write("### Title Tags:")
            for title in titles:
                st.text(title)
            
            st.write("### People Also Ask Questions:")
            for question in paa_questions:
                st.text(question)

            st.subheader("Generated Content")
            st.markdown(generated_content, unsafe_allow_html=True)
