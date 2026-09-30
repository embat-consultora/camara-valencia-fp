import streamlit as st
import json
import logging
import random
import smtplib
from datetime import datetime, time
from httpx import HTTPError
from modules.forms_helper import required_ok, slug
from modules.data_base import upsert,add, upsertCustome,getCiclosYAreas,getEqual
from modules.emailSender import send_welcome_email
from postgrest.exceptions import APIError
from streamlit_javascript import st_javascript
from variables import empresaEstadosTabla,formTabla,empresasTabla,necesidadFP,estados,tutoresTabla,localidades,sectorEmpresa,usuariosTabla

logger = logging.getLogger(__name__)
DRAFT_STORAGE_KEY = "form_empresa_draft_v1"
DRAFT_LOADED_KEY = "_form_empresa_draft_loaded"
FORM_SUBMITTED_KEY = "_form_empresa_submitted"
# ---------------------------------
# Config
# ---------------------------------
st.set_page_config(page_title="Empresas Formación", page_icon="🏢", layout="centered")
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@300;400;700&display=swap');

    /* Esto aplica la fuente a toda la app */
    html, body, [class*="css"], .stApp {
        font-family: 'Montserrat', sans-serif;
    }
    </style>
    """,
    unsafe_allow_html=True
)
curso_academico = st.query_params.get("curso_academico","2026-2027")
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

try:
    formValues = getEqual(formTabla, "tipo", "empresa")
    if not formValues:
        raise RuntimeError("No existe la configuración del formulario de empresa.")
    TITLE = formValues[0].get("titulo", "Formulario de Formación en Empresa")
    SUBTITLE = formValues[0].get("subtitulo", "Este formulario tiene como objetivo conocer vuestras preferencias para la Formación en Empresa.")
    DESCRIPTION = formValues[0].get("description",
        "⚙️ Objetivo: Este formulario permite registrar a vuestra empresa para participar en el Formación en Empresa (FE). Por favor, completad todos los campos con la información solicitada."
    )
    CICLOS,AREAS_MAP = getCiclosYAreas()
except (APIError, HTTPError, IndexError, KeyError, TypeError, RuntimeError) as error:
    logger.exception("No se pudo cargar la configuración del formulario de empresa")
    st.error(
        "No se pudo cargar el formulario de empresa. Comprueba la conexión e inténtalo de nuevo "
        "más tarde. Si el problema continúa, contacta con el administrador."
    )
    st.caption(f"Tipo de error: {type(error).__name__}")
    st.stop()

draft_widget_keys = [
    "nombre_empresa",
    "nombre_contacto",
    "sector",
    "telefono_contacto",
    "direccion",
    "email_contacto",
    "cp",
    "nombre_responsable",
    "localidad",
    "nie_responsable",
    "cif",
    "fin",
    "inicio",
    "pagina_web",
    "nombre_tutor",
    "email_tutor",
    "nif_tutor",
    "telefono_tutor",
    "direccion_centro",
    "cp_centro",
    "localidad_centro",
    "posible_contrato",
    "vehiculo",
    "requisitos",
]
valid_widget_options = {
    "sector": sectorEmpresa,
    "localidad": localidades,
    "posible_contrato": ["Sí", "No"],
    "vehiculo": ["Sí", "No"],
}
time_widget_keys = {"fin", "inicio"}
for ciclo in CICLOS:
    ciclo_key = slug(ciclo)
    draft_widget_keys.extend((f"chk_{ciclo_key}", f"num_{ciclo_key}"))
    for area in AREAS_MAP.get(ciclo, []):
        area_key = slug(area)
        draft_widget_keys.extend((
            f"chk_area_{ciclo_key}_{area_key}",
            f"proy_{ciclo_key}_{area_key}",
        ))


def load_form_draft():
    if st.session_state.get(DRAFT_LOADED_KEY):
        return

    draft = st_javascript(
        f"""(() => {{
            try {{
                const value = sessionStorage.getItem({json.dumps(DRAFT_STORAGE_KEY)});
                return value === null ? null : JSON.parse(value);
            }} catch (error) {{
                return {{__storage_error: String(error)}};
            }}
        }})()""",
        key="form_empresa_draft_load",
    )
    if draft == 0:
        return

    if isinstance(draft, dict) and "__storage_error" in draft:
        st.warning("No se pudo recuperar el borrador guardado en este navegador.")
    elif isinstance(draft, dict):
        for key, value in draft.items():
            if key not in draft_widget_keys:
                continue
            if key in valid_widget_options and value not in valid_widget_options[key]:
                continue
            if key in time_widget_keys:
                if not isinstance(value, str):
                    continue
                try:
                    value = time.fromisoformat(value)
                except ValueError:
                    continue
            elif key.startswith("chk_"):
                if not isinstance(value, bool):
                    continue
            elif key.startswith("num_"):
                if (
                    not isinstance(value, int)
                    or isinstance(value, bool)
                    or not 1 <= value <= 50
                ):
                    continue
            elif not isinstance(value, str):
                continue
            st.session_state[key] = value
    elif draft is not None:
        st.warning("El borrador del navegador no tiene un formato válido y no se pudo recuperar.")

    st.session_state[DRAFT_LOADED_KEY] = True


def save_form_draft():
    draft = {}
    for key in draft_widget_keys:
        if key not in st.session_state:
            continue
        value = st.session_state[key]
        if isinstance(value, time):
            value = value.isoformat()
        draft[key] = value

    draft_json = json.dumps(draft, ensure_ascii=False)
    result = st_javascript(
        f"""(() => {{
            try {{
                sessionStorage.setItem(
                    {json.dumps(DRAFT_STORAGE_KEY)},
                    {json.dumps(draft_json, ensure_ascii=False)}
                );
                return {{ok: true}};
            }} catch (error) {{
                return {{__storage_error: String(error)}};
            }}
        }})()""",
        key=f"form_empresa_draft_save_{hash(draft_json)}",
    )
    if isinstance(result, dict) and "__storage_error" in result:
        st.warning("No se pudo guardar el borrador en este navegador.")
    elif isinstance(result, dict) and result.get("ok"):
        st.caption("El borrador se guarda temporalmente en esta pestaña y se elimina al enviar.")


def clear_form_draft():
    result = st_javascript(
        f"""(() => {{
            try {{
                sessionStorage.removeItem({json.dumps(DRAFT_STORAGE_KEY)});
                return {{ok: true}};
            }} catch (error) {{
                return {{__storage_error: String(error)}};
            }}
        }})()""",
        key="form_empresa_draft_save",
    )
    if isinstance(result, dict) and "__storage_error" in result:
        st.warning("No se pudo borrar el borrador guardado en este navegador.")


load_form_draft()
if st.session_state.get(FORM_SUBMITTED_KEY):
    st.success("✅ ¡Formulario de empresa enviado correctamente! Ya puede cerrar la ventana.")
    st.stop()


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
with col2:
    nombre_contacto = input_requerido("Nombre de la persona que rellena el formulario *", key="nombre_contacto")

col1, col2 = st.columns(2)
with col1:
    sector = st.selectbox("Sector de la empresa *", (sectorEmpresa), key="sector")
with col2:
    telefono_contacto = input_requerido("Teléfono de contacto *", key="telefono_contacto")

col1, col2 = st.columns(2)
with col1:
    direccion = input_requerido("Dirección *", key="direccion")
with col2:
    email_contacto = input_requerido("Email de contacto *", key="email_contacto")

col1, col2 = st.columns(2)
with col1:
    cp = input_requerido("Código Postal *", key="cp")
with col2:
    nombre_responsable = input_requerido("Nombre del responsable legal *", key="nombre_responsable")

col1, col2 = st.columns(2)
with col1:
    localidad = st.selectbox("Localidad *", (localidades), key="localidad")
with col2:
    nie_responsable = input_requerido("NIF del responsable legal *", key="nie_responsable")

col1, col2 = st.columns(2)
with col1:
    cif = input_requerido("CIF *", key="cif")
with col2:
    horario_fin = st.time_input("Horario Empresa fin *", step=900, key="fin")

col1, col2 = st.columns(2)
with col1:
    horario_inicio = st.time_input("Horario Empresa inicio *", step=900, key="inicio")
with col2:
    pagina_web = st.text_input("Página web", key="pagina_web")
st.divider()
st.write("DATOS DEL TUTOR DE LA EMPRESA (PERSONA QUE SE ENCARGARÁ DE SEGUIR AL ALUMNO EN FORMACIONES)")
col1, col2 = st.columns(2)
with col1:
    nombre_tutor = input_requerido("Nombre Completo del tutor *", key="nombre_tutor")
with col2:
    email_tutor = input_requerido("Email del tutor *", key="email_tutor")

col1, col2 = st.columns(2)
with col1:
    nif_tutor = input_requerido("NIF del tutor *", key="nif_tutor")
with col2:
    telefono_tutor = input_requerido("Teléfono del tutor *", key="telefono_tutor")
st.divider()
st.write("DIRECCIÓN DEL CENTRO DE TRABAJO DONDE SE REALIZARÁN LAS FORMACIONES")
direccion_centro = st.text_input("Dirección del centro de trabajo", key="direccion_centro")
col1, col2 = st.columns(2)
with col1:
    cp_centro = st.text_input("Código Postal del centro de trabajo", key="cp_centro")
with col2:
    localidad_centro = st.text_input("Localidad del centro de trabajo", key="localidad_centro")
st.divider()
st.write("INFORMACIÓN ADICIONAL")
posible_contrato = st.radio(
    "Si el alumno cubre vuestras expectativas, ¿habría posibilidad de hacerle un contrato laboral? *",
    ["Sí", "No"],
    horizontal=True,
    key="posible_contrato",
)
vehiculo = st.radio(
    "¿Se necesita vehículo propio para acceder a vuestras instalaciones? *",
    ["Sí", "No"],
    horizontal=True,
    key="vehiculo",
)
st.divider()
# --- Ciclos y cantidad ---
st.write("¿DE QUE CICLO/S FORMATIVO/S OS INTERESA INCORPORAR ALUMNOS EN FORMACIONES Y CANTIDAD DE ALUMNO POR CADA UNO?(Puedes seleccionar uno o varios)")
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
    st.write("¿EN QUÉ PUESTOS/ÁREAS SE DESARROLLARÍA LA FORMACIÓN? - DESCRIBE EN QUÉ PROYECTO/S PODRÍA COLABORAR EL ALUMNO EN FORMACIONES.")
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
    "Por favor, indícanos si el alumno debe cumplir algún requisito adicional (por ejemplo, B1 de inglés, trabajo en equipo, residencia, etc.) *",
    key="requisitos",
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
if st.session_state.get(DRAFT_LOADED_KEY):
    save_form_draft()
submit = st.button("Enviar formulario", disabled=not can_submit)


# ---------------------------------
# Submit
# ---------------------------------
if submit:
    with st.spinner("⏳ Enviando formulario, por favor espera..."):
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
            "estado": estados[4],
            "direccion_empresa": direccion.strip() if not direccion_centro.strip() else direccion_centro.strip(),
            "cp_empresa": cp.strip() if not cp_centro.strip() else cp_centro.strip(),
            "localidad_empresa": localidad.strip() if not localidad_centro.strip() else localidad_centro.strip(),
            "nombre_rellena_form": nombre_contacto.strip(),
            "cupo_alumnos": sum(v["alumnos"] for v in cantidades.values()) if cantidades else 0,
            "anio": curso_academico
        }

        paso_actual = "guardar la empresa"
        try:
            res_emp = upsert(empresasTabla, payloadEmpresa, keys=["CIF"])
            if not res_emp or not res_emp.data:
                raise RuntimeError("La base de datos no devolvió la empresa guardada.")

            empresa_cif = res_emp.data[0]["CIF"]
            paso_actual = "guardar el estado de la empresa"
            upsert(empresaEstadosTabla,
                {"empresa": empresa_cif, "form_completo": datetime.now().isoformat()},
                keys=["empresa"],
            )

            paso_actual = "guardar el tutor"
            tutor = upsertCustome(tutoresTabla, {
                "cif_empresa": empresa_cif,
                "nombre": nombre_tutor.strip(),
                "nif": nif_tutor.strip().upper(),
                "email": email_tutor.strip().lower(),
                "telefono": telefono_tutor.strip()
            }, keys=["nif"])
            if not tutor or not tutor.data:
                raise RuntimeError("La base de datos no devolvió el tutor guardado.")

            ofertaPayload["tutor"] = tutor.data[0]["id"]
            paso_actual = "guardar la oferta formativa"
            oferta = add(necesidadFP, ofertaPayload | {"empresa": empresa_cif})
            if not oferta or not oferta.data:
                raise RuntimeError("La base de datos no devolvió la oferta guardada.")

            paso_actual = "crear el usuario de la empresa"
            new_pass = f"{empresa_cif}{random.randint(10, 99)}"
            _, usuario_creado = upsertCustome(usuariosTabla, {
                "email": empresa_cif,
                "password": new_pass,
                "rol": "empresa",
            }, keys=["email"], return_created=True)

            paso_actual = "crear el usuario del tutor"
            new_passT = f"{nif_tutor}{random.randint(10, 99)}"
            _, usuario_creadoT = upsertCustome(usuariosTabla, {
                "email": nif_tutor,
                "password": new_passT,
                "rol": "tutor",
            }, keys=["email"], return_created=True)
        except (APIError, HTTPError, KeyError, IndexError, TypeError, ValueError, RuntimeError) as error:
            logger.exception("Error en el formulario de empresa durante: %s", paso_actual)
            st.error(
                f"No se pudo completar el envío al intentar {paso_actual}. "
                "Es posible que algunos datos ya se hayan guardado; contacta con el administrador "
                "antes de volver a enviar el formulario."
            )
            st.caption(f"Tipo de error: {type(error).__name__}")
        else:
            errores_email = []
            if usuario_creado and email_contacto.strip():
                try:
                    send_welcome_email(
                        email_contacto.strip().lower(),
                        empresa_cif,
                        new_pass,
                        nombre_empresa.strip(),
                    )
                except (smtplib.SMTPException, OSError, KeyError, TypeError, ValueError):
                    logger.exception("No se pudo enviar el email de bienvenida a la empresa")
                    errores_email.append("la empresa")

            if usuario_creadoT and email_tutor.strip():
                try:
                    send_welcome_email(
                        email_tutor.strip().lower(),
                        nif_tutor,
                        new_passT,
                        nombre_tutor.strip(),
                    )
                except (smtplib.SMTPException, OSError, KeyError, TypeError, ValueError):
                    logger.exception("No se pudo enviar el email de bienvenida al tutor")
                    errores_email.append("el tutor")

            st.session_state[FORM_SUBMITTED_KEY] = True
            clear_form_draft()
            st.success("✅ ¡Formulario de empresa enviado correctamente! Ya puede cerrar la ventana")
            if errores_email:
                st.warning(
                    "El formulario se guardó, pero no se pudo enviar el email de bienvenida para "
                    + " y ".join(errores_email)
                    + ". Contacta con el administrador para obtener las credenciales."
                )
