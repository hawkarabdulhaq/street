import streamlit as st
import osmnx as ox
import folium
from pyproj import Proj, transform
from folium.plugins import MiniMap
import streamlit.components.v1 as components
import pandas as pd

# Sidebar information with emojis
st.sidebar.title("🌍 Interactive Erbil Map Viewer")
st.sidebar.write("🔹 **Prepared by Iman Nawzad**")
st.sidebar.write("🔹 **Explore the Erbil street network with custom points.**")
st.sidebar.write("🗺️ **Features**:")
st.sidebar.write("- View Erbil's street network")
st.sidebar.write("- Interactive map with zoom controls")
st.sidebar.write("- Map points from erbilpoints.txt")
st.sidebar.write("Enjoy exploring! 🎉")

# Main title with emoji
st.title("📍 Erbil Street Network Visualization with Points")

# Original Web Mercator coordinates (EPSG:3857) for bounding box
x_north, y_north = 4901332.950, 4328501.526  # Top left (north)
x_south, y_south = 4902747.019, 4327210.908  # Bottom right (south)

# Define projections for Web Mercator and Latitude/Longitude
proj_3857 = Proj('epsg:3857')
proj_4326 = Proj('epsg:4326')

# Convert bounding box coordinates from EPSG:3857 to EPSG:4326
north, west = transform(proj_3857, proj_4326, x_north, y_north)
south, east = transform(proj_3857, proj_4326, x_south, y_south)
bbox = (north, south, east, west)

# Inform the user about the bounding box
st.write(f"📍 **Bounding box (lat/lon):** North={north}, South={south}, East={east}, West={west}")

# Fetch the street network for the bounding box
st.write("⏳ Fetching the street network for the specified bounding box...")
G = ox.graph_from_bbox(north, south, east, west, network_type='drive')

# Load points from erbilpoints.txt
points_df = pd.read_csv("erbilpoints.txt", header=None, names=["x", "y", "z"])

# Convert each point from EPSG:3857 to EPSG:4326
points_df["lat"], points_df["lon"] = transform(proj_3857, proj_4326, points_df["x"].values, points_df["y"].values)

# Create a folium map centered around the middle of the bounding box
m = folium.Map(location=[(north + south) / 2, (east + west) / 2], zoom_start=13, control_scale=True)

# Add a mini-map with a toggle button
minimap = MiniMap(toggle_display=True)
m.add_child(minimap)

# Add the street network to the folium map
gdf_nodes, gdf_edges = ox.graph_to_gdfs(G)
folium.GeoJson(gdf_edges).add_to(m)

# Add points from erbilpoints.txt to the folium map
for _, row in points_df.iterrows():
    folium.Marker(
        location=[row["lat"], row["lon"]],
        popup=f"Point: ({row['x']}, {row['y']})",
        icon=folium.Icon(icon="map-marker", color="blue")
    ).add_to(m)

# Add interactive features
m.add_child(folium.LatLngPopup())  # Shows lat/lon when clicking on the map
m.add_child(folium.LayerControl())  # Toggle layers

# Display the folium map in Streamlit using components
st.write("🌐 **Interactive map with zoom and controls**:")
components.html(m._repr_html_(), height=600)
