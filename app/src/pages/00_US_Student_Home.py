import logging
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import get_nav_config
from streamlit_navigation_bar import st_navbar

if "authenticated" not in st.session_state:
    st.switch_page("Home.py")

pages, styles, logo, options = get_nav_config(show_home=False)
page = st_navbar(pages, styles=styles, logo_path=logo, options=options)

logger.info(page)
st.title(f"Welcome, {st.session_state['first_name']}.")
st.write('')
st.write('')
st.write('### What would you like to do today?')

if st.button('View your personalized feed', 
             type='primary',
             use_container_width=True) or page == "Feed":
  st.switch_page('pages/02_Interest_Feed.py')

if st.button('Update your interests', 
             type='primary',
             use_container_width=True) or page == "Update Interests":
  st.switch_page('pages/03_Update_Interests.py')

if st.button('View another user\'s profile', 
             type='primary',
             use_container_width=True) or page == "View Other Profile":
  st.switch_page('pages/04_View_Other_Profile.py')

if page == "Logout":
  del st.session_state["role"]
  del st.session_state["authenticated"]
  st.switch_page("Home.py")