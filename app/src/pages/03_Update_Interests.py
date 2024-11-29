import logging
logger = logging.getLogger(__name__)
import streamlit as st
from modules.nav import get_nav_config
from streamlit_navigation_bar import st_navbar

st.set_page_config(page_title="Profile Page", layout="wide")
pages, styles, logo, options = get_nav_config(show_home=False)
page = st_navbar(pages, styles=styles, logo_path=logo, options=options)

if page == "Feed":
  st.switch_page('pages/02_Interest_Feed.py')

if page == "Update Interests":
  st.switch_page('pages/03_Update_Interests.py')

if page == "View Other Profile":
  st.switch_page('pages/04_View_Other_Profile.py')

if page == "Logout":
  del st.session_state["role"]
  del st.session_state["authenticated"]
  st.switch_page("Home.py")

# Layout: Profile and Additional Info
st.write("## Edit Profile")
profile_col1, profile_col2 = st.columns([11,9])
with profile_col1:
    # Profile Section
    profile = st.container(border=True)
    profile.image("assets/bg_kali.jpg")
    profile.divider()

    col1, col2 = profile.columns([2,3])
    with col1:
       st.image("assets/kali.jpg", width=200)
    with col2:
      st.write("##### Kali Linux")
      st.write("She/Her")
      st.write("512 Points")

    # Information Section
    information = st.container(border=True)
    information.write("##### Information")
    information.text_area("Username", "kali_linux", 68)
    information.text_area("Email Address", "lin.k@northeastern.edu", 68)
    information.text_area("Phone Number", "4324123903", 68)
    information.text_area("Location", "Pasadena, California", 68)

# Right column: Bio, Interests, and Group Chats
with profile_col2:
    # Bio Section
    bio = st.container(border=True)
    bio.text_area("Bio", "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostru.\n" + 
      "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostru.", 170)

    # Interests Section
    interests = st.container(border=True)
    interests.write("#### Interests")
    interest_list = ["Pets", "Sports", "Photography", "LGBTQ+"]
    selected_interests = interests.multiselect("Add More Interests", interest_list, interest_list)

    # Group Chats Section
    groupchats = st.container(border=True)
    groupchats.write("#### Group Chats")
    chat_images = [
        "GC1",
        "GC2",
        "GC3",
        "GC4",
        "GC5",
    ]
    groupchats.multiselect("Leave a group chat", chat_images, chat_images)