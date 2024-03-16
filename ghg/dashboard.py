import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Placeholder function to simulate fetching CO2e emissions from the Climatiq API
def get_co2e_from_energy(energy_consumption):
    # Example: assume 0.233 kgCO2e per kWh, a placeholder value
    return energy_consumption * 0.233

def get_co2e_from_travel(miles):
    # Example: assume 0.404 kgCO2e per mile for fleet travel, a placeholder value
    return miles * 0.404

# Start of Streamlit app
st.title("Climate Impact Assessment Tool")

with st.form("emissions_form"):
    st.write("Please enter your data:")
    energy_consumption = st.number_input("What is your annual energy consumption in kWh?", min_value=0.0, value=0.0, step=100.0)
    fleet_travel_miles = st.number_input("How many miles does your fleet travel annually?", min_value=0.0, value=0.0, step=100.0)
    submitted = st.form_submit_button("Submit")

if submitted:
    energy_co2e = get_co2e_from_energy(energy_consumption)
    travel_co2e = get_co2e_from_travel(fleet_travel_miles)
    total_co2e = energy_co2e + travel_co2e

    st.write(f"Total CO2e Emissions: {total_co2e} kg")

    # Prepare data for the breakdown chart
    data = {'Category': ['Energy Consumption', 'Fleet Travel'], 'CO2e': [energy_co2e, travel_co2e]}
    df = pd.DataFrame(data)

    # Generate a pie chart
    fig, ax = plt.subplots()
    ax.pie(df['CO2e'], labels = df['Category'], autopct='%1.1f%%', startangle=90)
    ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

    st.pyplot(fig)
