import streamlit as st
from datetime import datetime
import json, re
from modules.forms_helper import required_ok, slug
from modules.data_base import upsert,add
from variables import empresaEstadosTabla,empresasTabla,necesidadFP,ciclos, preferencias,estados
# ---------------------------------
# Config
# ---------------------------------
st.set_page_config(page_title="Empresas Formación", page_icon="🏢", layout="centered")

TITLE = "Formación Empresas"
SUBTITLE = "Ficha 2025/2026"
DESCRIPTION = (
    "⚙️ **Objetivo:** Este formulario permite registrar a vuestra empresa para participar "
    "en el programa de Formación en Centros de Trabajo (FCT). "
    "Por favor, completad todos los campos con la información solicitada."
)

CICLOS = ciclos

AREAS_JSON = preferencias

AREAS_MAP = json.loads(AREAS_JSON)

# ---------------------------------
# UI
# ---------------------------------
st.title(TITLE)
st.subheader(SUBTITLE)
st.write(DESCRIPTION)

st.write("DATOS DE LA EMPRESA Y PERSONA DE CONTACTO")
col1, col2 = st.columns(2)
with col1:
    nombre_empresa = st.text_input("Nombre de la empresa *")
    direccion = st.text_input("Dirección *")
    cp = st.text_input("Código Postal *")
    localidad = st.text_input("Localidad *")
    cif = st.text_input("CIF *")
    horario_inicio = st.time_input("Horario Empresa inicio *", step=900)
    pagina_web = st.text_input("Página web")
with col2:
    nombre_contacto = st.text_input("Nombre de la persona que rellena el formulario *")
    telefono_contacto = st.text_input("Teléfono de contacto *")
    email_contacto = st.text_input("Email de contacto *")
    nombre_responsable = st.text_input("Nombre del responsable legal *")
    nie_responsable = st.text_input("NIF del responsable legal *")
    horario_fin = st.time_input("Horario Empresa fin *", step=900)
st.divider()
st.write("DATOS DEL TUTOR DE LA EMPRESA (PERSONA QUE SE ENCARGARÁ DE SEGUIR AL ALUMNO EN PRÁCTICAS)")
col1, col2 = st.columns(2)
with col1:
    nombre_tutor = st.text_input("Nombre Completo del tutor *")
    nif_tutor = st.text_input("NIF del tutor *")
with col2:
    email_tutor = st.text_input("Email del tutor *")
    telefono_tutor = st.text_input("Teléfono del tutor *")
st.divider()
st.write("DIRECCIÓN DEL CENTRO DE TRABAJO DONDE SE REALIZARÁN LAS PRÁCTICAS")
direccion_centro = st.text_input("Dirección del centro de trabajo")
col1, col2 = st.columns(2)
with col1:
    cp_centro = st.text_input("Código Postal del centro de trabajo")
with col2:
    localidad_centro = st.text_input("Localidad del centro de trabajo")
st.divider()
st.write("INFORMACIÓN ADICIONAL")
posible_contrato = st.radio(
    "Si el alumno cubre vuestras expectativas, ¿habría posibilidad de hacerle un contrato laboral? *",
    ["Sí", "No"],
    horizontal=True
)
vehiculo = st.radio("¿Se necesita vehículo propio para acceder a vuestras instalaciones? *", ["Sí", "No"], horizontal=True)
st.divider()
# --- Ciclos y cantidad ---
st.write("¿DE QUE CICLO/S FORMATIVO/S OS INTERESA INCORPORAR ALUMNOS EN PRÁCTICAS Y CANTIDAD DE ALUMNO POR CADA UNO?(Puedes seleccionar uno o varios)")
st.write("Selecciona los ciclos y especifica la cantidad de alumnos por cada uno:")
selected_ciclos = []
cantidades = {}

with st.expander("Seleccionar ciclos y cantidad de alumnos", expanded=False):
    for ciclo in CICLOS:
        col1, col2 = st.columns([3, 1])
        with col1:
            sel = st.checkbox(ciclo, key=f"chk_{slug(ciclo)}")
        with col2:
            if sel:
                cantidad = st.number_input(f"Cantidad - {ciclo}", min_value=1, max_value=50, step=1, key=f"num_{slug(ciclo)}")
                selected_ciclos.append(ciclo)
                cantidades[ciclo] = cantidad

# --- Puestos / áreas ---
puestos_seleccionados = {}
if selected_ciclos:
    st.write("¿EN QUÉ PUESTOS/ÁREAS SE DESARROLLARÍA LA PRÁCTICA? - DESCRIBE EN QUÉ PROYECTO/S PODRÍA COLABORAR EL ALUMNO EN PRÁCTICAS.")
    for ciclo in selected_ciclos:
        with st.expander(f"{ciclo}", expanded=False):
            opciones = AREAS_MAP.get(ciclo, [])
            for area in opciones:
                col1, col2 = st.columns([3, 2])
                with col1:
                    elegido = st.checkbox(area, key=f"chk_area_{slug(ciclo)}_{slug(area)}")
                with col2:
                    if elegido:
                        proyecto = st.text_input(f"Proyecto relacionado ({area})", key=f"proy_{slug(ciclo)}_{slug(area)}")
                        puestos_seleccionados.setdefault(ciclo, []).append({"area": area, "proyecto": proyecto})

st.write("REQUISITOS ADICIONALES")
requisitos = st.text_area(
    "Por favor, indícanos si el alumno debe cumplir algún requisito adicional (por ejemplo, B1 de inglés, trabajo en equipo, residencia, etc.) *"
)

# ---------------------------------
# Validación
# ---------------------------------
required_fields = {
    "Nombre empresa": nombre_empresa,
    "Dirección": direccion,
    "CP": cp,
    "Localidad": localidad,
    "CIF": cif,
    "Persona contacto": nombre_contacto,
    "Teléfono contacto": telefono_contacto,
    "Email contacto": email_contacto,
    "Responsable legal": nombre_responsable,
    "NIE responsable": nie_responsable,
    "Tutor": nombre_tutor,
    "NIF tutor": nif_tutor,
    "Email tutor": email_tutor,
    "Teléfono tutor": telefono_tutor,
    "Horario inicio": horario_inicio,
    "Horario fin": horario_fin,
    "Posible contrato": posible_contrato,
    "Vehículo": vehiculo,
    "Ciclos seleccionados": selected_ciclos
}

faltantes = [k for k, v in required_fields.items() if not required_ok(v)]

if faltantes:
    st.info("Completa los campos obligatorios: " + ", ".join(faltantes))

can_submit = len(faltantes) == 0
submit = st.button("Enviar formulario", disabled=not can_submit)

# ---------------------------------
# Submit
# ---------------------------------
if submit:
    payloadEmpresa = {
        "nombre": nombre_empresa.strip(),
        "direccion": direccion.strip(),
        "codigo_postal": cp.strip(),
        "localidad": localidad.strip(),
        "CIF": cif.strip().upper(),
        "telefono": telefono_contacto.strip(),
        "email_empresa": email_contacto.strip().lower(),
        "responsable_legal": nombre_responsable.strip(),
        "nif_responsable_legal": nie_responsable.strip(),
        "horario": str(horario_inicio) + " - " + str(horario_fin),
        "pagina_web": pagina_web.strip(),

    }
    ofertaPayload={
        "contrato": posible_contrato,
        "vehiculo": vehiculo,
        "ciclos_formativos": cantidades,
        "puestos": puestos_seleccionados,
        "requisitos": requisitos.strip(),
        "estado": estados[0],
        "nombre_tutor": nombre_tutor.strip(),
        "nif_tutor": nif_tutor.strip(),
        "email_tutor": email_tutor.strip().lower(),
        "telefono_tutor": telefono_tutor.strip(),
        "direccion_empresa": direccion_centro.strip(),
        "cp_empresa": cp_centro.strip(),
        "localidad_empresa": localidad_centro.strip(),
        "nombre_rellena_form": nombre_contacto.strip(),
    }
    res_emp = upsert(empresasTabla, payloadEmpresa, keys=["CIF"])
    if res_emp and res_emp.data:
        upsert(empresaEstadosTabla,
                {"empresa": res_emp.data[0]["CIF"], "form_completo": datetime.now().isoformat()},
                keys=["empresa"],
            )
        add(necesidadFP, ofertaPayload | {"empresa": res_emp.data[0]["CIF"]})
    st.success("✅ ¡Formulario de empresa enviado correctamente!")
