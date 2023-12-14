#!/usr/bin/env python
# coding: utf-8

# In[19]:


import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import requests
import base64
import xml.etree.ElementTree as ET

class Footprint:
    def __init__(self):
        self.sectors = {}
        self.benchmark = {}
        self.value = {}

    def emission_sector(self, sector, use_cases):
        self.sectors[sector] = {use_case: {} for use_case in use_cases}
        self.benchmark[sector] = {use_case: 0 for use_case in use_cases}
        self.value[sector] = {use_case: {} for use_case in use_cases}

    def input_value(self, sector, use_case, year):
        if sector in self.sectors and use_case in self.sectors[sector]:
            st.write(f"### {use_case} ({sector})")
            if use_case == "Electricity":
                creading = st.number_input("What is the current reading on the electricity counter (Kwh/year):")
                preading = st.number_input("What was the last reading on the electricity counter (Kwh/year):")
                url = f"https://api.carbonkit.net/3.6/categories/electricity/calculation?country=Switzerland&values.currentReading={creading}&values.lastReading={preading}"
                headers = {
                    "Accept": "application/json",
                    "Authorization": "Basic " + base64.b64encode(b"AC221:fozzie7").decode("utf-8")
                }
                response = requests.get(url, headers=headers)
                if response.status_code == 200:
                        try:
                            data = response.json()
                            output = data.get("output", [])

                            if output and isinstance(output, list) and len(output) > 0:
                                total_direct_co2e = float(output[0].get("value", 0))
                                st.session_state.setdefault(sector, {}).setdefault(use_case, {})[year] = total_direct_co2e
                                self.value[sector][use_case][year] = total_direct_co2e
                        except (json.JSONDecodeError, ValueError):
                            print("Error decoding JSON or extracting value.")
                else:
                    return 0
            elif use_case == "Fuel Combustion":
                fueltype = st.selectbox(f"Select an option for {use_case}", ["Diesel", "Petrol", "Gas oil", "Natural Gas", "Coal (industrial)", "Burning Oil"])
                fuelvolume = st.number_input(f"What volume of it have you used (net): ")
                url = f"https://api.carbonkit.net/3.6/categories/Fuel_Defra/calculation?fuel={fueltype}&netOrgross=net&unit=volume&values.volume={fuelvolume}"
                headers = {
                    "Accept": "application/json",
                    "Authorization": "Basic " + base64.b64encode(b"AC221:fozzie7").decode("utf-8")
                }
                response = requests.get(url, headers=headers)
                if response.status_code == 200:
                    try:
                            data = response.json()
                            output = data.get("output", [])

                            if output and isinstance(output, list) and len(output) > 0:
                                total_direct_co2e = float(output[0].get("value", 0))
                                st.session_state.setdefault(sector, {}).setdefault(use_case, {})[year] = total_direct_co2e
                                self.value[sector][use_case][year] = total_direct_co2e
                    except (json.JSONDecodeError, ValueError):
                            print("Error decoding JSON or extracting value.")
                else:
                    return 0
            elif use_case == "Water":
                watervol = st.number_input(f"How much water was used (in liters)")
                url = f"https://api.carbonkit.net/3.6/categories/water/calculation?type=cold&values.volume{watervol}"
                headers = {
                    "Accept": "application/json",
                    "Authorization": "Basic " + base64.b64encode(b"AC221:fozzie7").decode("utf-8")
                }
                response = requests.get(url, headers=headers)
                if response.status_code == 200:
                    try:
                            data = response.json()
                            output = data.get("output", [])

                            if output and isinstance(output, list) and len(output) > 0:
                                total_direct_co2e = float(output[0].get("value", 0))
                                st.session_state.setdefault(sector, {}).setdefault(use_case, {})[year] = total_direct_co2e
                                self.value[sector][use_case][year] = total_direct_co2e
                    except (json.JSONDecodeError, ValueError):
                            print("Error decoding JSON or extracting value.")
                else:
                    return 0
            elif use_case == "Train Freighting":
                traindistance = st.number_input(f"What is the distance freighted (in km)")
                trainloadmass = st.number_input(f"What is the load mass (in tonnes)")
                url = f"https://api.carbonkit.net/3.6/categories/Train_Freight_Defra/calculation?values.distance={traindistance}&values.mass{trainloadmass}"
                headers = {
                    "Accept": "application/json",
                    "Authorization": "Basic " + base64.b64encode(b"AC221:fozzie7").decode("utf-8")
                }
                response = requests.get(url, headers=headers)
                if response.status_code == 200:
                    try:
                            data = response.json()
                            output = data.get("output", [])

                            if output and isinstance(output, list) and len(output) > 0:
                                total_direct_co2e = float(output[0].get("value", 0))
                                st.session_state.setdefault(sector, {}).setdefault(use_case, {})[year] = total_direct_co2e
                                self.value[sector][use_case][year] = total_direct_co2e
                    except (json.JSONDecodeError, ValueError):
                            print("Error decoding JSON or extracting value.")
                else:
                    return 0
            elif use_case == "Large Goods Vehicle Freighting":
                lgvftype = st.selectbox(f"What is the size of the vehicle", ["Articulated", "NonArticulated"])
                lgvfdist = st.number_input(f"What is the distance freighted")
                url = f"https://api.carbonkit.net/3.6/categories/Generic_large_goods_vehicle_transport/calculation?size={lgvftype}&values.distance{lgvfdist}"
                headers = {
                    "Accept": "application/json",
                    "Authorization": "Basic " + base64.b64encode(b"AC221:fozzie7").decode("utf-8")
                }
                response = requests.get(url, headers=headers)
                if response.status_code == 200:
                    try:
                            data = response.json()
                            output = data.get("output", [])

                            if output and isinstance(output, list) and len(output) > 0:
                                total_direct_co2e = float(output[0].get("value", 0))
                                st.session_state.setdefault(sector, {}).setdefault(use_case, {})[year] = total_direct_co2e
                                self.value[sector][use_case][year] = total_direct_co2e
                    except (json.JSONDecodeError, ValueError):
                            print("Error decoding JSON or extracting value.")
                else:
                    return 0
            elif use_case == "Transport by Train":
                traintyp = st.selectbox(f"What type of train are you taking", ["national", "underground", "tram"])
                traindist = st.number_input(f"What distance was traveled by train (km)")
                url = f"https://api.carbonkit.net/3.6/categories/Generic_train_transport/calculation?type={traintyp}&values.distance={traindist}"
                headers = {
                    "Accept": "application/json",
                    "Authorization": "Basic " + base64.b64encode(b"AC221:fozzie7").decode("utf-8")
                }
                response = requests.get(url, headers=headers)
                if response.status_code == 200:
                    try:
                            data = response.json()
                            output = data.get("output", [])

                            if output and isinstance(output, list) and len(output) > 0:
                                total_direct_co2e = float(output[0].get("value", 0))
                                st.session_state.setdefault(sector, {}).setdefault(use_case, {})[year] = total_direct_co2e
                                self.value[sector][use_case][year] = total_direct_co2e
                    except (json.JSONDecodeError, ValueError):
                            print("Error decoding JSON or extracting value.")
                else:
                    return 0
            elif use_case == "Ship Freighting":
                shiptype = st.selectbox(f"What type of ship is being used for freighting", ["small tanker", "large tanker"])
                shipdistance = st.number_input(f"What distance was the load freighted (in km)")
                shipmass = st.number_input(f"What is the mass of the load freighted (in tonnes)")
                url = f"https://api.carbonkit.net/3.6/categories/Ship_Freight_Defra/calculation?type={shiptype}&values.distance{shipdistance}&values.mass={shipmass}"
                headers = {
                    "Accept": "application/json",
                    "Authorization": "Basic " + base64.b64encode(b"AC221:fozzie7").decode("utf-8")
                }
                response = requests.get(url, headers=headers)
                if response.status_code == 200:
                    try:
                            data = response.json()
                            output = data.get("output", [])

                            if output and isinstance(output, list) and len(output) > 0:
                                total_direct_co2e = float(output[0].get("value", 0))
                                st.session_state.setdefault(sector, {}).setdefault(use_case, {})[year] = total_direct_co2e
                                self.value[sector][use_case][year] = total_direct_co2e
                    except (json.JSONDecodeError, ValueError):
                            print("Error decoding JSON or extracting value.")
                else:
                    return 0
            elif use_case == "Transport by Bus":
                busdist = st.number_input(f"What distance was traveled by bus (km)")
                url = f"https://api.carbonkit.net/3.6/categories/Generic_bus_transport/calculation?type=typical&values.distance={busdist}"
                headers = {
                    "Accept": "application/json",
                    "Authorization": "Basic " + base64.b64encode(b"AC221:fozzie7").decode("utf-8")
                }
                response = requests.get(url, headers=headers)
                if response.status_code == 200:
                    try:
                            data = response.json()
                            output = data.get("output", [])

                            if output and isinstance(output, list) and len(output) > 0:
                                total_direct_co2e = float(output[0].get("value", 0))
                                st.session_state.setdefault(sector, {}).setdefault(use_case, {})[year] = total_direct_co2e
                                self.value[sector][use_case][year] = total_direct_co2e
                    except (json.JSONDecodeError, ValueError):
                            print("Error decoding JSON or extracting value.")
                else:
                    return 0
            elif use_case == "Transport by Ship":
                shipdist = st.number_input(f"What distance was traveled by ship (km)")
                url = f"https://api.carbonkit.net/3.6/categories/Generic_ship_transport/calculation?type=ferry&values.distance={shipdist}"
                headers = {
                    "Accept": "application/json",
                    "Authorization": "Basic " + base64.b64encode(b"AC221:fozzie7").decode("utf-8")
                }
                response = requests.get(url, headers=headers)
                if response.status_code == 200:
                    try:
                            data = response.json()
                            output = data.get("output", [])

                            if output and isinstance(output, list) and len(output) > 0:
                                total_direct_co2e = float(output[0].get("value", 0))
                                st.session_state.setdefault(sector, {}).setdefault(use_case, {})[year] = total_direct_co2e
                                self.value[sector][use_case][year] = total_direct_co2e
                    except (json.JSONDecodeError, ValueError):
                            print("Error decoding JSON or extracting value.")
                else:
                    return 0
            elif use_case == "Transport by Plane":
                planedist = st.number_input(f"What distance was traveled by plane (km)")
                url = f"https://api.carbonkit.net/3.6/categories/Generic_plane_transport/calculation?type=domestic&size=return&values.distance={planedist}"
                headers = {
                    "Accept": "application/json",
                    "Authorization": "Basic " + base64.b64encode(b"AC221:fozzie7").decode("utf-8")
                }
                response = requests.get(url, headers=headers)
                if response.status_code == 200:
                    try:
                            data = response.json()
                            output = data.get("output", [])

                            if output and isinstance(output, list) and len(output) > 0:
                                total_direct_co2e = float(output[0].get("value", 0))
                                st.session_state.setdefault(sector, {}).setdefault(use_case, {})[year] = total_direct_co2e
                                self.value[sector][use_case][year] = total_direct_co2e
                    except (json.JSONDecodeError, ValueError):
                            print("Error decoding JSON or extracting value.")
                else:
                    return 0
            elif use_case == "Transport by Car":
                carfueltype = st.selectbox(f"What does the car run on", ["petrol", "diesel"])
                carsize = st.selectbox(f"What size is the car", ["small", "medium", "large"])
                cardistance = st.number_input(f"What distance did you travel by car")
                url = f"https://api.carbonkit.net/3.6/categories/Generic_car_transport/calculation?fuel={carfueltype}&size={carsize}&values.distance={cardistance}"
                headers = {
                    "Accept": "application/json",
                    "Authorization": "Basic " + base64.b64encode(b"AC221:fozzie7").decode("utf-8")
                }
                response = requests.get(url, headers=headers)
                if response.status_code == 200:
                    try:
                            data = response.json()
                            output = data.get("output", [])

                            if output and isinstance(output, list) and len(output) > 0:
                                total_direct_co2e = float(output[0].get("value", 0))
                                st.session_state.setdefault(sector, {}).setdefault(use_case, {})[year] = total_direct_co2e
                                self.value[sector][use_case][year] = total_direct_co2e
                    except (json.JSONDecodeError, ValueError):
                            print("Error decoding JSON or extracting value.")
                else:
                    return 0
            elif use_case == "Transport by Taxi":
                taxdist = st.number_input("What distance was traveled by taxi")
                url = f"https://api.carbonkit.net/3.6/categories/Generic_taxi_transport/calculation?values.distance={taxdist}"
                headers = {
                    "Accept": "application/json",
                    "Authorization": "Basic " + base64.b64encode(b"AC221:fozzie7").decode("utf-8")
                }
                response = requests.get(url, headers=headers)
                if response.status_code == 200:
                    try:
                            data = response.json()
                            output = data.get("output", [])

                            if output and isinstance(output, list) and len(output) > 0:
                                total_direct_co2e = float(output[0].get("value", 0))
                                st.session_state.setdefault(sector, {}).setdefault(use_case, {})[year] = total_direct_co2e
                                self.value[sector][use_case][year] = total_direct_co2e
                    except (json.JSONDecodeError, ValueError):
                            print("Error decoding JSON or extracting value.")
                else:
                    return 0
            elif use_case == "Landfill":
                metrec = st.number_input("Volume of Methane Recovered (m3)")
                url = f"https://api.carbonkit.net/3.6/categories/Landfill_emissions_based_on_methane_recovery/calculation?values.collected{metrec}"
                headers = {
                    "Accept": "application/json",
                    "Authorization": "Basic " + base64.b64encode(b"AC221:fozzie7").decode("utf-8")
                }
                response = requests.get(url, headers=headers)
                if response.status_code == 200:
                    try:
                            data = response.json()
                            output = data.get("output", [])

                            if output and isinstance(output, list) and len(output) > 0:
                                total_direct_co2e = float(output[0].get("value", 0))
                                st.session_state.setdefault(sector, {}).setdefault(use_case, {})[year] = total_direct_co2e
                                self.value[sector][use_case][year] = total_direct_co2e
                    except (json.JSONDecodeError, ValueError):
                            print("Error decoding JSON or extracting value.")
                else:
                    return 0
            elif use_case == "Biological Waste Treatment":
                btype = st.selectbox(f"What kind of composting are you using", ["Anaerobic Digestion", "Composting"])
                qtmethane = st.number_input("What quantity of methane was recovered (in Gg):")
                qttreatment = st.number_input("How much waste was treated (in Gg):")
                url = f"https://api.carbonkit.net/3.6/categories/biological_waste_treatment/calculation?type={btype}&values.recoveredMethane={qtmethane}&values.mass={qttreatment}"
                headers = {
                    "Accept": "application/json",
                    "Authorization": "Basic " + base64.b64encode(b"AC221:fozzie7").decode("utf-8")
                }
                response = requests.get(url, headers=headers)
                if response.status_code == 200:
                    try:
                            data = response.json()
                            output = data.get("output", [])

                            if output and isinstance(output, list) and len(output) > 0:
                                total_direct_co2e = float(output[0].get("value", 0))
                                st.session_state.setdefault(sector, {}).setdefault(use_case, {})[year] = total_direct_co2e
                                self.value[sector][use_case][year] = total_direct_co2e
                    except (json.JSONDecodeError, ValueError):
                            print("Error decoding JSON or extracting value.")
                else:
                    return 0
            elif use_case == "Industrial Waste Combustion":
                ind = st.selectbox(f"What industry are you in?", ["food/beverages/tobacco", "textile", "wood/wood products", "pulp and paper", "rubber", "petroleum products/solvents/plastics", "construction and demolition", "other"])
                qtburned = st.number_input("What quantity was burned (in tonnes)")
                url = f"https://api.carbonkit.net/3.6/categories/Industrial_waste_combustion/calculation?industry={ind}&values.mass={qtburned}"
                headers = {
                    "Accept": "application/json",
                    "Authorization": "Basic " + base64.b64encode(b"AC221:fozzie7").decode("utf-8")
                }
                response = requests.get(url, headers=headers)
                if response.status_code == 200:
                    try:
                            data = response.json()
                            output = data.get("output", [])

                            if output and isinstance(output, list) and len(output) > 0:
                                total_direct_co2e = float(output[0].get("value", 0))
                                st.session_state.setdefault(sector, {}).setdefault(use_case, {})[year] = total_direct_co2e
                                self.value[sector][use_case][year] = total_direct_co2e
                    except (json.JSONDecodeError, ValueError):
                            print("Error decoding JSON or extracting value.")
                else:
                    return 0
            elif use_case == "Livestock":
                    ltype = st.selectbox(f"What type of livestock do you own", ["Dairy cattle", "Other Cattle", "Buffalo", "sheep", "Goats", "Camels", "Horses", "Mules/Asses", "Deer", "Alpacas", "Swine"])
                    region = st.selectbox(f"What region is it from (Specify region for cattle and developed country for others)", ["North America", "Eastern Europe", "Western Europe", "Oceania", "Latin America", "Asia", "Africa and Middle East", "Indian Subcontinent", "Developed Countries", "Developing Countries"])
                    lsize = st.number_input(f"How many do you own: ")
                    url = f"https://api.carbonkit.net/3.6/categories/Enteric_fermentation/livestockType={ltype}&region={region}&values.livestockNumber={lsize}"
                    headers = {
                        "Accept": "application/json",
                        "Authorization": "Basic " + base64.b64encode(b"AC221:fozzie7").decode("utf-8")
                    }
                    response = requests.get(url, headers=headers)
                    if response.status_code == 200:
                        try:
                            data = response.json()
                            output = data.get("output", [])

                            if output and isinstance(output, list) and len(output) > 0:
                                total_direct_co2e = float(output[0].get("value", 0))
                                st.session_state.setdefault(sector, {}).setdefault(use_case, {})[year] = total_direct_co2e
                                self.value[sector][use_case][year] = total_direct_co2e
                        except (json.JSONDecodeError, ValueError):
                            print("Error decoding JSON or extracting value.")
                    else:
                        return 0
            else:
                value = st.number_input(f"Enter Value for {use_case} in tCO2eq for {year}", value=None, key=f"{sector}_{use_case}_{year}")
                st.session_state.setdefault(sector, {}).setdefault(use_case, {})[year] = value
                self.value[sector][use_case][year] = value

    def emission_benchmark(self, sector, use_case, value):
        if sector in self.benchmark and use_case in self.sectors[sector]:
            self.benchmark[sector][use_case] = value

    def total_emissions_by_year(self, year):
        total_emissions = 0
        for sector in self.value.keys():
            for use_case in self.value[sector].keys():
                if st.session_state.get(sector, {}).get(use_case, {}).get(year):
                    total_emissions += st.session_state[sector][use_case][year]
        return total_emissions

    def display_values(self, sector, selected_year):
        if sector in self.sectors:
            total = 0
            for use_case, year_values in st.session_state.get(sector, {}).items():
                value = year_values.get(selected_year, 0)
                benchmark = self.benchmark[sector][use_case]
                st.write(f"{use_case}: {value} (Standard Emissions: {benchmark})")

                if value > benchmark:
                    st.warning(f"  - Excess Emissions compared to Standard of {value - benchmark} tCO2eq")
                elif value < benchmark:
                    st.success(f"  - Below Standard Emissions by {benchmark - value} tCO2eq")

                total += value

            st.write(f"Total Emissions for {sector}: {total} tCO2eq")
            st.caption("Benchmark Approximation Source: https://data.europa.eu/doi/10.2760/028705")
            num_trees = int(self.total_emissions_by_year(selected_year) * 45)

            st.write(f"Number of Trees to Offset Emissions per Year: {num_trees}")
            forest = generate_forest(num_trees)
            plot_forest(forest)
            st.caption("Approximately 45 Trees per Ton of GHGs Emitted")
def generate_forest(num_trees):
    forest = []
    for _ in range(num_trees):
        x = np.random.rand()
        y = np.random.rand()
        tree = {'x': x, 'y': y}
        forest.append(tree)
    return forest

def plot_forest(forest):
    fig, ax = plt.subplots()
    for tree in forest:
        ax.scatter(tree['x'], tree['y'], marker='^', s=50, color='green')
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.set_aspect('equal', adjustable='box')
    ax.axis('off')
    st.pyplot(fig)
            
def initialize_sectors(footprint_manager):
    sectors_data = {
        "Energy": ["Electricity", "Fuel Combustion"],
        "Production and Manufacturing": ["Production Processes"],
        "Transportation and Freighting": ["Transport by Taxi", "Transport by Car", "Transport by Plane", "Transport by Bus", "Transport by Train", "Transport by Ship", "Ship Freighting", "Large Goods Vehicle Freighting", "Train Freighting", "Plane Freighting"],
        "Water Supply and Waste Management": ["Water", "Landfill", "Biological Waste Treatment", "Industrial Waste Combustion"],
        "Wholesale and Retail Trade": ["Distribution Centers"],
        "Agriculture": ["Livestock", "Farming"],
    }
    
    for sector, use_cases in sectors_data.items():
        footprint_manager.emission_sector(sector, use_cases)
        
        for use_case in use_cases:
            footprint_manager.input_value(sector, use_case, year = 2022)
    
    footprint_manager.emission_benchmark("Energy", "Electricity", 12.1)
    footprint_manager.emission_benchmark("Energy", "Fuel Combustion", 42)
    footprint_manager.emission_benchmark("Production and Manufacturing", "Production Processes", 18.3)
    footprint_manager.emission_benchmark("Transportation and Freighting", "Transport by Taxi", 1)
    footprint_manager.emission_benchmark("Transportation and Freighting", "Transport by Car", 1)
    footprint_manager.emission_benchmark("Transportation and Freighting", "Transport by Plane", 1)
    footprint_manager.emission_benchmark("Transportation and Freighting", "Transport by Bus", 1)
    footprint_manager.emission_benchmark("Transportation and Freighting", "Transport by Train", 1)
    footprint_manager.emission_benchmark("Transportation and Freighting", "Transport by Ship", 1)
    footprint_manager.emission_benchmark("Transportation and Freighting", "Ship Freighting", 1)
    footprint_manager.emission_benchmark("Transportation and Freighting", "Large Goods Vehicle Freighting", 1)
    footprint_manager.emission_benchmark("Transportation and Freighting", "Train Freighting", 1)
    footprint_manager.emission_benchmark("Transportation and Freighting", "Plane Freighting", 1)
    footprint_manager.emission_benchmark("Water Supply and Waste Management", "Water", 0.8)
    footprint_manager.emission_benchmark("Water Supply and Waste Management", "Landfill", 1)
    footprint_manager.emission_benchmark("Water Supply and Waste Management", "Biological Waste Treatment", 1)
    footprint_manager.emission_benchmark("Water Supply and Waste Management", "Industrial Waste Combustion", 1)
    footprint_manager.emission_benchmark("Wholesale and Retail Trade", "Distribution Centers", 2.2)
    footprint_manager.emission_benchmark("Agriculture", "Livestock", 48.55)
    footprint_manager.emission_benchmark("Agriculture", "Farming", 17.32)
    

def get_headers_placeholder():
    return {
        "Accept": "application/json",
        "Authorization": "Basic " + base64.b64encode(b"AC221:fozzie7").decode("utf-8")
    }

def main_menu(footprint_manager):
    st.title("Carbon Footprint Tracker")
    options = ["Add/Update Values", "Display Emissions", "Plot Total Emissions"]

    choice = st.sidebar.selectbox("Select Option", options)

    if choice == "Add/Update Values":
        year = st.selectbox("Choose Year", list(range(2010, 2050)))
        sector = st.selectbox("Choose Sector", list(footprint_manager.sectors.keys()))
        st.session_state.selected_sector = sector
        for use_case in footprint_manager.sectors.get(sector, {}):
            footprint_manager.input_value(sector, use_case, year)

    elif choice == "Display Emissions":
        selected_year = st.selectbox("Choose Year", list(range(2010, 2050)))
        total_emissions = footprint_manager.total_emissions_by_year(selected_year)
        st.subheader(f"Total Emissions for {selected_year}: {total_emissions} tCO2eq")
        sector = st.selectbox("Choose Sector", list(footprint_manager.sectors.keys()))
        footprint_manager.display_values(sector, selected_year)

    elif choice == "Plot Total Emissions":
        plot_total_emissions(footprint_manager)

if __name__ == "__main__":
    footprint_manager = Footprint()
    initialize_sectors(footprint_manager)
    main_menu(footprint_manager)


# In[ ]:




