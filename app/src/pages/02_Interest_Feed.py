import logging
logger = logging.getLogger(__name__)
import streamlit as st
from modules.nav import get_nav_config
from streamlit_navigation_bar import st_navbar

pages, styles, logo, options = get_nav_config(show_home=False)
page = st_navbar(pages, styles=styles, logo_path=logo, options=options)

pages = ["Pets", "Photography", "LGBTQ+"]
st.markdown(
        f"""
        <style>
        .navbar {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            background-color: rgb(198,169,249);
            padding: 0.5rem 1rem;
        }}
        .navbar-logo {{
            margin-right: auto;
        }}
        .navbar-logo img {{
            height: 50px;
        }}
        .navbar-pages {{
            margin-left: auto;
            display: flex;
            gap: 1rem;
        }}
        .navbar-pages span {{
            border-radius: 0.5rem;
            color: rgb(49, 51, 63);
            padding: 0.4375rem 0.625rem;
            cursor: pointer;
        }}
        .navbar-pages span:hover {{
            background-color: rgba(255, 255, 255, 0.35);
        }}
        </style>
        <div class="navbar">
            <div class="navbar-logo">
                <img src="{logo}" alt="Logo">
            </div>
            <div class="navbar-pages">
                {"".join([f'<span>{page}</span>' for page in pages])}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

# Add some spacing below the navigation bar so it doesn't overlap with content
st.markdown("<div style='margin-top: 60px;'></div>", unsafe_allow_html=True)

# Layout with columns
col1, col2, col3 = st.columns([1, 2, 1])

with col1:
    # Sidebar content
    st.markdown(
        """
        <div style="
            background-color: rgb(198, 169, 249);
            padding: 20px;
            border-radius: 10px;
        ">
            <h3 style="color: white;">Column 1 Content</h3>
            <p style="color: white;">This column has a background color.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.header("Group Chats")
    group_chats = [
        {"name": "The Huntington Library", "time": "11:00 AM - 2:00 PM"},
        {"name": "USC Pacific Asia Museum", "time": "1:00 PM - 3:00 PM"},
        {"name": "Wrigley Mansion", "time": "3:00 PM - 5:00 PM"},
        {"name": "Norton Simon Museum", "time": "12:00 PM - 2:00 PM"},
        {"name": "Explore Pasadena", "time": "2:00 PM - 4:00 PM"}
    ]
    for chat in group_chats:
        st.write(f"**{chat['name']}**")
        st.write(f"{chat['time']}")
        st.markdown("---")
    st.markdown('</div>', unsafe_allow_html=True)

# Main Feed in the center column
with col2:
    st.markdown('<div class="feed">', unsafe_allow_html=True)
    st.text_input("Post about an event...", placeholder="Write something...")
    st.markdown("""
        <div class="post">
            <h4>Winston Church.</h4>
            <p>November 6, 2024<br>10:00 AM - 2:00 PM</p>
            <p>Lorem ipsum dolor sit amet consectetur. Porttitor.</p>
            <img src="https://via.placeholder.com/300x150" alt="Event Image">
            <button style="margin-top: 10px;">Join Group Chat</button>
        </div>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# Suggested Profiles in the right column
with col3:
    st.markdown('<div class="suggested">', unsafe_allow_html=True)
    st.header("Suggested for You")
    suggested_profiles = ["Alessandro Rossi", "Giovanni Conti", "Ethan Walker", "Ava Taylor", "Mia Johnson"]
    for profile in suggested_profiles:
        st.write(f"**{profile}**")
        st.button("Follow")
    st.markdown('</div>', unsafe_allow_html=True)
