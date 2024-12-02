import streamlit as st

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
group_chats = [
    {"id": 1, "name": "Teatro Carcano El Bella E La Bestia"},
    {"id": 2, "name": "Agevolazioni Orchestra Filarmonica"},
    {"id": 3, "name": "Collaborazione con Ponder"},
    {"id": 4, "name": "Agevolazioni Serate Musicali"},
    {"id": 5, "name": "Agevolazioni Fondazione S."},
    {"id": 6, "name": "Cinete Camilano Cloud"},
    {"id": 7, "name": "Explore Pavia"}
]

# data for the messages 
messages_data = {
    1: [
        {"sender": "John", "content": "I'm near the balcony on the left."},
        {"sender": "You", "content": "Okay, I think I know where you are."},
        {"sender": "John", "content": "Mhm, I'm in the front row wearing a black sweater."},
        {"sender": "You", "content": "Wait, I don't think I see you… Nvm, I'm coming!"}
    ],
    2: [],
    3: [],
    4: [],
    5: [],
    6: [],
    7: []
}

# initialize the session state
if "selected_chat" not in st.session_state:
    st.session_state.selected_chat = 1

if "messages" not in st.session_state:
    st.session_state.messages = messages_data

# update the selected chat when a button is clicked
def select_chat(chat_id):
    st.session_state.selected_chat = chat_id

# add a new message to the current chat
def send_message(message):
    if message.strip():
        st.session_state.messages[st.session_state.selected_chat].append({"sender": "You", "content": message.strip()})

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
    selected_chat_id = st.session_state.selected_chat
    selected_chat = next(chat for chat in group_chats if chat["id"] == selected_chat_id)
    st.markdown(f"## {selected_chat['name']}")

    # display messages
    chat_messages = st.session_state.messages[selected_chat_id]
    for msg in chat_messages:
        align = "flex-end" if msg["sender"] == "You" else "flex-start"
        bg_color = "#e0f7fa" if msg["sender"] == "You" else "#ffffff"
        st.markdown(
            f"""
            <div style="display: flex; justify-content: {align}; margin-bottom: 10px;">
                <div style="background-color: {bg_color}; padding: 10px; border-radius: 10px; max-width: 60%;">
                    <strong>{msg['sender']}</strong><br>{msg['content']}
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