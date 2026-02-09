import streamlit as st
from page_utils import apply_page_config
from navigation import make_sidebar

import re
apply_page_config()
make_sidebar()

st.set_page_config(page_title="Documentación", page_icon="🧑‍🎓")
st.markdown(
    "<h2 style='text-align: center;'>Links Útiles</h2>",
    unsafe_allow_html=True
)

def show_documentacion():
    st.title("📚 Centro de Documentación")
    st.info("Bienvenido al manual de uso del sistema de gestión de formaciones en empresas y feedbacks.")

    # --- SECCIÓN 1: INTRODUCCIÓN ---
    st.header("1. Introducción")
    st.write("""
    Este sistema permite automatizar el seguimiento de los alumnos en prácticas mediante 
    el envío de formularios de feedback programados.
    """)

    # --- SECCIÓN 2: PROCESOS PRINCIPALES ---
    st.header("2. Procesos del Gestor")
    
    with st.expander("📝 Asignación de Prácticas"):
        st.write("""
        1. Ve a la pestaña de **Seguimiento**.
        2. Selecciona la **Empresa** y el **Puesto**. 
        3. Esto creará automáticamente una nueva práctica con estado **Pendiente**
        4. Ve a la pestaña de **Prácticas**, busca la práctica recién creada y haz clic en el botón de **Iniciar**.
        5. Define la fecha de fin en el diálogo emergente.
        """)

    with st.expander("📧 Seguimiento de Feedbacks"):
        st.write("""
        El sistema genera automáticamente 3 hitos:
        * **Inicial:** A los 7 días.
        * **Adaptación:** A los 30 días.
        * **Final:** En la fecha de finalización pactada.
        * Cada hito envía un formulario específico al alumno, con preguntas adaptadas a cada etapa.
        * Puedes ver el estado de cada feedback en la pestaña de **Prácticas** seleccionando al alumno correspondiente.
        """)

    st.divider()

    # --- SECCIÓN 3: RECURSOS Y DESCARGAS ---
    st.header("3. Recursos y Descargas")
    
    col1, col2 = st.columns([1, 3])
    
    with col1:
        # Podés usar un icono de archivo o una imagen pequeña
        st.markdown("### 📄")
    
    with col2:
        st.subheader("Manual el Tutor")
        st.write("Consulta el documento detallado con capturas de pantalla y preguntas frecuentes.")
        
        # LINK AL DOCUMENTO
        # Opción A: Link externo (Google Drive, Dropbox, etc.)
        url_doc = "https://drive.google.com/file/d/1kkiQhUtY0dGd-W5vH16wlKWPRB6EpmCP/view?usp=drive_link"
        st.link_button("Descargar Documentación Completa", url_doc, type="primary")

    # --- PIE DE PÁGINA ---
    st.divider()
    st.caption("v1.0.2 - Sistema de Gestión de Prácticas FP - 2026")

if __name__ == "__main__":
    show_documentacion()