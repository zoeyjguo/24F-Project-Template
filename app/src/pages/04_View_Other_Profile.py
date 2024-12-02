import logging
logger = logging.getLogger(__name__)
import streamlit as st
from modules.nav import get_nav_config
from streamlit_navigation_bar import st_navbar

st.set_page_config(page_title="Profile Page", layout="wide")
pages, styles, logo, options = get_nav_config(show_home=False)
page = st_navbar(pages, selected="View Other Profile", styles=styles, logo_path=logo, options=options)

if page == "Feed":
  st.switch_page('pages/02_Interest_Feed.py')

if page == "Update Interests":
  st.switch_page('pages/03_Update_Interests.py')

if page == "Logout":
  del st.session_state["role"]
  del st.session_state["authenticated"]
  st.switch_page("Home.py")

# Layout: Profile and Additional Info
profile_col1, profile_col2 = st.columns([3,1])
with profile_col1:
    # Profile Section
    profile = st.container(border=True)
    profile.image("assets/bg_winston.jpg")
    profile.divider()

    col1, col2 = profile.columns([2,3])
    with col1:
       st.image("assets/winston.jpg", width=200)
    with col2:
      st.write("##### Winston Church")
      st.write("He/Him")
      st.write("Milan, Italy")
      st.write("100 Points")

    # Bio Section
    bio = st.container(border=True)
    bio.text_area("Bio", "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostru.\n" + 
      "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostru.", 170)

    # Interests Section
    interests = st.container(border=True)
    interests.write("### Interests")
    interests.markdown(
        """
        <style>
            .interest-tag {
                display: inline-block;
                background-color: #d6bcfa;
                color: white;
                padding: 8px 12px;
                margin: 5px;
                border-radius: 15px;
                font-size: 14px;
                font-weight: bold;
                text-align: center;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )

    # Static interests
    static_interests = ["Pets", "Sports", "Photography", "LGBTQ+"]
    interests_html = "".join(f"<span class='interest-tag'>{interest}</span>" for interest in static_interests)

    interests.markdown(interests_html, unsafe_allow_html=True)

# Column 2: Suggested for You
with profile_col2:
    suggested = st.container(border=True)
    suggested.write("### Suggested for You")
    suggested.markdown("<p style='text-align:right;'><a href='#'>See All</a></p>", unsafe_allow_html=True)

    # List of suggested users
    suggested_profiles = [
      {"name": "Alessandro Rossi", "img_url": "https://via.placeholder.com/50"},  # Placeholder image URL
      {"name": "Giovanni Conti", "img_url": "https://via.placeholder.com/50"},
      {"name": "Ethan Walker", "img_url": "https://via.placeholder.com/50"},
      {"name": "Ava Taylor", "img_url": "https://via.placeholder.com/50"},
      {"name": "Mia Johnson", "img_url": "https://via.placeholder.com/50"},
      {"name": "Sofia De Luca", "img_url": "https://via.placeholder.com/50"},
      {"name": "Adrien Greco", "img_url": "https://via.placeholder.com/50"}
    ]

    # Build the HTML content dynamically using a for loop
    html_content = ""
    for profile in suggested_profiles:
        html_content += f"""
        <div style="display: flex; align-items: center; justify-content: space-between; background-color: rgb(255, 255, 255); padding: 10px; margin-bottom: 10px; border-radius: 10px;">
            <div style="display: flex; align-items: center;">
                <img src="{profile['img_url']}" alt="{profile['name']}'s profile" style="border-radius: 10px; width: 50px; height: 50px; margin-right: 10px;">
                <p style="margin: 0; font-weight: normal;">{profile['name']}</p>
            </div>
            <button style="padding: 5px 10px; background-color: #e7e7e7; color: black; border: none; font-weight: bold; border-radius: 5px; cursor: pointer;">Follow</button>
        </div>
        """

    # Pass the HTML content to st.markdown
    st.markdown(
        f"""
        <div style="background-color: rgb(255, 255, 255); padding: 20px; border-radius: 10px;">
            <h3 style="color: black; text-align: center;">Suggested for you</h3>
            {html_content}
        </div>
        """,
        unsafe_allow_html=True,
    )