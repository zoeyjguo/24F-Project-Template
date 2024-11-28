import logging
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks

st.set_page_config(layout = 'wide')

# Show appropriate sidebar links for the role of the currently logged in user
SideBarLinks()

st.title(f"Welcome Admin {st.session_state['first_name']}.")
st.write('')
st.write('')
st.write('### What would you like to do today?')

if st.button('Delete a group chat', 
             type='primary',
             use_container_width=True):
  st.switch_page('pages/23_Delete_GroupChat.py')

if st.button('Flag a message in a group chat', 
             type='primary',
             use_container_width=True):
  st.switch_page('pages/25_Flag_Message.py')

if st.button("View user reports",
             type='primary',
             use_container_width=True):
  st.switch_page('pages/26_User_Reports.py')