import streamlit as st #type: ignore
import geopandas as gpd #type: ignore
import folium #type: ignore
from streamlit_folium import st_folium #type: ignore
import tempfile #type: ignore
import shutil #type: ignore
import os #type: ignore
from geopy.geocoders import Nominatim #type: ignore

# Page configuration
st.set_page_config(page_title="GIS Map", layout="wide")

# Initialize session state for uploaded data
if 'gdf' not in st.session_state:
    st.session_state.gdf = None
    # Add custom marker for Palestine

default_location = [31.0444, 31.2357]

def create_base_map(location=default_location):
    return folium.Map(location=location, zoom_start=7)

# Streamlined tabs
tabs = st.tabs(["Map View & Analysis", "Upload & Export", "Location Tools"])

# Tab 1: Combined Map View & Analysis
with tabs[0]:
    col1, col2 = st.columns([3, 1])
    with col2:
        st.markdown("### Map Controls")
        enable_draw = st.checkbox("Enable Drawing Tools")
        
        if st.session_state.gdf is not None:
            buffer_distance = st.slider("Buffer Distance (m)", 100, 5000, 1000)
            if st.button("Apply Buffer"):
                buffered_gdf = st.session_state.gdf.to_crs(epsg=3395)
                buffered_gdf['geometry'] = buffered_gdf.buffer(buffer_distance)
                st.session_state.gdf = buffered_gdf.to_crs(epsg=4326)

    with col1:
        map_main = create_base_map()

        if enable_draw:
            folium.plugins.Draw(export=True).add_to(map_main)
        if st.session_state.gdf is not None:
            folium.GeoJson(st.session_state.gdf).add_to(map_main)
            
        st_folium(map_main, width=800, height=600)

# Tab 2: Upload & Export
with tabs[1]:

    uploaded_file = st.file_uploader("Upload GeoJSON/Shapefile", type=["geojson", "shp", "zip"])
    if uploaded_file:
        file_extension = uploaded_file.name.split('.')[-1]
        with tempfile.NamedTemporaryFile(delete=False, suffix=f".{file_extension}") as tmp_file:
            tmp_file.write(uploaded_file.read())
            tmp_file.flush()
            try:
                if file_extension == 'geojson':
                    st.session_state.gdf = gpd.read_file(tmp_file.name)
                elif file_extension in ['shp', 'zip']:
                    with tempfile.TemporaryDirectory() as tmp_dir:
                        if file_extension == 'zip':
                            shutil.unpack_archive(tmp_file.name, tmp_dir)
                        for root, dirs, files in os.walk(tmp_dir):
                            for file in files:
                                if file.endswith('.shp'):
                                    st.session_state.gdf = gpd.read_file(os.path.join(root, file))
                                    break
                
                # Filter out Hebrew text
                st.session_state.gdf = st.session_state.gdf[~st.session_state.gdf['name'].str.contains('[\u0590-\u05FF]', na=False)]

                # Display data preview
                st.success("File uploaded successfully!")
                st.write("### Data Preview")
                st.write(st.session_state.gdf.head())
                
                # Display map with the uploaded data
                st.write("### Data Visualization")
                preview_map = create_base_map()
                folium.GeoJson(st.session_state.gdf).add_to(preview_map)
                st_folium(preview_map, width=600, height=400, key="preview_map")
                
                # Display basic statistics
                st.write("### Data Statistics")
                numeric_cols = st.session_state.gdf.select_dtypes(include=['float64', 'int64']).columns
                if not numeric_cols.empty:
                    st.write(st.session_state.gdf[numeric_cols].describe())
                
            except Exception as e:
                st.error(f"Error reading file: {e}")

# Tab 3: Location Tools
with tabs[2]:
    # Initialize session state for location data
    if 'location_data' not in st.session_state:
        st.session_state.location_data = None

    col1, col2 = st.columns(2)
    with col1:
        latitude = st.number_input("Latitude", min_value=-90.0, max_value=90.0, value=0.0, format="%.6f")
        longitude = st.number_input("Longitude", min_value=-180.0, max_value=180.0, value=0.0, format="%.6f")
        if st.button("Get Location"):
            geolocator = Nominatim(user_agent="student_gis_app", timeout=10)
            try:
                location = geolocator.reverse(f"{latitude}, {longitude}", language='en', timeout=10)
                if location:
                    st.session_state.location_data = {
                        'address': location.address,
                        'latitude': latitude,
                        'longitude': longitude
                    }
                else:
                    st.error("Location not found")
            except Exception as e:
                st.error(f"Error fetching location: {e}")

    with col2:
        if st.session_state.location_data:
            st.write("Location Details:")
            st.write(st.session_state.location_data['address'])
            map_location = create_base_map([st.session_state.location_data['latitude'], 
                                          st.session_state.location_data['longitude']])
            folium.Marker([st.session_state.location_data['latitude'], 
                         st.session_state.location_data['longitude']], 
                         popup=st.session_state.location_data['address']).add_to(map_location)
            st_folium(map_location, width=400, height=400)
