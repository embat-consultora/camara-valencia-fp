import streamlit as st
import pandas as pd
import re
from modules.data_base import getEquals, getPracticas,getFormsLinks
from page_utils import apply_page_config
from navigation import make_sidebar
from variables import alumnosTabla, practicaTabla,estados,max_file_size,carpetaPractica
from pathlib import Path
from modules.drive_helper import list_drive_files, upload_to_drive
from modules.forms_helper import file_size_bytes
import uuid

apply_page_config()
make_sidebar()
st.set_page_config(page_title="🧠 Mi Formación en Empresa", page_icon="🧑‍🎓")
st.markdown(
    "<h2 style='text-align: center;'>🏢 MI FORMACIÓN EN EMPRESA</h2>",
    unsafe_allow_html=True
)

dniAlumno = st.session_state.get("username", "alumno")

if "page" not in st.session_state:
    st.session_state.page = "lista"
if "practicas" not in st.session_state:
    st.session_state["practicas"] = []

# --- Traer datos del alumno ---
alumno_data = getEquals(alumnosTabla, {"dni": dniAlumno})

def fetch_practicas_alumno():
    todas_las_practicas = getPracticas(practicaTabla, {"alumno": dniAlumno})
    practica_res = [
    p for p in todas_las_practicas 
    if p.get("status") not in [estados[3], estados[2]]  # Excluir prácticas con estado "Canceladas" o "Finalizada"
]
    st.session_state["practicas"] = practica_res
    return practica_res

if not alumno_data:
    st.warning("⚠️ No encontramos formaciones en empresa asignadas aún.")
    st.stop()

# Buscar la práctica asignada
fetch_practicas_alumno()

if not st.session_state["practicas"] or len(st.session_state["practicas"]) == 0:
    st.info("ℹ️ Actualmente no tienes ninguna formación asignada.")
    st.stop()

# Como el usuario solo tiene 1 práctica, extraemos el primer elemento de la lista [{...}]
practica = st.session_state["practicas"][0]

# Estructurar los diccionarios anidados de forma segura
oferta = practica.get("oferta_fp") or {}
empresa = practica.get("empresas") or {}
alumno_detalles = practica.get("alumnos") or {}
practicaId = practica.get("id")
# Título informativo principal
nombre_completo = f"{alumno_detalles.get('nombre', '')} {alumno_detalles.get('apellido', '')}".strip()
st.title(f"📋 {nombre_completo} – {empresa.get('nombre', 'Empresa')}")

# --- Sección Visual Informativa (Solo Lectura) ---
col1, col2 = st.columns(2)

with col1:
    st.markdown("### 👤 Datos del Alumno")
    st.write(f"**Alumno:** {nombre_completo}")
    st.write(f"**DNI:** {alumno_detalles.get('dni', '—')}")
    st.write(f"**Email:** {alumno_detalles.get('email_alumno', '—')}")
    st.write(f"**Ciclo Formativo:** {practica.get('ciclo_formativo', '—')}")
    st.write(f"**Curso Académico:** {practica.get('anio') or 'No especificado'}")     
    st.write(f"**Curso:** {practica.get('curso') or 'No especificado'}")     
    st.write(f"**Área:** {practica.get('area') or 'No especificado'}")     
    st.write(f"**Proyecto:** {practica.get('proyecto') or 'No especificado'}")      
with col2:
    st.markdown("### 🏢 Datos de la Empresa")
    st.write(f"**Empresa:** {empresa.get('nombre', '—')}")
    st.write(f"**CIF:** {empresa.get('CIF', '—')}")
    
    direccion = oferta.get("direccion_empresa") or empresa.get('direccion', '—')
    st.write(f"**Dirección formación:** {direccion}") 
    
    localidad = oferta.get("localidad_empresa") or empresa.get('localidad', '—')
    st.write(f"**Localidad:** {localidad}")

    # Convertido de Selectbox a Texto Simple para cumplir el requerimiento Read-Only
    tutor_actual = practica.get("tutor") or "No asignado"
    st.write(f"**Tutor en Empresa:** {tutor_actual}")

    tutorc_actual = practica.get("tutor_centro") or "No asignado"
    st.write(f"**Tutor Centro:** {tutorc_actual}")

st.divider( )

st.write(f"**Estado de Formación:** `{practica.get('status', '—')}`")
st.write(f"**Fecha Inicio:** `{practica.get('fecha_inicio', '—')}`")
st.write(f"**Fecha Fin:** `{practica.get('fecha_fin', '—')}`")
st.divider( )

if (practica.get('status') is not None and practica.get('status') == estados[1]):
    links = getFormsLinks(practicaId)
    links_map = {item['tipo']: item['url'] for item in links}
    fechas_map = {item['tipo']: item['fecha_envio'] for item in links}
    with st.container(border=True):
        link_ini = links_map.get('feedback_inicial', '#')
        link_ada = links_map.get('feedback_adaptacion', '#')
        link_cie = links_map.get('feedback_cierre', '#')
        st.markdown(f"""
        **Próximos Hito:**
        * 📅 **Envio Feedback Acogida:** : {fechas_map.get('feedback_inicial')} | [🔗 Abrir Formulario]({link_ini})
        * 🕒 **Envio Feedback Adaptación:**  {fechas_map.get('feedback_adaptacion')} | [🔗 Abrir Formulario]({link_ada})
        * ⏲️ **Envio Feedback Cierre:** {fechas_map.get('feedback_cierre')}  | [🔗 Abrir Formulario]({link_cie})
        """)
# --- Sección del Calendario (Solo Lectura) ---
st.subheader("📅 Planificación y Calendario de Formación")

# Buscar archivos en Drive dinámicamente
folder_name = f"{alumno_detalles.get('apellido', '')}_{alumno_detalles.get('nombre', '')}_{alumno_detalles.get('dni', '')}_practica_{empresa.get('nombre', '')}".strip()

archivo_calendario = None
try:
    files = list_drive_files(folder_name)
    if files and len(files) > 0:
        archivo_calendario = next((f for f in files[0] if "calendario" in f.get('name', '').lower()), None)
except Exception:
    pass # Manejo pasivo por si la carpeta no existe en Drive aún

if archivo_calendario:
    st.info("🔍 **Vista Previa de tu Calendario de Prácticas:**")
    file_id = archivo_calendario.get('id')
    
    if file_id:
        preview_url = f"https://drive.google.com/file/d/{file_id}/preview"
        
        # Contenedor visual del documento embebido
        st.markdown(
            f"""
            <div style="border: 1px solid #ddd; border-radius: 10px; overflow: hidden; margin-bottom: 15px;">
                <iframe src="{preview_url}" width="100%" height="550px" frameborder="0"></iframe>
            </div>
            """,
            unsafe_allow_html=True
        )
        
        if archivo_calendario.get('webViewLink'):
            st.link_button("🔗 Abrir archivo completo en Google Drive", archivo_calendario.get('webViewLink'), use_container_width=True)
else:
    st.markdown(
        """
        <div style="border: 2px dashed #ccc; border-radius: 10px; height: 200px; display: flex; flex-direction: column; align-items: center; justify-content: center; color: #7f8c8d; background-color: #f9f9f9;">
            <span style="font-size: 24px;">📅</span>
            <p style="margin-top: 10px; font-weight: bold;">El centro aún no ha subido tu calendario.</p>
        </div>
        """,
        unsafe_allow_html=True
    )


st.subheader("📎 Adjuntar documentos")

folder_name = f"{alumno_detalles['apellido']}_{alumno_detalles['nombre']}_{alumno_detalles['dni']}_practica_{empresa['nombre']}".strip()
files, folderId = list_drive_files(folder_name)

if files:
    for f in files:
        fecha = f.get("modifiedTime", "")[:10]
        st.write(f"- [{f['name']}]({f['webViewLink']}) _(última modificación: {fecha})_")
else:
    st.warning("No hay archivos.")

uploaded_files = st.file_uploader(
    "Subir archivos",
    type=["pdf", "doc", "docx", "odt"],
    accept_multiple_files=True,
    key=f"up_{practicaId}"
)
st.html(
    """
    <style>
    [data-testid='stFileUploader'] [data-testid='stFileUploaderDropzoneInstructions'] > div > span {
    display: none;
    }
    [data-testid='stFileUploader'] [data-testid='stFileUploaderDropzoneInstructions'] > div::before {
    content: 'Arrastre aquí los archivos';
    }
    [data-testid='stFileUploader'] [data-testid='stBaseButton-secondary'] {
    text-indent: -9999px;
    line-height: 0;
    }
    [data-testid='stFileUploader'] [data-testid='stBaseButton-secondary']::after {
    line-height: initial;
    content: "Buscar";
    text-indent: 0;
    }
    [data-testid='stFileUploader'] [data-testid='stFileDropzoneInstructions'] {
    text-indent: -9999px;
    line-height: 0;
    }
    [data-testid='stFileUploader'] [data-testid='stFileDropzoneInstructions']::after {
    line-height: initial;
    content: "Límite 1MB por archivo";
    text-indent: 0;
    }
    </style>
    """
)
if uploaded_files:
    too_big = [f.name for f in uploaded_files if file_size_bytes(f) > max_file_size]
    if too_big:
        st.error("Archivos demasiado grandes: " + ", ".join(too_big))
    else:
        if st.button("Subir Archivos", key=f"subir_{practicaId}"):
            with st.spinner("Subiendo archivos..."):
                for file in uploaded_files:
                    extension = Path(file.name).suffix
                    nombre_alumno_limpio = f"{alumno_detalles['nombre']}_{alumno_detalles['apellido']}".replace(" ", "_")
                    nuevo_nombre = f"{nombre_alumno_limpio}_{file.name}"
                    temp = Path("/tmp") / f"{uuid.uuid4()}_{nuevo_nombre}"
                    with open(temp, "wb") as f:
                        f.write(file.getbuffer())
                    upload_to_drive(str(temp), carpetaPractica, folder_name, nuevo_nombre)
                    st.success(f"Subido: {nuevo_nombre}")