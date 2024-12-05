import streamlit as st
from modules.nav import get_nav_config
from streamlit_navigation_bar import st_navbar
import requests

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


col1, col2= st.columns([1, 2])

report_fetch = requests.get("http://api:4000/simple/reportInfo").json()
reports = []

for report in report_fetch:
  reports.append("{0} {1} {2} {3} {4} {5}".format(report["FirstName"], report["LastName"], report["Title"], report["Description"], report["TimeReported"], report["ReportId"]))

users = []

with col1:

    # Build the HTML content dynamically using a for loop
    html_content = ""
    for report in report_fetch:
        html_content += f"""
        <div style="display: flex; align-items: center; justify-content: space-between; background-color: rgb(255, 255, 255); padding: 10px; margin-bottom: 10px; border-radius: 10px;">
            <div style="display: flex; align-items: center;">
                <p style="margin: 20px; font-weight: normal;">
                <strong>{report["Title"]}</strong> — <span style="font-size: 0.9em; color: gray;">{report["TimeReported"]}</span><br>
                {report["Description"]}
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


def delete_report(report_id):
    try:
        # Make a DELETE request to the API
        response = requests.delete(f"http://api:4000/simple/report/{report_id}")
        if response.status_code == 200:
            st.success(f"Successfully deleted report {report_id}")
        else:
            st.error(f"Failed to delete report. Status code: {response.status_code}")
    except Exception as e:
        st.error(f"Error: {e}")


with col2: 
    html_content = f"""
         <div style="background-color: rgb(255, 255, 255); padding: 20px; border-radius: 10px;">
                <p style="font-size: 36px; "font-weight: bold;">{report['Title']}</p>
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px; font-size: 14px">
                    <p style="margin: 0;">By {report['FirstName']} {report['LastName']}</p>
                    <p style="margin: 0;">Posted: {report['TimeReported']}</p>
                </div>
                <p>{report['Description']}</p><br>
                <p style="font-weight: semi-bold;">Admin Answer</p>
                <input type="text" name="Admin Answer" placeholder="Type Answer..." 
                    style="height: 200px; width: 100%; background-color: #e7e7e7; padding: 10px; padding-top: 15px; border-radius: 8px; border: 1px solid #ccc; margin-bottom: 10px;"/>
            </div>
        </div>
    """

    # Display the HTML content
    st.markdown(html_content, unsafe_allow_html=True)

    st.write("")  # Add an empty line for spacing

    # Add the delete button functionality in Streamlit
    if st.button("Resolve Report"):
        delete_report(report["ReportId"])


