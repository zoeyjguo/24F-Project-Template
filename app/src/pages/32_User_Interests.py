import streamlit as st
from modules.nav import get_nav_config
from streamlit_navigation_bar import st_navbar
import pandas as pd 

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


data = {
    'Interests': ['LGBTQA+', 'Art', 'Music', 'Dance', 'Sports'],
    'Amount': [150, 200, 120, 180, 220]
}

df = pd.DataFrame(data)

st.markdown(
    """
    <div>
        <h3 style="color: black; text-align: center;">Interest Ranking</h3>

    </div>
    """,
    unsafe_allow_html=True,
)

st.bar_chart(df.set_index('Interests'))