import streamlit as st
from modules.data_base import getEqual
from modules.session_manager import load_user, validate_get_user
from variables import companyIcon, page_icon,usuariosTabla
import os
# Configuración inicial
st.set_page_config(page_title="Inicio", page_icon=page_icon)
col1, col2, col3 = st.columns(3)
with col2:
    st.image(companyIcon, width=500)

env = os.getenv("SUPABASE_ENV")
st.session_state["current_page"] = "streamlit_app"

if st.session_state.get("logged_in"):
    rol = st.session_state.get("rol", "admin")
    if rol == 'admin':   
        st.switch_page("pages/tablasPrincipales.py")
    if rol == 'empresa':
        st.switch_page("pages/empresaDetails.py")
    if rol == 'gestor':
        st.switch_page("pages/tablasPrincipales.py")
    if rol == 'tutor':
        st.switch_page("pages/practicas.py")
    if rol == 'tutorCentro':
        st.switch_page("pages/practicas.py")
    st.stop()

islogged =validate_get_user()
if islogged:
    st.switch_page("pages/tablasPrincipales.py")
# 💻 Login tradicional
username = st.text_input("Usuario", placeholder="Ingrese email")
password = st.text_input("Contraseña", type="password", placeholder="Ingrese contraseña")
st.markdown(
    f'<div style="text-align: right;"><a href="mailto:support@embatconsultora.com">Olvide mi contraseña</a></div>',
    unsafe_allow_html=True
)
if st.button("Iniciar Sesión", type="primary"):
    response = getEqual(usuariosTabla, "email", username)
    if response:
        user = response[0]
        if user["password"] == password:
            load_user(user["email"])
            st.rerun()
        else:
            st.error("Usuario/Password Incorrecto")
    else:
        st.error("Usuario/Password Incorrecto")

