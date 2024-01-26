import streamlit as st
import requests
import json
import pprint
import base64

# Streamlit interface for keyword input
st.title("Update2 - Retirement Glossary Generator")
keyword = st.text_input("Enter a keyword", "")

# Button to trigger the Data for SEO API call
if st.button("Generate Data For SEO"):
    if not keyword:
        st.warning("Please enter a keyword.")
    else:
        # Authentication
        login = st.secrets["DATAFORSEO_LOGIN"]
        password = st.secrets["DATAFORSEO_PASSWORD"]
        credentials = f"{login}:{password}"
        encoded_credentials = base64.b64encode(credentials.encode()).decode()

        # Headers
        headers = {
            "Authorization": f"Basic {encoded_credentials}",
            "Content-Type": "application/json"
        }

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
        
        # Check response status and process data
        if task_response.status_code == 200:
            task_response_data = task_response.json()
            task_id = task_response_data['tasks'][0]['id']

            # API Endpoint for retrieving task results
            results_url = f"https://sandbox.dataforseo.com/v3/serp/google/organic/task_get/advanced/{task_id}"

            # Send GET Request to retrieve results
            results_response = requests.get(results_url, headers=headers)
            results_response_data = results_response.json()

            try:
                results_response.status_code == 200:
                results_response_data = results_response.json()
                st.write("Debugging Response Data:", results_response_data)  # Debugging line
                items = results_response_data['tasks'][0]['result'][0]['items']
                
                # Populate top 5 results
                organic_elements = []
                for item in items:
                    if item.get('type') == 'organic' and len(organic_elements) < 5:
                        element_dict = {
                            "title": item.get('title'),
                            "URL": item.get('url'),
                            "group_rank": item.get('rank_group'),
                            'description': item.get('description')
                        }
                        organic_elements.append(element_dict)

                # Display in Streamlit
                st.subheader("Top 5 Organic Elements")
                st.json(organic_elements)
        
                # Rest of your code to process items...

                except KeyError as e:
                    st.error(f"Key error occurred: {e}")
                except IndexError as e:
                    st.error(f"Index error occurred: {e}")
                except Exception as e:
                    st.error(f"An unexpected error occurred: {e}")


        

        
        else:
            st.error("Error creating task. Code: %d Message: %s" % (task_response.status_code, task_response.json()["status_message"]))
