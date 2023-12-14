import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import base64
import requests
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
            value = st.number_input(f"Enter Value for {use_case} in tCO2eq for {year}", value=None, key=f"{sector}_{use_case}_{year}")
            if value is not None:
                st.session_state.setdefault(sector, {}).setdefault(use_case, {})[year] = value
                self.value[sector][use_case][year] = value

    def input_value_too(self, sector, use_case, year):
        use_cases = self.sectors.get(sector, [])
        for use_case in use_cases:
            creading_key = f"{sector}_{use_case}_{year}_creading_{use_case}"
            preading_key = f"{sector}_{use_case}_{year}_preading_{use_case}"
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
        tree = {"x": x, "y": y}
        forest.append(tree)
    return forest

def plot_forest(forest):
    fig, ax = plt.subplots()
    for tree in forest:
        ax.scatter(tree["x"], tree["y"], marker="^", s=50, color="green")

    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.set_aspect("equal", adjustable="box")

    ax.axis("off")

    st.pyplot(fig)

def initialize_sectors(footprint_manager):
    sectors_data = {
        "Energy": ["Electricity", "Fuel Combustion", "Thermal Energy"],
        "Production and Manufacturing": ["Production Processes"],
        "Transportation and Storage": ["Logistics"],
        "Water Supply and Waste Management": ["Water Treatment"],
        "Wholesale and Retail Trade": ["Distribution Centers"],
        "Agriculture": ["Livestock", "Farming"],
    }

    for sector, use_cases in sectors_data.items():
        footprint_manager.emission_sector(sector, use_cases)

    footprint_manager.emission_benchmark("Energy", "Electricity", 12.1)
    footprint_manager.emission_benchmark("Energy", "Fuel Combustion", 42)
    footprint_manager.emission_benchmark("Production and Manufacturing", "Production Processes", 18.3)
    footprint_manager.emission_benchmark("Transportation and Storage", "Logistics", 10.8)
    footprint_manager.emission_benchmark("Water Supply and Waste Management", "Water Treatment", 0.8)
    footprint_manager.emission_benchmark("Wholesale and Retail Trade", "Distribution Centers", 2.2)
    footprint_manager.emission_benchmark("Agriculture", "Livestock", 48.55)
    footprint_manager.emission_benchmark("Agriculture", "Farming", 17.32)

def plot_total_emissions(footprint_manager):
    years = list(range(2010, 2050))
    total_emissions_data = [footprint_manager.total_emissions_by_year(year) for year in years]

    non_zero_years = [year for year, emissions in zip(years, total_emissions_data) if emissions > 0]
    non_zero_emissions = [emissions for emissions in total_emissions_data if emissions > 0]

    fig, ax = plt.subplots()
    ax.plot(non_zero_years, non_zero_emissions, marker="o", linestyle="-", color="g")
    ax.set_xlabel("Year")
    ax.set_ylabel("Total Emissions (in tCO2eq)")
    st.pyplot(fig)

def main_menu(footprint_manager):
    st.sidebar.title("Carbon Footprint Tracker")
    options = ["Add/Update Values", "Display Emissions", "Plot Total Emissions"]

    choice = st.sidebar.selectbox("Select Option", options)

    if choice == "Add/Update Values":
        st.title("Add/Update Values")
        year = st.selectbox("Choose Year", list(range(2010, 2050)))
        sector = st.selectbox("Choose Sector", list(footprint_manager.sectors.keys()))
        st.session_state.selected_sector = sector
        for use_case in footprint_manager.sectors.get(sector, {}):
            footprint_manager.input_value(sector, use_case, year)
            footprint_manager.input_value_too(sector, use_case, year)

    elif choice == "Display Emissions":
        st.title("Display Emissions")
        selected_year = st.selectbox("Choose Year", list(range(2010, 2050)))
        total_emissions = footprint_manager.total_emissions_by_year(selected_year)
        st.subheader(f"Total Emissions for {selected_year}: {total_emissions} tCO2eq")
        sector = st.selectbox("Choose Sector", list(footprint_manager.sectors.keys()))
        footprint_manager.display_values(sector, selected_year)

    elif choice == "Plot Total Emissions":
        st.title("Plot Total Emissions")
        plot_total_emissions(footprint_manager)

if __name__ == "__main__":
    footprint_manager = Footprint()
    initialize_sectors(footprint_manager)
    main_menu(footprint_manager)
