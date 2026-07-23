import streamlit as st
from page_utils import apply_page_config
from navigation import make_sidebar
from variables import aniosList
import os
from st_copy import copy_button
apply_page_config()
make_sidebar()
st.set_page_config(page_title="Documentación", page_icon="📚")
# Simulación de rol si no existe (para pruebas)
rol_usuario = st.session_state.get("rol")
st.markdown(
    "<h2 style='text-align: center;'>Links Útiles</h2>",
    unsafe_allow_html=True
)

def show_documentacion():
    role = rol_usuario if rol_usuario else "admin" 
    st.title("📚 Centro de Documentación")
    # --- SECCIÓN 1: INTRODUCCIÓN SEGÚN ROL ---
    st.header("Link útiles")
    col1, col2 = st.columns([1, 2], vertical_alignment="bottom")

    with col1:
        st.selectbox(
            "Seleccione curso académico", 
            options=aniosList[1:], 
            key="selector_curso_ac_doc"
        )

    with col2:
        # Construimos la URL dinámica usando el valor actual del selectbox
        url_form_empresas = f"{st.secrets["FORM_EMPRESA"] }?curso_academico={st.session_state['selector_curso_ac_doc']}"
        colLink , colCopy = st.columns([3, 1])
        with colLink:
            st.info(url_form_empresas)
        with colCopy:
            st.caption("")
            copy_button( url_form_empresas, tooltip="Copiar Link", copied_label="Copiado!")

    st.header("1. Tu Rol en el Proyecto")
    
    if role == "admin" or role == "gestor":
        st.write("""
        Como **Administrador**, tienes la visión global del sistema. Tu objetivo es asegurar que la conexión 
        entre centros educativos y empresas sea fluida, supervisando el cumplimiento de los hitos y 
        gestionando la base de datos de usuarios.
        """)
    elif role == "empresa":
        st.write("""
        Tu función es estratégica. Debes asegurar que la empresa cumpla con los estándares de bienestar 
        y sostenibilidad que busca esta generación, además de supervisar el impacto positivo 
        que los aprendices dejan en tu trayectoria profesional.
        """)
    elif role == "tutor":
        st.write("""
        Eres el mentor directo. Tu misión es guiar, inspirar y hacer crecer al aprendiz en el día a día 
        del hotel/empresa. Eres responsable de convertir los errores en oportunidades de 
        aprendizaje.
        """)
    elif role == "tutorCentro":
        st.write("""
        Actúas como puente académico. Tu labor es realizar el seguimiento del bienestar del alumno y 
        asegurar que los conocimientos adquiridos en la empresa se alineen con el ciclo formativo.
        """)

    # --- SECCIÓN 2: PROCESOS ESPECÍFICOS ---
    st.header("2. Guía de Operaciones")

    # Contenido común o específico usando Expanders
    if role in ["admin", "empresa"]:
        with st.expander("📝 Gestión de Formaciones y Asignación"):
            st.write("""
            1. Ve a la pestaña de **Seguimiento**.
            2. Selecciona la **Empresa** y el **Puesto**. 
            3. Inicia la formación definiendo las fechas pactadas y el tutor asignado.
            """)

    if role in [ "tutorCentro", "admin", "gestor"]:
        with st.expander("📧 Seguimiento y Feedbacks"):
            st.write("El sistema requiere tu intervención en hitos clave:")
            st.write("* **Feedback Inspirador:** Reconoce logros específicos para motivar.")
            st.write("* **Escucha Activa:** Utiliza el espacio de dudas para conocer el bienestar del alumno.")
            st.write("* **Retos:** Si una tarea le resulta cómoda, anímalo a salir de su zona de confort.")

    if role == "tutor":
        with st.expander("💡 Tips para Enseñar (Metodología)"):
            st.write("""
            * **Explica en 10':** Concéntrate en lo esencial, menos es más.
            * **3 Ideas antes de preguntar:** Fomenta el pensamiento crítico pidiendo al aprendiz 3 soluciones antes de darle la respuesta.
            * **El Reto del Minuto:** Al finalizar, pídeles resumir los 5 puntos clave para asegurar la retención.
            """)

    st.divider()

    # --- SECCIÓN 3: RECURSOS Y DESCARGAS ---
    st.header("3. Recursos y Descargas")
    
    # Grid de manuales
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Guía de Onboarding")
        st.write("Claves para recibir al aprendiz y conectar desde el primer día.")
        url_onboarding = 'https://drive.google.com/file/d/1kkiQhUtY0dGd-W5vH16wlKWPRB6EpmCP/preview?usp=drive_link'
        st.link_button("Ver Manual Onboarding", url_onboarding)

    with col2:
        st.subheader("Guía de Seguimiento")
        st.write("Herramientas de feedback, resolución de conflictos y evaluación.")
        url_seguimiento = "https://drive.google.com/file/d/1l8tqTFbNsz07AqIvbGSoA-RWDoSkR30C/preview?usp=drive_link"
        st.link_button("Ver Manual Seguimiento", url_seguimiento)


if __name__ == "__main__":
    show_documentacion()