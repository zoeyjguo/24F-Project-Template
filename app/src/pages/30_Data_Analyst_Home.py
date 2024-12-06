import logging
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import get_nav_config
from streamlit_navigation_bar import st_navbar

if "authenticated" not in st.session_state:
    st.switch_page("Home.py")

pages, styles, logo, options = get_nav_config(show_home=False)
page = st_navbar(pages, styles=styles, logo_path=logo, options=options)

st.title(f"Welcome, Data Analyst {st.session_state['first_name']}.")
st.write('')
st.write('')
st.write('### What would you like to do today?')

if st.button('View user interests data', 
             type='primary',
             use_container_width=True) or page == "Interests":
  st.switch_page('pages/32_User_Interests.py')

if st.button('View user badge data', 
             type='primary',
             use_container_width=True) or page == "Badges":
  st.switch_page('pages/35_User_Badges.py')

if st.button("View the rank of a specific user",
             type='primary',
             use_container_width=True) or page == "User Rank":
  st.switch_page('pages/36_Specific_User_Rank.py')

if page == "Logout":
  del st.session_state["role"]
  del st.session_state["authenticated"]
  st.switch_page("Home.py")