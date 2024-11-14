import streamlit as st
import osmnx as ox
import matplotlib.pyplot as plt

# Set the title of the Streamlit app
st.title("Street Network Visualization for Specified Bounding Box")

# Coordinates in projected units (e.g., UTM)
north = 4902747.019
south = 4901332.950
east = 4328501.526
west = 4327210.908

# Define the bounding box tuple
bbox = (north, south, east, west)

# Download the street network using the bbox parameter
st.write("Fetching the street network for the specified bounding box...")
G = ox.graph_from_bbox(north, south, east, west, network_type='drive')

# Plot the street network
fig, ax = ox.plot_graph(G, node_size=0, show=False)

# Display the plot in Streamlit
st.pyplot(fig)
