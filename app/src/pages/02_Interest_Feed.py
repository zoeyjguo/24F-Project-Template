import logging
logger = logging.getLogger(__name__)
import streamlit as st
from modules.nav import get_nav_config
from streamlit_navigation_bar import st_navbar

pages, styles, logo, options = get_nav_config(show_home=False)
page = st_navbar(pages, styles=styles, logo_path=logo, options=options)


if page == "Feed":
  st.switch_page('pages/02_Interest_Feed.py')

if page == "Update Interests":
  st.switch_page('pages/03_Update_Interests.py')

if page == "View Other Profile":
  st.switch_page('pages/04_View_Other_Profile.py')

if page == "Logout":
  del st.session_state["role"]
  del st.session_state["authenticated"]
  st.switch_page("Home.py")

  
kali = "app/src/assets/kali.jpg"

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
                <img src="{logo}" alt="logo">
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

    # Group chat content
    group_chats = [
      {"name": "The Huntington Library", "time": "11:00 AM - 2:00 PM", "image": "https://via.placeholder.com/50"},
      {"name": "USC Pacific Asia Museum", "time": "1:00 PM - 3:00 PM", "image": "https://via.placeholder.com/50"},
      {"name": "Wrigley Mansion", "time": "3:00 PM - 5:00 PM", "image": "https://via.placeholder.com/50"},
      {"name": "Norton Simon Museum", "time": "12:00 PM - 2:00 PM", "image": "https://via.placeholder.com/50"},
      {"name": "Explore Pasadena", "time": "2:00 PM - 4:00 PM", "image": "https://via.placeholder.com/50"}
    ] 

      # Build the HTML content dynamically using a for loop
    html_content = ""
    for chat in group_chats:
        html_content += f"""
        <div style="display: flex; align-items: center; justify-content: space-between; background-color: rgb(255, 255, 255); padding: 10px; margin-bottom: 10px; border-radius: 10px;">
            <div style="display: flex; align-items: center;">
                <img src="{chat['image']}" alt="{chat['name']}'s profile" style="border-radius: 10px; width: 50px; height: 50px; margin-right: 10px;">
                <p style="margin: 0; font-weight: normal;">
                <strong>{chat['name']}</strong><br> 
                {chat['time']}
                </p>
            </div>
        </div>
        """

    # Pass the HTML content to st.markdown
    st.markdown(
        f"""
        <div style="background-color: rgb(255, 255, 255); padding: 20px; border-radius: 10px;">
            <h3 style="color: black; text-align: center;">Group Chats</h3>
            {html_content}
        </div>
        """,
        unsafe_allow_html=True,
    )





with col2:
    # Custom container with the white background, logo, and input field
    st.markdown(
        f""" 
        <style>
        .custom-container {{
            background-color: white;
            padding: 20px;
            border-radius: 10px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }}
        .custom-container img {{
            width: 10%;  /* Set the logo to take up 20% of the container width */
            border-radius: 50%;
        }}
        .custom-container .input {{
            width: 90%;  /* Set the input to take up 80% of the container width */
        }}
        .custom-container input {{
            width: 100%;  /* Make the input fill its container */
            padding: 10px;
            border-radius: 8px;
            border: 1px solid #ccc;
            background-color: #e7e7e7;
            text-color: black;
        }}
        .input-icon {{
            position: absolute;
            right: 35px; 
            top: 45px;
            transform: translateY(-50%);
            font-size: 18px;
            color: #888;
        }}
        </style>
        <head>
          <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css">
        </head>
        <div class="custom-container">
            <img src="https://via.placeholder.com/50x50" alt="kali" style="border-radius: 8px; width: 50px; height: 50px;">
            <div class="input">
                <i class="input-icon fa fa-paper-plane"></i>  <!-- Paper airplane icon -->
                <input type="text" placeholder="Post about an event..."/>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


    posts = [
      {"name": "Winston Church", "username": "Winston", "img_url": "https://via.placeholder.com/50", "date": "November 6, 2024","time": "10:00 AM - 2:00 PM", "time-posted-ago": "1 hour", "description": "Lorem ipsum dolor sit amet consectetur. Porttitor."}
    ]

    # post_content = ""
    # for post in posts:
    #     html_content += f"""
    #     <div style="display: flex; align-items: center; justify-content: space-between; background-color: rgb(255, 255, 255); padding: 10px; margin-bottom: 10px; border-radius: 10px;">
    #         <div style="display: flex; align-items: center;">
    #             <img src="{post['img_url']}" alt="{post['name']}'s profile" style="border-radius: 10px; width: 50px; height: 50px; margin-right: 10px;">
    #             <p style="margin: 0; font-weight: normal;">{post['username']}</p>
                
    #         </div>
    #         <button style="padding: 5px 10px; background-color: #e7e7e7; color: black; border: none; font-weight: bold; border-radius: 5px; cursor: pointer;">Follow</button>
    #     </div>
    #     """
    # Post content in the main feed
    st.markdown("""
        <div class="post">
            <h4>Winston Church.</h4>
            <p>November 6, 2024<br>10:00 AM - 2:00 PM</p>
            <p>Lorem ipsum dolor sit amet consectetur. Porttitor.</p>
            <img src="https://via.placeholder.com/300x150" alt="Event Image" width="100%">
            <button style="margin-top: 10px;">Join Group Chat</button>
        </div>
    """, unsafe_allow_html=True)




# Suggested Profiles in the right column
with col3:
     
    suggested_profiles = [
      {"name": "Alessandro Rossi", "img_url": "https://via.placeholder.com/50"},  # Placeholder image URL
      {"name": "Giovanni Conti", "img_url": "https://via.placeholder.com/50"},
      {"name": "Ethan Walker", "img_url": "https://via.placeholder.com/50"},
      {"name": "Ava Taylor", "img_url": "https://via.placeholder.com/50"},
      {"name": "Mia Johnson", "img_url": "https://via.placeholder.com/50"},
      {"name": "Sofia De Luca", "img_url": "https://via.placeholder.com/50"},
      {"name": "Adrien Greco", "img_url": "https://via.placeholder.com/50"}
    ]

    # Build the HTML content dynamically using a for loop
    html_content = ""
    for profile in suggested_profiles:
        html_content += f"""
        <div style="display: flex; align-items: center; justify-content: space-between; background-color: rgb(255, 255, 255); padding: 10px; margin-bottom: 10px; border-radius: 10px;">
            <div style="display: flex; align-items: center;">
                <img src="{profile['img_url']}" alt="{profile['name']}'s profile" style="border-radius: 10px; width: 50px; height: 50px; margin-right: 10px;">
                <p style="margin: 0; font-weight: normal;">{profile['name']}</p>
            </div>
            <button style="padding: 5px 10px; background-color: #e7e7e7; color: black; border: none; font-weight: bold; border-radius: 5px; cursor: pointer;">Follow</button>
        </div>
        """

    # Pass the HTML content to st.markdown
    st.markdown(
        f"""
        <div style="background-color: rgb(255, 255, 255); padding: 20px; border-radius: 10px;">
            <h3 style="color: black; text-align: center;">Suggested for you</h3>
            {html_content}
        </div>
        """,
        unsafe_allow_html=True,
    )
