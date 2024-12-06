import streamlit as st
from modules.nav import get_nav_config
from streamlit_navigation_bar import st_navbar
import pandas as pd 
import requests

if "authenticated" not in st.session_state:
    st.switch_page("Home.py")

pages, styles, logo, options = get_nav_config(show_home=False)
page = st_navbar(pages, selected="Interests", styles=styles, logo_path=logo, options=options)

if page == "Badges":
  st.switch_page('pages/35_User_Badges.py')

if page == "User Rank":
  st.switch_page('pages/36_Specific_User_Rank.py')

if page == "Logout":
  del st.session_state["role"]
  del st.session_state["authenticated"]
  st.switch_page("Home.py")

interests_fetch = requests.get("http://api:4000/m/interests").json()
interest_count = requests.get("http://api:4000/m/interests/counts").json()

all_interests = []
count = []

for interest in interests_fetch:
  all_interests.append(interest["Name"])

for interest in interest_count: 
  count.append(interest["NumStudents"])


data = {
    'Interests': all_interests,
    'Amount': count
}

df = pd.DataFrame(data)

st.markdown(
    """
    <div>
        <h3 style="color: black; text-align: center;">User Interest Data</h3>
        <div style="height: 100px;"></div> 
    </div>
    """,
    unsafe_allow_html=True,
)

st.bar_chart(df.set_index('Interests'), y_label='Number of Students', x_label='Interests')