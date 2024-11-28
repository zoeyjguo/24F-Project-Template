import logging
logger = logging.getLogger(__name__)
import streamlit as st
from modules.nav import get_nav_config
from streamlit_navigation_bar import st_navbar

import requests

st.set_page_config(layout = 'wide')
pages, styles, logo, options = get_nav_config(show_home=False)
page = st_navbar(pages, styles=styles, logo_path=logo, options=options)

if page == "Delete Group Chat":
  st.switch_page('pages/23_Delete_GroupChat.py')

if page == "Flag Message":
  st.switch_page('pages/25_Flag_Message.py')

if page == "Reports":
  st.switch_page('pages/26_User_Reports.py')

if page == "Logout":
  del st.session_state["role"]
  del st.session_state["authenticated"]
  st.switch_page("Home.py")

st.title('App Administration Page')

st.write('\n\n')
st.write('## Model 1 Maintenance')

st.button("Train Model 01", 
            type = 'primary', 
            use_container_width=True)

st.button('Test Model 01', 
            type = 'primary', 
            use_container_width=True)

if st.button('Model 1 - get predicted value for 10, 25', 
             type = 'primary',
             use_container_width=True):
  results = requests.get('http://api:4000/c/prediction/10/25').json()
  st.dataframe(results)
