import logging
logger = logging.getLogger(__name__)
import streamlit as st
import requests
from streamlit_extras.app_logo import add_logo
from modules.nav import get_nav_config
from streamlit_navigation_bar import st_navbar

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
  
# styling for group chats section
st.markdown(
    """
    <style>
    .group-chat {
        margin-top: 1px;
        padding: 1px;
    }
    .group-chat h3 {
        font-size: 1.5rem;
        font-weight: bold;
        margin-bottom: 10px;
        display: flex;
        align-items: center;
        justify-content: space-between; /* Align the icon to the right */
    }
    .create-chat-icon {
        height: 24px;
        cursor: pointer;
        margin-left: auto; /* Push the icon to the far right */
    }
    .group-chat-search {
        display: flex;
        align-items: center;
        padding: 10px;
        background-color: #f8f8f8;
        border-radius: 20px;
        box-shadow: 1px 1px 4px rgba(0,0,0,0.1);
        margin-bottom: 15px;
    }
    .group-chat-search input {
        border: none;
        outline: none;
        background-color: transparent;
        flex: 1;
        padding-left: 10px;
    }
    .group-chat-search img {
        height: 20px;
        width: 20px;
    }
    .group-chat-item {
        display: flex;
        align-items: center;
        margin-bottom: 15px; /* Adjusted spacing between chat items */
        padding: 10px;
        background-color: #ffffff;
        border-radius: 10px;
        box-shadow: 1px 1px 4px rgba(0,0,0,0.1);
    }
    .group-chat-item img {
        border-radius: 10px;
        height: 60px;
        width: 60px;
        margin-right: 15px;
    }
    .group-chat-item div {
        font-size: 14px;
        flex: 1;
    }
    .group-chat-item div strong {
        display: block;
        font-size: 16px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)
