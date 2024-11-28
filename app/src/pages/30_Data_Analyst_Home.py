import logging
logger = logging.getLogger(__name__)

import streamlit as st

st.title(f"Welcome, Data Analyst {st.session_state['first_name']}.")
st.write('')
st.write('')
st.write('### What would you like to do today?')

if st.button('View user interests data', 
             type='primary',
             use_container_width=True):
  st.switch_page('pages/32_User_Interests.py')

if st.button('View user badge rankings', 
             type='primary',
             use_container_width=True):
  st.switch_page('pages/35_User_Badges.py')

if st.button("View the rank of a specific user",
             type='primary',
             use_container_width=True):
  st.switch_page('pages/36_Specific_User_Rank.py')