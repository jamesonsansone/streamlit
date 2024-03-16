import streamlit as st
import pandas as pd
import numpy as np
#import matplotlib.pyplot as plt 

# Placeholder functions for CO2e emissions
def get_co2e_from_energy(energy_consumption):
    return energy_consumption * 0.233

def get_co2e_from_travel(miles):
    return miles * 0.404

# Streamlit app start
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
    chart_data = pd.DataFrame(data)

    st.line_chart(chart_data)
