import streamlit as st
from page_utils import apply_page_config
from navigation import make_sidebar
from variables import aniosList
from st_copy import copy_button
apply_page_config()
make_sidebar()
st.set_page_config(page_title="Documentación", page_icon="📚")
# Simulación de rol si no existe (para pruebas)
rol_usuario = st.session_state.get("rol") 

def get_documentation_links():
    st.subheader("Link útiles")
    st.info("Este es el link que le podrás enviar a las empresas para que completen el formulario de nuevas formaciones. Debes seleccionar primero el curso académico.")
    col1, col2 = st.columns([1, 2], vertical_alignment="bottom")

    with col1:
        st.selectbox(
            "Seleccione curso académico", 
            options=aniosList[1:], 
            key="selector_curso_ac_doc"
        )

    with col2:
        # Construimos la URL dinámica usando el valor actual del selectbox
        url_form_empresas = f"{st.secrets["urls"]["FORM_EMPRESA"] }?curso_academico={st.session_state['selector_curso_ac_doc']}"
        colLink , colCopy = st.columns([3, 1])
        with colLink:
            st.info(url_form_empresas)
        with colCopy:
            st.caption("")
            copy_button( url_form_empresas, tooltip="Copiar Link", copied_label="Copiado!")

def show_documentacion():
    role = rol_usuario if rol_usuario else "admin" 
    st.title("📚 Centro de Documentación")
    # --- SECCIÓN 1: INTRODUCCIÓN SEGÚN ROL ---
    if role == "admin" or role == "gestor" or role == "empresa":
        get_documentation_links()
    st.write("")
    st.subheader("Tu Rol en el Proyecto")
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
        en la empresa. Eres responsable de convertir los errores en oportunidades de 
        aprendizaje.
        """)
    elif role == "tutorCentro":
        st.write("""
        Actúas como puente académico. Tu labor es realizar el seguimiento del bienestar del alumno y 
        asegurar que los conocimientos adquiridos en la empresa se alineen con el ciclo formativo.
        """)


    st.divider()

    # --- SECCIÓN 3: RECURSOS Y DESCARGAS ---
    st.header("Recursos y Descargas")
    
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