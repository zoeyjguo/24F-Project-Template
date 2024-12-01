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
    }
    .chat-message-sender {
        background-color: #d1e7ff;
        margin-left: auto;
        text-align: right;
    }
    .chat-message-receiver {
        background-color: #f0f0f0;
        margin-right: auto;
        text-align: left;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# data for group chats and messages
group_chats = [
    "Teatro Carcano El Bella E La Bestia",
    "Agevolazioni Orchestra Filarmonica",
    "Collaborazione con Ponder",
    "Agevolazioni Serate Musicali",
    "Agevolazioni Fondazione S.",
    "Cinete Camilano Cloud",
    "Explore Pavia",
]

messages = {
    "Teatro Carcano El Bella E La Bestia": [
        {"sender": "John", "text": "I'm near the balcony on the left."},
        {"sender": "You", "text": "Okay, I think I know where you are."},
        {"sender": "John", "text": "Mhm, I'm in the front row wearing a black sweater."},
        {"sender": "You", "text": "Wait, I don't think I see you... Nvm, I'm coming!"},
    ],
    "Agevolazioni Orchestra Filarmonica": [
        {"sender": "John", "text": "I'm excited about this concert!"},
    ],
    # Add messages for other group chats as needed
}

# layout between group chat and messages 
col1, col2 = st.columns([1.3, 4])

# display messages when a group chat is selected 
with col1:
    st.subheader("Group Chats")
    selected_chat = st.session_state.get("selected_chat", group_chats[0])
    for chat in group_chats:
        if st.button(chat, key=chat):
            selected_chat = chat
            st.session_state["selected_chat"] = selected_chat

# show the messages of a person
with col2:
    st.subheader(selected_chat)
    chat_messages = messages.get(selected_chat, [])
    for message in chat_messages:
        if message["sender"] == "You":
            st.markdown(
                f"<div class='chat-message chat-message-sender'>{message['text']}</div>",
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                f"<div class='chat-message chat-message-receiver'><b>{message['sender']}</b>: {message['text']}</div>",
                unsafe_allow_html=True,
            )

    # add an input box to send the message
    st.text_input("Write a message", key="message_input")
    st.button("Send", key="send_button")