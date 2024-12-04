import streamlit as st
from modules.nav import get_nav_config
from streamlit_navigation_bar import st_navbar
import requests

# Navigation bar configuration
pages, styles, logo, options = get_nav_config(show_home=False)
page = st_navbar(pages, selected="Reports", styles=styles, logo_path=logo, options=options)

if page == "Delete Group Chat":
    st.switch_page('pages/23_Delete_GroupChat.py')

if page == "Flag Message":
    st.switch_page('pages/25_Flag_Message.py')

if page == "Logout":
    del st.session_state["role"]
    del st.session_state["authenticated"]
    st.switch_page("Home.py")

# Fetch flag reports
flagWithUsers = requests.get("http://api:4000/simple//flagreports").json()

flagTitles = []
flagUser = []
flagDescription = []
originalMessage = []
flagIds = []  # Assume each flag has a unique ID for deletion

for flag in flagWithUsers:
    flagTitles.append(flag["Title"])
    flagUser.append(flag["FirstName"])
    flagUser.append(" ")
    flagUser.append(flag["LastName"])
    flagDescription.append(flag["Description"])
    originalMessage.append(flag["Text"])
    flagIds.append(flag["FlagId"])  # Store the unique ID

# Layout columns
col1, col2 = st.columns([1, 2])

# Sidebar display of all flagged reports
with col1:
    html_content = ""
    for title, description in zip(flagTitles, flagDescription):
        html_content += f"""
        <div style="display: flex; align-items: center; justify-content: space-between; background-color: rgb(255, 255, 255); padding: 10px; margin-bottom: 10px; border-radius: 10px;">
            <div style="display: flex; align-items: center;">
                <p style="margin: 0; font-weight: normal;">
                <strong>{title}</strong><br> 
                {description}
                </p>
            </div>
        </div>
        """
    st.markdown(
        f"""
        <div style="background-color: #e7e7e7; padding: 20px; border-radius: 10px;">
            {html_content}
        </div>
        """,
        unsafe_allow_html=True,
    )

# Detailed view and action button for the first flag
with col2:
    if flagTitles:  # Ensure there is at least one flag to display
        html_content = f"""
            <div style="background-color: rgb(255, 255, 255); padding: 20px; border-radius: 10px;">
                <p style="font-size: 36px; font-weight: bold;">{flagTitles[0]}</p>
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px; font-size: 14px">
                    <p style="margin: 0;">By {flagUser[0]}{flagUser[1]}{flagUser[2]}</p>
                </div>
                <p>Description:</p>
                <p>{flagDescription[0]}</p><br>
                <p>Original Message:</p>
                <p>{originalMessage[0]}</p><br>
                <p style="font-weight: semi-bold;">Admin Answer</p>
                <input type="text" name="Admin Answer" placeholder="Type Answer..." 
                    style="height: 100px; width: 100%; background-color: #e7e7e7; padding: 10px; padding-top: 15px; border-radius: 8px; border: 1px solid #ccc; margin-bottom: 20px;"/>
            </div>
        """
        st.markdown(html_content, unsafe_allow_html=True)

        # Add a button for resolving the report
        if st.button("Resolve Report", key="resolve_button"):
            flag_id_to_delete = flagIds[0]  # Get the ID of the first report
            response = requests.delete(f"http://api:4000/simple/flagreports/{flag_id_to_delete}")

            if response.status_code == 200:
                st.success("Report resolved successfully!")
            else:
                st.error("Failed to resolve the report. Please try again.")
    else:
        st.warning("No flagged reports available.")
