import streamlit as st
from modules.data_base import (
    getEquals, getOrdered, crearPractica
)
from page_utils import apply_page_config
from navigation import make_sidebar
from datetime import datetime
from variables import ( alumnosTabla, empresasTabla)

# ----------------------------------------------
# CONFIG
# ----------------------------------------------
apply_page_config()
make_sidebar()
st.set_page_config(page_title="Prácticas autogestionada", page_icon="🚀")

st.markdown("<h2 style='text-align: center;'>🚀 Crear Práctica Autogestionada</h2>", unsafe_allow_html=True)
now = datetime.now().isoformat()

def fetch_alumnos_empresas():
    alumnos = getOrdered(
        alumnosTabla,
        searchFor="estado",
        searchValue="Sin Empresa",
        orderByColumn="tipoPractica"
    )
    empresas = getEquals(empresasTabla, {})
    return alumnos, empresas

# ----------------------------------------------
# INICIALIZAR SESSION_STATE (evita KeyError)
# ----------------------------------------------
if "alumnos" not in st.session_state:
    st.session_state["alumnos"] = []

if "empresas" not in st.session_state:
    st.session_state["empresas"] = []

if "data_loaded" not in st.session_state:
    st.session_state["data_loaded"] = False

if "force_reload" not in st.session_state:
    st.session_state["force_reload"] = False
# ----------------------------------------------
# BOTÓN DE REFRESCAR (arriba a la derecha)
# ----------------------------------------------
col_refresh = st.columns([1, 0.15])
with col_refresh[1]:
    if st.button("🔄 Actualizar", key="btn_refresh"):
        st.session_state["force_reload"] = True
# ----------------------------------------------
# CARGA CENTRAL DESDE BD → session_state
# ----------------------------------------------
def load_data():
    if st.session_state["data_loaded"] or not st.session_state["force_reload"]:
        with st.spinner("Cargando datos desde la base..."):

            alumnos, empresas = fetch_alumnos_empresas()
            st.session_state["alumnos"] = alumnos
            st.session_state["empresas"] = empresas

            st.session_state["data_loaded"] = True
            st.session_state["force_reload"] = False

# ----------------------------------------------
# CARGAR DATOS UNA SOLA VEZ
# ----------------------------------------------
load_data()

alumnos = st.session_state["alumnos"]
empresas = st.session_state["empresas"]

lista_empresas = [f"{e['nombre']} - {e.get('CIF','')}" for e in empresas]
empresa_sel = st.selectbox("Empresa", lista_empresas)
empresa_obj = empresas[lista_empresas.index(empresa_sel)]

lista_alumnos = [f"{a['nombre']} {a['apellido']} - {a['dni']}" for a in alumnos]
alumno_sel = st.selectbox("Alumno", lista_alumnos)
alumno_obj = alumnos[lista_alumnos.index(alumno_sel)]

if st.button("💾 Crear práctica"):
    with st.spinner("Creando práctica..."):
        try:
            crearPractica(
                empresa_obj["CIF"],
                alumno_obj["dni"],
                ciclo="Autogestionado",
                area="Autogestionado",
                proyecto="Autogestionado",
                fecha=now,
                ciclos_info=None,
                cupos_disp=None,
                oferta_id=None
            )

            st.success("Práctica creada 🎉")

            # 🔥 Refrescar datos desde BD
            load_data(force=True)
            st.rerun()

        except Exception as e:
            st.error(f"❌ Error al crear la práctica: {e}")
