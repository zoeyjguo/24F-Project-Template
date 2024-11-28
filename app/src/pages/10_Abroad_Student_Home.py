import logging
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import get_nav_config
from streamlit_navigation_bar import st_navbar

pages, styles, logo, options = get_nav_config(show_home=False)
page = st_navbar(pages, styles=styles, logo_path=logo, options=options)

st.title(f"Welcome, {st.session_state['first_name']}.")
st.write('')
st.write('')
st.write('### What would you like to do today?')

if st.button('Update your location', 
             type='primary',
             use_container_width=True) or page == "Update Location":
  st.switch_page('pages/11_Update_Location.py')

if st.button("View your calendar",
             type='primary',
             use_container_width=True) or page == "Calendar":
  st.switch_page('pages/13_Personal_Calendar.py')

if st.button('Send an image in one of your group chats', 
             type='primary',
             use_container_width=True) or page == "Group Chat":
  st.switch_page('pages/14_GroupChat.py')

if page == "Logout":
  del st.session_state["role"]
  del st.session_state["authenticated"]
  st.switch_page("Home.py")