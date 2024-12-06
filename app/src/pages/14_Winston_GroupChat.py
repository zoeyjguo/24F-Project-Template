import logging
logger = logging.getLogger(__name__)
import streamlit as st
import requests
from streamlit_extras.app_logo import add_logo
from modules.nav import get_nav_config
from streamlit_navigation_bar import st_navbar
from datetime import date, timedelta

if "authenticated" not in st.session_state:
    st.switch_page("Home.py")

# navigation bar
pages, styles, logo, options = get_nav_config(show_home=False)
page = st_navbar(pages, selected="Group Chat", styles=styles, logo_path=logo, options=options)

if page == "Update Location":
  st.switch_page('pages/11_Update_Location.py')

if page == "Calendar":
  st.switch_page('pages/13_Personal_Calendar.py')

if page == "Logout":
  del st.session_state["role"]
  del st.session_state["authenticated"]
  st.switch_page("Home.py")

# styling for the group chats and messages
st.markdown(
    """
    <style>
    .group-chat-bubble {
        display: block;
        padding: 10px 15px;
        margin: 5px 0;
        background-color: #eaeaea;
        border-radius: 25px;
        text-align: center;
        cursor: pointer;
        font-size: 16px;
        font-weight: bold;
        transition: background-color 0.3s ease;
    }
    .group-chat-bubble:hover {
        background-color: #d0d0d0;
    }
    .chat-message {
        padding: 10px;
        margin: 10px;
        border-radius: 15px;
        max-width: 70%;
        font-size: 14px;
        font-weight: normal;
        display: flex;
        flex-direction: column;
        gap: 10px;
    }
    .chat-message img {
        max-width: 100%; /* Ensure images span the full width of the message */
        height: auto; /* Maintain aspect ratio */
        border-radius: 10px;
    }
    .chat-message-sender {
        background-color: #d8eefe;
        margin-left: auto;
        text-align: right;
        color: #0a3e6d;
    }
    .chat-message-receiver {
        background-color: #fefefe; 
        margin-right: auto;
        text-align: left;
        color: #3d3d3d;
    }
    .input-container {
        display: flex;
        flex-direction: column;
        gap: 10px;
        margin-top: 20px;
    }
    .input-box {
        flex-grow: 1;
        padding: 10px;
        font-size: 14px;
        border: 1px solid #ddd;
        border-radius: 20px;
        margin-right: 10px;
    }
    .send-button {
        padding: 8px 16px;
        background-color: #66b3ff; 
        color: white;
        border: none;
        border-radius: 20px;
        cursor: pointer;
        font-size: 14px;
        font-weight: bold;
        transition: background-color 0.3s ease;
        align-self: flex-start;
    }
    .send-button:hover {
        background-color: #549fd6;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# get from generated data
fetch_groupchats = requests.get('http://api:4000/u/users/1002/groupchats').json()
group_chats = []
fetch_messages = requests.get('http://api:4000/g/groupchats/399/messages').json()
messages_data = []

for message in fetch_messages:
  messages_data.append({"sender": "{0} {1}".format(message["FirstName"], message["LastName"]),
                  "content": message["Text"],
                  "image": message["ImageLink"]})
      
for groupchat in fetch_groupchats:
    group_chats.append({"name": groupchat["Name"], "id": groupchat["GroupChatId"]})

# add images to the group chat
def send_message_with_image(message, image_url, groupchat_id):
    if not image_url:
        st.error("Invalid image URL. Message not sent.")
        return

    data = {"Sender": 1002,"Text": message.strip(),"ImageLink": image_url}
    try:
        response = requests.post(f'http://api:4000/g/groupchats/{groupchat_id}/messages', json=data)
        if response.status_code == 200:
            st.success("Message with image sent successfully!")
        else:
            st.error(f"Error sending message with image: {response.text}")
    except requests.exceptions.RequestException as e:
        st.error(f"Error connecting to server: {str(e)}")

def upload_image_to_server(uploaded_image):
   try:
      files = {"file": uploaded_image.getvalue()}
      response = requests.post('http://api:4000/simple/upload', files=files)
      if response.status_code == 200:
         image_url = response.json().get("image_url")
         return image_url
      else:
         st.error(f"Error uploading image: {response.text}")
         return None
   except requests.exceptions.RequestException as e:
      st.error(f"Error connecting to the server: {str(e)}")
      return None
   
# initialize the session state
if "selected_chat_id" not in st.session_state:
    st.session_state.selected_chat_id = 399

# update the selected chat when a button is clicked
def select_chat(chat_id):
    st.session_state.selected_chat_id = chat_id

# add a new message to the current chat
def send_message(message, groupchat_id):
    data = {
                "Sender": 1002,
                "Text": message.strip(),
                "ImageLink": None
            }
    try:
      response = requests.post('http://api:4000/g/groupchats/{0}/messages'.format(groupchat_id), json=data)
      if response.status_code == 200:
        st.success("Message sent successfully!")
      else:
        st.error(f"Error sending message: {response.text}")
    except requests.exceptions.RequestException as e:
      st.error(f"Error connecting to server: {str(e)}")

# set up layout of the page
col1, col2 = st.columns([1.3, 4])

# set up the group chats column
with col1:
    st.markdown("### Group Chats")
    for chat in group_chats:
        if st.button(chat["name"], key=f"chat_{chat['id']}", use_container_width=True):
            select_chat(chat["id"])

# set up the messages column
with col2:
    selected_chat_id = st.session_state.selected_chat_id
    for gc in group_chats:
        if gc["id"] == selected_chat_id:
            current = gc["name"]
            st.markdown(f"## {current}")
            break

    # display messages
    fetch_messages = requests.get(f'http://api:4000/g/groupchats/{selected_chat_id}/messages').json()
    messages_data = []
    for message in fetch_messages:
        messages_data.append({"sender": f"{message['FirstName']} {message['LastName']}",
                              "content": message["Text"],
                              "image": message["ImageLink"]})
    for msg in messages_data:
        align = "flex-end" if msg["sender"] == "Winston Church" else "flex-start"
        bg_color = "#e0f7fa" if msg["sender"] == "Winston Church" else "#ffffff"
        
        # Render message with optional image
        content_html = f"""
        <div style="display: flex; justify-content: {align}; margin-bottom: 10px;">
            <div style="background-color: {bg_color}; padding: 10px; border-radius: 10px; max-width: 60%;">
                <strong>{msg['sender']}</strong><br>{msg['content']}
        """
        if "image" in msg and msg["image"] is not None:
            content_html += f'<img src="{msg["image"]}" alt="Image" style="width: 100px; margin-top: 10px;"/>'
        content_html += "</div></div>"
        
        st.markdown(content_html, unsafe_allow_html=True)

    # input text messages and image URL
    st.markdown("---")
    st.markdown("### Add a Message")
    with st.form(key="send_message_form", clear_on_submit=True):
        new_message = st.text_input("Write a message", key="new_message")
        new_image_url = st.text_input("Attach an image URL (optional)", key="new_image_url", placeholder="Paste image URL here (optional)")
        submit_button = st.form_submit_button("Send")

        if submit_button:
            if not new_image_url:
                send_message(new_message, selected_chat_id)
            else:
                send_message_with_image(new_message, new_image_url, selected_chat_id)