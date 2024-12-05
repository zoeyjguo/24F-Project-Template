import logging
logger = logging.getLogger(__name__)
import streamlit as st
from modules.nav import get_nav_config
from streamlit_navigation_bar import st_navbar
import requests
from datetime import datetime

# Setup navigation
pages, styles, logo, options = get_nav_config(show_home=False)
page = st_navbar(pages, styles=styles, logo_path=logo, options=options)

# Page switching logic
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

# Fetch data from APIs
kali_suggested = requests.get("http://api:4000/u/users/1001/suggestions").json()
suggestions = []
users_fetch = requests.get("http://api:4000/u/users").json()
users = []

# For getting group chats
chat_fetch = requests.get("http://api:4000/u/users/1001/groupchatsInfo").json()
group_chats = []

# For getting interests
interest_fetch = requests.get("http://api:4000/u/users/1001/interests").json()
all_interests = []

# For getting events posts
post_interest_fetch = requests.get("http://api:4000/simple/postInterest").json()
post_interest = []

post_user_fetch = requests.get("http://api:4000/simple/postUser").json()
post_user = []

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

# Post details
for post in post_user_fetch:
    post_user.append(post)



# # Match posts with creators
# for id in eventId:
#     for user in post_user:
#         if id == user["EventId"]:
#             curr_creator.append(user)

# Custom Navbar Styling
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


# Layout spacing
st.markdown("<div style='margin-top: 60px;'></div>", unsafe_allow_html=True)

# Layout with columns
col1, col2, col3 = st.columns([1, 2, 1])

with col1:
    # Display group chats
    st.title("Group Chats")
    
    for chat in group_chats:
        group_name = chat['Name']
        start_date = chat['StartTime']
        end_date = chat['EndTime']
        
    
        # Button text will show the group name and dates
        button_text = f"{group_name} ({start_date} - {end_date})"
        
        # Button functionality for redirecting to '04_groupchats' page
        if st.button(button_text, key=f'group_chat_button_{group_name}'):
            st.session_state.selected_chat_id = chat['GroupChatId']
            st.switch_page('pages/14_GroupChat.py')


def update_event(endpoint_url, data):
    try:
        response = requests.put(endpoint_url, json=data)
        if response.status_code == 200:
            st.success("Event updated successfully!")
        else:
            st.error(f"Failed to update event. Status code: {response.status_code}")
    except Exception as e:
        st.error(f"An error occurred: {e}")


with col2:
    
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
    with st.container():
        title = st.text_input("Add Post Title", placeholder="Post Title")
                
        date_col, time_col = st.columns([1, 1])
        with date_col:
            date = st.date_input("", label_visibility="collapsed")  # Date picker
        with time_col:
            time = st.time_input("", label_visibility="collapsed")
                
        description = st.text_area("Add Description", placeholder="Event Description")
            
        # Submit button that spans the whole section
        if st.button("Submit", key="submit", use_container_width=True):
            # Prepare data for PUT request
            event_data = {
                "title": title,
                "date": str(date),  # Convert date to string
                "time": str(time),  # Convert time to string
                "description": description,
            }

            # Example endpoint URL (replace with your actual endpoint)
            endpoint = "https://example.com/api/update-event"

            # Make the PUT request
            update_event(endpoint, event_data)   


    # # Display posts
    # post_content = ""
    # for creator in curr_creator:
    #     post_content += f"""
    #     <div style="display: flex; flex-direction: column; background-color: rgb(255, 255, 255); padding: 10px; margin-bottom: 10px; border-radius: 10px">
    #         <div style="display: flex; align-items: center; justify-content: flex-start; margin-bottom: 10px;">
    #             <div style="display: flex; flex-direction: column;">
    #                 <h4 style="margin: 0; font-size: 16px;">{creator["FirstName"]} {creator["LastName"]}</h4>
    #             </div>
    #             <p style="margin-left: auto; color: grey; font-size: 12px;">{startTime}</p>
    #         </div>
    #         <p>{description}</p>
    #     </div>
    #     """
    # st.markdown(post_content, unsafe_allow_html=True)


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
  st.title("Suggested")
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
