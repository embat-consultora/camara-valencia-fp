import streamlit as st
from datetime import datetime
import json
from modules.forms_helper import required_ok, slug
from modules.data_base import upsert,add
from variables import empresaEstadosTabla,empresasTabla,necesidadFP,ciclos, preferencias,estados,tutoresTabla,localidades,sectorEmpresa
# ---------------------------------
# Config
# ---------------------------------
st.set_page_config(page_title="Empresas Formación", page_icon="🏢", layout="centered")
st.markdown("""
<style>
div[data-testid="stTextInput"] input {
    border: 2px solid #1E90FF; /* azul */
    border-radius: 8px;
    padding: 6px;
}
</style>
""", unsafe_allow_html=True)
st.image("./images/cv-fp.png", width=250)
TITLE = "Formación Empresas"
SUBTITLE = "Ficha 2025/2026"
DESCRIPTION = (
    "⚙️ **Objetivo:** Este formulario permite registrar a vuestra empresa para participar "
    "en el Formación en Empresa (FE). "
    "Por favor, completad todos los campos con la información solicitada."
)

CICLOS = ciclos

AREAS_JSON = preferencias

AREAS_MAP = json.loads(AREAS_JSON)

def input_requerido(label, key=None, **kwargs):
    """Input obligatorio con mensaje inline inmediato"""
    valor = st.text_input(label, key=key, **kwargs)
    # Si el valor está vacío, mostrar mensaje en rojo
    if not valor.strip():
        st.markdown("<span style='color:red;font-size:0.9em;'>Este valor es requerido</span>", unsafe_allow_html=True)
    return valor

# ---------------------------------
# UI
# ---------------------------------
st.title(TITLE)
st.subheader(SUBTITLE)
st.write(DESCRIPTION)

st.write("DATOS DE LA EMPRESA Y PERSONA DE CONTACTO")
col1, col2 = st.columns(2)
with col1:
    nombre_empresa = input_requerido("Nombre de la empresa *", key="nombre_empresa")
    sector = st.selectbox("Sector de la empresa *", (sectorEmpresa), key="sector")
    direccion = input_requerido("Dirección *", key="direccion")
    cp = input_requerido("Código Postal *", key="cp")
    localidad = st.selectbox("Localidad *", (localidades), key="localidad")
    cif = input_requerido("CIF *", key="cif")
    horario_inicio = st.time_input("Horario Empresa inicio *", step=900, key="inicio")
    pagina_web = st.text_input("Página web")
with col2:
    nombre_contacto = input_requerido("Nombre de la persona que rellena el formulario *", key="nombre_contacto")
    telefono_contacto = input_requerido("Teléfono de contacto *", key="telefono_contacto")
    email_contacto = input_requerido("Email de contacto *", key="email_contacto")
    nombre_responsable = input_requerido("Nombre del responsable legal *", key="nombre_responsable")
    nie_responsable = input_requerido("NIF del responsable legal *", key="nie_responsable")
    horario_fin = st.time_input("Horario Empresa fin *", step=900)
st.divider()
st.write("DATOS DEL TUTOR DE LA EMPRESA (PERSONA QUE SE ENCARGARÁ DE SEGUIR AL ALUMNO EN PRÁCTICAS)")
col1, col2 = st.columns(2)
with col1:
    nombre_tutor = input_requerido("Nombre Completo del tutor *", key="nombre_tutor")
    nif_tutor = input_requerido("NIF del tutor *", key="nif_tutor")
with col2:
    email_tutor = input_requerido("Email del tutor *", key="email_tutor")
    telefono_tutor = input_requerido("Teléfono del tutor *", key="telefono_tutor")
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
                cantidades[ciclo] = {
                    "alumnos": cantidad,
                    "disponibles": cantidad
                }
if not selected_ciclos:
    st.markdown("<span style='color:red;'>Debes seleccionar al menos un ciclo formativo</span>", unsafe_allow_html=True)
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
                        proyecto = st.text_input(
                            f"Proyecto relacionado ({area})",
                            key=f"proy_{slug(ciclo)}_{slug(area)}"
                        )
                        # agregamos el área/proyecto al ciclo
                        puestos_seleccionados.setdefault(ciclo, [])
                        # evitamos duplicados
                        if not any(p["area"] == area for p in puestos_seleccionados[ciclo]):
                            puestos_seleccionados[ciclo].append(
                                {"area": area, "proyecto": proyecto}
                            )
                    else:
                        # si se desmarca, lo quitamos del diccionario
                        if ciclo in puestos_seleccionados:
                            puestos_seleccionados[ciclo] = [
                                p for p in puestos_seleccionados[ciclo] if p["area"] != area
                            ]
if not puestos_seleccionados:
    st.markdown("<span style='color:red;'>Debes seleccionar al menos un puesto/area</span>", unsafe_allow_html=True)
st.write("REQUISITOS ADICIONALES")
requisitos = st.text_area(
    "Por favor, indícanos si el alumno debe cumplir algún requisito adicional (por ejemplo, B1 de inglés, trabajo en equipo, residencia, etc.) *"
)
errores_ciclos = []
for ciclo in selected_ciclos:
    # validar cantidad de alumnos
    if ciclo not in cantidades or cantidades[ciclo]["alumnos"] <= 0:
        errores_ciclos.append(f"Cantidad de alumnos en {ciclo}")

    # validar que haya al menos un área seleccionada
    if ciclo not in puestos_seleccionados or not puestos_seleccionados[ciclo]:
        errores_ciclos.append(f"Área no seleccionada en {ciclo}")

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

can_submit = len(faltantes) == 0 and len(errores_ciclos) == 0 and len(selected_ciclos) > 0

st.write("*Si completó todo el formulario, y aun no se habilita el botón de enviar, presione dentro y fuera de los campos nombrados.")
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
        "sectorEmpresa": sector.strip()

    }
    ofertaPayload={
        "contrato": posible_contrato,
        "vehiculo": vehiculo,
        "ciclos_formativos": cantidades,
        "puestos": puestos_seleccionados,
        "requisitos": requisitos.strip(),
        "estado": estados[0],
        "direccion_empresa": direccion.strip() if not direccion_centro.strip() else direccion_centro.strip(),
        "cp_empresa": cp.strip() if not cp_centro.strip() else cp_centro.strip(),
        "localidad_empresa": localidad.strip() if not localidad_centro.strip() else localidad_centro.strip(),
        "nombre_rellena_form": nombre_contacto.strip(),
        "cupo_alumnos": sum(v["alumnos"] for v in cantidades.values()) if cantidades else 0,
    }
    res_emp = upsert(empresasTabla, payloadEmpresa, keys=["CIF"])
    if res_emp and res_emp.data:
        upsert(empresaEstadosTabla,
                {"empresa": res_emp.data[0]["CIF"], "form_completo": datetime.now().isoformat()},
                keys=["empresa"],
            )
        tutor = upsert(tutoresTabla, {
            "cif_empresa": res_emp.data[0]["CIF"],
            "nombre": nombre_tutor.strip(),
            "nif": nif_tutor.strip().upper(),
            "email": email_tutor.strip().lower(),
            "telefono": telefono_tutor.strip()
        }, keys=["nif"])
        ofertaPayload["tutor"] = tutor.data[0]["id"] if tutor and tutor.data else None
        oferta = add(necesidadFP, ofertaPayload | {"empresa": res_emp.data[0]["CIF"]})

    st.success("✅ ¡Formulario de empresa enviado correctamente!")
