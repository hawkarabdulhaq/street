import streamlit as st
import osmnx as ox
import matplotlib.pyplot as plt
from pyproj import Proj, transform

# Set the title of the Streamlit app
st.title("Erbil Street Network Visualization")

# Original Web Mercator coordinates (EPSG:3857)
x_north, y_north = 4901332.950, 4328501.526  # Top left (north)
x_south, y_south = 4902747.019, 4327210.908  # Bottom right (south)

# Define projections for Web Mercator and Latitude/Longitude
proj_3857 = Proj('epsg:3857')
proj_4326 = Proj('epsg:4326')

# Convert coordinates from EPSG:3857 to EPSG:4326 (latitude/longitude)
north, west = transform(proj_3857, proj_4326, x_north, y_north)
south, east = transform(proj_3857, proj_4326, x_south, y_south)

# Define the bounding box in latitude and longitude
bbox = (north, south, east, west)

# Inform the user about the bounding box being used
st.write(f"Bounding box (lat/lon): North={north}, South={south}, East={east}, West={west}")

# Download the street network using the converted bbox
st.write("Fetching the street network for the specified bounding box...")
G = ox.graph_from_bbox(north, south, east, west, network_type='drive')

# Plot the street network
fig, ax = ox.plot_graph(G, node_size=0, show=False)

# Display the plot in Streamlit
st.pyplot(fig)
