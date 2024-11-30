import logging
logger = logging.getLogger(__name__)
import streamlit as st
import requests
from streamlit_extras.app_logo import add_logo
from modules.nav import get_nav_config
from streamlit_navigation_bar import st_navbar

pages, styles, logo, options = get_nav_config(show_home=False)
page = st_navbar(pages, styles=styles, logo_path=logo, options=options)

if page == "Update Location":
  st.switch_page('pages/11_Update_Location.py')

if page == "Calendar":
  st.switch_page('pages/13_Personal_Calendar.py')

if page == "Group Chat":
  st.switch_page('pages/14_GroupChat.py')

if page == "Logout":
  del st.session_state["role"]
  del st.session_state["authenticated"]
  st.switch_page("Home.py")
  
# styling for group chats section
st.markdown(
    """
    <style>
    .group-chat {
        margin-top: 1px;
        padding: 1px;
    }
    .group-chat h3 {
        font-size: 1.5rem;
        font-weight: bold;
        margin-bottom: 10px;
        display: flex;
        align-items: center;
        justify-content: space-between; /* Align the icon to the right */
    }
    .create-chat-icon {
        height: 24px;
        cursor: pointer;
        margin-left: auto; /* Push the icon to the far right */
    }
    .group-chat-search {
        display: flex;
        align-items: center;
        padding: 10px;
        background-color: #f8f8f8;
        border-radius: 20px;
        box-shadow: 1px 1px 4px rgba(0,0,0,0.1);
        margin-bottom: 15px;
    }
    .group-chat-search input {
        border: none;
        outline: none;
        background-color: transparent;
        flex: 1;
        padding-left: 10px;
    }
    .group-chat-search img {
        height: 20px;
        width: 20px;
    }
    .group-chat-item {
        display: flex;
        align-items: center;
        margin-bottom: 15px; /* Adjusted spacing between chat items */
        padding: 10px;
        background-color: #ffffff;
        border-radius: 10px;
        box-shadow: 1px 1px 4px rgba(0,0,0,0.1);
    }
    .group-chat-item img {
        border-radius: 10px;
        height: 60px;
        width: 60px;
        margin-right: 15px;
    }
    .group-chat-item div {
        font-size: 14px;
        flex: 1;
    }
    .group-chat-item div strong {
        display: block;
        font-size: 16px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# create columns for layout
col1, col2 = st.columns([1.3, 4])

# group Chats Section in Left Column
with col1:
    # group chat title with create chat icon
    st.markdown(
        """
        <div class="group-chat">
            <h3>
                Group Chats
                <img src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQ04rOxt6qIkj9mDqd9wTEvL0wa8IiycjGR_Q&s" 
                     class="create-chat-icon" 
                     title="Create Chat" 
                     alt="Create Chat Icon">
            </h3>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # search bar
    st.markdown(
        """
        <div class="group-chat-search">
            <img src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSnPWyKosZe-ytzAr3D130bkyo_KVrD05c0sg&s">
            <input type="text" placeholder="Search Messages">
        </div>
        """,
        unsafe_allow_html=True,
    )

    # group chats content
    group_chats = [
        {"name": "Teatro Carcano El Bella E L...", "last_message": "You: I'm coming!", "image": "https://carlotomeoteatro.com/wp-content/uploads/2023/04/bb1.jpeg?w=1024"},
        {"name": "Agevolazioni Orchestra Fila...", "last_message": "John: I'm excited", "image": "https://santacecilia.it/wp-content/uploads/2024/11/HARDING_KANG_023-1920x1281.jpg"},
        {"name": "Collaborazione con Ponder", "last_message": "Abby: Works for me!", "image": "https://t4.ftcdn.net/jpg/05/49/98/39/360_F_549983970_bRCkYfk0P6PP5fKbMhZMIb07mCJ6esXL.jpg"},
        {"name": "Agevolazioni Serate Musica...", "last_message": "Jenny: Slay", "image": "https://www.fsnews.it/content/dam/fs_news/focus-2022/giugno/servizi/21_06_2022_concerto_apertura.jpg"},
        {"name": "Agevolazioni Fondazione S...", "last_message": "You: What does everyone think?", "image": "https://t4.ftcdn.net/jpg/05/49/98/39/360_F_549983970_bRCkYfk0P6PP5fKbMhZMIb07mCJ6esXL.jpg"},
        {"name": "Cinete Camilano Cloud", "last_message": "You: I can do Friday", "image": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTF4mVorkXgFOVKVuXYQRU-rJ2MQAM6Y6q4xA&s"},
        {"name": "Explore Pavia", "last_message": "You joined the group chat", "image": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTHezNTGIPOQOqTY2ZowLW34Kk1TurBKojfdg&s"},
    ]

    # render group chat items
    for chat in group_chats:
        st.markdown(
            f"""
            <div class="group-chat-item">
                <img src="{chat['image']}" alt="{chat['name']}">
                <div>
                    <strong>{chat['name']}</strong>
                    <span>{chat['last_message']}</span>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown('</div>', unsafe_allow_html=True)

# group chat content
with col2:
    st.markdown(
        """
        <div class="chat-content-container">
            <h3>Teatro Carcano El Bella E La Bestia</h3>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )