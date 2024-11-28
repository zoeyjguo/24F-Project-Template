import streamlit as st
import requests
from modules.nav import get_nav_config
from streamlit_navigation_bar import st_navbar

pages, styles, logo, options = get_nav_config(show_home=False)
page = st_navbar(pages, selected="User Rank", styles=styles, logo_path=logo, options=options)

if page == "Interests":
  st.switch_page('pages/32_User_Interests.py')

if page == "Badges":
  st.switch_page('pages/35_User_Badges.py')

if page == "Logout":
  del st.session_state["role"]
  del st.session_state["authenticated"]
  st.switch_page("Home.py")

# title = requests.get('http://api:4000/u/users/0/rank').json()
# st.dataframe(title)