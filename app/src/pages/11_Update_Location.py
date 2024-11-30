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
from modules.nav import get_nav_config
from streamlit_navigation_bar import st_navbar

pages, styles, logo, options = get_nav_config(show_home=False)
page = st_navbar(pages, styles=styles, logo_path=logo, options=options)

if page == "Update Location":
  st.switch_page('pages/11_Update_Location.py')

if page == "Calendar":
  st.switch_page('pages/13_Personal_Calendar.py')

if page == "Group Chat":
  st.switch_page('pages/14_GroupChat.py')

if page == "Logout":
  del st.session_state["role"]
  del st.session_state["authenticated"]
  st.switch_page("Home.py")

# Page Header
st.header("Update Your Location")

# Set default lat & long (based on image of Milan)?
latitude = 45.4627  
longitude = 9.1965 

# Create the map with a draggable marker
m = folium.Map(location=[latitude, longitude], zoom_start=14)
folium.Marker(
    location=[latitude, longitude],
    popup="Drag me to update location",
    draggable=True,
).add_to(m)

# Display the map in the app
map_output = st_folium(m, width=700, height=500)

# Update location if the map is interacted with
if map_output["last_clicked"]:
    lat = map_output["last_clicked"]["lat"]
    lng = map_output["last_clicked"]["lng"]
    st.session_state["user_location"] = (lat, lng)

# Save Button
# st.markdown('<div style="text-align: center; margin-top: 20px;">', unsafe_allow_html=True)
if st.button("Save", use_container_width=True):
    st.success("Location saved successfully!")
# st.markdown('</div>', unsafe_allow_html=True)