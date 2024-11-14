import streamlit as st
import osmnx as ox
import matplotlib.pyplot as plt

# Set the title of the Streamlit app
st.title("Erbil Street Network with Urban Buildings")

# Corrected coordinates for the Erbil area
north = 36.3285858594
south = 36.0677186039
east = 44.1787842755
west = 43.8447719235

# Define the bounding box tuple
bbox = (north, south, east, west)

# Download the street network and building footprints within the bbox
st.write("Fetching the street network and building footprints for the specified bounding box...")
G = ox.graph_from_bbox(north, south, east, west, network_type='drive')
buildings = ox.geometries_from_bbox(north, south, east, west, tags={'building': True})

# Plot the street network and buildings
fig, ax = plt.subplots(figsize=(10, 10))
# Plot the street network
ox.plot_graph(G, ax=ax, node_size=0, show=False, close=False)
# Plot the building footprints
buildings.plot(ax=ax, facecolor="lightgray", edgecolor="black", alpha=0.7)

# Display the plot in Streamlit
st.pyplot(fig)
