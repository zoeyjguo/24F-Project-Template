import streamlit as st
from modules.nav import get_nav_config
from streamlit_navigation_bar import st_navbar
import requests

if "authenticated" not in st.session_state:
    st.switch_page("Home.py")

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

report_fetch = requests.get("http://api:4000/m/reports").json()
reports = []

for report in report_fetch:
  reports.append("{0} {1} {2} {3} {4} {5}".format(report["FirstName"], report["LastName"], report["Title"], report["Description"], report["TimeReported"], report["ReportId"]))

if "selected_report" not in st.session_state:
    st.session_state["selected_report"] = None

def select_report(report_id):
    """Update session state with the selected report."""
    st.session_state["selected_report"] = report_id

def delete_report(report_id):
    try:
        # Make a DELETE request to the API
        response = requests.delete(f"http://api:4000/m/report/{report_id}")
        if response.status_code == 200:
            st.success(f"Successfully deleted report {report_id}")
        else:
            st.error(f"Failed to delete report. Status code: {response.status_code}")
    except Exception as e:
        st.error(f"Error: {e}")

# Layout columns
col1, col2 = st.columns([1, 3])

# Sidebar display of all flagged reports
with col1:
    for report in report_fetch:
        button_label = (
            f"**{report['Title']}**\n"
            # f"*{report['TimeReported']}*\n"
            # f"{report['Description'][:100]}..."  
        )

        if st.button(button_label, key=f"btn_{report['ReportId']}"):
            select_report(report["ReportId"])

with col2: 
    selected_report_id = st.session_state["selected_report"]
    if selected_report_id:
        selected_report = next(
            (r for r in report_fetch if r["ReportId"] == selected_report_id), None
        )
        if selected_report:
            st.markdown(
                f"""
                <div style="background-color: rgb(255, 255, 255); padding: 20px; border-radius: 10px;">
                    <p style="font-size: 36px; font-weight: bold;">{selected_report['Title']}</p>
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px; font-size: 14px">
                        <p style="margin: 0;">By {selected_report['FirstName']} {selected_report['LastName']}</p>
                        <p style="margin: 0;">Posted: {selected_report['TimeReported']}</p>
                    </div>
                    <p>{selected_report['Description']}</p><br>
                    <p style="font-weight: semi-bold;">Admin Answer</p>
                    <textarea placeholder="Type Answer..." 
                        style="height: 200px; width: 100%; background-color: #e7e7e7; padding: 10px; border-radius: 8px; border: 1px solid #ccc; margin-bottom: 10px;"></textarea>
                </div>
                """,
                unsafe_allow_html=True,
            )
            st.markdown("<div style='margin-top: 10px;'></div>", unsafe_allow_html=True)

            if st.button("Resolve Report"):
                delete_report(selected_report["ReportId"])
        else:
            st.error("Report not found.")
    else:
        st.warning("No report selected.")