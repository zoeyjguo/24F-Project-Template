import streamlit as st

def get_nav_config(show_home=False):
    pages = ["Home"] if not st.session_state.get("authenticated", False) else []

    if "authenticated" not in st.session_state or show_home:
        st.session_state.authenticated = False
        pages = ["Kali", "Winston", "Chloe", "Joey"]

    if st.session_state["authenticated"]:
        if st.session_state["role"] == "us_coop_student":
            pages = ["Feed", "Update Interests", "View Other Profile", "Logout"]
        
        if st.session_state["role"] == "abroad_coop_student":
            pages = ["Update Location", "Calendar", "Group Chat", "Logout"]

        if st.session_state["role"] == "administrator":
            pages = ["Delete Group Chat", "Flag Message", "Reports", "Logout"]

        if st.session_state["role"] == "data_analyst":
            pages = ["Interests", "Badges", "User Rank", "Logout"]

    styles = {
        "nav": {
            "background-color": "rgb(198,169,249)",
            "justify-content": "space-between",
            "align-items": "center",
            "padding": "0 1rem",
        },
        "div": {
            "max-width": "32rem",
        },
        "span": {
            "border-radius": "0.5rem",
            "color": "rgb(49, 51, 63)",
            "margin": "0 0.125rem",
            "padding": "0.4375rem 0.625rem",
        },
        "active": {
            "background-color": "rgba(255, 255, 255, 0.25)",
        },
        "hover": {
            "background-color": "rgba(255, 255, 255, 0.35)",
        },
    }
    logo = "/appcode/assets/logo.svg"
    options = {
        "show_menu": False,
        "show_sidebar": False,
    }

    return pages, styles, logo, options