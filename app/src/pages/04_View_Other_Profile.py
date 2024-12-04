import logging
logger = logging.getLogger(__name__)
import streamlit as st
from modules.nav import get_nav_config
from streamlit_navigation_bar import st_navbar
import requests

st.set_page_config(page_title="Profile Page", layout="wide")
pages, styles, logo, options = get_nav_config(show_home=False)
page = st_navbar(pages, selected="View Other Profile", styles=styles, logo_path=logo, options=options)

if page == "Feed":
  st.switch_page('pages/02_Interest_Feed.py')

if page == "Update Interests":
  st.switch_page('pages/03_Update_Interests.py')

if page == "Logout":
  del st.session_state["role"]
  del st.session_state["authenticated"]
  st.switch_page("Home.py")

winston_info = requests.get("http://api:4000/u/users/1002").json()
interests_fetch = requests.get("http://api:4000/u/users/1002/interests").json()
winston_interests = []
kali_suggested = requests.get("http://api:4000/u/users/1001/suggestions").json()
suggestions = []
users_fetch = requests.get("http://api:4000/u/users").json()
users = []

for interest in interests_fetch:
  winston_interests.append(interest["Name"])
for suggested in kali_suggested:
  suggestions.append("{0} {1}".format(suggested["FirstName"], suggested["LastName"]))
for user in users_fetch:
  users.append(("{0} {1}".format(user["FirstName"], user["LastName"]), user["UserId"]))

logger.info(users)

# Layout: Profile and Additional Info
profile_col1, profile_col2 = st.columns([3,1])
with profile_col1:
    # Profile Section
    profile = st.container(border=True)
    profile.image("assets/bg_winston.jpg")
    profile.divider()

    col1, col2 = profile.columns([2,3])
    with col1:
       st.image("assets/winston.jpg", width=200)
    with col2:
      st.write("##### {0} {1}".format(winston_info[0]["FirstName"], winston_info[0]["LastName"]))
      st.write("{0}".format(winston_info[0]["Pronouns"]))
      st.write("Milan, Italy")
      st.write("{0} Points".format(winston_info[0]["Points"]))

    # Bio Section
    bio = st.container(border=True)
    bio.text_area("Bio", "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostru.\n" + 
      "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostru.", 170)

    # Interests Section
    interests = st.container(border=True)
    interests.write("### Interests")
    interests.markdown(
        """
        <style>
            .interest-tag {
                display: inline-block;
                background-color: #d6bcfa;
                color: white;
                padding: 8px 12px;
                margin: 5px;
                border-radius: 15px;
                font-size: 14px;
                font-weight: bold;
                text-align: center;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )

    # Static interests
    interests_html = "".join(f"<span class='interest-tag'>{interest}</span>" for interest in winston_interests)

    interests.markdown(interests_html, unsafe_allow_html=True)

# Column 2: Suggested for You
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
    
with profile_col2:
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