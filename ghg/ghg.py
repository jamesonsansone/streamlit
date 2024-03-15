
import streamlit as st
import requests
import json

# Your Climatiq API Key
api_key = st.secrets["climatiq_api_key"]
# Streamlit app title
st.title('Greenhouse Gas Emissions Calculator')

# Form for user input
with st.form("emissions_form"):
    energy_consumption = st.number_input('Enter energy consumption in kWh (e.g., 4200 for an average UK household):', min_value=0.0, value=4200.0, step=100.0)
    submitted = st.form_submit_button("Calculate Emissions")

    if submitted:
        # Climatiq API endpoint
        api_endpoint = 'https://api.climatiq.io/data/v1/estimate'

        # Data payload for the POST request
        data_payload = {
            "emission_factor": {
                "activity_id": "electricity-supply_grid-source_residual_mix",
                "data_version": "^6"
            },
            "parameters": {
                "energy": energy_consumption,
                "energy_unit": "kWh"
            }
        }

        # Headers including the authorization token
        headers = {
            'Authorization': f'Bearer {API_KEY}',
            'Content-Type': 'application/json'
        }

        # Making the POST request to Climatiq API
        response = requests.post(api_endpoint, headers=headers, data=json.dumps(data_payload))

        if response.status_code == 200:
            response_data = response.json()
            co2e = response_data.get('co2e', 'N/A')
            co2e_unit = response_data.get('co2e_unit', '')

            # Display the result
            st.write(f"Estimated CO2e Emissions: {co2e} {co2e_unit}")
        else:
            st.error("Failed to fetch data from Climatiq API. Please check your inputs and try again.")

# Instructions for users to obtain their API key and learn more about Climatiq
st.markdown("""
#### How to get a Climatiq API Key
- Sign up at [Climatiq.io](https://www.climatiq.io) and navigate to your account settings to find your API key.

#### Learn More
- Visit Climatiq's [Data Explorer](https://explorer.climatiq.io) to explore more emission factors.
- Check out Climatiq's [API Documentation](https://docs.climatiq.io) for detailed information on using the API.
""")

# Running the Streamlit app (this line is needed if running the script directly with Streamlit)
if __name__ == "__main__":
    st._main()
