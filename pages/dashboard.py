import streamlit as st
from page_utils import apply_page_config
from navigation import make_sidebar

apply_page_config()
make_sidebar()

st.markdown(
    f"<h2 style='text-align: center;'>PANEL DE CONTROL</h2>",
    unsafe_allow_html=True
)