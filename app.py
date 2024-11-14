import streamlit as st
import folium
from pyproj import Proj, transform
from folium.plugins import MiniMap
import streamlit.components.v1 as components
import ee
import geemap  # Helps convert the Earth Engine dataset to folium layers

# Initialize Earth Engine with error handling
try:
    ee.Initialize()
except Exception as e:
    st.error("Earth Engine Initialization failed. Please check your credentials.")
    st.stop()

st.title("Erbil Street Network and Landsat NDVI Visualization (Optimized)")

# Define the bounding box in Web Mercator (EPSG:3857) coordinates
x_north, y_north = 4901332.950, 4328501.526  # Top left (north)
x_south, y_south = 4902747.019, 4327210.908  # Bottom right (south)

# Projections
proj_3857 = Proj('epsg:3857')
proj_4326 = Proj('epsg:4326')

# Convert coordinates
north, west = transform(proj_3857, proj_4326, x_north, y_north)
south, east = transform(proj_3857, proj_4326, x_south, y_south)

st.write(f"Bounding box (lat/lon): North={north}, South={south}, East={east}, West={west}")

# Setup Folium map with center of bounding box
map_center = [(north + south) / 2, (east + west) / 2]
m = folium.Map(location=map_center, zoom_start=13, control_scale=True)

# Add a mini-map
minimap = MiniMap(toggle_display=True)
m.add_child(minimap)

# Only initialize street network if user opts to view it (for efficiency)
if st.button("Load Street Network"):
    with st.spinner("Fetching the street network..."):
        try:
            import osmnx as ox
            # Define a simplified bounding box for a quicker load
            G = ox.graph_from_bbox(north, south, east, west, network_type='drive')
            gdf_nodes, gdf_edges = ox.graph_to_gdfs(G)
            folium.GeoJson(gdf_edges).add_to(m)
            st.success("Street network loaded successfully.")
        except Exception as e:
            st.error("Street network loading failed. Check network or bounding box.")
            st.stop()

# Add Earth Engine NDVI layer (optional loading)
if st.button("Load NDVI Data"):
    with st.spinner("Fetching Landsat NDVI data for 2017..."):
        try:
            # Define and configure Earth Engine dataset
            dataset = ee.ImageCollection('LANDSAT/COMPOSITES/C02/T1_L2_32DAY_NDVI').filterDate('2017-01-01', '2017-12-31')
            colorized = dataset.select('NDVI')
            colorizedVis = {
                'min': 0,
                'max': 1,
                'palette': [
                    'ffffff', 'ce7e45', 'df923d', 'f1b555', 'fcd163', '99b718', '74a901',
                    '66a000', '529400', '3e8601', '207401', '056201', '004c00', '023b01',
                    '012e01', '011d01', '011301'
                ],
            }

            # Clip to bounding box and add as folium layer
            ndvi_map = colorized.mean().clip(ee.Geometry.Rectangle([west, south, east, north]))
            ndvi_layer = geemap.ee_tile_layer(ndvi_map, colorizedVis, 'NDVI 2017')
            m.add_child(ndvi_layer)
            st.success("NDVI data loaded successfully.")
        except Exception as e:
            st.error("NDVI data layer failed to load.")
            st.stop()

# Display the map
st.write("Interactive map with zoom, controls, and optional layers:")
components.html(m._repr_html_(), height=600)
