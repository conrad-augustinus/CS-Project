import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import xml.etree.ElementTree as ET
import requests
import base64
import json

class Footprint:
    def __init__(self):
        self.sectors = {}
        self.benchmark = {}
        self.value = {}

    def emission_sector(self, sector, use_cases):
        self.sectors[sector] = {use_case: {} for use_case in use_cases}
        self.benchmark[sector] = {use_case: 0 for use_case in use_cases}
        self.value[sector] = {use_case: {} for use_case in use_cases}

    def input_value(self, sector, year):
        use_cases = self.sectors.get(sector, [])
        for use_case in use_cases:
            if use_case == "Electricity":
                creading_key = f"{sector}_{use_case}_{year}_creading"
                preading_key = f"{sector}_{use_case}_{year}_preading"
                creading = st.number_input("What is the current reading on the electricity counter (Kwh/year):", key=creading_key)
                preading = st.number_input("What was the last reading on the electricity counter (Kwh/year):", key=preading_key)
                url = f"https://api.carbonkit.net/3.6/categories/electricity/calculation?country=Switzerland&values.currentReading={creading}&values.lastReading={preading}"
                headers = {
                    "Accept": "application/xml",
                    "Authorization": "Basic " + base64.b64encode(b"AC221:fozzie7").decode("utf-8")
                }
                response = requests.get(url, headers=headers)
                if response.status_code == 200:
                    try:
                        root = ET.fromstring(response.content)
                        amount_element = root.find('.//Amount')
                        if amount_element is not None:
                            amount_text = amount_element.text
                            amount_value = float(amount_text)
                            value = st.write(f"Value for {use_case} in tCO2eq for {year}: {amount_value}")
                            st.session_state.setdefault(sector, {}).setdefault(use_case, {})[year] = value
                            self.value[sector][use_case][year] = value
                        else:
                            st.error('Amount element not found in the XML response.')
                            amount_value = 0
                    except ET.ParseError as e:
                        st.error(f"XML parse error: {e}")
                    except ValueError as e:
                        st.error(f"Value error: Could not convert {amount_text} to float. {e}")
                else:
                    st.error(f"Received response code {response.status_code}: {response.content}")
            elif use_case == "Fuel Combustion":
                fueltype_key = f"{sector}_{use_case}_{year}_fueltype"
                fuelvolume_key = f"{sector}_{use_case}_{year}_fuelvolume"
                fueltype = st.selectbox("Select an option for Fuel Combustion", ["Diesel", "Petrol", "Gas oil", "Natural Gas", "Coal (industrial)", "Burning Oil"], key=fueltype_key)
                fuelvolume = st.number_input("What volume of it have you used (net):", key=fuelvolume_key)
                url = f"https://api.carbonkit.net/3.6/categories/Fuel_Defra/calculation?fuel={fueltype}&netOrGross=net&unit=volume&values.volume={fuelvolume}"
                headers = {
                    "Accept": "application/xml",
                    "Authorization": "Basic " + base64.b64encode(b"AC221:fozzie7").decode("utf-8")
                }
                response = requests.get(url, headers=headers)
                if response.status_code == 200:
                    try:
                        root = ET.fromstring(response.content)
                        amount_element = root.find('.//Amount')
                        if amount_element is not None:
                            amount_text = amount_element.text
                            amount_value = float(amount_text)
                            value = st.write(f"Value for {use_case} in tCO2eq for {year}: {amount_value}")
                            st.session_state.setdefault(sector, {}).setdefault(use_case, {})[year] = value
                            self.value[sector][use_case][year] = value
                        else:
                            st.error('Amount element not found in the XML response.')
                            amount_value = 0
                    except ET.ParseError as e:
                        st.error(f"XML parse error: {e}")
                    except ValueError as e:
                        st.error(f"Value error: Could not convert {amount_text} to float. {e}")
                else:
                    st.error(f"Received response code {response.status_code}: {response.content}")
            elif use_case == "Transport by Bus":
                busdist_key = f"{sector}_{use_case}_{year}_busdist"
                busdist = st.number_input("What distance was traveled by bus (km):", key=busdist_key)
                url = f"https://api.carbonkit.net/3.6/categories/Generic_bus_transport/calculation?type=typical&values.distance={busdist}"
                headers = {
                    "Accept": "application/xml",
                    "Authorization": "Basic " + base64.b64encode(b"AC221:fozzie7").decode("utf-8")
                }
                response = requests.get(url, headers=headers)
                if response.status_code == 200:
                    try:
                        root = ET.fromstring(response.content)
                        amount_element = root.find('.//Amount')
                        if amount_element is not None:
                            amount_text = amount_element.text
                            amount_value = float(amount_text)
                            value = st.write(f"Value for {use_case} in tCO2eq for {year}: {amount_value}")
                            st.session_state.setdefault(sector, {}).setdefault(use_case, {})[year] = value
                            self.value[sector][use_case][year] = value
                        else:
                            st.error('Amount element not found in the XML response.')
                            amount_value = 0
                    except ET.ParseError as e:
                        st.error(f"XML parse error: {e}")
                    except ValueError as e:
                        st.error(f"Value error: Could not convert {amount_text} to float. {e}")
                else:
                    st.error(f"Received response code {response.status_code}: {response.content}")
            elif use_case == "Transport by Ship":
                shipdist_key = f"{sector}_{use_case}_{year}_shipdist"
                shipdist = st.number_input("What distance was traveled by ship (km):", key=shipdist_key)
                url = f"https://api.carbonkit.net/3.6/categories/Generic_ship_transport/calculation?type=ferry&values.distance={shipdist}"
                headers = {
                    "Accept": "application/xml",
                    "Authorization": "Basic " + base64.b64encode(b"AC221:fozzie7").decode("utf-8")
                }
                response = requests.get(url, headers=headers)
                if response.status_code == 200:
                    try:
                        root = ET.fromstring(response.content)
                        amount_element = root.find('.//Amount')
                        if amount_element is not None:
                            amount_text = amount_element.text
                            amount_value = float(amount_text)
                            value = st.write(f"Value for {use_case} in tCO2eq for {year}: {amount_value}")
                            st.session_state.setdefault(sector, {}).setdefault(use_case, {})[year] = value
                            self.value[sector][use_case][year] = value
                        else:
                            st.error('Amount element not found in the XML response.')
                            amount_value = 0
                    except ET.ParseError as e:
                        st.error(f"XML parse error: {e}")
                    except ValueError as e:
                        st.error(f"Value error: Could not convert {amount_text} to float. {e}")
                else:
                    st.error(f"Received response code {response.status_code}: {response.content}")
            elif use_case == "Transport by Plane":
                planedist_key = f"{sector}_{use_case}_{year}_planedist"
                planedist = st.number_input("What distance was traveled by plane (km):", key=planedist_key)
                url = f"https://api.carbonkit.net/3.6/categories/Generic_plane_transport/calculation?type=domestic&size=return&values.distance={planedist}"
                headers = {
                    "Accept": "application/xml",
                    "Authorization": "Basic " + base64.b64encode(b"AC221:fozzie7").decode("utf-8")
                }
                response = requests.get(url, headers=headers)
                if response.status_code == 200:
                    try:
                        root = ET.fromstring(response.content)
                        amount_element = root.find('.//Amount')
                        if amount_element is not None:
                            amount_text = amount_element.text
                            amount_value = float(amount_text)
                            value = st.write(f"Value for {use_case} in tCO2eq for {year}: {amount_value}")
                            st.session_state.setdefault(sector, {}).setdefault(use_case, {})[year] = value
                            self.value[sector][use_case][year] = value
                        else:
                            st.error('Amount element not found in the XML response.')
                            amount_value = 0
                    except ET.ParseError as e:
                        st.error(f"XML parse error: {e}")
                    except ValueError as e:
                        st.error(f"Value error: Could not convert {amount_text} to float. {e}")
                else:
                    st.error(f"Received response code {response.status_code}: {response.content}")
            elif use_case == "Transport by Car":
                carfueltype_key = f"{sector}_{use_case}_{year}_carfueltype"
                carsize_key = f"{sector}_{use_case}_{year}_carsize"
                cardistance_key = f"{sector}_{use_case}_{year}_cardistance"
                carfueltype = st.selectbox("What does the car run on", ["petrol", "diesel"], key=carfueltype_key)
                carsize = st.selectbox("What size is the car", ["small", "medium", "large"], key=carsize_key)
                cardistance = st.number_input("What distance did you travel by car", key=cardistance_key)
                url = f"https://api.carbonkit.net/3.6/categories/Generic_car_transport/calculation?fuel={carfueltype}&size={carsize}&values.distance={cardistance}"
                headers = {
                    "Accept": "application/xml",
                    "Authorization": "Basic " + base64.b64encode(b"AC221:fozzie7").decode("utf-8")
                }
                response = requests.get(url, headers=headers)
                if response.status_code == 200:
                    try:
                        root = ET.fromstring(response.content)
                        amount_element = root.find('.//Amount')
                        if amount_element is not None:
                            amount_text = amount_element.text
                            amount_value = float(amount_text)
                            value = st.write(f"Value for {use_case} in tCO2eq for {year}: {amount_value}")
                            st.session_state.setdefault(sector, {}).setdefault(use_case, {})[year] = value
                            self.value[sector][use_case][year] = value
                        else:
                            st.error('Amount element not found in the XML response.')
                            amount_value = 0
                    except ET.ParseError as e:
                        st.error(f"XML parse error: {e}")
                    except ValueError as e:
                        st.error(f"Value error: Could not convert {amount_text} to float. {e}")
                else:
                    st.error(f"Received response code {response.status_code}: {response.content}")
            elif use_case == "Transport by Taxi":
                taxdist_key = f"{sector}_{use_case}_{year}_taxdist"
                taxdist = st.number_input("What distance was traveled by taxi", key=taxdist_key)
                url = f"https://api.carbonkit.net/3.6/categories/Generic_taxi_transport/calculation?values.distance={taxdist}"
                headers = {
                    "Accept": "application/xml",
                    "Authorization": "Basic " + base64.b64encode(b"AC221:fozzie7").decode("utf-8")
                }
                response = requests.get(url, headers=headers)
                if response.status_code == 200:
                    try:
                        root = ET.fromstring(response.content)
                        amount_element = root.find('.//Amount')
                        if amount_element is not None:
                            amount_text = amount_element.text
                            amount_value = float(amount_text)
                            value = st.write(f"Value for {use_case} in tCO2eq for {year}: {amount_value}")
                            st.session_state.setdefault(sector, {}).setdefault(use_case, {})[year] = value
                            self.value[sector][use_case][year] = value
                        else:
                            st.error('Amount element not found in the XML response.')
                            amount_value = 0
                    except ET.ParseError as e:
                        st.error(f"XML parse error: {e}")
                    except ValueError as e:
                        st.error(f"Value error: Could not convert {amount_text} to float. {e}")
                else:
                    st.error(f"Received response code {response.status_code}: {response.content}")
            elif use_case == "Biological Waste Treatment":
                btype_key = f"{sector}_{use_case}_{year}_btype"
                qtmethane_key = f"{sector}_{use_case}_{year}_qtmethane"
                qttreatment_key = f"{sector}_{use_case}_{year}_qttreatment"
                btype = st.selectbox("What kind of composting are you using", ["Anaerobic Digestion", "Composting"], key=btype_key)
                qtmethane = st.number_input("What quantity of methane was recovered (in Gg):", key=qtmethane_key)
                qttreatment = st.number_input("How much waste was treated (in Gg):", key=qttreatment_key)
                url = f"https://api.carbonkit.net/3.6/categories/biological_waste_treatment/calculation?type={btype}&values.recoveredMethane={qtmethane}&values.mass={qttreatment}"
                headers = {
                    "Accept": "application/xml",
                    "Authorization": "Basic " + base64.b64encode(b"AC221:fozzie7").decode("utf-8")
                }
                response = requests.get(url, headers=headers)
                if response.status_code == 200:
                    try:
                        root = ET.fromstring(response.content)
                        amount_element = root.find('.//Amount')
                        if amount_element is not None:
                            amount_text = amount_element.text
                            amount_value = float(amount_text)
                            value = st.write(f"Value for {use_case} in tCO2eq for {year}: {amount_value}")
                            st.session_state.setdefault(sector, {}).setdefault(use_case, {})[year] = value
                            self.value[sector][use_case][year] = value
                        else:
                            st.error('Amount element not found in the XML response.')
                            amount_value = 0
                    except ET.ParseError as e:
                        st.error(f"XML parse error: {e}")
                    except ValueError as e:
                        st.error(f"Value error: Could not convert {amount_text} to float. {e}")
                else:
                    st.error(f"Received response code {response.status_code}: {response.content}")
            elif use_case == "Industrial Waste Combustion":
                ind_key = f"{sector}_{use_case}_{year}_ind"
                qtburned_key = f"{sector}_{use_case}_{year}_qtburned"
                ind = st.selectbox("What industry are you in?", ["food/beverages/tobacco", "textile", "wood/wood products", "pulp and paper", "rubber", "petroleum products/solvents/plastics", "construction and demolition", "other"], key=ind_key)
                qtburned = st.number_input("What quantity was burned (in tonnes)", key=qtburned_key)
                url = f"https://api.carbonkit.net/3.6/categories/Industrial_waste_combustion/calculation?industry={ind}&values.mass={qtburned}"
                headers = {
                    "Accept": "application/xml",
                    "Authorization": "Basic " + base64.b64encode(b"AC221:fozzie7").decode("utf-8")
                }
                response = requests.get(url, headers=headers)
                response = requests.get(url, headers=headers)
                if response.status_code == 200:
                    try:
                        root = ET.fromstring(response.content)
                        amount_element = root.find('.//Amount')
                        if amount_element is not None:
                            amount_text = amount_element.text
                            amount_value = float(amount_text)
                            value = st.write(f"Value for {use_case} in tCO2eq for {year}: {amount_value}")
                            st.session_state.setdefault(sector, {}).setdefault(use_case, {})[year] = value
                            self.value[sector][use_case][year] = value
                        else:
                            st.error('Amount element not found in the XML response.')
                            amount_value = 0
                    except ET.ParseError as e:
                        st.error(f"XML parse error: {e}")
                    except ValueError as e:
                        st.error(f"Value error: Could not convert {amount_text} to float. {e}")
                else:
                    st.error(f"Received response code {response.status_code}: {response.content}")
            elif use_case == "Livestock":
                ltype_key = f"{sector}_{use_case}_{year}_ltype"
                region_key = f"{sector}_{use_case}_{year}_region"
                lsize_key = f"{sector}_{use_case}_{year}_lsize"
                ltype = st.selectbox("What type of livestock do you own", ["Dairy cattle", "Other Cattle", "Buffalo", "sheep", "Goats", "Camels", "Horses", "Mules/Asses", "Deer", "Alpacas", "Swine"], key=ltype_key)
                region = st.selectbox("What region is it from (Specify region for cattle and developed country for others)", ["North America", "Eastern Europe", "Western Europe", "Oceania", "Latin America", "Asia", "Africa and Middle East", "Indian Subcontinent", "Developed Countries", "Developing Countries"], key=region_key)
                lsize = st.number_input("How many do you own:", key=lsize_key)
                url = f"https://api.carbonkit.net/3.6/categories/Enteric_fermentation/livestockType={ltype}&region={region}&values.livestockNumber={lsize}"
                headers = {
                    "Accept": "application/xml",
                    "Authorization": "Basic " + base64.b64encode(b"AC221:fozzie7").decode("utf-8")
                }
                response = requests.get(url, headers=headers)
                if response.status_code == 200:
                    try:
                        root = ET.fromstring(response.content)
                        amount_element = root.find('.//Amount')
                        if amount_element is not None:
                            amount_text = amount_element.text
                            amount_value = float(amount_text)
                            value = st.write(f"Value for {use_case} in tCO2eq for {year}: {amount_value}")
                            st.session_state.setdefault(sector, {}).setdefault(use_case, {})[year] = value
                            self.value[sector][use_case][year] = value
                        else:
                            st.error('Amount element not found in the XML response.')
                            amount_value = 0
                    except ET.ParseError as e:
                        st.error(f"XML parse error: {e}")
                    except ValueError as e:
                        st.error(f"Value error: Could not convert {amount_text} to float. {e}")
                else:
                    st.error(f"Received response code {response.status_code}: {response.content}")
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
        "Transportation": [
            "Transport by Taxi", "Transport by Car", "Transport by Plane",
            "Transport by Bus", "Transport by Train", "Transport by Ship",
        ],
        "Waste Management": [
            "Biological Waste Treatment", "Industrial Waste Combustion"
        ],
        "Wholesale and Retail Trade": ["Distribution Centers"],
        "Agriculture": ["Livestock", "Farming"],
    }

    for sector, use_cases in sectors_data.items():
        footprint_manager.emission_sector(sector, use_cases)
    
    footprint_manager.emission_benchmark("Energy", "Electricity", 12.1)
    footprint_manager.emission_benchmark("Energy", "Fuel Combustion", 42)
    footprint_manager.emission_benchmark("Production and Manufacturing", "Production Processes", 18.3)
    footprint_manager.emission_benchmark("Transportation", "Transport by Taxi", 1)
    footprint_manager.emission_benchmark("Transportation", "Transport by Car", 1)
    footprint_manager.emission_benchmark("Transportation", "Transport by Plane", 1)
    footprint_manager.emission_benchmark("Transportation", "Transport by Bus", 1)
    footprint_manager.emission_benchmark("Transportation", "Transport by Train", 1)
    footprint_manager.emission_benchmark("Transportation", "Transport by Ship", 1)
    footprint_manager.emission_benchmark("Waste Management", "Biological Waste Treatment", 1)
    footprint_manager.emission_benchmark("Waste Management", "Industrial Waste Combustion", 1)
    footprint_manager.emission_benchmark("Wholesale and Retail Trade", "Distribution Centers", 2.2)
    footprint_manager.emission_benchmark("Agriculture", "Livestock", 48.55)
    footprint_manager.emission_benchmark("Agriculture", "Farming", 17.32)

    print("Sectors initialized:", footprint_manager.sectors)

def get_headers_placeholder():
    return {
        "Accept": "application/json",
        "Authorization": "Basic " + base64.b64encode(b"AC221:fozzie7").decode("utf-8")
    }
def main_menu(footprint_manager):
    st.sidebar.title("Carbon Footprint Tracker")
    options = ["Add/Update Values", "Display Emissions", "Plot Total Emissions"]

    choice = st.sidebar.radio("Select Option", options)

    if choice == "Add/Update Values":
        st.title("Add/Update Values")
        year = st.selectbox("Choose Year", list(range(2010, 2050)), key="year")
        sector = st.selectbox("Choose Sector", list(footprint_manager.sectors.keys()), key="sector")
        st.session_state['selected_year'] = year
        st.session_state['selected_sector'] = sector
        footprint_manager.input_value(sector, year)
    elif choice == "Display Emissions":
        st.title("Display Emissions")
        selected_year = st.session_state.get('selected_year', 2021)
        selected_sector = st.session_state.get('selected_sector', list(footprint_manager.sectors.keys())[0])
        total_emissions = footprint_manager.total_emissions_by_year(selected_year)
        st.subheader(f"Total Emissions for {selected_year}: {total_emissions} tCO2eq")
        footprint_manager.display_values(selected_sector, selected_year)
    elif choice == "Plot Total Emissions":
        st.title("Plot Total Emissions")
        selected_sector = st.session_state.get('selected_sector', list(footprint_manager.sectors.keys())[0])
        plot_total_emissions(footprint_manager, selected_sector)

if __name__ == "__main__":
    footprint_manager = Footprint()
    initialize_sectors(footprint_manager)
    main_menu(footprint_manager)
