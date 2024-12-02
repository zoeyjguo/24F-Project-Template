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

# ***************************************************
#    The major content of this page
# ***************************************************
col1, col2 = st.columns([2, 4])

title_response = requests.get("http://api:4000/u/user/1/rank").json()
events_response = requests.get("http://api:4000/u/user/1/events").json()
posts_response = requests.get("http://api:4000/u/user/1/posts").json()

# Column 1: Profile Info
with col1:
    profile_info = st.container(border=True)
    profile_info.image("assets/prof pic.png", width=150)  
    profile_info.markdown("### Eva Smith", unsafe_allow_html=True)
    profile_info.markdown("<p>She/Her</p>", unsafe_allow_html=True)

    stats = st.container(border=True)
    stats.markdown("#### Profile Overview", unsafe_allow_html=True)

    col1_1, col1_2 = stats.columns(2)
    with col1_1:
        stats.metric("Rank", title_response[0]["Title"])
        stats.metric("Achievements", "23")
    with col1_2:
        stats.metric("Points", "157")
        stats.metric("Events", "17")

# Column 2: Posts and Events
with col2:
    posts_events = st.container(border=True)
    posts_events.markdown("#### Posts You've Made", unsafe_allow_html=True)
    posts_events.dataframe(posts_response)

    posts_events.divider()

    posts_events.markdown("#### Events You're Attending", unsafe_allow_html=True)
    posts_events.write("Event Content")
    posts_events.dataframe(events_response)
