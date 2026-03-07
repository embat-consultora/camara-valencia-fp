import streamlit as st
from time import sleep
from variables import logoutButton
import os
def get_current_page_name():
    return st.session_state.get("current_page", "")

def load_env_once():
    if "env" not in st.session_state:
        st.session_state["env"] = os.getenv("SUPABASE_ENV", "local")

def make_sidebar():
    load_env_once()
    rol = st.session_state.get("rol", "admin")
    user = st.session_state.get("username")
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
            st.caption(f"Entorno: **{st.session_state['env']}**")
            st.caption(f"Rol: **{rol}**")
            st.caption(f"Usuario: **{user}**")
            st.title("Menú")
            st.write("")
            st.write("")
            if st.session_state.get("logged_in", False):
                if rol == "admin":
                    st.page_link("pages/dashboard_msa.py", label="Dashboard MSA", icon="📈")
                    st.page_link("pages/tablasPrincipales.py", label="Seguimiento")
                    st.page_link("pages/practicas.py", label="Prácticas")
                    st.page_link("pages/matchs.py", label="Matchs")
                    
                    st.page_link("pages/empresas.py", label="Empresas")
                    st.page_link("pages/alumnos.py", label="Alumnos")
                    st.page_link("pages/documentacion.py", label="Documentación")
                    st.write("")
                    st.write("")
                if rol == "gestor":
                    st.page_link("pages/dashboard_msa.py", label="Dashboard MSA", icon="📈")
                    st.page_link("pages/tablasPrincipales.py", label="Seguimiento")
                    st.page_link("pages/practicas.py", label="Prácticas")
                    st.page_link("pages/documentacion.py", label="Documentación")
                if rol == "tutor":
                    st.page_link("pages/practicas.py", label="Prácticas")
                    st.page_link("pages/documentacion.py", label="Documentación")
                if rol == "tutorCentro":
                    st.page_link("pages/practicas.py", label="Prácticas")
                    st.page_link("pages/documentacion.py", label="Documentación")
                if rol == "empresa":
                    st.page_link("pages/empresaDetails.py", label="Mi Empresa")
                if st.button(logoutButton):
                    logout()

            elif get_current_page_name() != "streamlit_app":
                st.switch_page("streamlit_app.py")

def logout():
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    sleep(0.5)
    st.rerun()

