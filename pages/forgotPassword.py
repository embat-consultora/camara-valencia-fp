import streamlit as st
import base64
import time
from variables import page_icon
from modules.data_base import getEqual, usuariosTabla  # Ajusta la importación según tu estructura
# Si tienes una función para actualizar registros (ej. updateRecord), impórtala aquí.
# de lo contrario, asegúrate de guardar el cambio en tu BD.

# ==============================================================================
# 1. CONFIGURACIÓN INICIAL Y FUENTES
# ==============================================================================
st.set_page_config(page_title="MCC - Recuperar Contraseña", layout="centered" , page_icon=page_icon)

# ==============================================================================
# 2. INYECCIÓN DE CSS (Fondo, Tarjeta Blanca y Montserrat)
# ==============================================================================
st.markdown(
    f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@300;400;700&display=swap');

    html, body, [class*="css"], .stApp {{
        font-family: 'Montserrat', sans-serif;
    }}

    .st-key-recovery_container {{
        background-color: rgba(255, 255, 255, 255);
        padding: 50px;
        border-radius: 15px;
        box-shadow: 0 .5rem 1rem rgb(0 0 0 / .15); 
    }}
    
    @media (max-width: 768px) {{"
        .st-key-recovery_container {{
            padding: 25px !important;
        }}
    }}
    </style>
    """,
    unsafe_allow_html=True
)

# ==============================================================================
# 3. INTERFAZ GRÁFICA Y LÓGICA
# ==============================================================================
col1, col2, col3 = st.columns([1, 4, 1])

with col2:
    with st.container(key="recovery_container"):
        
        st.markdown("<h2 style='text-align: center; color: #2D3748; margin-top:0;'>Recuperar Contraseña</h2>", unsafe_allow_html=True)
        st.write("---")
        st.write(" 🛠️ Página en desarrollo")
        st.write("Contáctanos para recuperar tu contraseña, escribenos a 'antopiscio@gmail.com' con tu email o nombre de usuario")
        if st.button("Volver al Login", use_container_width=True):
            st.switch_page("streamlit_app.py") # Cambia por la ruta exacta de tu Login principal

    