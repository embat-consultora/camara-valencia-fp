import streamlit as st
import pandas as pd
from modules.data_base import (
    getEquals, getPracticas,
    update, upsert,asignarFechasFormsFeedback
)
from page_utils import apply_page_config
from navigation import make_sidebar
from modules.grafico_helper import mostrar_fases
from datetime import datetime
from modules.drive_helper import list_drive_files, upload_to_drive
from modules.forms_helper import file_size_bytes
from pathlib import Path
from modules.feedback_helper import render_feedback_card
import uuid
from variables import (
    practicaTabla, tutoresTabla, practicaEstadosTabla,
    fasesPractica, faseColPractica, max_file_size, carpetaPractica,
    necesidadFP,linkCalendar,feedbackResponseTabla,forms
)
import plotly.graph_objects as go

# ----------------------------------------------
# CONFIG
# ----------------------------------------------
apply_page_config()
make_sidebar()
st.set_page_config(page_title="Prácticas", page_icon="🚀")

now = datetime.now().isoformat()

# ----------------------------------------------
# INICIALIZAR SESSION_STATE (evita KeyError)
# ----------------------------------------------
if "practicas" not in st.session_state:
    st.session_state["practicas"] = []

if "tutores" not in st.session_state:
    st.session_state["tutores"] = []

if "estados" not in st.session_state:
    st.session_state["estados"] = []
# ----------------------------------------------
# FETCH FUNCTIONS
# ----------------------------------------------
def fetch_practicas_tutores():
    practicas = getPracticas(practicaTabla, {})
    tutores = getEquals(tutoresTabla, {})
    return practicas, tutores

# ----------------------------------------------
# BOTÓN REFRESCAR
# ----------------------------------------------
col_refresh = st.columns([1, 0.15])
with col_refresh[1]:
    if st.button("🔄 Actualizar", key="btn_refresh"):
        st.session_state["force_reload"] = True
        st.rerun()

# ----------------------------------------------
# CARGA DE DATOS
# ----------------------------------------------
def load_data(force=False):
    if force or "data_loaded" not in st.session_state or st.session_state.get("force_reload"):

        practicas, tutores = fetch_practicas_tutores()

        estados = getEquals(practicaEstadosTabla, {})
        estados_map = {e["practicaId"]: e for e in estados}
        st.session_state["practicas"] = practicas
        st.session_state["tutores"] = tutores
        st.session_state["estados"] = estados_map

        st.session_state["data_loaded"] = True
        st.session_state["force_reload"] = False

load_data()

practicas = st.session_state["practicas"]
tutores = st.session_state["tutores"]

# ----------------------------------------------
# HELPER
# ----------------------------------------------
def tutores_por_empresa(empresa_id, lista_tutores):
    return [t for t in lista_tutores if t.get("cif_empresa") == empresa_id]

# ----------------------------------------------
# RUTEO
# ----------------------------------------------
if "page" not in st.session_state:
    st.session_state.page = "lista"

if "practica_seleccionada" not in st.session_state:
    st.session_state.practica_seleccionada = None

# ----------------------------------------------
# PAGINA: LISTA
# ----------------------------------------------
def mostrar_lista():
    st.title("🚀 Prácticas")

    filtro_estado = st.selectbox("Filtrar por estado", ["Todos"] + fasesPractica, index=0)
    estado_por_practica = {}

    for p in practicas:
        pid = p["id"]
        estadosPractica = st.session_state["estados"].get(pid, {})
        if not estadosPractica:
            estado_por_practica[pid] = "Pendiente"
        else:
            registro = estadosPractica
            estado_actual = "Pendiente"
            for fase in fasesPractica:
                col = faseColPractica[fase]
                if registro.get(col):
                    estado_actual = fase
            estado_por_practica[pid] = estado_actual

    practicas_filtradas = practicas if filtro_estado == "Todos" else [
        p for p in practicas if estado_por_practica[p["id"]] == filtro_estado
    ]

    st.write("Selecciona una práctica para ver el detalle:")

    for p in practicas_filtradas:
        empresa = p.get("empresas") or {}
        alumno = p.get("alumnos") or {}

        label = f"{alumno.get('nombre')} {alumno.get('apellido')} — {empresa.get('nombre')}"

        if st.button(label, key=f"btn_{p['id']}"):
            st.session_state.practica_seleccionada = p["id"]
            st.session_state.page = "detalle"
            st.rerun()

# ----------------------------------------------
# PAGINA: DETALLE
# ----------------------------------------------
def mostrar_detalle():
    practicaId = st.session_state.practica_seleccionada
    p = next((x for x in practicas if x["id"] == practicaId), None)

    if not p:
        st.error("Práctica no encontrada.")
        return

    p["oferta_fp"] = p.get("oferta_fp") or {}
    p["empresas"] = p.get("empresas") or {}
    p["alumnos"] = p.get("alumnos") or {}
    oferta = p["oferta_fp"]
    empresa = p["empresas"]
    alumno = p["alumnos"]
    st.title(f"{alumno['nombre']} {alumno['apellido']} – {empresa['nombre']}")

    # ------------------------------------------
    # DATOS (idéntico)
    # ------------------------------------------
    col1, col2 = st.columns(2)
    with col1:
        st.write(f"**Alumno:** {alumno['nombre']} {alumno['apellido']}")
        st.write(f"**DNI:** {alumno['dni']}")
        st.write(f"**Email:** {alumno['email_alumno']}")
        st.write(f"**Ciclo:** {p.get('ciclo_formativo', '—')}")
        area = oferta.get("area") or "No especificado"
        st.write(f"**Área:** {area}")     
        proyecto = oferta.get("proyecto") or "No especificado"
        st.write(f"**Proyecto:** {proyecto}")      

    with col2:
        st.write(f"**Empresa:** {empresa['nombre']}")
        st.write(f"**CIF:** {empresa['CIF']}")
        direccion = oferta.get("direccion_empresa") or "No especificado"
        st.write(f"**Dirección práctica:** {direccion}")
        localidad = oferta.get("localidad_empresa") or "No especificado"
        st.write(f"**Localidad:** {localidad}")

    # ------------------------------------------
    # TUTOR (idéntico)
    # ------------------------------------------
    tutor_actual = None

    if oferta.get("tutor"):
        tutor_actual = next((t for t in tutores if t["id"] == oferta.get("tutor")), None)

    tutor_empresa = tutores_por_empresa(empresa["CIF"], tutores)

    st.write(f"**Tutor actual:** {tutor_actual['nombre'] if tutor_actual else '— Sin tutor —'}")

    opciones_nombres = ["— Sin tutor —"] + [t["nombre"] for t in tutor_empresa]
    
    # 4. Determinar el índice inicial
    # Si hay un tutor actual y está en la lista de la empresa, buscamos su posición (+1 por el "Sin tutor")
    if tutor_actual and tutor_actual["nombre"] in [t["nombre"] for t in tutor_empresa]:
        index_actual = [t["nombre"] for t in tutor_empresa].index(tutor_actual["nombre"]) + 1
    else:
        index_actual = 0 # Posición de "— Sin tutor —"
    col1, col2 = st.columns([2, 4])
    with col1:
        nuevo_tutor_nombre = st.selectbox(
            "Asignar o cambiar tutor",
            options=opciones_nombres,
            index=index_actual,
            key=f"tutor_select_{practicaId}"
        )

    tutor_elegido = next((t for t in tutor_empresa if t["nombre"] == nuevo_tutor_nombre), None)
    id_a_guardar = tutor_elegido["id"] if tutor_elegido else None
    id_en_db = oferta.get("tutor")

    # Solo actualizamos si el ID cambió
    if id_a_guardar != id_en_db:
        st.write('etro')
        with st.spinner("Actualizando tutor..."):
            try:
                oferta_id = oferta.get("id")
                if oferta_id:
                    update(necesidadFP, {"tutor": id_a_guardar}, {"id": oferta_id})
                    st.success(f"Tutor actualizado a: {nuevo_tutor_nombre}")
                    # Forzamos recarga para que el estado de la oferta se actualice en la sesión
                    st.session_state["force_reload"] = True
                    #st.rerun()
            except Exception as e:
                st.error(f"Error al actualizar tutor: {e}")

    # ------------------------------------------
    # ESTADOS (idéntico, sin value=)
    # ------------------------------------------
    st.divider()
    st.subheader("Seguimiento")

    estado_actual = st.session_state["estados"].get(practicaId, {})
    mostrar_fases(fasesPractica, faseColPractica, estado_actual)

    cols = st.columns(len(fasesPractica))
    for i, fase in enumerate(fasesPractica):
        col = faseColPractica[fase]
        valor = bool(estado_actual.get(col))
        key_checkbox = f"{empresa['CIF']}_{alumno['dni']}_{col}"

        if key_checkbox not in st.session_state:
            st.session_state[key_checkbox] = valor

        with cols[i]:
            if fase == fasesPractica[2]:
                checked = st.checkbox(fase, key=key_checkbox, help="Al marcar esta casilla, se comenzarán a enviar los formularios de feedack segun las fechas especificadas.")
            else:
                checked = st.checkbox(fase, key=key_checkbox)

        if checked != valor:
            new_value = datetime.now().isoformat() if checked else None
            upsert(practicaEstadosTabla, {"practicaId": practicaId, col: new_value}, keys=["practicaId"])
            estado_actual[col] = new_value

            if fase == fasesPractica[2] and checked:
                st.success("📌 La práctica ha pasado a estado EN CURSO")
                asignarFechasFormsFeedback(practicaId, datetime.now().date(), alumno['email_alumno'])

            st.session_state["estados"][practicaId] = estado_actual
            st.success(f"Estado actualizado: {fase}")
    # ------------------------------------------
    # CALENDARIO 
    # ------------------------------------------
# ------------------------------------------
    # CALENDARIO (VISTA IMAGEN PNG)
    # ------------------------------------------
    st.divider()
    st.subheader("📅 Planificación de Prácticas")

    # 1. Preparar datos de Drive
    folder_name = f"{alumno['apellido']}_{alumno['nombre']}_{alumno['dni']}_practica_{empresa['nombre']}".strip()
    files, folderId = list_drive_files(folder_name)
    
    # Buscamos el archivo (ahora aceptando png, jpg, etc.)
    archivo_calendario = next((f for f in files if "calendario" in f['name']), None)

    col_cal1, col_cal2 = st.columns([1, 1.5]) # Ajustamos el ancho para la imagen
    
    with col_cal1:
        url_generador = linkCalendar
        st.link_button("🛠️ Generar Nuevo Calendario", url_generador, use_container_width=True)
        
        st.info("Sube el calendario en formato imagen (PNG/JPG).")
        uploaded_cal = st.file_uploader(
            "Subir imagen del Calendario",
            type=["png", "jpg", "jpeg"],
            key=f"cal_up_{practicaId}"
        )
        if uploaded_cal:
            if st.button("Guardar en Drive", key=f"btn_save_cal_{practicaId}"):
                with st.spinner("Subiendo imagen..."):
                    temp_path = Path("/tmp") / f"CAL_{uuid.uuid4()}_{uploaded_cal.name}"
                    with open(temp_path, "wb") as f:
                        f.write(uploaded_cal.getbuffer())
                    upload_to_drive(str(temp_path), carpetaPractica, folder_name, uploaded_cal.name)
                    st.success("Imagen guardada.")
                    st.rerun()

    with col_cal2:
        if archivo_calendario:
            st.write("🔍 **Vista Previa del Calendario:**")
            
            # Obtenemos el ID del archivo
            file_id = archivo_calendario.get('id')
            
            if file_id:
                # Construimos la URL de previsualización oficial de Google Drive
                preview_url = f"https://drive.google.com/file/d/{file_id}/preview"
                
                # Usamos un contenedor de Streamlit para el estilo
                with st.container():
                    st.markdown(
                        f"""
                        <div style="border: 1px solid #ddd; border-radius: 10px; overflow: hidden;">
                            <iframe src="{preview_url}" width="100%" height="500px" frameborder="0"></iframe>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
            
            st.link_button("Abrir imagen completa en Drive", archivo_calendario.get('webViewLink'), use_container_width=True)
        else:
            # Placeholder si no hay imagen
            st.markdown(
                """
                <div style="border: 2px dashed #ccc; border-radius: 10px; height: 500px; display: flex; align-items: center; justify-content: center; color: #aaa;">
                    Esperando archivo de calendario (PNG/JPG)...
                </div>
                """,
                unsafe_allow_html=True
            )
    
    # ------------------------------------------
    # FEEDBACK 
    # ------------------------------------------
    st.divider()
    st.subheader("¿Cómo se siente el candidato?")

    feedbacks_db = getEquals(feedbackResponseTabla, {"practica_id": practicaId})
    progreso_feedback = {
        forms[0]: None,
        forms[1]: None,
        forms[2]: None,
        forms[3]: None
    }

    for f in feedbacks_db:
        tipo = f["respuestas_json"].get("tipo")
        if tipo in progreso_feedback:
            progreso_feedback[tipo] = f["respuestas_json"]

    # 3. Crear las columnas y mostrar las cards
    col_ini, col_ada, col_seg, col_cie = st.columns(4)

    with col_ini:
        render_feedback_card(progreso_feedback[forms[0]], "Inicial")

    with col_ada:
        render_feedback_card(progreso_feedback[forms[1]], "Adaptación")

    with col_seg:
        render_feedback_card(progreso_feedback[forms[2]], "Seguimiento")

    with col_cie:
        render_feedback_card(progreso_feedback[forms[3]], "Cierre")
    # ------------------------------------------
    # FILE UPLOADER (idéntico)
    # ------------------------------------------
    st.divider()
    st.subheader("📎 Adjuntar documentos")

    folder_name = f"{alumno['apellido']}_{alumno['nombre']}_{alumno['dni']}_practica_{empresa['nombre']}".strip()
    files, folderId = list_drive_files(folder_name)

    if folderId:
        st.link_button("Abrir carpeta en Drive", f"https://drive.google.com/drive/folders/{folderId}")

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

    if uploaded_files:
        too_big = [f.name for f in uploaded_files if file_size_bytes(f) > max_file_size]
        if too_big:
            st.error("Archivos demasiado grandes: " + ", ".join(too_big))
        else:
            if st.button("Subir Archivos", key=f"subir_{practicaId}"):
                with st.spinner("Subiendo archivos..."):
                    for file in uploaded_files:
                        temp = Path("/tmp") / f"{uuid.uuid4()}_{file.name}"
                        with open(temp, "wb") as f:
                            f.write(file.getbuffer())
                        upload_to_drive(str(temp), carpetaPractica, folder_name, file.name)
                        st.success(f"Subido: {file.name}")



    # with feedbacktab:


    # ------------------------------------------
    # VOLVER SIN EXPERIMENTAL
    # ------------------------------------------
    if st.button("⬅️ Volver"):
        st.session_state.page = "lista"
        st.rerun()

# ----------------------------------------------
# RENDER SEGÚN PÁGINA
# ----------------------------------------------
if st.session_state.page == "lista":
    mostrar_lista()
else:
    mostrar_detalle()
