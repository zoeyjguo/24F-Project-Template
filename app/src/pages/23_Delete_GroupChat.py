import logging
logger = logging.getLogger(__name__)
import streamlit as st
import requests
from streamlit_extras.app_logo import add_logo
from modules.nav import get_nav_config
from streamlit_navigation_bar import st_navbar

# Navigation bar
pages, styles, logo, options = get_nav_config(show_home=False)
page = st_navbar(pages, selected="Delete Group Chat", styles=styles, logo_path=logo, options=options)

if page == "Flag Message":
    st.switch_page('pages/25_Flag_Message.py')

if page == "Reports":
    st.switch_page('pages/26_User_Reports.py')

if page == "Logout":
    del st.session_state["role"]
    del st.session_state["authenticated"]
    st.switch_page("Home.py")

# Function to call the DELETE API route
def delete_gc(group_chat_id):
    api_url = f"http://api:4000/g/groupchats/{group_chat_id}"  # Replace with your API URL
    headers = {"Authorization": "Bearer your_admin_token"}  # Example of secure admin verification

    try:
        response = requests.delete(api_url, headers=headers)
        if response.status_code == 200:
            st.success(f"Group chat {group_chat_id} deleted successfully!")
        elif response.status_code == 404:
            st.error("Group chat not found.")
        elif response.status_code == 403:
            st.error("Unauthorized access. Only admins can delete group chats.")
        else:
            st.error(f"Failed to delete group chat. Error: {response.status_code}")
    except requests.exceptions.RequestException as e:
        st.error(f"Error connecting to the server: {e}")

def fetch_group_chats():
    api_url = "http://api:4000/g/groupchats"  # Replace with your API URL
    try:
        response = requests.get(api_url)
        if response.status_code == 200:
            return response.json()  # Assuming the API returns a JSON array of group chats
        else:
            st.error(f"Failed to fetch group chats. Error: {response.status_code}")
            return []
    except requests.exceptions.RequestException as e:
        st.error(f"Error connecting to the server: {e}")
        return []

# Page Title
st.title("Delete Group Chats")

# Fetch group chats dynamically
group_chats = fetch_group_chats()

if group_chats:
    # Display group chats with a delete button for each
    for gc in group_chats:
        col1, col2 = st.columns([8, 1])
        with col1:
            st.write(f"**Group Chat ID:** {gc['GroupChatID']}")
            st.write(f"**Name:** {gc['Name']}")
            st.write(f"**Monitor ID:** {gc['Monitor']}")
        with col2:
            if st.button("Delete", key=f"delete_{gc['GroupChatID']}"):
                delete_gc(gc['GroupChatID'])
        st.markdown("---")
else:
    st.info("No group chats available to delete.")
