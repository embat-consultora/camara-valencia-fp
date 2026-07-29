from variables import title, page_icon, companyIcon
import streamlit as st
def apply_page_config():
    st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@300;400;700&display=swap');

    /* Esto aplica la fuente a toda la app */
    html, body, [class*="css"], .stApp {
        font-family: 'Montserrat', sans-serif;
    }
    </style>
    """,
    unsafe_allow_html=True
)
    st.set_page_config(
        page_title=title,
        page_icon=page_icon,  # You can use an emoji or a URL to an icon image
        layout="wide", # Optional: You can set the layout as "centered" or "wide"
        initial_sidebar_state="collapsed"
    )
    
    st.logo(companyIcon,size="large")

