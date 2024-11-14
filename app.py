import streamlit as st
import osmnx as ox
import folium
from pyproj import Proj, transform
from folium.plugins import MiniMap
import streamlit.components.v1 as components
import ee
import geemap  # To help with converting the Earth Engine dataset to folium layers
import time

# Initialize Earth Engine
try:
    ee.Initialize()
except Exception as e:
    st.error("Earth Engine Initialization failed. Please check your credentials.")
    st.stop()

st.title("Erbil Street Network and Landsat NDVI Visualization")

# Test smaller coordinates if possible
x_north, y_north = 4901332.950, 4328501.526  
x_south, y_south = 4902747.019, 4327210.908  

proj_3857 = Proj('epsg:3857')
proj_4326 = Proj('epsg:4326')
north, west = transform(proj_3857, proj_4326, x_north, y_north)
south, east = transform(proj_3857, proj_4326, x_south, y_south)
bbox = (north, south, east, west)
st.write(f"Bounding box (lat/lon): North={north}, South={south}, East={east}, West={west}")

# Profiling street network loading time
start_time = time.time()
st.write("Fetching the street network for the specified bounding box...")
try:
    G = ox.graph_from_bbox(north, south, east, west, network_type='drive')
except Exception as e:
    st.error("Street network loading failed.")
    st.stop()
st.write(f"Street network fetched in {time.time() - start_time:.2f} seconds.")

# Map and minimap setup
m = folium.Map(location=[(north + south) / 2, (east + west) / 2], zoom_start=13, control_scale=True)
minimap = MiniMap(toggle_display=True)
m.add_child(minimap)

# Add street network layer
gdf_nodes, gdf_edges = ox.graph_to_gdfs(G)
folium.GeoJson(gdf_edges).add_to(m)
m.add_child(folium.LatLngPopup())
m.add_child(folium.LayerControl())

# Earth Engine NDVI dataset and layer
st.write("Fetching Landsat NDVI data for 2017...")
dataset = ee.ImageCollection('LANDSAT/COMPOSITES/C02/T1_L2_32DAY_NDVI').filterDate('2017-01-01', '2017-12-31')
colorized = dataset.select('NDVI')
colorizedVis = {
    'min': 0, 'max': 1,
    'palette': ['ffffff', 'ce7e45', 'df923d', 'f1b555', 'fcd163', '99b718', '74a901', '66a000', '529400', '3e8601', '207401', '056201', '004c00', '023b01', '012e01', '011d01', '011301']
}

# Visualize the NDVI layer
try:
    ndvi_map = colorized.mean().clip(ee.Geometry.Rectangle([west, south, east, north]))
    ndvi_layer = geemap.ee_tile_layer(ndvi_map, colorizedVis, 'NDVI 2017')
    m.add_child(ndvi_layer)
except Exception as e:
    st.error("NDVI data layer failed to load.")
    st.stop()

st.write("Interactive map with zoom, controls, and Landsat NDVI layer:")
components.html(m._repr_html_(), height=600)
