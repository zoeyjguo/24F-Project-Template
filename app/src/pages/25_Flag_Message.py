import streamlit as st
import requests
from modules.nav import get_nav_config
from streamlit_navigation_bar import st_navbar

pages, styles, logo, options = get_nav_config(show_home=False)
page = st_navbar(pages, selected="Flag Message", styles=styles, logo_path=logo, options=options)

if page == "Delete Group Chat":
  st.switch_page('pages/23_Delete_GroupChat.py')

if page == "Reports":
  st.switch_page('pages/26_User_Reports.py')

if page == "Logout":
  del st.session_state["role"]
  del st.session_state["authenticated"]
  st.switch_page("Home.py")

flags = requests.get("http://api:4000/simple/tenFlags").json()
st.session_state["flags"] = flags

def ignore_flag(flag_id):
  response = requests.put(f"http://api:4000/f/flags/{flag_id}")
  if response.status_code == 200:
      st.success("Flag ignored.")

def delete_message(message_id):
    response = requests.delete(f"http://api:4000/simple/messages/{message_id}")
    if response.status_code == 200:
      st.success("Message deleted successfully!")

st.title("Flagged Messages")
for flag in st.session_state["flags"]:
  col1, col2, col3 = st.columns([7, 1, 1])
  with col1:
    st.write(f"<strong>Message ID: {flag['MessageId']}</strong>", unsafe_allow_html=True)
    st.write(f"<strong>Flag ID: {flag['FlagId']}</strong>", unsafe_allow_html=True)
    st.write(f"Message Content: {flag['Text']}")
    st.write(f"Title: {flag['Title']}")
  with col2:
    if st.button("Ignore Flag", key=f"ignore_{flag['FlagId']}", type="secondary"):
      ignore_flag(flag['FlagId'])
  with col3: 
    if st.button("Delete Message", key=f"delete_{flag['FlagId']}", type="primary"):
      delete_message(flag['MessageId'])
  st.markdown("---")