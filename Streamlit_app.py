import streamlit as st
from simulator import simulator

from PIL import Image

# Set the title & favicon of the tab
favicon = Image.open("data/logo.png")
st.set_page_config(page_title="Simulation Project", page_icon = favicon, initial_sidebar_state = 'auto')


# Title for the app
st.title("Simulation & Modeling Simulator Project | Group-15")

# Cover line for the app
st.write("<names>")

# Input fields
num_simulations = st.number_input("Number of Simulations", min_value=1)
num_servers = st.number_input("Number of Servers", min_value=1)

# Distribution selection
arrival_dist = st.selectbox("Distribution for Interarrival Times", ["Poisson", "Exponential", "Uniform", "Normal"])
service_dist = st.selectbox("Distribution for Service Times", ["Poisson", "Exponential", "Uniform", "Normal"])
priority = st.radio("Include Priority?", ["Yes", "No"])

# Additional parameters based on distributions
poisson_lambda = st.number_input("Poisson Lambda", key="poisson_lambda") if arrival_dist == "Poisson" or service_dist == "Poisson" else None
exponential_scale = st.number_input("Exponential Mean (1/lambda)", key="exponential_scale") if arrival_dist == "Exponential" or service_dist == "Exponential" else None
uniform_low = st.number_input("Uniform Min", key="uniform_low") if arrival_dist == "Uniform" or service_dist == "Uniform" else None
uniform_high = st.number_input("Uniform Max", key="uniform_high") if arrival_dist == "Uniform" or service_dist == "Uniform" else None
normal_mean = st.number_input("Normal Mean", key="normal_mean") if arrival_dist == "Normal" or service_dist == "Normal" else None
normal_std_dev = st.number_input("Normal Std Dev", key="normal_std_dev") if arrival_dist == "Normal" or service_dist == "Normal" else None

# Create input dictionary
input_handler = {
    "num_simulations": num_simulations,
    "num_servers": num_servers,
    "arrival_dist": arrival_dist.lower(),
    "service_dist": service_dist.lower(),
    "poisson_lambda": poisson_lambda if poisson_lambda is not None else 1.0,
    "exponential_scale": exponential_scale if exponential_scale is not None else 1.0,
    "uniform_low": uniform_low if uniform_low is not None else 0.0,
    "uniform_high": uniform_high if uniform_high is not None else 10.0,
    "normal_mean": normal_mean if normal_mean is not None else 5.0,
    "normal_std_dev": normal_std_dev if normal_std_dev is not None else 2.0,
    "priority": priority.lower()
}

# Run simulation
if st.button("Run Simulation"):
    if num_simulations > 0 and num_servers > 0:
        with st.spinner("Running the simulation..."):
            try:
                # Get simulation outputs
                table_data, server_utilization, gantt_chart = simulator(input_handler)
                
                # Display results in Streamlit UI
                st.subheader("Simulation Results")
                
                # Display table data
                st.dataframe(table_data)
                
                # Display server utilization
                st.subheader("Server Utilization")
                st.write(f"**Total utilization time, server took: {server_utilization[0]:.2f} seconds**")
                
                # Display Gantt chart
                st.subheader("Gantt Chart")
                st.pyplot(gantt_chart)
            except Exception as e:
                st.error(f"An error occurred: {e}")
    else:
        st.warning("Please fill all required inputs!")
