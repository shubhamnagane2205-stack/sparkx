import streamlit as st
from screens.home_screen import home_screen
from config import APP_NAME

st.set_page_config(
    page_title=f"{APP_NAME} - Material Classifier",
    page_icon="\u2728",
    layout="centered",
)

if st.session_state.get("screen")=='home' or st.session_state.get('screen')==None:
    home_screen()