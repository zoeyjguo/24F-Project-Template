import streamlit as st
from modules.nav import get_nav_config
from streamlit_navigation_bar import st_navbar
import requests

if "authenticated" not in st.session_state:
    st.switch_page("Home.py")

pages, styles, logo, options = get_nav_config(show_home=False)
page = st_navbar(pages, selected="Badges", styles=styles, logo_path=logo, options=options)

if page == "Interests":
  st.switch_page('pages/32_User_Interests.py')

if page == "User Rank":
  st.switch_page('pages/36_Specific_User_Rank.py')

if page == "Logout":
  del st.session_state["role"]
  del st.session_state["authenticated"]
  st.switch_page("Home.py")

# icon classes for each badge category
badge_icons = {
    "Adventurer": "🧭",
    "Music Lover": "🎵",
    "Eco-friendly": "🌳",
    "Player One": "🎮",
    "Book Worm": "📚",
    "Film Buff": "🎥",
    "Gym Rat": "🏋️",
    "Tech Enthusiast": "💻",
    "Foodie": "🍴",
    "Fashionista": "👗",
}
# fetch badge data
fetch_badge_data = requests.get('http://api:4000/m/badges/counts').json()
badges = []

for badge in fetch_badge_data:
    badges.append({
        "name": badge["Name"],
        "icon": badge_icons.get(badge["Name"], "🏅"),
        "count": badge["NumStudents"]
    })

# display title
st.markdown("## User Badge Data")

# create a grid layout for the badges
columns = st.columns(4) 
col_index = 0

for badge in badges:
    with columns[col_index]:
        st.markdown(
            f"""
            <div style="text-align: center; margin-bottom: 20px; border: 1px solid #ddd; border-radius: 10px; padding: 10px; background-color: #f9f9f9;">
                <div style="font-size: 40px; margin-bottom: 10px;">{badge['icon']}</div>
                <div style="font-weight: bold; font-size: 18px;">{badge["name"]}</div>
                <div style="font-weight: bold; font-size: 18px;">{badge["count"]} users</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    col_index = (col_index + 1) % 4