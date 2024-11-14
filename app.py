import streamlit as st
import osmnx as ox
import folium
from pyproj import Proj, transform
from folium.plugins import MiniMap
import streamlit.components.v1 as components

# Set the title of the Streamlit app
st.title("Erbil Street Network Visualization with Interactive Map")

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

# Create a folium map centered around the middle of the bounding box
m = folium.Map(location=[(north + south) / 2, (east + west) / 2], zoom_start=13, control_scale=True)

# Add a mini-map
minimap = MiniMap(toggle_display=True)
m.add_child(minimap)

# Add the street network to the folium map using osmnx's graph_to_gdf method
gdf_nodes, gdf_edges = ox.graph_to_gdfs(G)
folium.GeoJson(gdf_edges).add_to(m)

# Add zoom control and other controls
m.add_child(folium.LatLngPopup())  # Shows lat/lon when clicking on the map
m.add_child(folium.LayerControl())  # Toggle layers

# Display the folium map in Streamlit using components
st.write("Interactive map with zoom and controls:")
# Render the folium map HTML
components.html(m._repr_html_(), height=600)
