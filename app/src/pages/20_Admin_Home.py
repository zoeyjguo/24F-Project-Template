import logging
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import get_nav_config
from streamlit_navigation_bar import st_navbar

if "authenticated" not in st.session_state:
    st.switch_page("Home.py")

pages, styles, logo, options = get_nav_config(show_home=False)
page = st_navbar(pages, styles=styles, logo_path=logo, options=options)

st.title(f"Welcome, Admin {st.session_state['first_name']}.")
st.write('')
st.write('')
st.write('### What would you like to do today?')

if st.button('Delete a group chat', 
             type='primary',
             use_container_width=True) or page == "Delete Group Chat":
  st.switch_page('pages/23_Delete_GroupChat.py')

if st.button('Flag a message in a group chat', 
             type='primary',
             use_container_width=True) or page == "Flag Message":
  st.switch_page('pages/25_Flag_Message.py')

if st.button("View user reports",
             type='primary',
             use_container_width=True) or page == "Reports":
  st.switch_page('pages/26_User_Reports.py')

if page == "Logout":
  del st.session_state["role"]
  del st.session_state["authenticated"]
  st.switch_page("Home.py")