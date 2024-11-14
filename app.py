import streamlit as st
import osmnx as ox
import folium
from pyproj import Proj, transform
from folium.plugins import MiniMap
import streamlit.components.v1 as components
import ee
import geemap  # To help with converting the Earth Engine dataset to folium layers

# Initialize Earth Engine
ee.Initialize()

# Set the title of the Streamlit app
st.title("Erbil Street Network and Landsat NDVI Visualization")

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

# Add the NDVI dataset as the second layer
st.write("Fetching Landsat NDVI data for 2017...")

# Define the Earth Engine dataset
dataset = ee.ImageCollection('LANDSAT/COMPOSITES/C02/T1_L2_32DAY_NDVI').filterDate('2017-01-01', '2017-12-31')
colorized = dataset.select('NDVI')

# Set visualization parameters
colorizedVis = {
    'min': 0,
    'max': 1,
    'palette': [
        'ffffff', 'ce7e45', 'df923d', 'f1b555', 'fcd163', '99b718', '74a901',
        '66a000', '529400', '3e8601', '207401', '056201', '004c00', '023b01',
        '012e01', '011d01', '011301'
    ],
}

# Visualize the NDVI data over the bounding box
ndvi_map = colorized.mean().clip(ee.Geometry.Rectangle([west, south, east, north]))  # Clip the dataset to the bbox
ndvi_layer = geemap.ee_tile_layer(ndvi_map, colorizedVis, 'NDVI 2017')  # Convert to folium tile layer
m.add_child(ndvi_layer)

# Show the map in Streamlit
st.write("Interactive map with zoom, controls, and Landsat NDVI layer:")
# Render the folium map HTML
components.html(m._repr_html_(), height=600)
