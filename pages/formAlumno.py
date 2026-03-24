import streamlit as st
from pathlib import Path
from datetime import datetime
import json, uuid
from modules.drive_helper import upload_to_drive
from modules.data_base import upsert
from modules.forms_helper import required_ok, file_size_bytes, slug
from variables import carpetaAlumnos,estadosAlumno,alumnosTabla,alumnoEstadosTabla,ciclos, preferencias,max_file_size, localidades,cursoList , aniosList

# ---------------------------------
# Config
# ---------------------------------
st.set_page_config(page_title="Alumnos Formación", page_icon="🏫", layout="centered")
st.image("./images/cv-fp.png", width=250)
TITLE = "Alumnos Formación"
SUBTITLE = "Este formulario tiene como objetivo conocer vuestras preferencias para la Formación en Empresa."
DESCRIPTION = (
    "⚠️ **Importante**: La información que facilitéis será tenida en cuenta en el proceso de asignación, "
    "pero la decisión final dependerá de: el tipo de empresas solicitantes, los requisitos que planteen "
    "y vuestro perfil, potencial y desempeño académico. Por tanto, aunque intentaremos ajustarnos en la "
    "medida de lo posible a vuestras preferencias, **no podemos garantizar** que se cumplan."
)

CICLOS = ciclos

PREFERENCIAS_JSON = preferencias
PREFS_MAP = json.loads(PREFERENCIAS_JSON)

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

# Datos personales
st.subheader("Datos personales")
col1, col2 = st.columns(2)
with col1:
    nombre = input_requerido("Nombre *", key="nombre_alumno")
    email = input_requerido("Email *", key="email_alumno")
    dni = input_requerido("DNI/NIE *", key="dni_alumno")
    cp = input_requerido("Código Postal *", key="cp_alumno")
    ano = st.selectbox("Año *", aniosList, key="ano_alumno")
with col2:
    apellidos = input_requerido("Apellidos *", key="apellidos_alumno")
    direccion = input_requerido("Dirección *", key="direccion_alumno")
    localidad = st.selectbox("Localidad *", (localidades), key="localidad_alumno")
    sexo = st.selectbox("Sexo *", ("Prefiero No especificar","Femenino", "Masculino"), key="sexo_alumno")
    nuss = st.text_input("NUSS", key="nuss_alumno")
    curso = st.selectbox("Curso *", cursoList, key="curso_alumno")

vehiculo = st.radio("¿Dispones de vehículo? *", ["Sí", "No"], horizontal=True)

st.subheader("Tipo de práctica")
tipo_practica = st.radio(
    "Indica si tu práctica es autogestionada o si prefieres que sea asignada por el centro:",
    ["Práctica autogestionada", "Práctica asignada por el centro"],
    index=None,
    horizontal=False
)
if not tipo_practica:
    st.markdown("<span style='color:red;'>Debes seleccionar el tipo de práctica</span>", unsafe_allow_html=True)
# Ciclo formativo (único)
st.subheader("Ciclo Formativo")
ciclo = st.radio("Selecciona tu ciclo formativo", CICLOS, index=None)

# Preferencias según ciclo (única) dentro de un expander con el título del ciclo
preferencia = None
if ciclo:
    opciones = PREFS_MAP.get(ciclo, [])
    with st.expander(ciclo, expanded=True):
        preferencias_seleccionadas = st.multiselect(
            "Indica qué áreas son de tu interés (indicar al menos 3)",
            options=opciones,
            max_selections=3,
            placeholder="Selecciona tus preferencias",
            key=f"prefs_{slug(ciclo)}"
        )
        if not preferencias_seleccionadas:
            st.markdown("<span style='color:red;'>Debes seleccionar al menos una preferencia</span>", unsafe_allow_html=True)
if not ciclo:
    st.markdown("<span style='color:red;'>Debes seleccionar al menos un ciclo formativo</span>", unsafe_allow_html=True)
# Subida de CV
st.subheader("Subir CV")
st.caption("El nombre del archivo debe seguir el formato: Nombre_Apellidos_CV (ejemplo: Juan_Perez_12345678A.pdf)")
cv_file = st.file_uploader("Selecciona tu CV (PDF/DOC/DOCX)", type=["pdf", "doc", "docx"], accept_multiple_files=False)
cv_too_big = False
if cv_file is not None:
    size_bytes = file_size_bytes(cv_file)
    if size_bytes > max_file_size:
        st.error("El archivo supera el máximo permitido (20 MB).")
        cv_too_big = True



# ---------------------------------
# Validación requerida
# ---------------------------------
missing = []

if not required_ok(nombre): missing.append("Nombre")
if not required_ok(apellidos): missing.append("Apellidos")
if not required_ok(email): missing.append("Email")
if not required_ok(dni): missing.append("DNI/NIE")
if not required_ok(direccion): missing.append("Dirección")
if not required_ok(cp): missing.append("CP")
if not required_ok(localidad): missing.append("Localidad")

if vehiculo not in ("Sí", "No"): missing.append("Dispones de vehículo")
if not ciclo: missing.append("Ciclo formativo")
if cv_file is None: missing.append("CV")
if cv_too_big: missing.append("CV ≤ 20 MB")

if missing:
    st.info("Completa los campos obligatorios: " + ", ".join(missing))

can_submit = (len(missing) == 0) and (not cv_too_big)
submit = st.button("Enviar", disabled=not can_submit)

# ---------------------------------
# Submit
# ---------------------------------
if submit:
    with st.spinner("⏳ Enviando formulario, por favor espera..."):
        payload = {
                "nombre": nombre.strip(),
                "apellido": apellidos.strip(),
                "email_alumno": email.strip().lower(),
                "sexo": sexo,
                "dni": dni.strip().upper(),
                "direccion": direccion.strip(),
                "codigo_postal": cp.strip(),
                "localidad": localidad.strip(),
                "vehiculo": vehiculo,
                "ciclo_formativo": ciclo,
                "preferencias_fp": preferencias_seleccionadas,
                "estado":estadosAlumno[0],
                "tipoPractica": tipo_practica,
                "nuss": nuss.strip(),
                "anio": ano.strip(),
                "curso": curso.strip()
        }
        res_al = upsert(alumnosTabla, payload, keys=["dni"])
        upsert(
            alumnoEstadosTabla,
            {"alumno": res_al.data[0]["dni"], "form_completo": datetime.now().isoformat()},
            keys=["alumno"],
            )
        # Subir CV a Drive como {dni}_cv.ext
        try:
            if cv_file:

                tmp_path = Path("/tmp") / f"{uuid.uuid4()}_{cv_file.name}"
                with open(tmp_path, "wb") as f:
                    f.write(cv_file.getbuffer())
                
                # upload_to_drive(path, folder_id, dni) -> ajusta si tu helper usa otro tercer parámetro
                folderName= payload["nombre"]+"_"+payload["apellido"]+"_"+payload["dni"]
                res = upload_to_drive(str(tmp_path), carpetaAlumnos, folderName,cv_file.name )
                if isinstance(res, dict):
                    file_id = res.get("id")
                    link = res.get("webViewLink") or res.get("webContentLink")
                else:
                    file_id, link = str(res), None

                st.success("¡Formulario enviado correctamente!, ya puedes cerrar la página.")
                if link:
                    st.success(f"CV subido. [Abrir en Drive]({link})")
                else:
                    st.success(f"CV subido correctamente")

        except Exception as e:
            st.error(f"No se pudo subir el CV a Drive: {e}")
