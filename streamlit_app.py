import streamlit as st
import extra_streamlit_components as stx
from modules.data_base import getEqual
from modules.session_manager import load_user, validate_get_user
from variables import page_icon,usuariosTabla
import os
# Configuración inicial
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
st.set_page_config(page_title="Cámara FP - Inicio", page_icon=page_icon)

cookie_manager = stx.CookieManager(key="main_cookie_manager")

if not st.session_state.get("logged_in"):
            st.session_state["logged_in"] = False
            st.rerun()

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
        
        url_logo = "https://github.com/user-attachments/assets/c1da5d43-519c-4f0e-9ab9-d7e78ad4cbd2" 
        
        st.markdown(
            f"""
            <div style="display: flex; justify-content: center; align-items: center; width: 100%; margin-bottom: 25px;">
                <img src="{url_logo}" style="width: 250px; max-width: 100%; height: auto; object-fit: contain;">
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
    if rol == 'alumno':
        st.switch_page("pages/alumno.py")
    st.stop()

islogged =validate_get_user()
if islogged:
    st.switch_page("pages/tablasPrincipales.py")