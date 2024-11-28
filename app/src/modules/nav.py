import streamlit as st
from streamlit_navigation_bar import st_navbar

def page():
    pages = ["Home", "Kali", "Winston", "Chloe", "Joey"]
    styles = {
        "nav": {
            "background-color": "rgb(198,169,249)",
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

    options = {
        "show_menu": False,
        "show_sidebar": False,
    }

    return st_navbar(pages, styles=styles, logo_path="/appcode/assets/logo.svg", options=options)