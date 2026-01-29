import streamlit as st
from modules.data_base import (
    getEquals, getOrdered, crearPractica, upsert
)
from page_utils import apply_page_config
from navigation import make_sidebar
from datetime import datetime
from variables import (alumnosTabla, empresasTabla,tipoPracticas,formFieldsTabla,estadosAlumno)
import json
# ----------------------------------------------
# CONFIG
# ----------------------------------------------
# Importante: set_page_config debe ir antes de apply_page_config si esta última no lo tiene
st.set_page_config(page_title="Prácticas autogestionada", page_icon="🚀", layout="wide")
apply_page_config()
make_sidebar()

st.markdown("<h2 style='text-align: center;'>🚀 Gestión de Prácticas Autogestionadas</h2>", unsafe_allow_html=True)
now = datetime.now().isoformat()

# ----------------------------------------------
# LÓGICA DE CARGA DE DATOS
# ----------------------------------------------
def fetch_alumnos_empresas():
    alumnos = getOrdered(
        alumnosTabla,
        searchFor="estado",
        searchValue="Sin Empresa",
        orderByColumn="tipoPractica"
    )
    empresas = getEquals(empresasTabla, {})
    return alumnos, empresas

if "data_loaded" not in st.session_state:
    st.session_state["data_loaded"] = False

def load_data(force=False):
    if not st.session_state["data_loaded"] or force:
        with st.spinner("Actualizando datos..."):
            alumnos, empresas = fetch_alumnos_empresas()
            st.session_state["alumnos"] = alumnos
            st.session_state["empresas"] = empresas
            st.session_state["data_loaded"] = True

load_data()
st.info("Utiliza esta sección para dar de alta rápidamente una empresa y un alumno que no existen en la base de datos y vincularlos en una práctica.")

# 1. DATOS DE LA EMPRESA
st.subheader("🏢 Datos de la Empresa")
c1, c2 = st.columns(2)
new_emp_nombre = c1.text_input("Nombre Comercial / Razón Social", key="qr_emp_nom")
new_emp_cif = c2.text_input("CIF (Obligatorio)", key="qr_emp_cif").upper().strip()

c1_2, c2_2 = st.columns(2)
new_emp_tel = c1_2.text_input("Teléfono Empresa", key="qr_emp_tel")
new_emp_email = c2_2.text_input("Email Empresa", key="qr_emp_email")

st.divider()

# 2. DATOS DEL ALUMNO
st.subheader("🧑‍🎓 Datos del Alumno")
c3, c4, c5 = st.columns([1, 1, 1.5])
new_alu_dni = c3.text_input("DNI (Obligatorio)", key="qr_alu_dni").upper().strip()
new_alu_nombre = c4.text_input("Nombre", key="qr_alu_nom")
new_alu_apellido = c5.text_input("Apellidos", key="qr_alu_ape")

new_alu_email = st.text_input("Email Alumno", key="qr_alu_email")

# 3. CONFIGURACIÓN DE PRÁCTICA Y CICLO
st.subheader("📋 Configuración de la Práctica")
col_p1, col_p2 = st.columns(2)

# Obtenemos los tipos de práctica de tus variables
new_alu_tipo = col_p1.selectbox(
    "Tipo de Práctica", 
    options=tipoPracticas, 
    key="qr_alu_tipo"
)

# Lógica de Ciclos Formativos (Basada en tu código de alumnos)
form_fields = getEquals(formFieldsTabla, {"category": "Alumno", "type": "Opciones"})
ciclo_field = next((f for f in form_fields if f["columnName"] == "ciclo_formativo"), None)
pref_field = next((f for f in form_fields if f["columnName"] == "preferencias_fp"), None)

ciclos_opts = json.loads(ciclo_field["options"]) if ciclo_field else []
prefs_opts_dict = json.loads(pref_field["options"]) if pref_field else {}

new_alu_ciclo = col_p2.selectbox(
    "Ciclo Formativo",
    options=[""] + ciclos_opts,
    key="qr_alu_ciclo"
)

new_alu_pref = []
if new_alu_ciclo and new_alu_ciclo in prefs_opts_dict:
    new_alu_pref = st.multiselect(
        "Preferencias/Áreas",
        options=prefs_opts_dict[new_alu_ciclo],
        key="qr_alu_pref"
    )

# 4. BOTÓN DE ACCIÓN
if st.button("🚀 Guardar y Vincular Práctica", use_container_width=True):
    if not new_emp_cif or not new_alu_dni or not new_emp_nombre or not new_alu_nombre:
        st.error("⚠️ CIF, DNI y Nombres son obligatorios para procesar el alta.")
    else:
        with st.spinner("Procesando alta rápida..."):
            try:
                # A. Alta Empresa
                upsert(empresasTabla, {
                    "CIF": new_emp_cif,
                    "nombre": new_emp_nombre,
                    "telefono": new_emp_tel,
                    "email_empresa": new_emp_email
                }, keys=["CIF"])

                # B. Alta Alumno
                upsert(alumnosTabla, {
                    "dni": new_alu_dni,
                    "nombre": new_alu_nombre,
                    "apellido": new_alu_apellido,
                    "email_alumno": new_alu_email,
                    "tipoPractica": new_alu_tipo,
                    "ciclo_formativo": new_alu_ciclo,
                    "preferencias_fp": new_alu_pref,
                    "estado": estadosAlumno[1]
                }, keys=["dni"])

                # C. Crear la Práctica (Vincular)
                # Usamos los parámetros que requiere tu función crearPractica
                crearPractica(
                    empresaCif=new_emp_cif,
                    alumnoDni=new_alu_dni,
                    ciclo=new_alu_ciclo if new_alu_ciclo else "Autogestionado",
                    area="General",
                    proyecto="Alta Rápida",
                    fecha=datetime.now().isoformat(),
                    ciclos_info=None,
                    cupos_disp=None,
                    oferta_id=None
                )

                st.success(f"✅ ¡Éxito! Práctica creada entre {new_emp_nombre} y {new_alu_nombre}.")
                
                # Limpiamos caché de sesión si usas una
                if "data_loaded" in st.session_state:
                    st.session_state["data_loaded"] = False
                
                st.rerun()

            except Exception as e:
                st.error(f"❌ Error en el proceso: {str(e)}")