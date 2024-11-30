import logging
logger = logging.getLogger(__name__)
import streamlit as st
import requests
from streamlit_extras.app_logo import add_logo
from modules.nav import get_nav_config
from streamlit_navigation_bar import st_navbar
from datetime import datetime
import calendar

# navigation bar
pages, styles, logo, options = get_nav_config(show_home=False)
page = st_navbar(pages, styles=styles, logo_path=logo, options=options)

if page == "Update Location":
  st.switch_page('pages/11_Update_Location.py')

if page == "Calendar":
  st.switch_page('pages/13_Personal_Calendar.py')

if page == "Group Chat":
  st.switch_page('pages/14_GroupChat.py')

if page == "Logout":
  del st.session_state["role"]
  del st.session_state["authenticated"]
  st.switch_page("Home.py")

# group chat box styling size
st.markdown(
    """
    <style>
    .group-chat {
        margin-bottom: 15px;
    }
    .group-chat h3 {
        font-size: 1.5rem;
        font-weight: bold;
        margin-bottom: 15px;
    }
    .group-chat-item {
        display: flex;
        align-items: center;
        margin-bottom: 15px;
    }
    .group-chat-item img {
        border-radius: 10px;
        height: 60px;
        width: 60px;
        margin-right: 15px;
    }
    .group-chat-item div {
        font-size: 14px;
    }
    .group-chat-item div strong {
        display: block;
        font-size: 16px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# create columns for layout of group chat and calendar
col1, col2 = st.columns([1, 4])

# group chats on the left section
with col1:
    st.markdown("<h2>Group chats</h2>", unsafe_allow_html=True)

    # data for group chats
    group_chats = [
        {"name": "The Huntingt--", "last_message": "You: I'm coming!", "image": "https://via.placeholder.com/60?text=H"},
        {"name": "USC Pacific As--", "last_message": "John: I'm excited", "image": "https://via.placeholder.com/60?text=U"},
        {"name": "Wrigley Mans--", "last_message": "Jenny: Slay", "image": "https://via.placeholder.com/60?text=W"},
        {"name": "Norton Simon--", "last_message": "Jenny: Slay", "image": "https://via.placeholder.com/60?text=N"},
        {"name": "The Gamble --", "last_message": "You: What does everyone think?", "image": "https://via.placeholder.com/60?text=G"},
        {"name": "Explore Pasa--", "last_message": "You joined the group chat", "image": "https://via.placeholder.com/60?text=E"},
    ]

    # render the items in group chat
    for chat in group_chats:
        st.markdown(
            f"""
            <div class="group-chat-item">
                <img src="{chat['image']}" alt="{chat['name']}">
                <div>
                    <strong>{chat['name']}</strong>
                    <span>{chat['last_message']}</span>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown('</div>', unsafe_allow_html=True)
