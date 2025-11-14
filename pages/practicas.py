import streamlit as st
import pandas as pd
from modules.data_base import getEquals, getPracticas,getEqual,update,upsert
from page_utils import apply_page_config
from navigation import make_sidebar
from modules.grafico_helper import mostrar_fases
from datetime import datetime
from modules.drive_helper import list_drive_files,upload_to_drive
from modules.forms_helper import  file_size_bytes
from pathlib import Path
import uuid
from variables import (
    practicaTabla,
    tutoresTabla,
    practicaEstadosTabla,
    fasesPractica,
    faseColPractica,
    max_file_size,
    carpetaPractica,
    necesidadFP
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

# Estados posibles (si querés después lo traemos de base)
estados_posibles = ["Pendiente", "En curso", "Finalizada", "Cancelada"]

# Helper para filtrar tutores por empresa
def tutores_por_empresa(empresa_id, lista_tutores):
    return [t for t in lista_tutores if t.get("cif_empresa") == empresa_id]

# --- Render de prácticas ---
for p in practicas:

    oferta = p.get("oferta_fp")
    empresa = p.get("empresas")
    alumno = p.get("alumnos")
    practicaId = p.get("id")
    # Tutor actual
    if oferta.get("tutor"):
        tutor_actual = getEquals(tutoresTabla, {"id": oferta["tutor"]})
        tutor_actual = tutor_actual[0] if tutor_actual else None
    else:
        tutor_actual = None

    # Tutores disponibles para esta empresa
    tutor_empresa = tutores_por_empresa(empresa["CIF"], tutores)
    # --------------------------
    # EXPANDER
    # --------------------------
    with st.expander(f"📋 {alumno['nombre']} {alumno['apellido']} — {empresa['nombre']}"):

        # --- Datos en columnas ---
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


        # ---------------------------------------------------------------------
        # SELECTOR DE TUTOR
        # ---------------------------------------------------------------------
        st.write("👨‍🏫 Tutor asignado")
        colTutor1, colTutor2 = st.columns([1, 1])
        with colTutor1:
             st.write(f"**Tutor actual:** {tutor_actual['nombre'] if tutor_actual else '— Sin tutor asignado —'}")
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
                key=f"tutor_select_{p['id']}"
            )
            tutor_elegido = next((t for t in tutor_empresa if t["nombre"] == nuevo_tutor), None)
            tutor_id_nuevo = tutor_elegido["id"] if tutor_elegido else None
            if tutor_id_nuevo != (tutor_actual["id"] if tutor_actual else None):
                update(
                        necesidadFP,
                        {"tutor": tutor_id_nuevo}, "id", oferta["id"]
                        )
                st.success(f"Tutor actualizado: {nuevo_tutor}")
        # ---------------------------------------------------------------------
        # SELECTOR DE ESTADO
        # ---------------------------------------------------------------------
        st.divider()
        estadosPracticas = getEqual(practicaEstadosTabla, "practicaId", practicaId)
        st.subheader(f"Seguimiento - {empresa['nombre']}")

        if not estadosPracticas:
            mostrar_fases(fasesPractica, faseColPractica, None)
            estado_actual = {}
        else:
            mostrar_fases(fasesPractica, faseColPractica, estadosPracticas[0])
            estado_actual = estadosPracticas[0]

        # --- Checkboxes dinámicos para cada fase ---
        cols = st.columns(len(fasesPractica))

        for i, fase in enumerate(fasesPractica):
            col = faseColPractica[fase]
            valor_actual = True if estado_actual.get(col) else False

            with cols[i]:
                checked = st.checkbox(fase, value=valor_actual, key=f"{empresa['CIF']}_{col}")

            if checked != valor_actual:  # solo si cambió
                if checked:
                    new_value = datetime.now().isoformat()
                else:
                    new_value = None
            
                upsert(
                        practicaEstadosTabla,
                        {"practicaId": practicaId, col: new_value},
                        keys=["practicaId"]
                    )
                st.success(f"Estado actualizado: {fase} → {new_value if new_value else '❌'}")
                st.rerun()
        # ---------------------------------------------------------------------
        # FILE UPLOADER — Cargar documentación
        # ---------------------------------------------------------------------
        st.divider()
        st.subheader("📎 Adjuntar documentos")

        folder_name = f"{alumno['apellido']}_{alumno['nombre']}_{alumno['dni']}_practica_{empresa["nombre"]}".strip()
        files, folderId = list_drive_files(folder_name)

        if not files:
            st.warning("No hay archivos en la carpeta de la práctica.")
        else:
            if folderId:
                folder_link = f"https://drive.google.com/drive/folders/{folderId}"
                st.link_button("🔗 Abrir carpeta en Drive", folder_link)
            st.write("Archivos encontrados:")
            for f in files:
                        fecha = f.get("modifiedTime", "")[:10]
                        col1, col2, col3 = st.columns([5, 1, 1])
                        with col1:
                            st.write(f"- [{f['name']}]({f['webViewLink']}) _(última modificación: {fecha})_")

        st.write("📤 Subir archivos adicionales para la práctica:")

        uploaded_files = st.file_uploader(
            "Selecciona uno o varios archivos (PDF/DOC/DOCX/ODT)",
            type=["pdf", "doc", "docx", "odt"],
            accept_multiple_files=True,
            key=f"file_uploader_{practicaId}"
        )

        if uploaded_files:
            too_big_files = [f.name for f in uploaded_files if file_size_bytes(f) > max_file_size]

            if too_big_files:
                st.error(f"Los siguientes archivos superan los 20 MB: {', '.join(too_big_files)}")
            else:
                if st.button("Subir Archivos"):
                    try:
                        total = len(uploaded_files)
                        st.info(f"Subiendo {total} archivo(s), por favor espera...")

                        for i, file in enumerate(uploaded_files, start=1):
                            original_name = file.name
                            tmp_path = Path("/tmp") / f"{uuid.uuid4()}_{original_name}"
                            with open(tmp_path, "wb") as f:
                                f.write(file.getbuffer())

                            res = upload_to_drive(str(tmp_path), carpetaPractica, folder_name, original_name)

                            if isinstance(res, dict):
                                link = res.get("webViewLink") or res.get("webContentLink")
                            else:
                                link = None

                            st.success(f"✅ {i}/{total}: {original_name} subido correctamente")
                            if link:
                                st.markdown(f"[Abrir en Drive]({link})")

                        st.success("🎉 Todos los archivos se subieron correctamente.")
                        st.rerun()

                    except Exception as e:
                        st.error(f"❌ Error al subir los archivos: {e}")

