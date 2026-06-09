import streamlit as st
import extra_streamlit_components as stx
from modules.data_base import getEqual
from modules.session_manager import load_user, validate_get_user
from variables import page_icon, usuariosTabla
import os
import base64

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@300;400;700&display=swap');
    html, body, [class*="css"], .stApp { font-family: 'Montserrat', sans-serif; }
    </style>
""", unsafe_allow_html=True)

st.set_page_config(page_title="Cámara FP - Inicio", page_icon=page_icon)
def get_base64(bin_file):
    with open(bin_file, "rb") as f:
        return base64.b64encode(f.read()).decode()
img = get_base64("images/fondo.webp")

st.markdown(
    f"""
    <style>
    .stApp {{
        background-image: url("data:image/jpg;base64,{img}");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }}
    </style>
    """,
    unsafe_allow_html=True
)
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
col1, col2, col3 = st.columns([1, 4, 1])
with col2:
    css = """
    .st-key-my_white_container {
        background-color: rgba(255, 255, 255, 255);
        padding: 50px;
        border-radius: 15px;
        box-shadow: 0 .5rem 1rem rgb(0 0 0 / .15); 
    }
    
    /* Forzamos el centrado absoluto del bloque de imagen en cualquier pantalla (PC y Móvil) */
    .st-key-my_white_container [data-testid="stImage"] {
        display: flex !important;
        justify-content: center !important;
        align-items: center !important;
        width: 100% !important;
        margin: 0 auto 20px auto !important;
    }

    /* Aseguramos que el contenedor interno de la etiqueta img de Streamlit también se centre */
    .st-key-my_white_container [data-testid="stImageContainer"] {
        display: flex !important;
        justify-content: center !important;
        width: auto !important;
    }
    
    /* Reducimos un poco el padding en móviles para que no coma tanto espacio de pantalla */
    @media (max-width: 768px) {
        .st-key-my_white_container {
            padding: 25px !important;
        }
    }
    """

    st.html(f"<style>{css}</style>")
    
    # Eliminamos el parámetro 'width=500' que no pertenece a st.container
    with st.container(key="my_white_container"):
        
        url_logo = "https://github.com/user-attachments/assets/e8f8238a-65f8-4132-9d9f-efe8c0effbc7"
        
        st.markdown(
            f"""
            <div style="display: flex; justify-content: center; align-items: center; width: 100%; margin-bottom: 25px;">
                <img src="{url_logo}" style="width: 350px; max-width: 100%; height: auto; object-fit: contain;">
            </div>
            """,
            unsafe_allow_html=True)
        
        # 3. Campos de Streamlit (se renderizan de forma normal)
        username = st.text_input("Usuario", placeholder="Ingrese email o usuario", key="login_username")
        password = st.text_input("Contraseña", type="password", placeholder="Ingrese contraseña", key="login_pass")
        
        col_vacia, col_enlace = st.columns([1, 1])

        with col_enlace:
            st.markdown(
            f"""
                <div style="text-align: right; margin-bottom: 15px;">
                    <a href="/forgotPassword" target="_self" style="
                        color: #4A5568; 
                        text-decoration: none; 
                        font-size: 0.9em; 
                        font-family: 'Montserrat', sans-serif;
                        font-weight: 500;
                    " onmouseover="this.style.color='#FF4B4B'" onmouseout="this.style.color='#4A5568'">
                        Olvidé mi contraseña
                    </a>
                </div>
                """,
                unsafe_allow_html=True
            )
        if st.button("Acceder", type="primary", use_container_width=True): # use_container_width ayuda en mobile
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
