import streamlit as st
import requests
from modules.nav import get_nav_config
from streamlit_navigation_bar import st_navbar

if "authenticated" not in st.session_state:
    st.switch_page("Home.py")

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
col1, col2, col3 = st.columns([1, .1, 1])

user_info = requests.get("http://api:4000/u/users/1").json()
title_response = requests.get("http://api:4000/u/users/1/rank").json()
events_response = requests.get("http://api:4000/u/users/1/events").json()
posts_response = requests.get("http://api:4000/u/users/1/posts").json()

# Column 1: Profile Info
with col1:
    st.markdown(
    """
    <style>
        .profile-container {
            display: flex;
            flex-direction: column;
            align-items: center;
            background-color: #f0f0f0;
            border-radius: 15px;
            padding: 20px;
            max-width: 800px;
            margin: auto;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }

        .background-image {
            width: 100%;
            height: 150px;
            background-image: url('https://t4.ftcdn.net/jpg/03/20/54/47/360_F_320544707_YKQ0cZaHnHAhqy2AqggqDkGjP0APSWqr.jpg');
            background-size: cover;
            background-position: center;
            border-radius: 15px 15px 0 0;
        }

        .profile-picture {
            width: 120px;
            height: 120px;
            background-image: url('https://cdn.pixabay.com/photo/2022/07/28/22/04/sun-7350734_640.jpg');
            background-size: cover;
            background-position: center;
            border-radius: 50%;
            border: 3px solid white;
            margin-top: -60px;
        }

        .info-container {
            background-color: white;
            width: 100%;
            border-radius: 0 0 15px 15px;
            padding: 20px;
            box-sizing: border-box;
            text-align: center;
        }

        .name {
            font-size: 24px;
            font-weight: bold;
            margin-bottom: 5px;
        }

        .pronouns {
            font-size: 16px;
            color: gray;
        }
    </style>
    """,
    unsafe_allow_html=True,
    )

    user_name = "{0} {1}".format(user_info[0]["FirstName"], user_info[0]["LastName"])
    user_pronouns = "{0}".format(user_info[0]["Pronouns"])
    # HTML layout for the profile
    st.markdown(
        f"""
        <div class="profile-container">
            <div class="background-image"></div>
            <div class="profile-picture"></div>
            <div class="info-container">
                <div class="name">{user_name}</div>
                <div class="pronouns">{user_pronouns}</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.write("")
    st.write("")
    stats = st.container(border=True)
    stats.markdown("#### Profile Overview", unsafe_allow_html=True)

    stats.metric("Rank", title_response[0]["Title"])
    stats.metric("Points", title_response[0]["Points"])

with col2:
   st.empty()
   
# Column 2: Posts and Events
with col3:
    posts_events = st.container(border=True)
    posts_events.markdown("#### Posts {0} {1} Has Made".format(user_info[0]["FirstName"], user_info[0]["LastName"]), unsafe_allow_html=True)
    for post in posts_response:
        posts_events.markdown(f"<b>{post['Title']}</b>", unsafe_allow_html=True)

    posts_events.divider()

    posts_events.markdown("#### Events {0} {1} Is Attending/Has Attended".format(user_info[0]["FirstName"], user_info[0]["LastName"]), unsafe_allow_html=True)
    for event in events_response:
        posts_events.markdown(f"<b>{event['Title']}</b>", unsafe_allow_html=True)
        posts_events.markdown(f"Starts at {event['StartTime']}")
        posts_events.markdown(f"Ends at {event['EndTime']}")
