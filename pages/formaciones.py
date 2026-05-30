import streamlit as st
import pandas as pd
from modules.data_base import getPracticas
from page_utils import apply_page_config
from navigation import make_sidebar
from variables import practicaTabla, locale_tabla_principal,estados,aniosList, cursoList
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode, DataReturnMode
from modules.drive_helper import list_drive_files
import os

apply_page_config()
make_sidebar()

st.set_page_config(page_title="Histórico Formaciones en Empresas", page_icon="🏢")
st.markdown(
    "<h2 style='text-align: center;'>Histórico de Formaciones en Empresas</h2>",
    unsafe_allow_html=True
)

user_role = st.session_state.get("rol") 
username = st.session_state.get("username", "")    

# Asignación de identificadores semánticos según el rol
cif = username if user_role in ["empresa", "tutor", "gestor"] else None
dni_alumno = username if user_role == "alumno" else None

if "page_hist" not in st.session_state:
    st.session_state.page_hist = "lista"
if "practicas" not in st.session_state:
    st.session_state["practicas"] = []
if "practicas_finalizadas" not in st.session_state:
    st.session_state["practicas_finalizadas"] = []
if "practicas_canceladas" not in st.session_state:
    st.session_state["practicas_canceladas"] = []
if "practica_seleccionada_hist" not in st.session_state:
    st.session_state.practica_seleccionada_hist = None

# --- OPTIMIZACIÓN: 1 Sola llamada por tabla y filtros en Python ---
def fetch_datos_optimizados():
    todas_activas = getPracticas(practicaTabla, {})
    practica_can_fin = [
        p for p in todas_activas 
        if p.get("status") in [estados[2], estados[3]]
    ]
    final = []

    if user_role == "admin":
        final = practica_can_fin

    elif user_role == "empresa":
        final = [p for p in practica_can_fin if p.get("empresa") == username]

    elif user_role == "alumno":
        final = [p for p in practica_can_fin if p.get("alumno") == username]

    elif user_role == "tutor":
        final = [p for p in practica_can_fin if p.get("tutor") == username]

    elif user_role == "tutorCentro":
        final = [p for p in practica_can_fin if p.get("tutor_centro") == username]
    
    elif user_role == "gestor":
        final = [p for p in practica_can_fin if p.get("gestor") == username]


    st.session_state["practicas"] = final


# Ejecutar proceso unificado en memoria
fetch_datos_optimizados()

practicas = st.session_state["practicas"]

# -------------------------------------------------------------------
# LÓGICA DE VISUALIZACIÓN (LISTA / DETALLE)
# -------------------------------------------------------------------
def mostrarLista():
    st.write("Aquí podraís consultar el historial de formaciones en empresas que han sido finalizadas o canceladas. Cliquea sobre una de ellas para ver el detalle.")
    if not practicas:
        st.info(f"No hay formaciones canceladas o finalizadas para el filtro seleccionado.")
    else:
        data_for_grid = []
        for p in practicas:
            anioFiltro = aniosList[st.session_state.get("index_academic", 0)]
            cursoFiltro = cursoList[st.session_state.get("index_curso", 0)]
            if st.session_state.get("index_academic", 0)>0 and p.get("anio", []) != anioFiltro:
                continue
            if st.session_state.get("index_curso", 0)>0 and p.get("curso") != cursoFiltro:
                continue
            data_for_grid.append({
                "ID": p["id"],
                "Alumno": f"{p.get('alumnos', {}).get('nombre', '')} {p.get('alumnos', {}).get('apellido', '')}",
                "Empresa": p.get('empresas', {}).get('nombre', ''),
                "Estado": p.get("status", "—"),
                "Ciclo": p.get('ciclo_formativo', '—'),
                "Fecha Finalización": p.get('fecha_fin', {}),
                "Fecha Cancelación": p.get('fecha_cancelacion', {}),
                "Motivo": p.get('motivo', {})
            })

        df = pd.DataFrame(data_for_grid)
        if df.empty:
            st.info("No hay formaciones canceladas o finalizadas aun para el curso académico o curso seleccionado.")
        else:   
            gb = GridOptionsBuilder.from_dataframe(df)
            gb.configure_grid_options(localeText=locale_tabla_principal)
            gb.configure_selection('single', use_checkbox=False)
            gb.configure_column("ID", hide=True)
            gridOptions = gb.build()

            response = AgGrid(df, gridOptions=gridOptions, update_mode=GridUpdateMode.SELECTION_CHANGED, data_return_mode=DataReturnMode.FILTERED_AND_SORTED, fit_columns_on_grid_load=True, theme='streamlit', height=400)

            selected_rows = response.get('selected_rows')
            if selected_rows is not None and len(selected_rows) > 0:
                selected_id = selected_rows.iloc[0]['ID'] if isinstance(selected_rows, pd.DataFrame) else selected_rows[0]['ID']
                st.session_state.practica_seleccionada_hist = selected_id
                st.session_state.page_hist = "detalle"
                st.rerun()

def mostrar_detalle():
    practicaId = st.session_state.practica_seleccionada_hist
    p = next((x for x in practicas if x["id"] == practicaId), None)

    if not p:
        st.error("Formación no encontrada.")
        return

    oferta = p.get("oferta_fp", {}) or {}
    empresa = p.get("empresas", {}) or {}
    alumno = p.get("alumnos", {}) or {}
    
    st.title(f"{alumno.get('nombre', '')} {alumno.get('apellido', '')} – {empresa.get('nombre', '')}")
    
    # Detalle expandido en modo estricto de lectura
    seccion_detalle(alumno, empresa, p, oferta)
    st.divider( )

    st.write(f"**Estado de Formación:** `{p.get('status', '—')}`")
    st.write(f"**Fecha Inicio:** `{p.get('fecha_inicio', '—')}`")
    st.write(f"**Fecha Cancelación:** `{p.get('fecha_cancelacion', '—')}`")
    st.write(f"**Motivo:** `{p.get('motivo', '—')}`")
    st.divider( )


    seccion_planificacion(alumno, empresa, p)
    st.divider( )
    seccion_documentacion(alumno, empresa)

    if st.button("⬅ Volver",type="primary"):
        st.session_state.page_hist = "lista"
        st.rerun()

def seccion_detalle(alumno, empresa, p, oferta):
    col1, col2 = st.columns(2)
    with col1:
        st.write(f"**Alumno:** {alumno.get('nombre', '')} {alumno.get('apellido', '')}")
        st.write(f"**DNI:** {alumno.get('dni', '')}")
        st.write(f"**Email:** {alumno.get('email_alumno', '')}")
        st.write(f"**Ciclo Formativo:** {p.get('ciclo_formativo', '—')}")
        st.write(f"**Curso Académico:** {p.get('anio') or 'No especificado'}")     
        st.write(f"**Curso:** {p.get('curso') or 'No especificado'}")     
        st.write(f"**Área:** {p.get('area') or 'No especificado'}")     
        st.write(f"**Proyecto:** {p.get('proyecto') or 'No especificado'}")      


    with col2:
        st.write(f"**Empresa:** {empresa.get('nombre', '')}")
        st.write(f"**CIF:** {empresa.get('CIF', '')}")
        st.write(f"**Dirección formación:** {oferta.get('direccion_empresa') or empresa.get('direccion', '')}") 
        st.write(f"**Localidad:** {oferta.get('localidad_empresa') or empresa.get('localidad', '')}")
        st.write(f"**Tutor Empresa:** {p.get('tutor') or 'No asignado'}")
        st.write(f"**Tutor Centro:** {p.get('tutor_centro', 'Sin asignar')}")
        st.write(f"**Gestor:** {alumno.get('gestor', 'Sin asignar')}")

def seccion_planificacion(alumno, empresa, p):
    st.subheader("📅 Planificación de Formaciones")
    folder_name = f"{alumno.get('apellido', '')}_{alumno.get('nombre', '')}_{alumno.get('dni', '')}_practica_{empresa.get('nombre', '')}".strip()
    
    archivo_calendario = None
    try:
        files = list_drive_files(folder_name)
        archivo_calendario = next((f for f in files[0] if "calendario" in f['name']), None)
    except Exception:
        pass
    
    with st.expander("Ver Calendario", expanded=True):
        if archivo_calendario and archivo_calendario.get('id'):
            preview_url = f"https://drive.google.com/file/d/{archivo_calendario.get('id')}/preview"
            st.markdown(f'<div style="border: 1px solid #ddd; border-radius: 10px; overflow: hidden;"><iframe src="{preview_url}" width="100%" height="500px" frameborder="0"></iframe></div>', unsafe_allow_html=True)
            st.link_button("Abrir imagen completa", archivo_calendario.get('webViewLink'), width='stretch')
        else:
            st.markdown('<div style="border: 2px dashed #ccc; border-radius: 10px; height: 350px; display: flex; align-items: center; justify-content: center; color: #aaa; text-align: center; padding: 10px;">No hay archivos de calendario subidos en la carpeta de Drive de esta pasantía.</div>', unsafe_allow_html=True)

def seccion_documentacion(alumno,empresa):
    st.subheader("📎 Documentos Adjuntos")

    folder_name = f"{alumno['apellido']}_{alumno['nombre']}_{alumno['dni']}_practica_{empresa['nombre']}".strip()
    files, folderId = list_drive_files(folder_name)

    if files:
        for f in files:
            fecha = f.get("modifiedTime", "")[:10]
            st.write(f"- [{f['name']}]({f['webViewLink']}) _(última modificación: {fecha})_")
    else:
        st.warning("No hay archivos.")


# Renderizado condicional del flujo de la página
if st.session_state.page_hist == "lista":
    mostrarLista()
else:
    mostrar_detalle()