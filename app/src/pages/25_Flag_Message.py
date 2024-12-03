import streamlit as st
import requests
from modules.nav import get_nav_config
from streamlit_navigation_bar import st_navbar

pages, styles, logo, options = get_nav_config(show_home=False)
page = st_navbar(pages, selected="Flag Message", styles=styles, logo_path=logo, options=options)

if page == "Delete Group Chat":
  st.switch_page('pages/23_Delete_GroupChat.py')

if page == "Reports":
  st.switch_page('pages/26_User_Reports.py')

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
    }
    .chat-message-sender {
        background-color: #d8eefe; /* Pastel blue */
        margin-left: auto;
        text-align: right;
        color: #0a3e6d;
    }
    .chat-message-receiver {
        background-color: #fefefe; /* White with a softer tone */
        margin-right: auto;
        text-align: left;
        color: #3d3d3d;
    }
    .input-container {
        display: flex;
        align-items: center;
        margin-top: 10px;
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
        background-color: #66b3ff; /* Pastel blue button */
        color: white;
        border: none;
        border-radius: 20px;
        cursor: pointer;
        font-size: 14px;
        font-weight: bold;
        transition: background-color 0.3s ease;
    }
    .send-button:hover {
        background-color: #549fd6;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# data for group chats and messages

group_chats = requests.get('http://api:4000/simple/admin/77/groupchats').json()

# data for the messages 
messages_data = {}

for i in range(len(group_chats)):
  messages_data[group_chats[i]['GroupChatId']] = requests.get('http://api:4000/g/groupchats/{0}/messages'.format(group_chats[i]['GroupChatId'])).json()

# initialize the session state
if "selected_chat" not in st.session_state:
    st.session_state['selected_chat'] = group_chats[0]['GroupChatId']

if "messages" not in st.session_state:
    st.session_state['messages'] = messages_data

# update the selected chat when a button is clicked
def select_chat(chat_id):
    st.session_state['selected_chat'] = chat_id

# add a new message to the current chat
def send_message(message):
    if message.strip():
        st.session_state['messages'][selected_chat_id].append({"FirstName": "Chloe", "LastName": "Lane", "Sender": 77, "Text": message})

# set up layout of the page
col1, col2 = st.columns([1.3, 4])

# set up the group chats column
with col1:
    st.markdown("### Group Chats")
    for chat in group_chats:
        if st.button(chat['Name'], key=f"chat_{chat['GroupChatId']}", use_container_width=True):
            select_chat(chat['GroupChatId'])

# set up the messages column
with col2:
    selected_chat_id = st.session_state['selected_chat']
    selected_chat = next(chat for chat in group_chats if chat['GroupChatId'] == selected_chat_id)
    st.markdown(f"## {selected_chat['Name']}")

    # display messages
    chat_messages = st.session_state['messages'][selected_chat_id]
    for msg in chat_messages:
        align = "flex-end" if msg["Sender"] == 77 else "flex-start"
        bg_color = "#e0f7fa" if msg["Sender"] == 77 else "#ffffff"
        st.markdown(
            f"""
            <div style="display: flex; justify-content: {align}; margin-bottom: 10px;">
                <div style="background-color: {bg_color}; padding: 10px; border-radius: 10px; max-width: 60%;">
                    <strong>{msg['FirstName']} {msg['LastName']}</strong><br>{msg['Text']}
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # input into the box to send a message
    st.markdown("---")
    with st.form(key="send_message_form", clear_on_submit=True):
        new_message = st.text_input("Write a message", key="new_message")
        submit_button = st.form_submit_button("Send")

        if submit_button:
            send_message(new_message)