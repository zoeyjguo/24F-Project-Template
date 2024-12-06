import logging
logger = logging.getLogger(__name__)
import streamlit as st
from streamlit_extras.app_logo import add_logo
import pandas as pd
import pydeck as pdk
from urllib.error import URLError

import streamlit as st
from streamlit_folium import st_folium
import folium
from folium import Icon
from modules.nav import get_nav_config
from streamlit_navigation_bar import st_navbar
import requests

pages, styles, logo, options = get_nav_config(show_home=False)
page = st_navbar(pages, selected="Update Location", styles=styles, logo_path=logo, options=options)

if page == "Calendar":
  st.switch_page('pages/13_Personal_Calendar.py')

if page == "Group Chat":
  st.switch_page('pages/14_GroupChat.py')

if page == "Logout":
  del st.session_state["role"]
  del st.session_state["authenticated"]
  st.switch_page("Home.py")

st.header("Update Your Location")

# Fetch previous location
location = requests.get("http://api:4000/u/users/1002/location").json()
latitude = location[0]['Latitude']
longitude = location[0]['Longitude']
if 'user_location' not in st.session_state:
   st.session_state["user_location"] = (latitude, longitude)

# Create map given previous location
m = folium.Map(location=[latitude,longitude], zoom_start=14)
folium.Marker(
    location=[latitude, longitude],
    popup="Drag me to update location",
    draggable=True,
    icon=Icon(icon="map-marker", prefix="fa", color="purple")
).add_to(m)

# Formatting
col1, col2, col3 = st.columns([1, 8, 1])
with col1:
   st.write("")
with col2:
    map_output = st_folium(m, width=1400, height=700)
with col3:
   st.write("")

# Update location based on moved clicker
if map_output["last_clicked"]:
    lat = map_output["last_clicked"]["lat"]
    lng = map_output["last_clicked"]["lng"]
    st.session_state["user_location"] = (lat, lng)

# Update new location to database
if st.button("Save", use_container_width=True):
    if "user_location" in st.session_state:
        lat, lng = st.session_state["user_location"]
        userId = st.session_state.get("userId", 1)
        payload = {
            "Latitude": lat,
            "Longitude": lng
        }
        try:
            response = requests.put('http://api:4000/u/users/1002/location', json=payload)
            if response.status_code == 200:
                st.success("Location updated successfully!")
            else:
                st.error(f"Failed to update location: {response.status_code}")
        except requests.exceptions.RequestException as e:
            st.error(f"Error connecting to the server: {e}")
    else:
        st.warning("Please select a location on the map before saving.")