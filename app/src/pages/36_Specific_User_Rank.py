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

st.markdown("""
  <style>
  .white-box {
      background-color: white;
      border-radius: 10px;
      padding: 20px;
      box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
      margin-bottom: 20px;
  }
  </style>
  """, unsafe_allow_html=True)

# ***************************************************
#    The major content of this page
# ***************************************************
col1, col2 = st.columns([2, 4])

# Column 1: Profile and Overview
with col1:
  # Profile Box
  # TODO: figure out how to get the profile picture to show up
  st.markdown(
      """
      <div class="white-box">
          <img src="app/src/assets/prof pic.png" alt="Profile Picture" style="width: 150px; border-radius: 50%; margin-bottom: 10px;">
          <h3 style="margin: 10px 0;">Eva Smith</h3>
          <p style="margin: 5px 0;">She/Her</p>
          <p style="margin: 5px 0;">On Co-op</p>
      </div>
      """,
      unsafe_allow_html=True,
  )

  # Overview Box
  st.markdown(
      """
      <div class="white-box">
          <h4 style="margin-bottom: 20px;">Overview</h4>
          <div style="display: flex; justify-content: space-between; gap: 20px;">
              <div style="flex: 1;">
                  <div style="margin-bottom: 10px;">
                      <p style="margin: 0; font-weight: bold;">Rank</p>
                      <p style="margin: 0; font-size: 1.2em; color: #666">Gold</p>
                  </div>
                  <div style="margin-bottom: 10px;">
                      <p style="margin: 0; font-weight: bold;">Achievements</p>
                      <p style="margin: 0; font-size: 1.2em; color: #666;">23</p>
                  </div>
              </div>
              <div style="flex: 1;">
                  <div style="margin-bottom: 10px;">
                      <p style="margin: 0; font-weight: bold;">Points</p>
                      <p style="margin: 0; font-size: 1.2em; color: #666">157</p>
                  </div>
                  <div style="margin-bottom: 10px;">
                      <p style="margin: 0; font-weight: bold;">Events</p>
                      <p style="margin: 0; font-size: 1.2em; color: #666">17</p>
                  </div>
              </div>
          </div>
      </div>
      """,
      unsafe_allow_html=True,
  )


# Column 2: Posts and Events
with col2:
  st.markdown(
      """
      <div class="white-box">
          <h4 style="margin-bottom: 20px;">Posts You've Made</h4>
          <div>
              <div style="margin-bottom: 15px;">
                  <p style="margin: 0; font-weight: bold; font-size: 1.1em;">Post Title 1</p>
                  <p style="margin: 0; color: #666;">Post Content</p>
              </div>
              <div style="margin-bottom: 15px;">
                  <p style="margin: 0; font-weight: bold; font-size: 1.1em;">Post Title 2</p>
                  <p style="margin: 0; color: #666;">Post Content</p>
              </div>
              <div style="margin-bottom: 15px;">
                  <p style="margin: 0; font-weight: bold; font-size: 1.1em;">Post Title 3</p>
                  <p style="margin: 0; color: #666;">Post Content</p>
              </div>
          </div>
      </div>
      """,
      unsafe_allow_html=True,
  )

  # Events Box
  st.markdown(
      """
      <div class="white-box">
          <h4 style="margin-bottom: 20px;">Events You've Gone To</h4>
          <ul style="list-style-type: disc; padding-left: 20px; margin: 0;">
              <li style="margin-bottom: 10px;">Event 1</li>
              <li style="margin-bottom: 10px;">Event 2</li>
          </ul>
      </div>
      """,
      unsafe_allow_html=True,
  )
