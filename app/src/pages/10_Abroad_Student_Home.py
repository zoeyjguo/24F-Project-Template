import logging
logger = logging.getLogger(__name__)

import streamlit as st

st.title(f"Welcome, {st.session_state['first_name']}.")
st.write('')
st.write('')
st.write('### What would you like to do today?')

if st.button('Update your location', 
             type='primary',
             use_container_width=True):
  st.switch_page('pages/11_Update_Location.py')

if st.button('Send an image in one of your group chats', 
             type='primary',
             use_container_width=True):
  st.switch_page('pages/14_GroupChat.py')

if st.button("View your calendar",
             type='primary',
             use_container_width=True):
  st.switch_page('pages/13_Personal_Calendar.py')