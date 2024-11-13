# GIS Map Application

This is an interactive GIS application built with Streamlit and Folium. It allows users to upload GeoJSON and Shapefile data, analyze spatial features, apply buffers, and visualize maps. Users can also reverse geocode specific coordinates to get location details.

## Features

- Upload and display GeoJSON and Shapefile data
- Buffering spatial features
- Map drawing tools for interactive analysis
- Reverse geocoding to get address details for given coordinates

## Getting Started

### Prerequisites

To run this project, you'll need to have **Python 3.7 or above** installed. If you don't have it, download and install it from [python.org](https://www.python.org/).

### Installation

1. **Clone the Repository**

   First, clone this repository to your local machine:

   ```bash
   git clone https://github.com/NoorBnHossam/GIS.git
   cd GIS
   ```

2. **Create a Virtual Environment**

   It is recommended to create a virtual environment to manage dependencies. You can do this using the following commands:

   ```bash
   python -m venv env
   ```

   Activate the virtual environment:

   - On **Windows**:
     ```bash
     .\env\Scripts\activate
     ```
   - On **macOS/Linux**:
     ```bash
     source env/bin/activate
     ```

3. **Install Dependencies**

   With the virtual environment activated, install the required packages:

   ```bash
   pip install -r requirements.txt
   ```

   ```bash
   pip install streamlit geopandas folium streamlit-folium geopy
   ```

4. **Run the Application**

   Use the following command to start the Streamlit application:

   ```bash
   streamlit run app.py
   ```

5. **Access the Application**

   After running the command above, Streamlit will provide a local URL (usually `http://localhost:8501`). Open this URL in your web browser to access the app.

### Usage

- **Upload Data**: Use the **Upload & Export** tab to upload a GeoJSON or Shapefile.
- **Buffer & Analysis**: In the **Map View & Analysis** tab, adjust the buffer distance for uploaded data.
- **Reverse Geocode**: In the **Location Tools** tab, enter latitude and longitude to get location details.

## Dependencies

Here is a list of main dependencies:

- **Streamlit**: Web app framework for data apps
- **Geopandas**: Library for handling geospatial data
- **Folium**: Python mapping library based on Leaflet.js
- **Streamlit-Folium**: Integration of Folium maps with Streamlit
- **Geopy**: Geocoding library to get location details
