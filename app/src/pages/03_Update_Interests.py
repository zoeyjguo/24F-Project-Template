import logging
logger = logging.getLogger(__name__)
import streamlit as st
from modules.nav import get_nav_config
from streamlit_navigation_bar import st_navbar

st.set_page_config(page_title="Profile Page", layout="wide")
pages, styles, logo, options = get_nav_config(show_home=False)
page = st_navbar(pages, selected="Update Interests", styles=styles, logo_path=logo, options=options)

if page == "Feed":
  st.switch_page('pages/02_Interest_Feed.py')

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
      st.write("0 Points")

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

    st.markdown(
    f"""
    <style>
        .profile-container {{
            display: flex;
            flex-direction: column;
            align-items: center;
            background-color: #f0f0f0;
            border-radius: 15px;
            padding: 20px;
            max-width: 800px;
            margin: auto;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }}

        .background-image {{
            width: 100%;
            height: 300px;
            background-image: url('./app/static/bg_kali.jpg');
            background-size: cover;
            background-position: center;
            border-radius: 15px 15px 0 0;
            position: relative;
        }}

        .profile-picture {{
            width: 120px;
            height: 120px;
            background-image: url('./app/static/kali.jpg');
            background-size: cover;
            background-position: center;
            border-radius: 15px;
            border: 3px solid white;
            position: absolute;
            bottom: -60px;
            left: 30px;
        }}

        .info-container {{
            background-color: white;
            width: 100%;
            border-radius: 0 0 15px 15px;
            padding: 20px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            box-sizing: border-box;
        }}

        .info-left {{
            margin-left: 150px;
        }}

        .name {{
            font-size: 24px;
            font-weight: bold;
            margin-bottom: 5px;
        }}

        .pronouns {{
            font-size: 16px;
            color: gray;
        }}

        .points-container {{
            display: flex;
            align-items: center;
            font-size: 16px;
            font-weight: bold;
        }}

        .points-container img {{
            width: 20px;
            height: 20px;
            margin-left: 5px;
        }}
    </style>
    """,
    unsafe_allow_html=True,
)

# Layout HTML
st.markdown(
    """
    <div class="profile-container">
        <div class="background-image">
            <div class="profile-picture">
              <img src="/assets/kali.jpg" alt="Kali Profile Picture">
            </div>
        </div>
        <div class="info-container">
            <div class="info-left">
                <div class="name">Kali Linux</div>
                <div class="pronouns">She/Her</div>
            </div>
            <div class="points-container">
                512 Points
                <img src="https://img.icons8.com/ios-filled/50/null/trophy.png" alt="Trophy Icon">
            </div>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)