import streamlit as st
import pandas as pd
from modules.data_base import (
    generarFormularioCierre,finalizarPractica,getEquals,logError,update, getPracticas, upsert,asignarFechasFormsFeedback,get, upsertCustome, cancelarPractica,crearPractica,getFormsLinks,getCiclosYAreas
)
from page_utils import apply_page_config
from navigation import make_sidebar
from datetime import datetime, timedelta
from modules.drive_helper import list_drive_files, upload_to_drive,folderNamePractica,archivoNombre
from modules.forms_helper import file_size_bytes
from modules.emailSender import enviarRecordatoriosMasivos, send_welcome_email,send_feedback_tutor_email
from pathlib import Path
from modules.feedback_helper import render_feedback_card
import uuid
import random
from variables import (forms as formsFeedback, 
    practicaTabla, tutoresTabla,
    max_file_size, carpetaPractica,linkCalendar,feedbackResponseTabla,forms,gestoresTabla, feedbackFormsTabla, alumnosTabla,
    empresasTabla,tipoPracticas,estadosAlumno,usuariosTabla,tutoresCentroTabla,estados,aniosList,cursoList,locale_tabla_principal
)
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode, DataReturnMode
# ----------------------------------------------
# CONFIG
# ----------------------------------------------
apply_page_config()

make_sidebar()
now = datetime.now().isoformat()
# ----------------------------------------------
# BOTÓN REFRESCAR
# ----------------------------------------------

if "practicas" not in st.session_state:
    st.session_state["practicas"] = []
if "tutores" not in st.session_state:
    st.session_state["tutores"] = []
if "estados" not in st.session_state:
    st.session_state["estados"] = []
if "feedbacks" not in st.session_state:
    st.session_state["feedbacks"] = []
if "gestores" not in st.session_state:
    st.session_state["gestores"] = []
if "tutorCentro" not in st.session_state:
    st.session_state["tutorCentro"] = []
if "practicas_filtradas" not in st.session_state:
    st.session_state["practicas_filtradas"] = []
if "page" not in st.session_state:
    st.session_state.page = "lista"
if "practica_seleccionada" not in st.session_state:
    st.session_state.practica_seleccionada = None
if "fecha_inicio_widget" not in st.session_state:
    st.session_state["fecha_inicio_widget"] = None
if "missing_anexos" not in st.session_state:
    st.session_state["missing_anexos"] = None
if "fecha_fin_widget" not in st.session_state:
    st.session_state["fecha_fin_widget"] = None
if "email_alumno" not in st.session_state:
    st.session_state["email_alumno"] = None
if "edit_disabled" not in st.session_state:
    st.session_state["edit_disabled"] = None
if "feedback_response" not in st.session_state:
    st.session_state["feedback_response"] = None
if "data_loaded" not in st.session_state:
    st.session_state["data_loaded"] = False
if "force_reload" not in st.session_state:
    st.session_state["force_reload"] = True
rol_usuario = st.session_state.get("rol")
col_refresh, col_volver = st.columns([1, 0.15])
with col_refresh:
    if st.session_state.page == "lista":
        st.title("Formaciones en Empresa", text_alignment="center")
    else:
        st.title("Datos formación en Empresa", text_alignment="center")
with col_volver:
    if st.button("🔄 Actualizar", key="btn_refresh"):
        st.session_state["force_reload"] = True
        st.session_state["data_loaded"] = False
        st.rerun()
# ----------------------------------------------
# FETCH FUNCTIONS
# ----------------------------------------------
@st.cache_data(ttl=300, show_spinner=False)
def fetch_ciclos_areas_cached():
    return getCiclosYAreas()


@st.cache_data(ttl=120, show_spinner=False)
def fetch_base_data_cached(statuses_key):
    practicas = getPracticas(
        practicaTabla,
        conditions=None,
        in_filters={"status": list(statuses_key)},
    )
    tutores = getEquals(tutoresTabla, {})
    tutoresCentro = getEquals(tutoresCentroTabla, {})
    feedback = get(feedbackResponseTabla)
    gestores = get(gestoresTabla)
    return practicas, tutores, tutoresCentro, feedback, gestores


@st.cache_data(ttl=120, show_spinner=False)
def get_feedback_forms_cached(practica_id):
    return getEquals(feedbackFormsTabla, {"practica_id": practica_id})


@st.cache_data(ttl=120, show_spinner=False)
def get_feedback_forms_sent_cached(practica_id):
    return getEquals(feedbackFormsTabla, {"practica_id": practica_id}, not_equals={"estado": "pendiente", "tipo_form": forms[3]})

@st.cache_data(ttl=120, show_spinner=False)
def get_feedback_responses_cached(practica_id):
    return getEquals(feedbackResponseTabla, {"practica_id": practica_id})


@st.cache_data(ttl=120, show_spinner=False)
def get_all_feedback_forms_cached():
    return get(feedbackFormsTabla)


@st.cache_data(ttl=180, show_spinner=False)
def list_drive_files_cached(folder_name):
    return list_drive_files(folder_name)


def invalidate_runtime_caches():
    fetch_base_data_cached.clear()
    get_feedback_forms_cached.clear()
    get_feedback_forms_sent_cached.clear()
    get_feedback_responses_cached.clear()
    get_all_feedback_forms_cached.clear()
    list_drive_files_cached.clear()
    st.session_state["force_reload"] = True
    st.session_state["data_loaded"] = False


def fetch_practicas_tutores():
    practicas = getPracticas(practicaTabla,  conditions=None,
    in_filters={"status": [estados[0], estados[1], estados[2], estados[3],estados[4]]})    
    tutores = getEquals(tutoresTabla, {})
    tutoresCentro = getEquals(tutoresCentroTabla, {})
    return practicas, tutores,tutoresCentro

ciclos_opts,prefs_opts_dict = fetch_ciclos_areas_cached()
def handle_update(tabla, dni_o_id, campo_a_actualizar, columna_id, key_widget, label):
    nuevo_valor = st.session_state.get(key_widget)
    if nuevo_valor:
        try:
            payload = {
                columna_id: dni_o_id, 
                campo_a_actualizar: nuevo_valor
            }
            upsert(tabla, payload, keys=[columna_id])
            invalidate_runtime_caches()
            st.toast(f"✅ {label} actualizado a: {nuevo_valor}")
        except Exception as e:
            st.error(f"Error al actualizar {label}: {e}")


# ----------------------------------------------
# CARGA DE DATOS
# ----------------------------------------------
def load_data():
    practicas, tutores, tutoresCentro, feedback, gestores = fetch_base_data_cached(tuple(estados[:5]))
    user_email = st.session_state.get("username")
    if rol_usuario == "gestor":
        gestorDatos = [g for g in gestores if g.get("email") == user_email]
        if gestorDatos:
            gestorNombre = gestorDatos[0].get("nombre")
            practicas = [
            p for p in practicas 
            if p.get("gestor") == gestorNombre or p.get("gestor") is None
        ]
        else:
            practicas = []
   
    if rol_usuario == "tutor":
        tutorDatos = [t for t in tutores if t.get("nif") == user_email]
        if tutorDatos:
            tutorNombre = tutorDatos[0].get("nombre")
            practicas = [
            p for p in practicas 
            if p.get("tutor") is not None and p.get("tutor") == tutorNombre
        ]
        else:
            practicas = []
    if rol_usuario == "tutorCentro":
        tutorCentroDatos = [t for t in tutoresCentro if t.get("email") == user_email]
        if tutorCentroDatos:
            tutorCentroNombre = tutorCentroDatos[0].get("nombre")
            practicas = [
            p for p in practicas 
            if p.get("tutor_centro") is not None and p.get("tutor_centro") == tutorCentroNombre
        ]
        else:
            practicas = []
    st.session_state["practicas"] = practicas
    st.session_state["tutores"] = tutores
    st.session_state["tutorCentro"] = tutoresCentro
    st.session_state["gestores"] = gestores
    st.session_state["feedbacks"] = feedback
    st.session_state["data_loaded"] = True
    st.session_state["force_reload"] = False
if st.session_state.get("force_reload") or not st.session_state.get("data_loaded") or not st.session_state.get("practicas"):
    with st.spinner("Cargando datos de formaciones...la primera vez puede tardar unos minutos"):
        load_data()
anioFiltro = aniosList[st.session_state.get("index_academic", 0)]
cursoFiltro = cursoList[st.session_state.get("index_curso", 0)]
practicas = st.session_state.practicas
if anioFiltro != aniosList[0]: 
    practicas = [p for p in practicas if p.get("anio") == anioFiltro]
if cursoFiltro != cursoList[0]:
    practicas = [p for p in practicas if p.get("curso") == cursoFiltro]

tutores = st.session_state["tutores"]
gestores =  st.session_state["gestores"]
tutoresCentro =st.session_state["tutorCentro"]

# ----------------------------------------------
# HELPER
# ----------------------------------------------
def tutores_por_empresa(empresa_id, lista_tutores):
    return [t for t in lista_tutores if t.get("cif_empresa") == empresa_id]

def contarAnexos(practicas: list) -> int:
    st.session_state["missing_anexos"] = 0
    for p in practicas:
        estados_p = p.get("status", {})    
        if estados_p != estados[4]:
                continue
        anexos_creados = p.get("anexos_creados")
        anexos_enviados = p.get("anexos_enviados")
        anexos_firmados = p.get("anexos_firmados")
        doc_sao_entregada = p.get("doc_sao_entregada")

        if not all([
            anexos_creados,
            anexos_enviados,
            anexos_firmados,
            doc_sao_entregada
        ]):
            st.session_state["missing_anexos"] += 1

    return st.session_state["missing_anexos"]

# ----------------------------------------------
# PAGINA: LISTA
# ----------------------------------------------
def mostrar_lista():
    st.set_page_config(page_title="Formaciones en Empresas", page_icon="🚀")
    tabs_visibles = ["📋 Listado de FE"]
    label_anexos = "📃 Anexos"
    if rol_usuario == 'admin':
        contarAnexos(practicas)  
        label_anexos = f"📃 Anexos  🔴 ({st.session_state["missing_anexos"]})" if st.session_state["missing_anexos"] > 0 else "📃 Anexos"
        tabs_visibles.extend([label_anexos, "📊 Dashboard de Feedback", "⚡️ Carga Rápida"])
    elif rol_usuario in ['gestor', 'tutorCentro']:
        tabs_visibles.append("📊 Dashboard de Feedback")
   
    tabs = st.tabs(tabs_visibles)
    with tabs[0]:
        mostrar_lista_practicas()
    
    if label_anexos in tabs_visibles:
        idx = tabs_visibles.index(label_anexos)
        with tabs[idx]:
            mostrar_anexos()

    if "📊 Dashboard de Feedback" in tabs_visibles:
        idx = tabs_visibles.index("📊 Dashboard de Feedback")
        with tabs[idx]:
            mostrar_dashboard()

    if "⚡️ Carga Rápida" in tabs_visibles:
        idx = tabs_visibles.index("⚡️ Carga Rápida")
        with tabs[idx]:
            mostrar_carga_rapida()
        
# ----------------------------------------------
# PAGINA: DETALLE
# ----------------------------------------------
def mostrar_lista_practicas():
        colText, colEmpresa, colFiltro = st.columns([1.5,1.5, 3])
        with colText:
            st.write("")
            st.write("**Selecciona una fila para ver el detalle.**")
        with colEmpresa:
            empresas_disponibles = list(
                dict.fromkeys(
                    p.get("empresas", {}).get("nombre") for p in practicas
                )
            )
            st.selectbox(
                "**Empresa**",
                options=["Todas"] + empresas_disponibles,
                index=0,
                key="selector_empresa"
            )
        with colFiltro:
            estadoFiltro = st.multiselect("**Estado**", options= estados,placeholder="Seleccione uno o más estados", default=[estados[0], estados[1], estados[4]], key="estados_tabla")
        if not practicas:
            st.info("No tienes formaciones asignadas aun para este curso académico")
            st.session_state.practicas_filtradas = []
            return
        data_for_grid = []
        practicas_filtradas_raw = []
        for p in practicas:
            pid = p["id"]
            estados_p = p.get("status", {})
            if estadoFiltro and (estados_p not in estadoFiltro):
                continue
            if st.session_state.get("selector_empresa") and st.session_state.get("selector_empresa") != "Todas":
                if p.get("empresas", {}).get("nombre") != st.session_state.get("selector_empresa"):
                    continue
            practicas_filtradas_raw.append(p)
            data_for_grid.append({
                "ID": pid,
                "Alumno": f"{p.get('alumnos', {}).get('nombre')} {p.get('alumnos', {}).get('apellido')}",
                "Empresa": p.get('empresas', {}).get('nombre'),
                "Estado": estados_p,
                "Fecha Inicio": p.get('fecha_inicio', '—'),
                "Ciclo": p.get('ciclo_formativo', '—'),
                "Gestor": p.get('gestor', 'Sin asignar'),
                "Curso Académico": f"{p.get('anio', '—')}/{p.get('curso', '—')}"
            })
        st.session_state.practicas_filtradas = practicas_filtradas_raw
        df = pd.DataFrame(data_for_grid)

        if df.empty:
            st.info("No hay formaciones con esos parametros de filtro.")
            return

        # 2. Configurar AgGrid
        gb = GridOptionsBuilder.from_dataframe(df)
        gb.configure_grid_options(localeText=locale_tabla_principal)
        gb.configure_selection('single', use_checkbox=False) # Selección de fila completa
        gb.configure_column("ID", hide=True) # Ocultamos el ID técnico
        gb.configure_grid_options(domLayout='normal')
        
        # Tip de experto: Hacer que las columnas se ajusten automáticamente
        gridOptions = gb.build()

        # 3. Renderizar el Grid
        response = AgGrid(
            df,
            gridOptions=gridOptions,
            update_mode=GridUpdateMode.SELECTION_CHANGED, # Se dispara al hacer click
            data_return_mode=DataReturnMode.FILTERED_AND_SORTED,
            fit_columns_on_grid_load=True,
            theme='streamlit', # O 'balham', 'alpine'
            height=400,
            allow_unsafe_html=True
        )

        # 4. Lógica de Navegación (Detección de Click)
        selected_rows = response.get('selected_rows')
        
        # st-aggrid v0.3.3+ devuelve una lista o un DataFrame según configuración
        if selected_rows is not None and len(selected_rows) > 0:
            # Extraemos el ID de la fila seleccionada
            # Dependiendo de la versión de aggrid, selected_rows puede ser un DataFrame o lista
            if isinstance(selected_rows, pd.DataFrame):
                selected_id = selected_rows.iloc[0]['ID']
            else:
                selected_id = selected_rows[0]['ID']

            # Seteamos el estado y redirigimos
            st.session_state.practica_seleccionada = selected_id
            st.session_state.page = "detalle"
            st.rerun()
@st.dialog("Cancelación de Formación")
def dialog_cancelacion(practica):
    st.write(f"Por favor, indica el motivo de la cancelación")
    motivo = st.text_input("", placeholder="Ej: El alumno no ha pasado la entrevista, la empresa ya no puede acoger, etc.")
    
    if st.button("Confirmar", type="primary"):
        cancelarPractica(practica, motivo)
        invalidate_runtime_caches()
        st.toast("✅  La Formación ha pasado a estado CANCELADA")
        st.session_state.page = "lista"
        st.rerun()

@st.dialog("Finalizar de Formación")
def dialog_finalizar(practica):
    st.write(f"Vas a finalizar la formación. Al confirmar se enviará el formulario de cierre al tutor de empresa")

    tutor_empresa = st.session_state.get(
        f"tutor_empresa_{practica.get('id')}"
    ) or {}

    tutor_email = tutor_empresa.get("email")

    if not tutor_email:
        tutor_email = (
            practica.get("empresas") or {}
        ).get("email_empresa")

        st.warning(
            "El tutor de empresa no fue asignado. "
            "Se enviará el correo a la empresa."
        )
    if st.button("Confirmar", type="primary"):
        finalizarPractica(practica)
        update(alumnosTabla, {"estado": estadosAlumno[0]}, {"dni": practica.get("alumno")})
        link_cierre = generarFormularioCierre(practica.get("id"), tutor_email)
        alumno = practica.get("alumnos") or {}
        nombre_alumno = f"{alumno.get('nombre', '')} {alumno.get('apellido', '')}".strip()
        sent = send_feedback_tutor_email(
            tutor_email,
            nombre_alumno,
            datetime.now().strftime("%d/%m/%Y"),
            link_cierre,
        )
        if not sent:
            st.error("❌ Error enviando email al tutor de empresa. Por favor, revisa la configuración de correo.")
            return
        else:
            st.toast("✅ Se ha enviado email a tutor de empresa con el formulario de cierre")
        invalidate_runtime_caches()
        st.toast("✅ La Formación ha pasado a estado FINALIZADA")
        st.session_state.page = "lista"
        st.rerun()

def mostrar_carga_rapida():
     with st.form("carga_rapida"):
        st.info("Utiliza esta sección para dar de alta rápidamente una empresa y un alumno que no existen en la base de datos y vincularlos en una formación.")

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

        # 3. CONFIGURACIÓN DE formación Y CICLO
        st.subheader("📋 Configuración de la Formación")
        col_p1, col_p2 = st.columns(2)

        # Obtenemos los tipos de formación de tus variables
        new_alu_tipo = col_p1.selectbox(
            "Tipo de Formación", 
            options=tipoPracticas, 
            key="qr_alu_tipo"
        )


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
        col1, col2 = st.columns(2)
        with col1:
            anio = st.selectbox("Ciclo Académico*", aniosList, key="ano_alumno")
        with col2:
            curso = st.selectbox("Curso *", cursoList, key="curso_alumno")
        # 4. BOTÓN DE ACCIÓN
        submit_btn = st.form_submit_button("🚀 Guardar y Vincular Formación")

        if submit_btn:
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
                        new_pass = f"{new_emp_cif}{random.randint(10, 99)}"
                        usuario, usuario_creado = upsertCustome(usuariosTabla, {
                                    "email": new_emp_cif,
                                    "password": new_pass,
                                    "rol": "empresa",
                                }, keys=["email"], return_created=True)
                        if usuario_creado and new_emp_cif:
                                send_welcome_email(new_emp_email, new_emp_cif,new_pass, new_emp_nombre)
                        # B. Alta Alumno
                        upsert(alumnosTabla, {
                            "dni": new_alu_dni,
                            "nombre": new_alu_nombre,
                            "apellido": new_alu_apellido,
                            "email_alumno": new_alu_email,
                            "tipoPractica": new_alu_tipo,
                            "ciclo_formativo": new_alu_ciclo,
                            "preferencias_fp": new_alu_pref,
                            "anio": anio,
                            "curso": curso,
                            "estado": estadosAlumno[1]
                        }, keys=["dni"])
                        new_passA = f"{new_alu_dni}{random.randint(10, 99)}"
                        usuario, usuario_creado = upsertCustome(usuariosTabla, {
                                    "email": new_alu_dni,
                                    "password": new_passA,
                                    "rol": "alumno",
                                }, keys=["email"], return_created=True)
                        if usuario_creado and new_alu_dni:
                            send_welcome_email(new_alu_email, new_alu_dni,new_passA, new_alu_nombre)

                        # C. Crear la formación (Vincular)
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
                            oferta_id=None,
                            status= estados[4],
                            anio= anio,
                            curso= curso,
                        )

                        st.success(f"✅ ¡Éxito! Formación creada entre {new_emp_nombre} y {new_alu_nombre}.")
                        st.success(f"✅ Se ha creado y enviado un usuario y contraseña para la empresa")
                        st.success(f"✅ Se ha creado y enviado un usuario y contraseña para el alumno")
                        invalidate_runtime_caches()
                    except Exception as e:
                        st.error(f"❌ Error en el proceso: {str(e)}")
def guardar_anexo_automatico(practica_id, campo_bd, key_widget):
    # Obtenemos el valor actual del checkbox directamente desde el session_state
    nuevo_valor = st.session_state[key_widget]
    
    payload_practica = {
        "id": practica_id,
        campo_bd: nuevo_valor
    }
    
    try:
        res = upsert(practicaTabla, payload_practica, keys=["id"])
        if res and getattr(res, 'data', None):
            invalidate_runtime_caches()
            st.toast(f"✅ Estado actualizado")
    except Exception as e:
        st.error(f"Error al actualizar la base de datos: {e}")

def mostrar_anexos_practica(practica):
    with st.expander("📋 Gestión de Anexos"):
        practica_id = practica.get("id")

        # Creamos 4 columnas para la fila horizontal
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.checkbox(
                "Anexos Creados", 
                value=bool(practica.get('anexos_creados')),
                key=f"chk_creado_{practica_id}",
                on_change=guardar_anexo_automatico,
                args=(practica_id, 'anexos_creados', f"chk_creado_{practica_id}"),
                disabled=st.session_state["edit_disabled"]
            )
        
        with col2:
            st.checkbox(
                "Anexos Enviados", 
                value=bool(practica.get('anexos_enviados')),
                key=f"chk_enviados_{practica_id}",
                on_change=guardar_anexo_automatico,
                args=(practica_id, 'anexos_enviados', f"chk_enviados_{practica_id}"),
                disabled=st.session_state["edit_disabled"]
            )
            
        with col3:
            st.checkbox(
                "Anexos Firmados", 
                value=bool(practica.get('anexos_firmados')),
                key=f"chk_firmados_{practica_id}",
                on_change=guardar_anexo_automatico,
                args=(practica_id, 'anexos_firmados', f"chk_firmados_{practica_id}"),
                disabled=st.session_state["edit_disabled"]
            )
            
        with col4:
            st.checkbox(
                "DOC SAO", 
                value=bool(practica.get('doc_sao_entregada')),
                key=f"chk_sao_{practica_id}",
                on_change=guardar_anexo_automatico,
                args=(practica_id, 'doc_sao_entregada', f"chk_sao_{practica_id}"),
                disabled=st.session_state["edit_disabled"]
            )
def mostrar_anexos():
    if not practicas:
        st.info("No tienes formaciones asignadas aun.")
        return

    data_for_grid = []
    for p in practicas:
        pid = p["id"]
        
        estados_p = p.get("status", {})
        if estados_p != estados[4]:
            continue
            
        data_for_grid.append({
            "ID": pid,
            "Alumno": f"{p.get('alumnos', {}).get('nombre', '')} {p.get('alumnos', {}).get('apellido', '')}",
            "Empresa": p.get('empresas', {}).get('nombre', '—'),
            "Gestor": p.get('gestor', 'Sin asignar'),
            "Estado": estados_p,
            "Ciclo": p.get('ciclo_formativo', '—'),
            "Creado": True if p.get('anexos_creados') is True else False,
            "Enviados": True if p.get('anexos_enviados') is True else False,
            "Firmados": True if p.get('anexos_firmados') is True else False,
            "DOC SAO": True if p.get('doc_sao_entregada') is True else False
        })

    # Si después de revisar todas las prácticas la lista está vacía, muestra un solo mensaje
    if not data_for_grid:
        st.info("No tienes formaciones pendientes de documentación.")
        return

    # Todo lo siguiente se ejecuta una sola vez, fuera del bucle for
    df_original = pd.DataFrame(data_for_grid)
    st.subheader("📋 Gestión de Anexos")
    
    if "df_key" not in st.session_state:
        st.session_state.df_key = 0

    state_key = f"editor_anexos_{st.session_state.df_key}"

    edited_df = st.data_editor(
        df_original,
        key=state_key,
        hide_index=True,
        width='stretch',
        disabled=["ID", "Alumno", "Empresa", "Gestor", "Estado", "Ciclo"],
        column_config={
            "ID": None,
            "Creado": st.column_config.CheckboxColumn("Creado"),
            "Enviados": st.column_config.CheckboxColumn("Enviados"),
            "Firmados": st.column_config.CheckboxColumn("Firmados"),
            "DOC SAO": st.column_config.CheckboxColumn("DOC SAO"),
        }
    )

    cambios = st.session_state[state_key].get("edited_rows")
    
    if cambios:
        if st.button("💾 Guardar Cambios en Anexos"):
            with st.spinner("Guardando en base de datos..."):
                for row_idx_str, updated_cols in cambios.items():
                    idx = int(row_idx_str)
                    pid_db = int(df_original.at[idx, "ID"])
                    
                    payload_practica = {
                        "id": pid_db,
                        "anexos_creados": bool(edited_df.at[idx, "Creado"]),
                        "anexos_enviados": bool(edited_df.at[idx, "Enviados"]),
                        "anexos_firmados": bool(edited_df.at[idx, "Firmados"]),
                        "doc_sao_entregada": bool(edited_df.at[idx, "DOC SAO"]),
                    }
                    
                    try:
                        upsert(practicaTabla, payload_practica, keys=["id"])
                    except Exception as e:
                        st.error(f"Error en ID {pid_db}: {e}")
                
                st.toast("✅ Anexos actualizados correctamente.")
                st.session_state.df_key += 1
                invalidate_runtime_caches()
                st.session_state["force_reload"] = True 
                st.rerun()

def mostrar_dashboard():
    st.subheader("Seguimiento de Feedback")
    
    col_f1, col_f2, col_f3 = st.columns([1,1, 4])
    with col_f1:
        fecha_inicio_filtro = st.date_input("Desde", value=datetime.now() - timedelta(days=90))
    with col_f2:
        fecha_fin_filtro = st.date_input("Hasta", value=datetime.now())

    all_feedback_forms = get_all_feedback_forms_cached()
    ids_permitidos = [p["id"] for p in practicas]
    all_feedback_forms = [f for f in all_feedback_forms if f.get("practica_id") in ids_permitidos
]
    if not all_feedback_forms:
        st.info("No hay datos de envíos de feedback.")
        return
    else:
        # Convertir a DataFrame para filtrar fácil
        df_fb = pd.DataFrame(all_feedback_forms)
        df_fb['fecha_envio'] = pd.to_datetime(df_fb['fecha_envio'], errors='coerce')
        # Convertimos los filtros a Timestamp, no la columna a date
        ts_inicio = pd.Timestamp(fecha_inicio_filtro)
        ts_fin = pd.Timestamp(fecha_fin_filtro) + pd.Timedelta(days=1) - pd.Timedelta(seconds=1)
        mask = (df_fb['fecha_envio'] >= ts_inicio) & (df_fb['fecha_envio'] <= ts_fin)
        df_filtrado = df_fb.loc[mask]
        # 3. Métricas Principales (KPIs)
        # Tipos: feedback_inicial, feedback_adaptacion, feedback_cierre
        total_pendientes = len(df_filtrado[df_filtrado['estado'] == 'pendiente'])
        total_enviados = len(df_filtrado[df_filtrado['estado'] != 'pendiente'])
        total_respondidos = len(df_filtrado[df_filtrado['fecha_respuesta'].notna()])
        pct_respuesta = round((total_respondidos / total_enviados * 100) if total_enviados > 0 else 0)
        pct_pendiente = 100 - pct_respuesta

        st.markdown("""
        <style>
        .kpi-card {
            background: #f8f9fa;
            border-radius: 16px;
            padding: 20px;
            text-align: center;
            border: 1px solid #e0e0e0;
        }
        .kpi-circle {
            width: 110px; height: 110px;
            border-radius: 50%;
            display: flex; flex-direction: column;
            align-items: center; justify-content: center;
            margin: 0 auto 10px auto;
            font-weight: bold;
        }
        .kpi-title { font-size: 13px; color: #666; margin-bottom: 4px; }
        .kpi-number { font-size: 32px; font-weight: 800; }
        .kpi-pct { font-size: 13px; }
        </style>
        """, unsafe_allow_html=True)

        st.subheader("📊 Métricas Envio Correos y Respuestas")
        c1, c2, c3, c4 = st.columns(4)
        with c1:
            st.markdown(f"""
            <div class="kpi-card">
                <div class="kpi-circle" style="background:#f3e5f5; color:#8e24aa;">
                    <div class="kpi-number">{total_pendientes}</div>
                    <div class="kpi-pct">Total</div>
                </div>
                <div class="kpi-title">Pendiente de Envio</div>
            </div>""", unsafe_allow_html=True)
        with c2:
            st.markdown(f"""
            <div class="kpi-card">
                <div class="kpi-circle" style="background:#e8f4fd; color:#1a73e8;">
                    <div class="kpi-number">{total_enviados}</div>
                    <div class="kpi-pct">Enviados</div>
                </div>
                <div class="kpi-title">Total Enviados</div>
            </div>""", unsafe_allow_html=True)

        with c3:
            st.markdown(f"""
            <div class="kpi-card">
                <div class="kpi-circle" style="background:#e6f4ea; color:#34a853;">
                    <div class="kpi-number">{total_respondidos}</div>
                    <div class="kpi-pct">{pct_respuesta}%</div>
                </div>
                <div class="kpi-title">Total Respondidos y %</div>
            </div>""", unsafe_allow_html=True)

        with c4:
            st.markdown(f"""
            <div class="kpi-card">
                <div class="kpi-circle" style="background:#fce8e6; color:#ea4335;">
                    <div class="kpi-number">{total_enviados - total_respondidos}</div>
                    <div class="kpi-pct">{pct_pendiente}%</div>
                </div>
                <div class="kpi-title">Total Pendientes Respuesta y %</div>
            </div>""", unsafe_allow_html=True)

        tipos = [
            ("feedback_inicial", "Acogida", "#fff3e0", "#f57c00"),
            ("feedback_adaptacion", "Adaptación", "#f3e5f5", "#8e24aa"),
            ("feedback_cierre", "Cierre", "#e0f2f1", "#00897b"),
        ]
        st.subheader("📊 Métricas Por tipo")
        col1, col2, col3 = st.columns(3)
        for col, (tipo, label, bg, color) in zip([col1, col2, col3], tipos):  # reutiliza columnas o ajusta
            count = len(df_filtrado[(df_filtrado['tipo_form'] == tipo) & (df_filtrado['estado'] == 'Completado')])
            with col:
                st.markdown(f"""
                <div class="kpi-card" style="margin-top:12px">
                    <div class="kpi-circle" style="background:{bg}; color:{color};">
                        <div class="kpi-number">{count}</div>
                        <div class="kpi-pct">Completos</div>
                    </div>
                    <div class="kpi-title">{label}</div>
                </div>""", unsafe_allow_html=True)

        st.divider()

        # 4. Alumnos Pendientes de Respuesta
        col_p1, col_p2 = st.columns([2, 1])
        
        with col_p1:
            st.write("### ⏳ Alumnos que no han respondido")
            # Filtramos los que se enviaron pero no tienen fecha_respuesta
            df_pendientes = df_filtrado[(df_filtrado['estado'] == 'enviado') & (df_filtrado['fecha_respuesta'].isna())]
            base_url = st.secrets["urls"]["URL"] 
            practicas_by_id = {item["id"]: item for item in practicas}
        
            listado_morosos = []
            for _, row in df_pendientes.iterrows():
                practica = practicas_by_id.get(row['practica_id'])
                if practica:
                    alumno_nom = f"{practica['alumnos']['nombre']} {practica['alumnos']['apellido']}"
                    tipo = row['tipo_form']
                    token = row['token']
                    link = f"{base_url.rstrip('/')}/{tipo}?token={token}&tipo={tipo}"

                    listado_morosos.append({
                        "Id": row['practica_id'],
                        "Alumno": alumno_nom,
                        "Email": row['email_destino'],
                        "Formulario": row['tipo_form'].replace('_', ' ').title(),
                        "Fecha Envío": row['fecha_real_envio'],
                        "Recordatorio Enviado": row['recordatorio'] if row['recordatorio'] else "No enviado aún",
                        "Link": f'<a href="{link}" target="_blank">Link</a>',
                        "_tipo_form": row['tipo_form'],
                    })

            if listado_morosos:
                    df_mostrar = pd.DataFrame(listado_morosos)
                    columnas_visibles = [c for c in df_mostrar.columns if not c.startswith("_")]
                    st.markdown(df_mostrar[columnas_visibles].to_html(escape=False, index=False).replace('<th>', '<th style="text-align:center">'), unsafe_allow_html=True)
            else:
                st.success("¡Todos los alumnos han respondido!")

        with col_p2:
            st.write("### ⚡ Acciones")
            st.info("Enviar recordatorio por correo a todos los alumnos pendientes de esta lista.")
            
            if st.button("🔔 Enviar Recordatorio Masivo", type="primary", width='stretch'):
                if not df_pendientes.empty:
                    with st.spinner("Enviando recordatorios..."):
                        emails_enviados, errores = enviarRecordatoriosMasivos(listado_morosos)
                        if emails_enviados:
                            st.success(f"✅ Recordatorios enviados a {emails_enviados} alumnos.")
                        if errores:
                            st.warning(f"⚠️ No se pudo enviar a: {', '.join(errores)}")
                else:
                    st.warning("No hay nadie a quien reclamar.")

def seccion_detalle(alumno, empresa, p, oferta, gestores, tutores):
    st.session_state["email_alumno"] = alumno.get("email_alumno")
    with st.expander("Detalle", expanded=True):
        col1, col2 = st.columns(2)
        with col1:
            st.write(f"**Alumno:** {alumno['nombre']} {alumno['apellido']}")
            st.write(f"**DNI:** {alumno['dni']}")
            st.write(f"**Email:** {alumno['email_alumno']}")
            st.write(f"**Teléfono Alumno:** {alumno['telefono']}")
            st.write(f"**Ciclo:** {p.get('ciclo_formativo', '—')}")
            area = p.get("area") or "No especificado"
            st.write(f"**Área:** {area}")     
            proyecto = p.get("proyecto") or "No especificado"
            st.write(f"**Proyecto:** {proyecto}")      
            st.write(f"**Curso Académico:** {p.get('anio', '—')}")  
            st.write(f"**Curso:** {p.get('curso', '—')}")  
        with col2:
            st.write(f"**Empresa:** {empresa['nombre']}")
            st.write(f"**CIF:** {empresa['CIF']}")
            st.write(f"**Teléfono:** {empresa['telefono']}")
            st.write(f"**Email:** {empresa['email_empresa']}")
            direccion = oferta.get("direccion_empresa") or  empresa['direccion']
            st.write(f"**Dirección Formación:** {direccion}")
            localidad = oferta.get("localidad_empresa") or  empresa['localidad'] 
            st.write(f"**Localidad:** {localidad}")

            lista_nombres_gestores = [g["nombre"] for g in gestores]
            if "No asignado" not in lista_nombres_gestores:
                lista_nombres_gestores.insert(0, "No asignado")
            gestor_actual = p.get("gestor")
            try:
                indice_gestor = lista_nombres_gestores.index(gestor_actual) if gestor_actual in lista_nombres_gestores else 0
            except:
                indice_gestor = 0
        colGestor, colTutor, colTCentro = st.columns(3)
        with colGestor:
            clave_gestor = f"gestor_{alumno['id']}"
            if rol_usuario in {"admin", "gestor"}:
                st.selectbox(
                    "**Gestor Asignado**",
                    options=lista_nombres_gestores,
                    index=indice_gestor,
                    key=clave_gestor,
                    on_change=handle_update,
                    # Pasamos la KEY en lugar del valor
                    args=(practicaTabla, p['id'], "gestor", "id", clave_gestor, "Gestor"),
                    disabled=st.session_state["edit_disabled"]
                )
            else:
                 st.write(f"**Gestor:** {gestor_actual or 'Sin asignar'}")
   
        tutores_filtrados = [g for g in tutores if g["cif_empresa"] == empresa['CIF']]
        lista_nombres_tutores = [g["nombre"] for g in tutores_filtrados]
        if "No asignado" not in lista_nombres_tutores:
            lista_nombres_tutores.insert(0, "No asignado")
        tutor_actual = p.get("tutor") 
        indice_tutor = lista_nombres_tutores.index(tutor_actual) if tutor_actual in lista_nombres_tutores else 0
        with colTutor:
            clave_tutor = f"tutor_{alumno['id']}"
            tutor_seleccionado = st.session_state.get(
                clave_tutor,
                tutor_actual,
            )

            tutor_empresa = next(
                (
                    tutor for tutor in tutores_filtrados
                    if tutor.get("nombre") == tutor_seleccionado
                ),
                {},
            )

            st.session_state[f"tutor_empresa_{p['id']}"] = tutor_empresa
            if rol_usuario in {"admin", "gestor"}:
                st.selectbox(
                    "**Tutor Empresa**",
                    options=lista_nombres_tutores,
                    index=indice_tutor,
                    key=clave_tutor,
                    on_change=handle_update,
                    args=(practicaTabla, p['id'], "tutor", "id", clave_tutor, "Tutor"),
                    disabled=st.session_state["edit_disabled"]
                    )
            else:
                st.write(f"**Tutor Empresa:** {tutor_actual  or 'Sin asignar'}")
                

        lista_nombres_tutoresCentro = [g["nombre"] for g in tutoresCentro]
        if "No asignado" not in lista_nombres_tutoresCentro:
            lista_nombres_tutoresCentro.insert(0, "No asignado")
        tutorc_actual = p.get("tutor_centro") 
        indice_tutorc = lista_nombres_tutoresCentro.index(tutorc_actual) if tutorc_actual in lista_nombres_tutoresCentro else 0
        with colTCentro:
            clave_tutorc = f"tutor_centro_{alumno['id']}"
            if rol_usuario in {"admin", "gestor"}:
                st.selectbox(
                    "**Tutor Centro**",
                    options=lista_nombres_tutoresCentro,
                    index=indice_tutorc,
                    key=clave_tutorc,
                    on_change=handle_update,
                    args=(practicaTabla, p['id'], "tutor_centro", "id", clave_tutorc, "TutorCentro"),
                    disabled=st.session_state["edit_disabled"]
                )
            else:
                st.write(f"**Tutor Centro:** {tutorc_actual or 'Sin asignar'}")

        pass

def seccion_programar(p):
    with st.expander("📅 Programación de la Formación", expanded=True):
        f_inicio_db = p.get('fecha_inicio')
        f_fin_db = p.get('fecha_fin')
        if f_inicio_db and f_fin_db:
            st.caption(f"✅ Periodo definido: de {f_inicio_db} hasta {f_fin_db}")
        fecha_inicio_val = datetime.strptime(f_inicio_db, '%Y-%m-%d').date() if f_inicio_db else datetime.now().date()
    
        if f_fin_db:
            fecha_fin_val = datetime.strptime(f_fin_db, '%Y-%m-%d').date()
        else:
            fecha_fin_val = fecha_inicio_val + timedelta(days=90) # Aprox 3 meses

        colForm , col, colCancel = st.columns([3,0.5, 1])
        with colForm:
            with st.form(key=f"form_fechas_{p['id']}"):
                col_ini, col_fin = st.columns(2)
                with col_ini:
                    nueva_f_ini = st.date_input(
                        "Fecha Inicio", 
                        value=fecha_inicio_val,
                        disabled=st.session_state["edit_disabled"]
                    )

                with col_fin:
                    nueva_f_fin = st.date_input(
                        "Fecha Fin (Prevista)", 
                        value=fecha_fin_val,
                        disabled=st.session_state["edit_disabled"]
                    )
                
                # Botón de guardado dentro del formulario
                submit_save = st.form_submit_button("💾 Guardar",  disabled=st.session_state["edit_disabled"])

            if submit_save:
                payload_practica = {
                                "id": int(p.get('id')),
                                "fecha_inicio": nueva_f_ini.isoformat(),
                                "fecha_fin": nueva_f_fin.isoformat()
                            }
                res = upsert(practicaTabla, payload_practica, keys=["id"])
                if res and getattr(res, 'data', None):
                    invalidate_runtime_caches()
                st.success("Fechas actualizadas")
                st.rerun()

def seccion_gestion(p):
    with st.expander("Gestión de la Formación", expanded=True):
        f_inicio_db = p.get('fecha_inicio')
        f_fin_db = p.get('fecha_fin_real')

        fecha_inicio_texto = f_inicio_db or "Sin asignar aún"
        fecha_fin_texto = f_fin_db or "Sin asignar aún"
        col1, col2 = st.columns(2)
        with col1:
            st.write(f"**Fecha de inicio:** {fecha_inicio_texto}")
        with col2:
            st.write(f"**Fecha de fin Real:** {fecha_fin_texto}")
        colForm , col, colCancel = st.columns([3,0.5, 1])
        with colForm:
            if st.button("Finalizar Formación", key=f"finalizar_{p['id']}", type="primary", disabled=st.session_state["edit_disabled"]):
                dialog_finalizar(p)       

        with colCancel:
            if st.button("Cancelar Formación", key=f"cancelar_{p['id']}", type="secondary", disabled= st.session_state["edit_disabled"]):
                dialog_cancelacion(p)       
                
def feedback_formaciones(practica):
    practicaId=practica.get('id')
    alumno = practica.get('alumnos', {})
    feedbacks_forms = get_feedback_forms_cached(practicaId)
    fechas = {f['tipo_form']: datetime.strptime(f['fecha_envio'], "%Y-%m-%d").strftime("%d/%m/%Y") for f in feedbacks_forms}

    if(practica.get('status') is not None and practica.get('status') != estados[1]):
        st.info(f"ℹ️ **Estado:** {practica.get('status')}", icon="🚀")
    else:
        st.info(f"ℹ️ **Estado:** {practica.get('status')}", icon="🚀")
        if len(feedbacks_forms) <= 0:
            fecha_inicio_dt = datetime.fromisoformat(practica.get('fecha_inicio'))
            fecha_fin_dt = datetime.fromisoformat(practica.get('fecha_fin'))
            asignarFechasFormsFeedback(int(practica.get('id')), fecha_inicio_dt, alumno.get('email_alumno'), fecha_fin_dt)
            invalidate_runtime_caches()
            st.toast("Generando formularios de feedback.")
            st.caption("Actualice la formación para ver los hitos")
        else:
            if (practica.get('status') is not None and practica.get('status') == estados[1]):
                links = getFormsLinks(practicaId)
                links_map = {item['tipo']: item['url'] for item in links}
                with st.container(border=True):
                    link_ini = links_map.get('feedback_inicial', '#')
                    link_ada = links_map.get('feedback_adaptacion', '#')
                    link_cie = links_map.get('feedback_cierre', '#')
                    st.markdown(f"""
                    **Próximo Hito:**
                    * 📅 **Envio Feedback Acogida:** : {fechas.get('feedback_inicial', '--')} | [🔗 Abrir Formulario]({link_ini})
                    * 🕒 **Envio Feedback Adaptación:** {fechas.get('feedback_adaptacion', '--')} | [🔗 Abrir Formulario]({link_ada})
                    * ⏲️ **Envio Feedback Cierre:** {fechas.get('feedback_cierre', '--')} | [🔗 Abrir Formulario]({link_cie})
                    """)

def seccion_feedback_candidato(p, practicaId, forms):
    feedback_formaciones(p)
    st.subheader("¿Cómo se siente el candidato?")
    st.session_state.feedback_response = feedbacks_db = get_feedback_responses_cached(practicaId)
    feedbacksEnviados_db = get_feedback_forms_sent_cached(practicaId)
    st.write(f"**Número de feedbacks enviados:** {len(feedbacksEnviados_db)}")
    progreso_feedback = {
        forms[0]: None,
        forms[1]: None,
        forms[2]: None,
    }

    for f in feedbacks_db:
        tipo = f["respuestas_json"].get("tipo")
        if tipo in progreso_feedback:
            progreso_feedback[tipo] = f["respuestas_json"]
    respuestasCierre= progreso_feedback[forms[2]]

    # 3. Crear las columnas y mostrar las cards
    col_ini, col_ada,col_cie = st.columns(3)

    with col_ini:
        render_feedback_card(progreso_feedback[forms[0]], "Acogida")

    with col_ada:
        render_feedback_card(progreso_feedback[forms[1]], "Adaptación")

    with col_cie:
        render_feedback_card(respuestasCierre, "Cierre")
    pass
    st.subheader(f"Resultado de la formación en Empresa")
    tabResultado, tabFeedback = st.tabs(["Resultado Formación", "Formulario Cierre Tutor Empresa"])
    with tabResultado:
        respuestasCierreFormacion = p.get("datos_cierre") or {}
        if respuestasCierre:
            # ¿Te contrata la empresa?
            contratado = respuestasCierreFormacion.get("contratado", False)
            st.markdown(f"{'✅' if contratado else '❌'} **¿Lo contrata la empresa?**")

            # ¿Sigue estudiando?
            sigue = respuestasCierreFormacion.get("sigueEstudiando", False)
            st.markdown(f"{'✅' if sigue else '❌'} **¿Sigue estudiando?**")
            if sigue:
                estudios = respuestasCierreFormacion.get("estudios") or "—"
                lugar = respuestasCierreFormacion.get("lugarEstudios") or "—"
                st.markdown(f"&nbsp;&nbsp;&nbsp;&nbsp;📚 **Qué:** {estudios}")
                st.markdown(f"&nbsp;&nbsp;&nbsp;&nbsp;📍 **Dónde:** {lugar}")

            # ¿Contratado por otra empresa?
            otra = respuestasCierreFormacion.get("contratadoOtraEmpresa", False)
            st.markdown(f"{'✅' if otra else '❌'} **¿Contratado por otra empresa?**")
            if otra:
                empresa = respuestasCierreFormacion.get("nombreEmpresa") or "—"
                st.markdown(f"&nbsp;&nbsp;&nbsp;&nbsp;🏢 **Empresa:** {empresa}")
        else:
            st.info("Aún no se ha completado el formulario de cierre.") 
    with tabFeedback:
            feedback_responses = st.session_state.get("feedback_response") or []
            feedback_tutor_empresa = [
                response
                for response in feedback_responses
                if (response.get("respuestas_json") or {}).get("tipo")
                == formsFeedback[3]
            ]

            if feedback_tutor_empresa:
                for feedback in feedback_tutor_empresa:
                    respuestas = feedback.get("respuestas_json") or {}

                    st.subheader("Formulario de cierre del tutor de empresa")

                    orden_secciones = [
                        "valoracion_tutor_empresa",
                        "insercion_laboral",
                    ]
                    etiquetas = {
                        "actitud_alumnado": "Actitud del alumnado",
                        "seguimiento_tutor_centro": "Seguimiento del tutor del centro",
                        "valoracion_general_formacion": "Valoración general de la formación",
                        "aspectos_positivos": "Aspectos positivos",
                        "propuestas_mejora": "Propuestas de mejora",
                        "oferta_relacion_laboral": "Oferta de relación laboral",
                        "alumno_acepto_oferta": "Aceptación del alumno",
                        "tipo_contrato": "Tipo de contrato",
                        "motivo_no_oferta": "Motivo de no ofrecer contrato",
                        "motivo_no_aceptacion": "Motivo de no aceptación",
                        "detalle_otros_motivo": "Detalle de otros motivos",
                        "recomendaria_contratacion": "Recomendaría la contratación",
                        "motivo_no_recomendacion": "Motivo de no recomendación",
                    }

                    for seccion in orden_secciones:
                        respuestas_seccion = respuestas.get(seccion)
                        if not isinstance(respuestas_seccion, dict):
                            continue

                        titulo = seccion.replace("_", " ").capitalize()
                        st.markdown(f"### {titulo}")

                        if seccion == "valoracion_tutor_empresa":
                            orden_preguntas = [
                                "actitud_alumnado",
                                "seguimiento_tutor_centro",
                                "valoracion_general_formacion",
                                "aspectos_positivos",
                                "propuestas_mejora",
                            ]
                        else:
                            oferta = respuestas_seccion.get("oferta_relacion_laboral")
                            aceptacion = respuestas_seccion.get("alumno_acepto_oferta")
                            orden_preguntas = ["oferta_relacion_laboral"]

                            if oferta == "No":
                                orden_preguntas.append("motivo_no_oferta")
                            elif oferta == "Sí":
                                orden_preguntas.append("alumno_acepto_oferta")
                                if aceptacion == "Sí":
                                    orden_preguntas.append("tipo_contrato")
                                elif aceptacion == "No":
                                    orden_preguntas.append("motivo_no_aceptacion")
                                    if respuestas_seccion.get("motivo_no_aceptacion") == "c) Otros":
                                        orden_preguntas.append("detalle_otros_motivo")

                            orden_preguntas.append("recomendaria_contratacion")
                            if respuestas_seccion.get("recomendaria_contratacion") == "No":
                                orden_preguntas.append("motivo_no_recomendacion")

                        for pregunta in orden_preguntas:
                            if pregunta in respuestas_seccion:
                                pregunta_titulo = etiquetas.get(
                                    pregunta, pregunta.replace("_", " ").capitalize()
                                )
                                st.write(f"**{pregunta_titulo}:** {respuestas_seccion[pregunta]}")
            else:
                st.info("Aún no se ha completado el formulario de cierre del tutor de empresa.")
def seccion_feedback_tutor(practicaId, p, tutor_actual, abierto:None):
    st.subheader("Seguimiento del Tutor Empresa")
    nombre_tutor = tutor_actual or "Sin Asignar"

    with st.expander(f"Tutor en Empresa: {nombre_tutor}", expanded=True):
        historial_feedback = p.get("feedback_tutor")
        if not isinstance(historial_feedback, list):
            historial_feedback = []
        if rol_usuario == 'tutor':
            with st.container(border=True):
                st.markdown("##### Añadir nueva observación")
                nuevo_comentario = st.text_area(
                    "Describe el progreso del alumno hoy:",
                    placeholder="Ej: El alumno ha empezado a manejar las herramientas de diseño con autonomía...",
                    key=f"input_fb_{practicaId}"
                )
                
                if st.button("💾 Publicar Comentario", width='stretch'):
                    if nuevo_comentario.strip():
                        # Crear el nuevo registro
                        nuevo_registro = {
                            "fecha": datetime.now().strftime("%d/%m/%Y %H:%M"),
                            "tutor": tutor_actual, 
                            "mensaje": nuevo_comentario.strip()
                        }
                        
                        # Añadir al historial existente
                        historial_feedback.append(nuevo_registro)
                        
                        try:
                            upsert(practicaTabla, {
                                "id": int(practicaId),
                                "feedback_tutor": historial_feedback
                            }, keys=["id"])
                            invalidate_runtime_caches()
                            
                            st.toast("✅ Comentario guardado")
                            # Actualizar el objeto p para mostrarlo sin esperar recarga manual
                            p["feedback_tutor"] = historial_feedback
                            st.rerun() 
                        except Exception as e:
                            st.error(f"Error al guardar: {e}")
                    else:
                        st.warning("Escribe algo antes de guardar.")

        # 3. VISUALIZACIÓN DEL HISTORIAL (Para Tutor y Gestor)
        # Lo mostramos en un contenedor con scroll si hay muchos
        if historial_feedback:
            with st.expander("Historial de observaciones", expanded=abierto):
                for fb in reversed(historial_feedback):
                    with st.chat_message("user", avatar="👨‍🏫"):
                        st.markdown(f"**{fb['tutor']}** - <span style='color:gray; font-size:0.8rem;'>{fb['fecha']}</span>", unsafe_allow_html=True)
                        st.write(fb['mensaje'])
        else:
            st.info("No hay feedback registrado todavía en esta formación.")
        pass

def seccion_feedback_tutorCentro(practicaId, p, tutor_actual):
    puede_editar = rol_usuario == "tutorCentro"
    ultimo_feedback = p.get("feedback_tutor_centro") or {}
    if "contratadoOtraEmpresa" not in st.session_state:
        st.session_state.contratadoOtraEmpresa = ultimo_feedback.get("contratadoOtraEmpresa", False)
    st.subheader("Seguimiento del Tutor Centro")
    with st.expander(f"Tutor Centro: {tutor_actual}", expanded=True):
        if "fp_contacto" not in st.session_state:
            st.session_state.fp_contacto = ultimo_feedback.get("programaFP", False)

        with st.form("form_feedback_tutor_centro"):
            st.info("Aquí puede añadir comentarios sobre el seguimiento de la formación del alumno, así como cualquier observación relevante para la empresa o el alumno.")
            comentarios_contacto1 = st.text_area("Comentarios",
                value=ultimo_feedback.get("primerContacto", ""),
                disabled=not puede_editar)
            fp = st.checkbox("¿He informado de los programas del ecosistema de FP?",
                disabled=not puede_editar, key="fp_contacto")
            ha_acogido = st.radio(
                label="**¿Alguna vez has acogido a algún estudiante de FP dual?**",
                options=[True, False],
                index=0 if ultimo_feedback.get("FPPYME") == True else 1,
                horizontal=True,
                key="ha_acogido_fp_dual",
                format_func=lambda x: "Sí" if x else "No",
                disabled=not puede_editar
            )
            
            submit = st.form_submit_button("💾 Guardar", type="primary", use_container_width=True, disabled= not puede_editar)

        if submit:
            nuevo_registro = {
                "fecha": datetime.now().strftime("%d/%m/%Y %H:%M"),
                "tutorCentro": tutor_actual,
                "primerContacto": comentarios_contacto1.strip(),
                "programaFP": fp,
                "FPPYME": ha_acogido
            }

            try:
                upsert(practicaTabla, {
                    "id": int(practicaId),
                    "feedback_tutor_centro": nuevo_registro,
                    "fp_dual_cogido":ha_acogido
                }, keys=["id"])
                invalidate_runtime_caches()

                st.toast("✅ Seguimiento guardado")
                p["feedback_tutor_centro"] = nuevo_registro
                st.rerun()
            except Exception as e:
                st.error(f"Error al guardar: {e}")

def actualizar_fecha(key_nombre, id_registro, tipo):
    nueva_fecha = st.session_state[key_nombre]
    st.write(nueva_fecha)
    st.toast(f"Actualizando fecha: {nueva_fecha}")
    payload_practica = {
                            "id": int(id_registro),
                            tipo: datetime.strptime(str(nueva_fecha.strftime("%Y-%m-%d")), "%Y-%m-%d").strftime("%Y-%m-%d")
                        }
    res = upsert(practicaTabla, payload_practica, keys=["id"])
    if res and getattr(res, 'data', None):
        invalidate_runtime_caches()
        st.toast("✅ Fecha actualizada")

def seccion_planificacion(folder_name, practica):
    with st.expander("🗓️ Calendario de Formación"):
        practicaId = practica.get("id")

        files = list_drive_files_cached(folder_name)
        archivo_calendario = next((f for f in files[0] if "calendario" in f['name']), None)

        if rol_usuario == 'admin'and st.session_state["edit_disabled"]==False:   
            col_cal1, col_cal2 = st.columns([1, 2]) # Ajustamos el ancho para la imagen
            with col_cal1:
                url_generador = linkCalendar
                st.link_button("🛠️ Generar Nuevo Calendario", url_generador, width='stretch')
                
                st.info("Sube el calendario en formato imagen (PNG/JPG).")
                uploaded_cal = st.file_uploader(
                    "Subir imagen del Calendario",
                    type=["png", "jpg", "jpeg"],
                    key=f"cal_up_{practicaId}"
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
                if uploaded_cal:
                    if st.button("Guardar", key=f"btn_save_cal_{practicaId}"):
                        with st.spinner("Subiendo imagen..."):
                            original_name = uploaded_cal.name
                            if not original_name.lower().startswith("calendario"):
                                original_name = f"calendario_{original_name}"
                            temp_path = Path("/tmp") / f"CAL_{uuid.uuid4()}_{original_name}"
                            with open(temp_path, "wb") as f:
                                f.write(uploaded_cal.getbuffer())
                            upload_to_drive(str(temp_path), carpetaPractica, folder_name, original_name)
                            invalidate_runtime_caches()
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
                    
                    st.link_button("Abrir imagen completa", archivo_calendario.get('webViewLink'), width='stretch')
                else:
                    st.markdown(
                        """
                        <div style="border: 2px dashed #ccc; border-radius: 10px; height: 500px; display: flex; align-items: center; justify-content: center; color: #aaa;">
                            Esperando archivo de calendario (PNG/JPG)...
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
        elif rol_usuario != 'admin' or st.session_state["edit_disabled"]==True:   
            if archivo_calendario:
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
                    
                        st.link_button("Abrir imagen completa", archivo_calendario.get('webViewLink'), width='stretch')
            else:
                st.write("No han subido calendario aun")
        pass

def seccion_documentos(folder_name, alumno, practicaId):
    st.subheader("📎 Documentos")
    files, folderId = list_drive_files_cached(folder_name)
    if files:
        for f in files:
            fecha = f.get("modifiedTime", "")[:10]
            st.write(f"- [{f['name']}]({f['webViewLink']}) _(última modificación: {fecha})_")
    else:
        st.warning("No hay documentación subida.")
    if rol_usuario != 'tutor':
        uploader_version = st.session_state.get(f"uploader_version_{practicaId}",0)

        uploaded_files = st.file_uploader(
            "Subir archivos",
            type=["pdf", "doc", "docx", "odt", "jpg", "jpeg", "png"],
            accept_multiple_files=True,
            key=f"up_{practicaId}_{uploader_version}"
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
                    try:
                        total = len(uploaded_files)
                        st.info(f"Subiendo {total} archivo(s), por favor espera...")
                        for file in uploaded_files:
                                nuevo_nombre = archivoNombre(alumno['nombre'],alumno['apellido'],file.name)
                                temp = Path("/tmp") / f"{uuid.uuid4()}_{nuevo_nombre}"
                                with open(temp, "wb") as f:
                                    f.write(file.getbuffer())
                                upload_to_drive(str(temp), carpetaPractica, folder_name, nuevo_nombre)
                        st.session_state[f"uploader_version_{practicaId}"] = (uploader_version + 1)
                        list_drive_files_cached.clear()
                        st.success(f"Subido: {nuevo_nombre}")
                        st.rerun()
                        invalidate_runtime_caches()
                    except Exception as e:
                            logError(f"{type(e).__name__}: {str(e)}", "Practica - Subida de Archivos")
                            st.error(f"❌ Error al subir los archivos: {e}")

        
        pass

def mostrar_detalle_cancelada(p):
    st.set_page_config(page_title="Datos formación en Empresas", page_icon="🚀")
    if not p:
        st.error("Formación no encontrada.")
        return

    oferta = p.get("oferta_fp", {}) or {}
    empresa = p.get("empresas", {}) or {}
    alumno = p.get("alumnos", {}) or {}
    folder_name= folderNamePractica(alumno['nombre'],alumno['apellido'], alumno['dni'], empresa['nombre'])
    st.title(f"{alumno.get('nombre', '')} {alumno.get('apellido', '')} – {empresa.get('nombre', '')}")
    
    # Detalle expandido en modo estricto de lectura
    seccion_detalle_cancelado(alumno, empresa, p, oferta)
    st.divider( )

    st.write(f"**Estado de Formación:** `{p.get('status', '—')}`")
    st.write(f"**Fecha Inicio:** `{p.get('fecha_inicio', '—')}`")
    st.write(f"**Fecha Cancelación:** `{p.get('fecha_cancelacion', '—')}`")
    st.write(f"**Motivo:** `{p.get('motivo', '—')}`")
    st.divider( )


    seccion_planificacion_cancelado(folder_name, p)
    st.divider( )
    seccion_documentacion_cancelado(folder_name)

def seccion_detalle_cancelado(alumno, empresa, p, oferta):
    st.error(f"ℹ️ **Estado:** {p.get('status')} — **Motivo:** {p.get('motivo') or 'No especificado'}", icon="🚀")
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
        st.write(f"**Tutor Centro:** {p.get('tutor_centro') or 'Sin asignar'}")
        st.write(f"**Gestor:** {p.get('gestor') or 'Sin asignar'}")

def seccion_planificacion_cancelado(folder_name, p):
    st.subheader("📅 Planificación de Formaciones")

    archivo_calendario = None
    try:
        files = list_drive_files_cached(folder_name)
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

def seccion_documentacion_cancelado(folder_name):
    st.subheader("📎 Documentos Adjuntos")

    files, folderId = list_drive_files_cached(folder_name)

    if files:
        for f in files:
            fecha = f.get("modifiedTime", "")[:10]
            st.write(f"- [{f['name']}]({f['webViewLink']}) _(última modificación: {fecha})_")
    else:
        st.warning("No hay archivos.")

def mostrar_detalle():
    st.set_page_config(page_title="Datos formación en Empresas", page_icon="🚀")
    practicaId = st.session_state.practica_seleccionada
    p = next((x for x in practicas if x["id"] == practicaId), None)
    if not p:
        st.error("Formación no encontrada, intente cambiando el curso académico.")
        st.session_state.page = "lista"
        return
    if p.get("status") == estados[3]:
        mostrar_detalle_cancelada(p)
    else:
        p["oferta_fp"] = p.get("oferta_fp") or {}
        p["empresas"] = p.get("empresas") or {}
        p["alumnos"] = p.get("alumnos") or {}
        oferta = p["oferta_fp"]
        empresa = p["empresas"]
        alumno = p["alumnos"]
        folder_name= folderNamePractica(alumno['nombre'],alumno['apellido'], alumno['dni'], empresa['nombre'])
        tutor_actual = p.get("tutor") 
        tutorCentro_actual = p.get("tutor_centro") 
        st.title(f"{alumno['nombre']} {alumno['apellido']} – {empresa['nombre']}")
        st.session_state["edit_disabled"] = p.get("status") == estados[2]


        st.info(f"ℹ️ **Estado:** {p.get('status')}", icon="🚀")
        planificacionTab, seguimientoTab, documentacionTab = st.tabs(["Detalle Formación", "Seguimiento y Feedback", "Documentación"])
        if rol_usuario == 'tutor':
            with planificacionTab:
                seccion_detalle(alumno, empresa, p, oferta, gestores, tutores)
                seccion_planificacion(folder_name, p)
            with seguimientoTab:
                seccion_feedback_tutor(practicaId, p, tutor_actual, True)
            with documentacionTab:
                seccion_documentos(folder_name,alumno, practicaId)
        else:
            with planificacionTab:
                seccion_detalle(alumno, empresa, p, oferta, gestores, tutores)
                mostrar_anexos_practica(p)
                seccion_programar(p)
                seccion_planificacion(folder_name, p)
                seccion_gestion(p)
            with seguimientoTab:
                seccion_feedback_tutorCentro(practicaId, p, tutorCentro_actual)
                st.divider()
                seccion_feedback_tutor(practicaId, p, tutor_actual, True)
                st.divider()
                seccion_feedback_candidato(p, practicaId, forms)
            with documentacionTab:
                seccion_documentos(folder_name,alumno, practicaId)

   
# ------------------------------------------
# VOLVER SIN EXPERIMENTAL
# ------------------------------------------

    st.divider() 
    if st.button("⬅ Volver",type="primary"):
        st.session_state.page = "lista"
        st.rerun()

# ----------------------------------------------
# RENDER SEGÚN PÁGINA
# ----------------------------------------------

if st.session_state.page == "lista":
    mostrar_lista()
else:
    mostrar_detalle()
