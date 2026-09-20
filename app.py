import streamlit as st
from screens.home_screen import home_screen
from screens.guide_screen import guide_screen
from screens.methodology_screen import methodology_screen
from config import APP_NAME

st.set_page_config(
    page_title=f"{APP_NAME} - Material Classifier",
    page_icon="\u2728",
    layout="centered",
)

screen = st.session_state.get("screen")
 
if screen == "guide":
    guide_screen()
elif screen == "methodology":
    methodology_screen()
else:
    home_screen()
 