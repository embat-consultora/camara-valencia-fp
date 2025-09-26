import streamlit as st
from time import sleep
from variables import logoutButton
def get_current_page_name():
    return st.session_state.get("current_page", "")


def make_sidebar():
    with st.sidebar:
        st.markdown(
        """
        <style>
        [data-testid="stSidebar"] {
            width: 200px;  /* Adjust the width to your preference */
        }
        </style>
        """,
        unsafe_allow_html=True
    )
        st.title("Menú")
        st.write("")
        st.write("")

        if st.session_state.get("logged_in", False):
            st.page_link("pages/dashboard.py", label="Dashboard")
            st.page_link("pages/empresas.py", label="Empresas")
            st.page_link("pages/alumnos.py", label="Alumnos")
            st.page_link("pages/emails.py", label="Contactar")
            st.page_link("pages/formsCreacion.py", label="Formularios")
            st.write("")
            st.write("")

            if st.button(logoutButton):
                logout()

        elif get_current_page_name() != "streamlit_app":
            # If anyone tries to access a secret page without being logged in,
            # redirect them to the login page
            st.switch_page("streamlit_app.py")

def logout():
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    sleep(0.5)
    st.rerun()

