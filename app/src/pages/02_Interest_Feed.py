import logging
logger = logging.getLogger(__name__)
import streamlit as st
from modules.nav import get_nav_config
from streamlit_navigation_bar import st_navbar
import requests
from datetime import datetime


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

#for suggested friend requests
kali_suggested = requests.get("http://api:4000/u/users/1001/suggestions").json()
suggestions = []
users_fetch = requests.get("http://api:4000/u/users").json()
users = []

#for getting group chats 
chat_fetch = requests.get("http://api:4000/u/users/1001/groupchats").json()
group_chats = []

#for getting interests 
interest_fetch = requests.get("http://api:4000/u/users/1001/interests").json() 
all_interests = []

#for getting events post  
post_interest_fetch = requests.get("http://api:4000/simple/postInterest").json() 
post_interest = []

post_user_fetch = requests.get("http://api:4000/simple/postUser").json() 
post_user = []


curr_creator = []

createdBy = []
description = [] 
endTime = []
startTime = [] 
eventId = [] 
firstName = [] 
lastName = [] 
interest = []
postTitle = [] 
chatName = []
lat = []
longi = []





#suggested friends
for suggested in kali_suggested:
  suggestions.append("{0} {1}".format(suggested["FirstName"], suggested["LastName"]))
for user in users_fetch:
  users.append(("{0} {1}".format(user["FirstName"], user["LastName"]), user["UserId"]))

logger.info(users)

#group chats 
for chat in chat_fetch: 
   group_chats.append(chat["Name"])

#interests
for i in interest_fetch: 
   all_interests.append(i["Name"])


for chat in chat_fetch: 
   group_chats.append(chat["Name"])


for post in post_user_fetch: 
   post_user.append(post)


for post in post_interest_fetch: 
  createdBy.append(post["CreatedBy"])
  description.append(post["Description"])
  endTime.append(datetime.strptime(post["EndTime"], "%a, %d %b %Y %H:%M:%S %Z").strftime("%d %b %Y %H:%M"))
  startTime.append(datetime.strptime(post["StartTime"], "%a, %d %b %Y %H:%M:%S %Z").strftime("%d %b %Y %H:%M"))
  eventId.append(post["EventId"])
  interest.append(post["Interest"])
  postTitle.append(post["PostTitle"]) 
  chatName.append(post["GroupChatName"])
  lat.append(post["Latitude"]) 
  longi.append(post["Longitude"])


for id in eventId:
   for user in post_user: 
      if(id == user["EventId"]): 
        curr_creator.append(user) 


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
            <div class="navbar-pages">
                {"".join([f'<span>{page}</span>' for page in all_interests])}
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
    html_content = ""
    for name, start, end in zip(chatName, startTime, endTime):
        html_content += f"""
        <div onclick="window.location.href='14_GroupChat.py'" 
            style="cursor: pointer; display: flex; flex-direction: column; align-items: flex-start; 
            background-color: rgb(255, 255, 255); padding: 10px; margin-bottom: 10px; 
            border-radius: 10px; width: 100%;">
            <p style="margin: 0; font-weight: bold; font-size: 16px;">{name}</p>
            <p style="margin: 0; font-size: 14px; color: rgb(100, 100, 100);">{start} - {end}</p>
        </div>
        """
        
    # Display group chats
    st.markdown(
        f"""
        <div style="background-color: rgb(255, 255, 255); padding: 20px; border-radius: 10px;">
            <h3 style="color: black; text-align: center;">Group Chats</h3>
            {html_content}
        </div>
        """,
        unsafe_allow_html=True,
    )

    # On the "GroupChatPage.py" page, handle the query parameter
    if "14_GroupChat.py" in st.session_state.get("page", ""):
        chat_name = st.experimental_get_query_params().get("chat", [""])[0]
        st.title(f"Group Chat: {chat_name}")




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
                <input type="text" placeholder="Title of the Event"/>
                <input type="text" placeholder="Date of the Event"/>
                <input type="text" placeholder="Description of the Event"/>
            </div>
            
        </div>
        """,
        unsafe_allow_html=True
    )



    post_content = ""
    for creator in curr_creator:
        post_content += f"""
        <div style="display: flex; flex-direction: column; background-color: rgb(255, 255, 255); padding: 10px; margin-bottom: 10px; border-radius: 10px">
            <div style="display: flex; align-items: center; justify-content: flex-start; margin-bottom: 10px;">
                <div style="display: flex; flex-direction: column;">
                    <h4 style="margin: 0; font-size: 16px;">{creator["FirstName"]} {creator["LastName"]}</h4>
                </div>
                <p style="margin: 0; font-size: 12px; color: gray; margin-left: auto;">{post['date']} | {post['time']}</p>
            </div>
            <p style="margin: 10px 0; font-size: 14px;">{post['description']}</p>
            <img src="https://via.placeholder.com/300x150" alt="Event Image" width="100%">
            <div style="display: flex; align-items: center; justify-content: space-between; margin-top: 10px;">
                <span style="font-size: 20px; color: black; cursor: pointer; padding: 5px;">
                    <i class="fa fa-heart"></i>
                </span>
                <button style="padding: 5px 10px; background-color: #007bff; color: white; border: none; font-weight: bold; border-radius: 5px; cursor: pointer;">Join Group Chat</button>
            </div>
        </div>
        """

    st.markdown(
          f"""
          <div style="background-color: rgb(255, 255, 255); padding: 20px; border-radius: 10px; margin-top: 15px">
              {post_content}
          </div>
          """,
          unsafe_allow_html=True,
      )


# Suggested Profiles in the right column
# Column 3: Suggested for You
def add_friend(friend_id):
  data = {
        "FriendId": friend_id
  }
  try:
      response = requests.post('http://api:4000/u/users/1001/friends', json=data)
      if response.status_code == 200:
          st.success("Friend added successfully!")
      else:
          st.error(f"Error adding friend: {response.text}")
  except requests.exceptions.RequestException as e:
      st.error(f"Error connecting to server: {str(e)}")

if 'button_states' not in st.session_state:
    st.session_state['button_states'] = {profile: False for profile in suggestions}
    
with col3:
  suggested = st.container(border = True)
  for index, profile in enumerate(suggestions):
    st.write(f"**{profile}**")
    friend_id = next(user[1] for user in users if user[0] == profile)

    # Button text based on current state
    button_text = 'Friend Added' if st.session_state['button_states'][profile] else 'Add Friend'

    # Button functionality
    if st.button(button_text, key=f'friend_button_{profile}'):
        if not st.session_state['button_states'][profile]:
            # Call the add_friend function only when the button is in 'Add Friend' state
            add_friend(friend_id)
            # Change the button text to 'Friend Added' after clicking
            st.session_state['button_states'][profile] = True
