import streamlit as st
import extra_streamlit_components as stx

from variables import logoutButton,nombres_roles, aniosList,cursoList
def get_current_page_name():
    return st.session_state.get("current_page", "")

def load_env_once():
    if "env" not in st.session_state:
        st.session_state["env"] = st.secrets["supabase"]["SUPABASE_ENV"]

from datetime import date

def get_index_anio_actual(anios_list, hoy=None):
    hoy = hoy or date.today()
    anio_actual = hoy.year
    corte = date(anio_actual, 9, 1)

    for idx, valor in enumerate(anios_list):
        if valor == "Seleccionar":
            continue

        try:
            anio_inicio_str, anio_fin_str = valor.split("-")
            anio_inicio = int(anio_inicio_str)
            anio_fin = int(anio_fin_str)
        except ValueError:
            continue  # ignora valores mal formateados

        # Antes del 1 de septiembre: tomar donde el año actual esté después del '-'
        if hoy < corte and anio_fin == anio_actual:
            return idx

        # Desde el 1 de septiembre: tomar donde el año actual esté antes del '-'
        if hoy >= corte and anio_inicio == anio_actual:
            return idx

    return 0  # fallback: "Seleccionar"

def make_sidebar():
    load_env_once()

    rol = st.session_state.get("rol", "admin")
    user = st.session_state.get("username")
    rol_amigable = nombres_roles.get(rol, rol.capitalize())
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
            if st.session_state["env"] == "test":
                st.caption(f"Entorno: **{st.session_state['env']}**")
            st.caption(f"Rol: **{rol_amigable}**")
            st.caption(f"Usuario: **{user}**")
        
            lista_cursosAcademico = aniosList
            lista_curso = cursoList
            if "index_curso" not in st.session_state:
                st.session_state["index_curso"] = 0
            if "index_academic" not in st.session_state:
                st.session_state["index_academic"] = get_index_anio_actual(aniosList)
        
            st.selectbox(
                "**Curso Académico**",
                options=lista_cursosAcademico,
                index=st.session_state["index_academic"],
                key="selector_curso_ac_global"
            )
        
            st.selectbox(
                    "**Curso**",
                    options=lista_curso,
                    index=st.session_state["index_curso"],
                    key="selector_curso_global"
                )
            st.session_state["index_curso"] = lista_curso.index(st.session_state.get("selector_curso_global"))
            st.session_state["index_academic"]  = lista_cursosAcademico.index(st.session_state.get("selector_curso_ac_global"))
            st.title("Menú")
            st.write("")
            if st.session_state.get("logged_in", False):
                if rol == "admin":
                    st.page_link("pages/dashboard_msa.py", label="Panel Estatégico")
                    st.page_link("pages/tablasPrincipales.py", label="Panel de Gestión de FE")
                    st.page_link("pages/practicas.py", label="Formación en Empresa")
                    st.page_link("pages/matchs.py", label="Panel de Matcheos")
                    st.page_link("pages/empresas.py", label="Gestión de Empresas")
                    st.page_link("pages/alumnos.py", label="Gestión de Alumnos")
                    st.page_link("pages/documentacion.py", label="Instructivos y Manuales de uso")
                    st.write("")
                    st.page_link("pages/configuracion.py", label="Configuraciones")
                    st.write("")
                if rol == "gestor":
                    st.page_link("pages/dashboard_msa.py", label="Panel Estatégico")
                    st.page_link("pages/tablasPrincipales.py", label="Panel de Gestión de FE")
                    st.page_link("pages/practicas.py", label="Formación en Empresa")
                    st.page_link("pages/documentacion.py", label="Instructivos y Manuales de uso")
                if rol == "tutor":
                    st.page_link("pages/practicas.py", label="Formación en Empresa")
                    st.page_link("pages/documentacion.py", label="Instructivos y Manuales de uso")
                if rol == "tutorCentro":
                    st.page_link("pages/practicas.py", label="Formación en Empresa")
                    st.page_link("pages/documentacion.py", label="Instructivos y Manuales de uso")
                if rol == "empresa":
                    st.page_link("pages/empresaDetails.py", label="Mi Empresa")
                if rol == "alumno":
                    st.page_link("pages/alumno.py", label="Mi Formación en Empresa")
                if st.button(logoutButton):
                    logout()

            elif get_current_page_name() != "streamlit_app":
                st.switch_page("streamlit_app.py")

def logout():
    # 1. Limpiamos TODO el session_state primero para "apagar" la interfaz
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    
    # 2. Forzamos el estado de salida para que los menús no intenten renderizarse
    st.session_state["logged_in"] = False
    
    # 3. Borramos la cookie de forma segura
    try:
        cookie_manager = stx.CookieManager(key="logout_manager")
        cookie_manager.delete("saved_user_email")
    except:
        pass # Silenciamos errores visuales del componente
    
    # 4. Una pausa un poco más larga para asegurar que el navegador limpie caché
    import time
    time.sleep(0.8)
    st.rerun()
