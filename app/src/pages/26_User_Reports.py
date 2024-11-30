import streamlit as st
from modules.nav import get_nav_config
from streamlit_navigation_bar import st_navbar

pages, styles, logo, options = get_nav_config(show_home=False)
page = st_navbar(pages, styles=styles, logo_path=logo, options=options)

if page == "Delete Group Chat":
  st.switch_page('pages/23_Delete_GroupChat.py')

if page == "Flag Message":
  st.switch_page('pages/25_Flag_Message.py')

if page == "Reports":
  st.switch_page('pages/26_User_Reports.py')

if page == "Logout":
  del st.session_state["role"]
  del st.session_state["authenticated"]
  st.switch_page("Home.py")


col1, col2= st.columns([1, 2])


with col1:
    reports = [
      {"title": "The Huntington Library", "username": "jacobmelano0202", "time-posted": "November 30, 2024", "description": "https://via.placeholder.com/50"},
      {"title": "The Huntington Library", "username": "lol", "time-posted": "November 30, 2024", "description": "https://via.placeholder.com/50"}
    ] 
  

    # Build the HTML content dynamically using a for loop
    html_content = ""
    for report in reports:
        html_content += f"""
        <div style="display: flex; align-items: center; justify-content: space-between; background-color: rgb(255, 255, 255); padding: 10px; margin-bottom: 10px; border-radius: 10px;">
            <div style="display: flex; align-items: center;">
                <p style="margin: 0; font-weight: normal;">
                <strong>{report['title']}</strong><br> 
                {report['description']}
                </p>
            </div>
        </div>
        """

    # Pass the HTML content to st.markdown
    st.markdown(
        f"""
        <div style="background-color: e7e7e7; padding: 20px; border-radius: 10px;">
            {html_content}
        </div>
        """,
        unsafe_allow_html=True,
    )



with col2: 
    selected = {
        "title": "The Huntington Library", 
        "username": "jacobmelano0202", 
        "time-posted": "November 30, 2024", 
        "description": "Finding more individuals like me that I can connect would be beneficial for me to find more aligned people like me, interest-wise. Is there a feature on this app that does, or do I have to find them by myself?"
    }

    html_content = f"""
         <div style="background-color: rgb(255, 255, 255); padding: 20px; border-radius: 10px;">
            <p style="font-size: 36px; "font-weight: bold;">{selected['title']}</p>
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px; font-size: 14px">
                <p style="margin: 0;">By {selected['username']}</p>
                <p style="margin: 0;">Posted: {selected['time-posted']}</p>
            </div>
            <p>{selected['description']}</p><br>
            <p style="font-weight: semi-bold;">Admin Answer</p>
            <input type="text" name="Admin Answer" placeholder="Type Answer..." 
                style="height: 100px; width: 100%; background-color: #e7e7e7; padding: 10px; padding-top: 15px; border-radius: 8px; border: 1px solid #ccc; margin-bottom: 20px;"/>
          <button style="padding: 10px 20px; border-radius: 5px; background-color: #c6a9f9; border: none;">Resolve Report</button>
        </div>
        """
    st.markdown(
        f"""
        <div style="background-color: rgb(255, 255, 255); padding: 20px; border-radius: 10px;">
            {html_content}
        </div>
        """,
        unsafe_allow_html=True,
    )





