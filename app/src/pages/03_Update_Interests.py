import logging
logger = logging.getLogger(__name__)
import streamlit as st
from streamlit_extras.app_logo import add_logo
import numpy as np
import random
import time
from modules.nav import get_nav_config
from streamlit_navigation_bar import st_navbar

def response_generator():
  response = random.choice (
    [
      "Hello there! How can I assist you today?",
      "Hi, human!  Is there anything I can help you with?",
      "Do you need help?",
    ]
  )
  for word in response.split():
    yield word + " "
    time.sleep(0.05)
#-----------------------------------------------------------------------

st.set_page_config (page_title="Sample Chat Bot", page_icon="🤖")
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

st.title("Echo Bot 🤖")

st.markdown("""
            Currently, this chat bot only returns a random message from the following list:
            - Hello there! How can I assist you today?
            - Hi, human!  Is there anything I can help you with?
            - Do you need help?
            """
           )


# Initialize chat history
if "messages" not in st.session_state:
  st.session_state.messages = []

# Display chat message from history on app rerun
for message in st.session_state.messages:
  with st.chat_message(message["role"]):
    st.markdown(message["content"])

# React to user input
if prompt := st.chat_input("What is up?"):
  # Display user message in chat message container
  with st.chat_message("user"):
    st.markdown(prompt)
  
  # Add user message to chat history
  st.session_state.messages.append({"role": "user", "content": prompt})

  response = f"Echo: {prompt}"

  # Display assistant response in chat message container
  with st.chat_message("assistant"):
    # st.markdown(response)
    response = st.write_stream(response_generator())

  # Add assistant response to chat history
  st.session_state.messages.append({"role": "assistant", "content": response})

