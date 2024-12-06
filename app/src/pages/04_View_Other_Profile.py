import logging
logger = logging.getLogger(__name__)
import streamlit as st
from modules.nav import get_nav_config
from streamlit_navigation_bar import st_navbar
import requests

if "authenticated" not in st.session_state:
    st.switch_page("Home.py")

st.set_page_config(page_title="Profile Page", layout="wide")
pages, styles, logo, options = get_nav_config(show_home=False)
page = st_navbar(pages, selected="View Other Profile", styles=styles, logo_path=logo, options=options)

if page == "Feed":
  st.switch_page('pages/02_Interest_Feed.py')

if page == "Update Interests":
  st.switch_page('pages/03_Update_Interests.py')

if page == "Group Chat":
    st.switch_page("pages/001_Kali_GroupChat.py")

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
profile_col1, profile_col2, profile_col3 = st.columns([3,.1,1])
with profile_col1:
    st.markdown(
    """
    <style>
        .profile-container {
            display: flex;
            flex-direction: column;
            align-items: center;
            background-color: #f0f0f0;
            border-radius: 15px;
            padding: 20px;
            max-width: 1000px;
            margin: auto;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }

        .background-image {
            width: 100%;
            height: 150px;
            background-image: url('https://media.istockphoto.com/id/149153272/photo/pargue-detail-from-lennon-wall.jpg?s=612x612&w=0&k=20&c=CWBjwvfoqR4zdA2m3wA7sHSe_llBxnSckuVM0VxCJ48=');
            background-size: cover;
            background-position: center;
            border-radius: 15px 15px 0 0;
        }

        .profile-picture {
            width: 120px;
            height: 120px;
            background-image: url('https://i0.wp.com/picjumbo.com/wp-content/uploads/portrait-of-smiling-young-african-man-in-suit-free-photo.jpg?w=600&quality=80');
            background-size: cover;
            background-position: center;
            border-radius: 50%;
            border: 3px solid white;
            margin-top: -60px;
        }

        .info-container {
            background-color: white;
            width: 100%;
            border-radius: 0 0 15px 15px;
            padding: 20px;
            box-sizing: border-box;
            text-align: center;
        }

        .name {
            font-size: 24px;
            font-weight: bold;
            margin-bottom: 5px;
        }

        .pronouns {
            font-size: 16px;
            color: gray;
        }

        .points-container {
            margin-top: 10px;
            font-size: 16px;
            font-weight: bold;
            display: flex;
            align-items: center;
            justify-content: center;
        }

        .points-container img {
            width: 20px;
            height: 20px;
            margin-left: 5px;
        }
    </style>
    """,
    unsafe_allow_html=True,
    )

    winston_name = "{0} {1}".format(winston_info[0]["FirstName"], winston_info[0]["LastName"])
    winston_pronouns = "{0}".format(winston_info[0]["Pronouns"])
    winston_points = "{0} Points".format(winston_info[0]["Points"])
    # HTML layout for the profile
    st.markdown(
        f"""
        <div class="profile-container">
            <div class="background-image"></div>
            <div class="profile-picture"></div>
            <div class="info-container">
                <div class="name">{winston_name}</div>
                <div class="pronouns">{winston_pronouns}</div>
                <div class="pronouns">Milan, Italy</div>
                <div class="points-container">
                    {winston_points}
                    <img src="https://img.icons8.com/ios-filled/50/null/trophy.png" alt="Trophy Icon">
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.write("")
    st.write("")

    bio, interests = st.columns([1,1])
    # Bio Section
    with bio:
      bio_cont = st.container(border=True)
      bio_cont.text_area("Bio", "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostru.\n" + 
      "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostru.", 136)

    with interests:
      # Interests Section
      interests_cont = st.container(border=True)
      interests_cont.write("### Interests")
      interests_cont.markdown(
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

      interests_cont.markdown(interests_html, unsafe_allow_html=True)

with profile_col2:
   st.empty()

# Column 3: Suggested for You
def add_friend(friend_id):
  data = {
        "FriendId": friend_id
  }
  try:
      response = requests.post('http://api:4000/u/users/1001/friends', json=data)
      if response.status_code == 200:
          logger.info("Friend added successfully!")
          try:
             response = requests.delete('http://api:4000/u/users/1001/suggestions', json=data)
          except requests.exceptions.RequestException as e:
             logger.error(f"Error connecting to server: {str(e)}")
      else:
          logger.error(f"Error adding friend: {response.text}")
  except requests.exceptions.RequestException as e:
      logger.error(f"Error connecting to server: {str(e)}")

if 'button_states' not in st.session_state:
    st.session_state['button_states'] = {profile: False for profile in suggestions}
    
with profile_col3:
  suggested = st.container(border = True)
  st.write("#### Suggested for you")
  st.write("")
  col1, col2 = st.columns([1,1])
  with col1:
     for profile in suggestions:
        st.write(f"**{profile}**")
        st.write("")
  with col2:
    for index, profile in enumerate(suggestions):
      
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