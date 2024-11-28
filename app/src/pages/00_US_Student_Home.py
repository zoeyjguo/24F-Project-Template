import logging
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks

st.set_page_config(layout = 'wide')

# Show appropriate sidebar links for the role of the currently logged in user
SideBarLinks()

st.title(f"Welcome Kali, {st.session_state['first_name']}.")
st.write('')
st.write('')
st.write('### What would you like to do today?')

if st.button('View your personalized feed for the "Pets" interest category', 
             type='primary',
             use_container_width=True):
  st.switch_page('pages/02_Interest_Feed.py')

if st.button('Update your interests', 
             type='primary',
             use_container_width=True):
  st.switch_page('pages/03_Update_Interests.py')

if st.button('View another user\'s profile', 
             type='primary',
             use_container_width=True):
  st.switch_page('pages/04_View_Other_Profile.py')