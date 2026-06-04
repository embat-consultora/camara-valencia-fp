import streamlit as st
import extra_streamlit_components as stx
from modules.data_base import getEqual
from modules.session_manager import load_user, validate_get_user
from variables import page_icon, usuariosTabla
import os

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@300;400;700&display=swap');
    html, body, [class*="css"], .stApp { font-family: 'Montserrat', sans-serif; }
    </style>
""", unsafe_allow_html=True)

st.set_page_config(page_title="Cámara FP - Inicio", page_icon=page_icon)

cookie_manager = stx.CookieManager(key="main_cookie_manager")
st.session_state["current_page"] = "streamlit_app"

# Inicializar estado
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

# ✅ Restaurar sesión desde cookie
# El cookie_manager necesita un render para estar listo, 
# get() devuelve None si aún no cargó
if not st.session_state["logged_in"]:
    saved_email = cookie_manager.get("saved_user_email")
    if saved_email:
        load_user(saved_email)
        st.session_state["logged_in"] = True
        st.rerun()

# ✅ Redirigir si ya está logueado
if st.session_state["logged_in"]:
    rol = st.session_state.get("rol")
    if rol == 'admin':
        st.switch_page("pages/tablasPrincipales.py")
    elif rol == 'empresa':
        st.switch_page("pages/empresaDetails.py")
    elif rol == 'gestor':
        st.switch_page("pages/tablasPrincipales.py")
    elif rol == 'tutor':
        st.switch_page("pages/practicas.py")
    elif rol == 'tutorCentro':
        st.switch_page("pages/practicas.py")
    elif rol == 'alumno':
        st.switch_page("pages/alumno.py")
    st.stop()

# ✅ Formulario de login
col1, col2, col3 = st.columns([1, 4, 1])
with col2:
    css = """..."""  # tu CSS igual que antes
    st.html(f"<style>{css}</style>")

    with st.container(key="my_white_container"):
        url_logo = "https://github.com/user-attachments/assets/e8f8238a-65f8-4132-9d9f-efe8c0effbc7"
        st.markdown(f"""
            <div style="display:flex;justify-content:center;margin-bottom:25px;">
                <img src="{url_logo}" style="width:250px;max-width:100%;height:auto;">
            </div>""", unsafe_allow_html=True)

        username = st.text_input("Usuario", placeholder="Ingrese email o usuario", key="login_username")
        password = st.text_input("Contraseña", type="password", placeholder="Ingrese contraseña", key="login_pass")

        col_vacia, col_enlace = st.columns([1, 1])
        with col_enlace:
            st.markdown("""
                <div style="text-align:right;margin-bottom:15px;">
                    <a href="/forgotPassword" target="_self" style="color:#4A5568;text-decoration:none;font-size:0.9em;">
                        Olvidé mi contraseña
                    </a>
                </div>""", unsafe_allow_html=True)

        if st.button("Acceder", type="primary", use_container_width=True):
            response = getEqual(usuariosTabla, "email", username)
            if response:
                user = response[0]
                if user["password"] == password:
                    st.session_state["logged_in"] = True
                    load_user(user["email"])
                    cookie_manager.set("saved_user_email", user["email"], key="set_user_cookie")
                    import time
                    time.sleep(0.5)
                    st.rerun()
                else:
                    st.error("Usuario/Password Incorrecto")
            else:
                st.error("Usuario/Password Incorrecto")