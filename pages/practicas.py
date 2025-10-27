import streamlit as st
import pandas as pd
from modules.data_base import getEquals, getPracticas
from page_utils import apply_page_config
from navigation import make_sidebar
from variables import (
    practicaTabla,
    tutoresTabla

)

apply_page_config()
make_sidebar()
st.set_page_config(page_title="Prácticas", page_icon="🚀")

st.markdown("<h2 style='text-align: center;'>🚀 PRÁCTICAS</h2>", unsafe_allow_html=True)

# --- Traer datos base ---
practicas = getPracticas(practicaTabla, {})
if not practicas:
    st.info("No se encontraron practicas asignadas aun.")
    st.stop()
tutores = getEquals(tutoresTabla, {})   
for p in practicas:
    oferta = p.get("oferta_fp")
    empresa = p.get("empresas")
    alumno = p.get("alumnos")
    if oferta["tutor"]:
        tutor = getEquals(tutoresTabla, {"id": oferta["tutor"]})
    else: 
        tutor = []

    st.subheader(f"📋 {alumno['nombre']} {alumno['apellido']}")
    col1, col2 = st.columns(2)
    with col1:
        st.write(f"**Alumno:** {alumno['nombre']} {alumno['apellido']}")
        st.write(f"**DNI:** {alumno['dni']}")
        st.write(f"**Ciclo:** {p.get('ciclo_formativo', '—')}")
        st.write(f"**Área:** {p.get('area', '—')}")
        st.write(f"**Proyecto:** {p.get('proyecto', '—')}")

    with col2:
        st.write(f"**Empresa:** {empresa['nombre']}")
        st.write(f"**CIF:** {empresa['CIF']}")
        st.write(f"**Dirección práctica:** {oferta['direccion_empresa']}")
        st.write(f"**Localidad:** {oferta['localidad_empresa']}")


    # # --- Tutores de la empresa ---
    # if tutor_empresa:
    #     st.markdown("**👩‍🏫 Tutores de la empresa:**")
    #     for t in tutor_empresa:
    #         st.markdown(f"- {t.get('nombre', '—')} ({t.get('email', '—')})")
    # else:
    #     st.markdown("**👩‍🏫 Tutores de la empresa:** No asignados")


# if not estadosEmpresa:
#     mostrar_fases(fasesEmpresa, fase2colEmpresa, None)
#     estado_actual = {}
# else:
#     mostrar_fases(fasesEmpresa, fase2colEmpresa, estadosEmpresa[0])
#     estado_actual = estadosEmpresa[0]