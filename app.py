import streamlit as st
import osmnx as ox
import matplotlib.pyplot as plt
import pandas as pd

# Sample data (replace this with your actual data loading code)
data = {
    "highway": [
        "residential", "service", "footway", "tertiary", "unclassified", "track", 
        "secondary", "trunk", "pedestrian", "primary", "path", "living_street",
        "trunk_link", "tertiary_link", "motorway_link", "secondary_link",
        "primary_link", "motorway", "[footway, steps]", "[residential, track]",
        "[footway, path]", "cycleway", "[residential, unclassified]",
        "[residential, service]", "[unclassified, track]", "[track, unclassified]",
        "[footway, service]", "[service, track]", "steps", "road",
        "[pedestrian, service]", "[footway, residential]", "[residential, footway]",
        "[residential, tertiary]", "[footway, pedestrian]", "[service, unclassified]",
        "[pedestrian, steps]", "[tertiary_link, tertiary]", "[residential, living_street]",
        "[residential, path]", "[service, tertiary]", "[tertiary_link, unclassified]",
        "[pedestrian, living_street]", "[residential, pedestrian, steps]",
        "[primary_link, trunk_link]", "[path, tertiary]", "[residential, pedestrian]",
        "[path, track]", "[residential, unclassified, track]", "[residential, track, unclassified]",
        "[motorway, motorway_link]", "[secondary, tertiary]", "[trunk, primary]",
        "[primary, trunk]", "[tertiary, trunk_link]", "[trunk_link, tertiary]",
        "[trunk, trunk_link]"
    ],
    "count": [
        97389, 15003, 12596, 10820, 3888, 3502, 2578, 2521, 1538, 1528, 1078, 866,
        660, 631, 378, 266, 263, 198, 104, 74, 72, 66, 62, 28, 22, 22, 20, 18, 16,
        14, 14, 14, 14, 12, 12, 12, 10, 6, 4, 4, 4, 2, 2, 2, 2, 2, 2, 1, 1, 1, 1,
        1, 1, 1, 1, 1
    ]
}

# Create DataFrame
df = pd.DataFrame(data)

# Set up the Streamlit app
st.title("Street Network Visualization for Selected Types")

# Create checkboxes for each unique highway type
st.write("Select the types of highways you want to include in the visualization:")
selected_types = []
for highway_type in df['highway']:
    if st.checkbox(highway_type):
        selected_types.append(highway_type)

# Filter the DataFrame to include only selected highway types
filtered_df = df[df['highway'].isin(selected_types)]

# Display selected data
st.write("### Selected Data")
st.write(filtered_df)

# Only proceed with network visualization if there are selected types
if not filtered_df.empty:
    # Define bounding box for Erbil in latitude and longitude
    north, south, east, west = 36.3285858594, 36.0677186039, 44.1787842755, 43.8447719235
    
    # Download the street network
    st.write("Fetching the street network for the selected bounding box...")
    G = ox.graph_from_bbox(north, south, east, west, network_type='drive')
    
    # Plot the filtered street network
    fig, ax = ox.plot_graph(G, node_size=0, show=False)

    # Display the plot in Streamlit
    st.pyplot(fig)
else:
    st.write("No data types selected. Please select at least one to visualize.")
