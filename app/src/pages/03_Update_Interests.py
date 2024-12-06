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
page = st_navbar(pages, selected="Update Interests", styles=styles, logo_path=logo, options=options)

if page == "Feed":
  st.switch_page('pages/02_Interest_Feed.py')

if page == "View Other Profile":
  st.switch_page('pages/04_View_Other_Profile.py')

if page == "Logout":
  del st.session_state["role"]
  del st.session_state["authenticated"]
  st.switch_page("Home.py")

if page == "Group Chat":
    st.switch_page("pages/001_Kali_GroupChat.py")

kali_info = requests.get("http://api:4000/u/users/1001").json()
kali_interests = requests.get("http://api:4000/u/users/1001/interests").json()
current_interests = []
kali_groupchats = requests.get("http://api:4000/u/users/1001/groupchats").json()
current_groupchats = []
groupchat_info = []
interests_fetch = requests.get("http://api:4000/m/interests").json()
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
            max-width: 800px;
            margin: auto;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }

        .background-image {
            width: 100%;
            height: 300px;
            background-image: url('https://www.psdstack.com/wp-content/uploads/2019/08/copyright-free-images-750x420.jpg');
            background-size: cover;
            background-position: center;
            border-radius: 15px 15px 0 0;
        }

        .profile-picture {
            width: 120px;
            height: 120px;
            background-image: url('https://t4.ftcdn.net/jpg/04/76/97/23/240_F_476972367_qJr5LEhIrfwEih4ECYsPIriFKGpaP3KE.jpg');
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

    kali_name = "{0} {1}".format(kali_info[0]["FirstName"], kali_info[0]["LastName"])
    kali_pronouns = "{0}".format(kali_info[0]["Pronouns"])
    kali_points = "{0} Points".format(kali_info[0]["Points"])
    # HTML layout for the profile
    st.markdown(
        f"""
        <div class="profile-container">
            <div class="background-image"></div>
            <div class="profile-picture"></div>
            <div class="info-container">
                <div class="name">{kali_name}</div>
                <div class="pronouns">{kali_pronouns}</div>
                <div class="points-container">
                    {kali_points}
                    <img src="https://img.icons8.com/ios-filled/50/null/trophy.png" alt="Trophy Icon">
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.write("")
    st.write("")
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

    placeholder2 = st.empty()
    placeholder2.write(selected_groupchats)
    placeholder2.empty()

    delete_groupchat()
