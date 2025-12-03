import streamlit as st
import pandas as pd
from modules.data_base import (
    getEquals, getPracticas,
    update, upsert
)
from page_utils import apply_page_config
from navigation import make_sidebar
from modules.grafico_helper import mostrar_fases
from datetime import datetime
from modules.drive_helper import list_drive_files, upload_to_drive
from modules.forms_helper import file_size_bytes
from pathlib import Path
import uuid
from variables import (
    practicaTabla, tutoresTabla, practicaEstadosTabla,
    fasesPractica, faseColPractica, max_file_size, carpetaPractica,
    necesidadFP
)

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
        st.stop()

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
            st.stop()

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
        st.write(f"**Ciclo:** {p.get('ciclo_formativo', '—')}")
        st.write(f"**Área:** {p.get('area', '—')}")
        st.write(f"**Proyecto:** {p.get('proyecto', '—')}")

    with col2:
        st.write(f"**Empresa:** {empresa['nombre']}")
        st.write(f"**CIF:** {empresa['CIF']}")
        st.write(f"**Dirección práctica:** {oferta.get('direccion_empresa','')}")
        st.write(f"**Localidad:** {oferta.get('localidad_empresa','')}")

    # ------------------------------------------
    # TUTOR (idéntico)
    # ------------------------------------------
    st.write("👨‍🏫 Tutor asignado")

    tutor_actual = None
    if oferta.get("tutor"):
        tutor_actual = next((t for t in tutores if t["id"] == oferta.get("tutor")), None)

    tutor_empresa = tutores_por_empresa(empresa["CIF"], tutores)

    colTutor1, colTutor2 = st.columns([1, 1])
    with colTutor1:
        st.write(f"**Tutor actual:** {tutor_actual['nombre'] if tutor_actual else '— Sin tutor —'}")

    with colTutor2:
        nombres_tutores = [t["nombre"] for t in tutor_empresa] if tutor_empresa else ["— Sin tutores —"]
        tutor_inicial = (
            nombres_tutores.index(tutor_actual["nombre"])
            if tutor_actual and tutor_actual["nombre"] in nombres_tutores
            else 0
        )

        nuevo_tutor = st.selectbox(
            "Cambiar tutor",
            options=nombres_tutores,
            index=tutor_inicial,
            key=f"tutor_select_{practicaId}"
        )

        tutor_elegido = next((t for t in tutor_empresa if t["nombre"] == nuevo_tutor), None)
        tutor_id_nuevo = tutor_elegido["id"] if tutor_elegido else None
        oferta_id = oferta.get("id")

        if oferta_id and tutor_id_nuevo != (tutor_actual["id"] if tutor_actual else None):
            update(necesidadFP, {"tutor": tutor_id_nuevo}, "id", oferta_id)
            st.success(f"Tutor actualizado: {nuevo_tutor}")

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
            checked = st.checkbox(fase, key=key_checkbox)

        if checked != valor:
            new_value = datetime.now().isoformat() if checked else None
            upsert(practicaEstadosTabla, {"practicaId": practicaId, col: new_value}, keys=["practicaId"])
            estado_actual[col] = new_value
            st.session_state["estados"][practicaId] = estado_actual
            st.success(f"Estado actualizado: {fase}")

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




    # ------------------------------------------
    # VOLVER SIN EXPERIMENTAL
    # ------------------------------------------
    if st.button("⬅️ Volver"):
        st.session_state.page = "lista"
        st.stop()

# ----------------------------------------------
# RENDER SEGÚN PÁGINA
# ----------------------------------------------
if st.session_state.page == "lista":
    mostrar_lista()
else:
    mostrar_detalle()
