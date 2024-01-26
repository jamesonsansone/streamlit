import streamlit as st
import requests
import pprint

# Streamlit interface for keyword input
st.title("Updated - Retirement Glossary Generator")
keyword = st.text_input("Enter a keyword", "")

# Button to trigger the Data for SEO API call
if st.button("Generate Data For SEO"):
    if not keyword:
        st.warning("Please enter a keyword.")
    else:
        login = st.secrets["DATAFORSEO_LOGIN"]
        password = st.secrets["DATAFORSEO_PASSWORD"]
        credentials = f"{login}:{password}"
        encoded_credentials = base64.b64encode(credentials.encode()).decode()

        # Headers
        headers = {
            "Authorization": f"Basic {encoded_credentials}",
            "Content-Type": "application/json"
        }
        # Proceed with the API call
        # Set up POST data for creating a task with user-inputted keyword
    task_post_data = json.dumps({
        0: {
            "language_code": "en",
            "location_code": 2840,
            "keyword": keyword,
            "calculate_rectangles": True
        }
    })

    # API Endpoints
    task_url = "https://sandbox.dataforseo.com/v3/serp/google/organic/live/advanced"
    task_response = requests.post(task_url, headers=headers, data=task_post_data)

    # Extracting Task ID
    if task_response.status_code == 200:
        task_id = task_response_data['tasks'][0]['id']
    else:
        print("Error creating task. Code: %d Message: %s" % (task_response.status_code, task_response_data["status_message"]))
        exit()
    
    # API Endpoint for retrieving task results
    results_url = f"https://sandbox.dataforseo.com/v3/serp/google/organic/task_get/advanced/{task_id}"

    # Send GET Request to retrieve results
    results_response = requests.get(results_url, headers=headers)
    results_response_data = results_response.json()

    if results_response.status_code == 200:
        keyword = results_response_data['tasks'][0]['result'][0]['keyword']
        items = results_response_data['tasks'][0]['result'][0]['items']
        
        #Populate top 5 results
        organic_elements = []
        for item in items:
            if item.get('type') == 'organic':
                element_dict = {
                    "title": item.get('title'),
                    "URL": item.get('url'),
                    "group_rank": item.get('rank_group'),
                    'description': item.get('description')
                }
                organic_elements.append(element_dict)
                print("\n")  # Adds an extra line break after the list

            if len(organic_elements) == 6:
                break  # Stop after collecting 5 elements

        print("First 5 Organic Elements:\n")

        pprint.pprint(organic_elements)
    
    #Display in Streamlit
    task_response_data = task_response.json()
    if task_response.status_code == 200:
        # Extracting Task ID and fetching results...
        # Display the data in Streamlit
        st.subheader("Top 5 Organic Elements")
        st.json(organic_elements)  # Assuming 'organic_elements' contains your data

        #st.subheader("Top 5 'People Also Ask'")
        #st.json(people_also_ask)  # Assuming 'people_also_ask' contains your data







# Initialize the OpenAI client with the API key from Streamlit secrets
#client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

#def generate_content(keyword):
#    """
#    Generate content based on the given keyword.
    # """
    # response = client.chat.completions.create(
    #     model="gpt-3.5-turbo",
    #     messages=[
    #         {
    #             "role": "system",
    #             "content": "You are a content generation assistant, expert in creating SEO-optimized articles with a focus on SEO. Your client is a FinTech 401(k) retirement benefit provider needing your help to write content for a new retirement glossary. Articles should be structured, authoritative similar to a glossary set of terms. Use Markdown for formatting, with '#' for main titles and '##' for subtitles. Ensure articles are concise, engaging, and no more than 1500 characters. Do not include conclusion paragraphs."
    #         },
    #         {
    #             "role": "user",
    #             "content": f"Write an informative and comprehensive article about '{keyword}'. The article should include an introduction to the topic, a detailed breakdown, and incorporate related SEO queries within the text. The headlines and subheadings should focus on content semantically related to '{keyword}'. Write content in a way that matches natural language processing. Keep the text between 750 to 1500 characters. Include Markdown-formatted headings. The first heading should be 'What is '{keyword}''"
    #         }
    #     ]
    # )
    # return response.choices[0].message.content


# Button to generate content
# if st.button("Generate Content"):
#     with st.spinner("Generating content..."):
#         generated_content = generate_content(keyword)
#         st.markdown(generated_content, unsafe_allow_html=True)
