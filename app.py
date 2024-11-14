import streamlit as st
import osmnx as ox
import matplotlib.pyplot as plt

# Set the title of the Streamlit app
st.title("Erbil Street Network Visualization")

# Corrected coordinates for the Erbil area
north = 36.3285858594
south = 36.0677186039
east = 44.1787842755
west = 43.8447719235

# Define the bounding box tuple
bbox = (north, south, east, west)

# Download the street network using the bbox parameter
st.write("Fetching the street network for the specified bounding box...")
G = ox.graph_from_bbox(north, south, east, west, network_type='drive')

# Plot the street network
fig, ax = ox.plot_graph(G, node_size=0, show=False)

# Display the plot in Streamlit
st.pyplot(fig)
