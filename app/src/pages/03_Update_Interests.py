import logging
logger = logging.getLogger(__name__)
import streamlit as st
from modules.nav import get_nav_config
from streamlit_navigation_bar import st_navbar
import requests

st.set_page_config(page_title="Profile Page", layout="wide")
pages, styles, logo, options = get_nav_config(show_home=False)
page = st_navbar(pages, selected="Update Interests", styles=styles, logo_path=logo, options=options)

if page == "Feed":
  st.switch_page('pages/02_Interest_Feed.py')

if page == "View Other Profile":
  st.switch_page('pages/04_View_Other_Profile.py')

if page == "Logout":
  del st.session_state["role"]
  del st.session_state["authenticated"]
  st.switch_page("Home.py")

kali_info = requests.get("http://api:4000/u/users/1001").json()
kali_interests = requests.get("http://api:4000/u/users/1001/interests").json()
current_interests = []
kali_groupchats = requests.get("http://api:4000/u/users/1001/groupchats").json()
current_groupchats = []
groupchat_info = []
interests_fetch = requests.get("http://api:4000/simple/interests").json()
all_interests = []

for interest in kali_interests:
  current_interests.append(interest["Name"])
for groupchat in kali_groupchats:
  groupchat_info.append((groupchat["Name"], groupchat["GroupChatId"]))
  current_groupchats.append(groupchat["Name"])
for interest in interests_fetch:
  all_interests.append(interest["Name"])

# Layout: Profile and Additional Info
st.write("## Edit Profile")
profile_col1, profile_col2 = st.columns([11,9])
with profile_col1:
    # Profile Section
    profile = st.container(border=True)
    profile.image("assets/bg_kali.jpg")
    profile.divider()

    col1, col2 = profile.columns([2,3])
    with col1:
       st.image("assets/kali.jpg", width=200)
    with col2:
      st.write("##### {0} {1}".format(kali_info[0]["FirstName"], kali_info[0]["LastName"]))
      st.write("{0}".format(kali_info[0]["Pronouns"]))
      st.write("{0} Points".format(kali_info[0]["Points"]))

    # Information Section
    information = st.container(border=True)
    information.write("##### Information")
    information.text_area("Username", "kali_linux", 68)
    information.text_area("Email Address", "lin.k@northeastern.edu", 68)
    information.text_area("Phone Number", "4324123903", 68)
    information.text_area("Location", "Pasadena, California", 68)

# Right column: Bio, Interests, and Group Chats
with profile_col2:
    # Bio Section
    bio = st.container(border=True)
    bio.text_area("Bio", "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostru.\n" + 
      "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostru.", 170)

    # Interests Section
    def update_interests():
      # if deleted interest
      if len(selected_interests) < len(current_interests):
        for interest in current_interests:
           if interest not in selected_interests:
              data = {
                "InterestId": all_interests.index(interest)+1
              }
              try:
                response = requests.delete('http://api:4000/u/users/1001/interests', json=data)
                if response.status_code == 200:
                  st.success("Interest deleted successfully!")
                else:
                  st.error(f"Error deleting interest: {response.text}")
              except requests.exceptions.RequestException as e:
                st.error(f"Error connecting to server: {str(e)}")
      # if added interest
      else:
        for interest in selected_interests:
          if interest not in current_interests:
              data = {
                "InterestId": all_interests.index(interest)+1
              }
              try:
                response = requests.post('http://api:4000/u/users/1001/interests', json=data)
                if response.status_code == 200:
                  st.success("Interest added successfully!")
                else:
                  st.error(f"Error adding interest: {response.text}")
              except requests.exceptions.RequestException as e:
                st.error(f"Error connecting to server: {str(e)}")

    interests = st.container(border=True)
    interests.write("#### Interests")
    selected_interests = interests.multiselect("Add More Interests", all_interests, current_interests)

    placeholder1 = st.empty()
    placeholder1.write(selected_interests)
    placeholder1.empty()

    update_interests()

    # Group Chats Section
    def delete_groupchat():
      for gc in current_groupchats:
        if gc not in selected_groupchats:
          for groupchat in groupchat_info:
            if gc == groupchat[0]:
              index = groupchat[1]
              break
          data = {
            "GroupChatId": index
          }
          logger.info(data)
          try:
            response = requests.delete('http://api:4000/u/users/1001/groupchats', json=data)
            if response.status_code == 200:
              st.success("Group chat deleted successfully!")
            else:
              st.error(f"Error deleting group chat: {response.text}")
          except requests.exceptions.RequestException as e:
            st.error(f"Error connecting to server: {str(e)}")

    groupchats = st.container(border=True)
    groupchats.write("#### Group Chats")
    selected_groupchats = groupchats.multiselect("Leave a group chat", current_groupchats, current_groupchats)
    logger.info(groupchat_info)

    placeholder2 = st.empty()
    placeholder2.write(selected_groupchats)
    placeholder2.empty()

    delete_groupchat()

    st.markdown(
    f"""
    <style>
        .profile-container {{
            display: flex;
            flex-direction: column;
            align-items: center;
            background-color: #f0f0f0;
            border-radius: 15px;
            padding: 20px;
            max-width: 800px;
            margin: auto;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }}

        .background-image {{
            width: 100%;
            height: 300px;
            background-image: url('./app/static/bg_kali.jpg');
            background-size: cover;
            background-position: center;
            border-radius: 15px 15px 0 0;
            position: relative;
        }}

        .profile-picture {{
            width: 120px;
            height: 120px;
            background-image: url('./app/static/kali.jpg');
            background-size: cover;
            background-position: center;
            border-radius: 15px;
            border: 3px solid white;
            position: absolute;
            bottom: -60px;
            left: 30px;
        }}

        .info-container {{
            background-color: white;
            width: 100%;
            border-radius: 0 0 15px 15px;
            padding: 20px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            box-sizing: border-box;
        }}

        .info-left {{
            margin-left: 150px;
        }}

        .name {{
            font-size: 24px;
            font-weight: bold;
            margin-bottom: 5px;
        }}

        .pronouns {{
            font-size: 16px;
            color: gray;
        }}

        .points-container {{
            display: flex;
            align-items: center;
            font-size: 16px;
            font-weight: bold;
        }}

        .points-container img {{
            width: 20px;
            height: 20px;
            margin-left: 5px;
        }}
    </style>
    """,
    unsafe_allow_html=True,
)

# Layout HTML
st.markdown(
    """
    <div class="profile-container">
        <div class="background-image">
            <div class="profile-picture">
              <img src="/assets/kali.jpg" alt="Kali Profile Picture">
            </div>
        </div>
        <div class="info-container">
            <div class="info-left">
                <div class="name">Kali Linux</div>
                <div class="pronouns">She/Her</div>
            </div>
            <div class="points-container">
                512 Points
                <img src="https://img.icons8.com/ios-filled/50/null/trophy.png" alt="Trophy Icon">
            </div>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)