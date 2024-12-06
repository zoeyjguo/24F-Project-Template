import logging
logger = logging.getLogger(__name__)
import streamlit as st
from modules.nav import get_nav_config
from streamlit_navigation_bar import st_navbar
import numpy as np
import requests
from datetime import datetime
import math

if "authenticated" not in st.session_state:
    st.switch_page("Home.py")

# Setup navigation
pages, styles, logo, options = get_nav_config(show_home=False)
page = st_navbar(pages, selected="Feed", styles=styles, logo_path=logo, options=options)

if page == "Update Interests":
    st.switch_page('pages/03_Update_Interests.py')

if page == "View Other Profile":
    st.switch_page('pages/04_View_Other_Profile.py')

if page == "Logout":
    del st.session_state["role"]
    del st.session_state["authenticated"]
    st.switch_page("Home.py")

if page == "Group Chat":
    st.switch_page("pages/001_Kali_GroupChat.py")

# Fetch data from APIs
kali_suggested = requests.get("http://api:4000/u/users/1001/suggestions").json()
suggestions = []
users_fetch = requests.get("http://api:4000/u/users").json()
users = []

location = requests.get("http://api:4000/u/users/1001/location").json()

# For getting group chats
chat_fetch = requests.get("http://api:4000/u/users/1001/groupchatsInfo").json()
group_chats = []

# For getting interests
interest_fetch = requests.get("http://api:4000/u/users/1001/interests").json()
all_interests = []

all_interest_fetch = requests.get("http://api:4000/m/interests").json()
all_interests_info = []

post_creators_fetch = requests.get("http://api:4000/u/users/postCreators").json() 
post_creators = []

#
# Processing API data
for suggested in kali_suggested:
    suggestions.append(f"{suggested['FirstName']} {suggested['LastName']}")
for user in users_fetch:
    users.append((f"{user['FirstName']} {user['LastName']}", user['UserId']))

logger.info(users)

# Group chats
for chat in chat_fetch:
    group_chats.append(chat)

# Interests
for i in interest_fetch:
    all_interests.append(i['Name'])

for i in all_interest_fetch: 
    all_interests_info.append(i) 

currInterests = [] 
for name in all_interests:
    for interest in all_interests_info:
        if name == interest["Name"]: 
            currInterests.append(interest) 

for creators in post_creators_fetch: 
    post_creators.append(creators) 

if "selected_interest" not in st.session_state:
    st.session_state.selected_interest = all_interests[0]  # Set a default selected interest

# Function to handle interest selection (updating session state)
def select_interest(page):
    st.session_state.selected_interest = page

col_count = len(all_interests)  # Number of columns needed (one per button)
columns = st.columns(col_count)

# Loop through the list of interests and create a button in each column
for idx, page in enumerate(all_interests):
    with columns[idx]:
        if st.button(page, key=page):
            select_interest(page)

st.markdown("---")

# Layout with columns
col1, btw1, col2, btw2, col3 = st.columns([1, 0.1, 2, 0.1, 1])

if "selected_chat_id" not in st.session_state:
    st.session_state.selected_chat_id = 399

# group chats section in the left column
with col1:
    st.markdown("### Group Chats")
    for chat in group_chats:
        if st.button(f'{chat["Name"]}'):
            st.session_state["selected_chat_id"] = chat['GroupChatId']
            st.session_state['authenticated'] = True
            st.switch_page('pages/001_Kali_GroupChat.py')
            st.rerun()
        st.markdown("<div style='margin-top: 10px;'></div>", unsafe_allow_html=True)



with btw1: 
    st.empty()

def join_groupchat(groupchat_id):
  data = {
        "UserId": 1001
  }
  try:
      response = requests.post(f'http://api:4000/g/groupchats/{groupchat_id}/members', json=data)
      if response.status_code == 200:
          st.info("Group chat joined successfully!")
      else:
          logger.error(f"Error joining group chat: {response.text}")
  except requests.exceptions.RequestException as e:
      logger.error(f"Error connecting to server: {str(e)}")


def add_post(title, startTime, description, lat, long, points): 
    data = {
        "Title": title,
        "StartTime": startTime,
        "Description": description, 
        "Latitude": lat, 
        "Longitude": long,
        "PointsWorth": points
    }

    try:
        response = requests.post('http://api:4000/u/users/1001/posts', json=data)
        if response.status_code == 200:
            st.success("Post added successfully!")
        else:
            st.error(f"Error adding post: {response.text}")
    except requests.exceptions.RequestException as e:
        st.error(f"Error connecting to server: {str(e)}")

with col2:
    st.markdown("### Make Post")
   # Add custom CSS to style the inputs
    st.markdown(
        '''
        <style>
            .stTextInput, .stDateInput, .stTimeInput, .stTextArea {
                background-color: white;
                border-radius: 5px;
                padding: 10px;
                width: 100%;
            }
            .stButton>button {
                width: 100%;  # Make the submit button span the entire width
                background-color: #4CAF50;  # Optional: customize button color
                color: white;
                font-size: 16px;
                padding: 10px;
                border-radius: 5px;
            }
        </style>
        ''',
        unsafe_allow_html=True
    )

    # Event form inputs
    with st.container(border=True):
        title = st.text_input("Add Post Title", placeholder="Post Title")
                
        date_col, time_col = st.columns([1, 1])
        with date_col:
            date = st.date_input("Add Date", label_visibility="visible")  # Date picker
        with time_col:
            time = st.time_input("Add Time", label_visibility="visible")
        lat_col, long_col = st.columns([1, 1])
        with lat_col:
            lat = st.text_input("Add Latitude", placeholder="Event Latitude")
        with long_col:
            long = st.text_input("Add Longitude", placeholder="Event Longitude")

        points = st.text_input("Points Worth", placeholder="Event Points Worth")
                
        description = st.text_area("Add Description", placeholder="Event Description")
            
        # Submit button that spans the whole section
        if st.button("Submit", key="submit", use_container_width=True):
            add_post(title, '{0}'.format(datetime.combine(date, time)), description, float(lat), float(long), int(points))   

    def get_InterestId(): 
        for interest in currInterests: 
            if interest["Name"] == st.session_state.selected_interest: 
                return interest["InterestId"]
  
    interestId = get_InterestId() 

    # For getting posts with their correlated interest 
    post_interest_fetch = requests.get(f"http://api:4000/m/posts/{interestId}").json()
    currPosts = []

    for post in post_interest_fetch: 
        if (math.fabs(location[0]["Latitude"] - post["Latitude"]) <= 0.15 and math.fabs(location[0]["Longitude"] == post["Longitude"]) <= 0.15):
            currPosts.append(post)

    if 'post_button_states' not in st.session_state:
        st.session_state['post_button_states'] = {}

    currPosts.sort(key=lambda x: datetime.strptime(x["StartTime"], "%a, %d %b %Y %H:%M:%S GMT"), reverse=True)
    post_w_creator = []
    for post in currPosts: 
        for creator in post_creators: 
            if post["CreatedBy"] == creator["CreatedBy"]: 
                c = creator
        post_w_creator.append({
            "post": post,
            "creator": c
        })
        
    for index, post in enumerate(post_w_creator):
        st.markdown(
            f"""
            <div style="display: flex; flex-direction: column; background-color: rgb(255, 255, 255); padding: 10px; margin-bottom: 20px; border-radius: 10px">
                <div style="display: flex; align-items: center; justify-content: flex-start; margin-bottom: 10px;">
                    <div style="display: flex; flex-direction: column;">
                        <p>{post['creator']['FirstName']} {post['creator']['LastName']}</p>
                    </div>
                    <p style="margin-left: auto; color: grey; font-size: 12px;">{post['post']['StartTime']} - {post['post']['EndTime']}</p>
                </div>
                <p style="font-size: 24px;"><strong>{post['post']['Title']}</strong></p>
                <p>Description: {post['post']['Description']}</p>
            </div>
            """,
            unsafe_allow_html=True
        )

        groupchat_id = post['post']["EventId"]

        if index not in st.session_state['post_button_states']:
            st.session_state['post_button_states'][index] = False

        gc_button_text = 'Group Chat Joined' if st.session_state['post_button_states'][index] else 'Join Group Chat'

        if st.button(gc_button_text, key=f"join_button_{index}"):
            st.session_state['post_button_states'][index] = True
            join_groupchat(groupchat_id)  

        st.markdown("<div style='margin-top: 30px;'></div>", unsafe_allow_html=True)

with btw2:
    st.empty()

# Column 3: Suggested for You
def add_friend(friend_id):
    data = {"FriendId": friend_id}
    try:
        response = requests.post(f'http://api:4000/u/users/1001/friends', json=data)
        if response.status_code == 200:
            logger.info("Friend added successfully!")
            # Remove from suggestions after adding
            requests.delete(f'http://api:4000/u/users/1001/suggestions', json=data)
        else:
            logger.error(f"Error adding friend: {response.text}")
    except requests.exceptions.RequestException as e:
        logger.error(f"Error connecting to server: {str(e)}")

if 'button_states' not in st.session_state:
    st.session_state['button_states'] = {profile: False for profile in suggestions}

with col3:
    st.write("#### Suggested for you")
    st.markdown("<div style='margin-bottom: 15px;'></div>", unsafe_allow_html=True)

    for index, profile in enumerate(suggestions):
        friend_id = next(user[1] for user in users if user[0] == profile)

        col1, col2 = st.columns([1.5, 1])
        with col1:
            st.write(f"**{profile}**")
        with col2:
            button_text = 'Friend Added' if st.session_state['button_states'][profile] else 'Add Friend'
            if st.button(button_text, key=f'friend_button_{profile}'):
                if not st.session_state['button_states'][profile]:
                    add_friend(friend_id)
                    st.session_state['button_states'][profile] = True

