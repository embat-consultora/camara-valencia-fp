import streamlit as st
import pandas as pd
from modules.data_base import (
    getEquals, getPracticas, upsert,asignarFechasFormsFeedback,get, upsertCustome, crearPractica
)
from page_utils import apply_page_config
from navigation import make_sidebar
from modules.grafico_helper import mostrar_fases
from datetime import datetime,timedelta
from modules.drive_helper import list_drive_files, upload_to_drive
from modules.forms_helper import file_size_bytes
from pathlib import Path
from modules.feedback_helper import render_feedback_card
import uuid
import json
from variables import (
    practicaTabla, tutoresTabla, practicaEstadosTabla,
    fasesPractica, faseColPractica, max_file_size, carpetaPractica,linkCalendar,feedbackResponseTabla,forms,gestoresTabla, feedbackFormsTabla, alumnosTabla,
    empresasTabla,tipoPracticas,formFieldsTabla,estadosAlumno,usuariosTabla,tutoresCentroTabla
)
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode, DataReturnMode
# ----------------------------------------------
# CONFIG
# ----------------------------------------------
apply_page_config()
make_sidebar()
st.set_page_config(page_title="Prácticas", page_icon="🚀")

now = datetime.now().isoformat()
st.title("🚀 Prácticas")

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
rol_usuario = st.session_state.get("rol")
# ----------------------------------------------
# FETCH FUNCTIONS
# ----------------------------------------------
def fetch_practicas_tutores():
    practicas = getPracticas(practicaTabla, {"status":"CONFIRMADA",})
    tutores = getEquals(tutoresTabla, {})
    tutoresCentro = getEquals(tutoresCentroTabla, {})
    return practicas, tutores,tutoresCentro

def handle_update(tabla, dni_o_id, campo_a_actualizar, columna_id, key_widget, label):
    nuevo_valor = st.session_state.get(key_widget)
    if nuevo_valor:
        try:
            payload = {
                columna_id: dni_o_id, 
                campo_a_actualizar: nuevo_valor
            }
            upsert(tabla, payload, keys=[columna_id])
            st.toast(f"✅ {label} actualizado a: {nuevo_valor}")
        except Exception as e:
            st.error(f"Error al actualizar {label}: {e}")
            
# ----------------------------------------------
# BOTÓN REFRESCAR
# ----------------------------------------------
col_refresh, col_volver = st.columns([1, 0.15])
with col_refresh:
    if st.button("🔄 Actualizar", key="btn_refresh"):
        st.session_state["force_reload"] = True
        st.rerun()

# ----------------------------------------------
# CARGA DE DATOS
# ----------------------------------------------
def load_data(force=False):
    if force or "data_loaded" not in st.session_state or st.session_state.get("force_reload"):
        practicas, tutores, tutoresCentro = fetch_practicas_tutores()
        feedback =get(feedbackResponseTabla)
        estados = getEquals(practicaEstadosTabla, {})
        estados_map = {e["practicaId"]: e for e in estados}
        user_email = st.session_state.get("username")
        gestores = get(gestoresTabla)
        if rol_usuario == "gestor":
            gestorDatos = [g for g in gestores if g.get("email") == user_email]
            gestorNombre = gestorDatos[0].get("nombre")
            if gestorDatos:
                practicas = [
                p for p in practicas 
                if p.get("alumnos") is not None and p.get("alumnos").get("gestor") == gestorNombre
            ]
            else:
                practicas = []
        if rol_usuario == "tutor":

            tutorDatos = [t for t in tutores if t.get("email") == user_email]
            tutorNombre = tutorDatos[0].get("nombre")
            if tutorDatos:
                practicas = [
                p for p in practicas 
                if p.get("tutor") is not None and p.get("tutor") == tutorNombre
            ]
            else:
                practicas = []
        if rol_usuario == "tutorCentro":
            tutorCentroDatos = [t for t in tutoresCentro if t.get("email") == user_email]
            tutorCentroNombre = tutorCentroDatos[0].get("nombre")
            if tutorCentroDatos:
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
        st.session_state["estados"] = estados_map
        st.session_state["feedbacks"] = feedback
        st.session_state["data_loaded"] = True
        st.session_state["force_reload"] = False

load_data()

practicas = st.session_state["practicas"]
tutores = st.session_state["tutores"]
gestores =  st.session_state["gestores"]
tutoresCentro =st.session_state["tutorCentro"]

##--- DIALOG
@st.dialog("Finalización de Práctica")
def dialog_fecha_fin(practica_id, email_alumno):
    st.write(f"Por favor, indica cuándo finalizará la práctica:")
    
    # Input de fecha
    fecha_fin = st.date_input("Fecha de finalización prevista", value=datetime.now().date() + timedelta(days=90))
    
    if st.button("Confirmar", type="primary"):
        asignarFechasFormsFeedback(int(practica_id), datetime.now().date(), email_alumno, fecha_fin)
        st.success("Fechas programadas correctamente.")
        st.toast("✅  La práctica ha pasado a estado INICIADA")

        st.rerun()
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
    tabs_visibles = ["📋 Listado de Prácticas"]

    if rol_usuario == 'admin':
        tabs_visibles.extend(["📃 Anexos", "📊 Dashboard de Feedback", "⚡️ Carga Rápida"])
    elif rol_usuario in ['gestor', 'tutor', 'tutorCentro']:
        tabs_visibles.append("📊 Dashboard de Feedback")
   
    tabs = st.tabs(tabs_visibles)
    with tabs[0]:
        mostrar_lista_practicas()
    
    if "📃 Anexos" in tabs_visibles:
        idx = tabs_visibles.index("📃 Anexos")
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
        if not practicas:
            st.info("No tienes prácticas asignadas aun.")
            return
        data_for_grid = []
        for p in practicas:
            pid = p["id"]
            # Lógica de estados simplificada para el grid
            estados_p = st.session_state["estados"].get(pid, {})
            estado_actual = "Pendiente"
            for fase in fasesPractica:
                    columna_fase = faseColPractica[fase]
                    if estados_p.get(columna_fase):
                        estado_actual = fase

            data_for_grid.append({
                "ID": pid,
                "Alumno": f"{p.get('alumnos', {}).get('nombre')} {p.get('alumnos', {}).get('apellido')}",
                "Empresa": p.get('empresas', {}).get('nombre'),
                "Estado": estado_actual,
                "Ciclo": p.get('ciclo_formativo', '—'),
                "Gestor": p.get('alumnos', {}).get('gestor', 'Sin asignar')
            })

        df = pd.DataFrame(data_for_grid)

        if df.empty:
            st.info("No hay prácticas asignadas aun")
            #return

        # 2. Configurar AgGrid
        gb = GridOptionsBuilder.from_dataframe(df)
        gb.configure_selection('single', use_checkbox=False) # Selección de fila completa
        gb.configure_column("ID", hide=True) # Ocultamos el ID técnico
        gb.configure_grid_options(domLayout='normal')
        
        # Tip de experto: Hacer que las columnas se ajusten automáticamente
        gridOptions = gb.build()

        st.write("Selecciona una fila para ver el detalle:")
        
        # 3. Renderizar el Grid
        response = AgGrid(
            df,
            gridOptions=gridOptions,
            update_mode=GridUpdateMode.SELECTION_CHANGED, # Se dispara al hacer click
            data_return_mode=DataReturnMode.FILTERED_AND_SORTED,
            fit_columns_on_grid_load=True,
            theme='streamlit', # O 'balham', 'alpine'
            height=400,
            allow_unsafe_縫tml=True
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

def mostrar_carga_rapida():
    st.info("Utiliza esta sección para dar de alta rápidamente una empresa y un alumno que no existen en la base de datos y vincularlos en una práctica.")

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

    # 3. CONFIGURACIÓN DE PRÁCTICA Y CICLO
    st.subheader("📋 Configuración de la Práctica")
    col_p1, col_p2 = st.columns(2)

    # Obtenemos los tipos de práctica de tus variables
    new_alu_tipo = col_p1.selectbox(
        "Tipo de Práctica", 
        options=tipoPracticas, 
        key="qr_alu_tipo"
    )

    # Lógica de Ciclos Formativos (Basada en tu código de alumnos)
    form_fields = getEquals(formFieldsTabla, {"category": "Alumno", "type": "Opciones"})
    ciclo_field = next((f for f in form_fields if f["columnName"] == "ciclo_formativo"), None)
    pref_field = next((f for f in form_fields if f["columnName"] == "preferencias_fp"), None)

    ciclos_opts = json.loads(ciclo_field["options"]) if ciclo_field else []
    prefs_opts_dict = json.loads(pref_field["options"]) if pref_field else {}

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

    # 4. BOTÓN DE ACCIÓN
    if st.button("🚀 Guardar y Vincular Práctica", use_container_width=True):
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
                    usuario = upsertCustome(usuariosTabla, {
                                "email": new_emp_cif,
                                "password": new_emp_cif,
                                "rol": "empresa",
                            }, keys=["email"])
                    # B. Alta Alumno
                    upsert(alumnosTabla, {
                        "dni": new_alu_dni,
                        "nombre": new_alu_nombre,
                        "apellido": new_alu_apellido,
                        "email_alumno": new_alu_email,
                        "tipoPractica": new_alu_tipo,
                        "ciclo_formativo": new_alu_ciclo,
                        "preferencias_fp": new_alu_pref,
                        "estado": estadosAlumno[1]
                    }, keys=["dni"])

                    # C. Crear la Práctica (Vincular)
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
                        oferta_id=None
                    )

                    st.success(f"✅ ¡Éxito! Práctica creada entre {new_emp_nombre} y {new_alu_nombre}.")
                    st.success(f"✅ Se ha creado un usuario y contraseña para la empresa - usuario: {new_emp_cif} password: {new_emp_cif}")

                except Exception as e:
                    st.error(f"❌ Error en el proceso: {str(e)}")

def mostrar_anexos():
    if not practicas:
        st.info("No tienes prácticas asignadas aun.")
        return

    # 1. Preparación de datos (Respetando TODOS tus campos y lógicas)
    data_for_grid = []
    for p in practicas:
        pid = p["id"]
        
        # Lógica de estados original
        estados_p = st.session_state.get("estados", {}).get(pid, {})
        estado_actual = "Pendiente"
        for fase in fasesPractica:
            columna_fase = faseColPractica[fase]
            if estados_p.get(columna_fase):
                estado_actual = fase

        # TRUCO MAESTRO: Convertimos el NULL (None) de Supabase en False
        # Si no hacemos esto, el checkbox de Streamlit no se dibuja bien.
        data_for_grid.append({
            "ID": pid,
            "Alumno": f"{p.get('alumnos', {}).get('nombre', '')} {p.get('alumnos', {}).get('apellido', '')}",
            "Empresa": p.get('empresas', {}).get('nombre', '—'),
            "Estado": estado_actual,
            "Ciclo": p.get('ciclo_formativo', '—'),
            # Usamos 'is True' para que solo sea True si es explícito en la BD
            "Creado": True if p.get('anexos_creados') is True else False,
            "Enviados": True if p.get('anexos_enviados') is True else False,
            "Firmados": True if p.get('anexos_firmados') is True else False,
            "DOC SAO": True if p.get('doc_sao_entregada') is True else False
        })

    # 2. Creamos el DataFrame
    df_original = pd.DataFrame(data_for_grid)

    st.subheader("📋 Gestión de Anexos")

    # 3. El Editor con KEY DINÁMICA (para que refresque al guardar)
    if "df_key" not in st.session_state:
        st.session_state.df_key = 0

    edited_df = st.data_editor(
        df_original,
        key=f"editor_anexos_{st.session_state.df_key}",
        hide_index=True,
        use_container_width=True,
        # Bloqueamos lo que no queremos que toquen
        disabled=["ID", "Alumno", "Empresa", "Estado", "Ciclo"],
        column_config={
            "ID": None,
            "Creado": st.column_config.CheckboxColumn("Creado"),
            "Enviados": st.column_config.CheckboxColumn("Enviados"),
            "Firmados": st.column_config.CheckboxColumn("Firmados"),
            "DOC SAO": st.column_config.CheckboxColumn("DOC SAO"),
        }
    )

    # 4. Lógica de Guardado (Capturando cambios del session_state)
    state_key = f"editor_anexos_{st.session_state.df_key}"
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
                st.session_state["force_reload"] = True 
                st.rerun()

def mostrar_dashboard():
    st.subheader("📊 Seguimiento de Feedback")
    
    col_f1, col_f2 = st.columns(2)
    with col_f1:
        fecha_inicio_filtro = st.date_input("Desde", value=datetime(2025, 9, 1))
    with col_f2:
        fecha_fin_filtro = st.date_input("Hasta", value=datetime(2026, 6, 30))

    all_feedback_forms = get(feedbackFormsTabla) 
    ids_permitidos = [p["id"] for p in practicas]
    all_feedback_forms = [f for f in all_feedback_forms if f.get("practica_id") in ids_permitidos
]
    if not all_feedback_forms:
        st.info("No hay datos de envíos de feedback.")
        return

    # Convertir a DataFrame para filtrar fácil
    df_fb = pd.DataFrame(all_feedback_forms)
    df_fb['fecha_envio'] = pd.to_datetime(df_fb['fecha_envio']).dt.date
    
    # Filtrar por rango de fecha
    mask = (df_fb['fecha_envio'] >= fecha_inicio_filtro) & (df_fb['fecha_envio'] <= fecha_fin_filtro)
    df_filtrado = df_fb.loc[mask]

    # 3. Métricas Principales (KPIs)
    # Tipos: feedback_inicial, feedback_adaptacion, feedback_cierre
    total_enviados = len(df_filtrado[df_filtrado['estado'] == 'enviado'])
    total_respondidos = len(df_filtrado[df_filtrado['fecha_respuesta'].notna()])
    pendientes = total_enviados - total_respondidos

    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Total Enviados", total_enviados)
    
    # Desglose por tipo (usando tus constantes de forms o strings)
    for i, tipo in enumerate(['feedback_inicial', 'feedback_adaptacion', 'feedback_cierre']):
        count = len(df_filtrado[(df_filtrado['tipo_form'] == tipo) & (df_filtrado['estado'] == 'enviado')])
        if i == 0: m2.metric("Acogida", count)
        if i == 1: m3.metric("Adaptación", count)
        if i == 2: m4.metric("Cierre", count)

    st.divider()

    # 4. Alumnos Pendientes de Respuesta
    col_p1, col_p2 = st.columns([2, 1])
    
    with col_p1:
        st.write("### ⏳ Alumnos que no han respondido")
        # Filtramos los que se enviaron pero no tienen fecha_respuesta
        df_pendientes = df_filtrado[(df_filtrado['estado'] == 'enviado') & (df_filtrado['fecha_respuesta'].isna())]
        if not df_pendientes.empty:
            listado_morosos = []
            for _, row in df_pendientes.iterrows():

                practica = next((x for x in practicas if x["id"] == row['practica_id']), None)
                if practica:
                    alumno_nom = f"{practica['alumnos']['nombre']} {practica['alumnos']['apellido']}"
                    listado_morosos.append({
                        "Alumno": alumno_nom,
                        "Email": row['email_destino'],
                        "Formulario": row['tipo_form'].replace('_', ' ').title(),
                        "Fecha Envío": row['fecha_envio']
                    })
                    st.table(pd.DataFrame(listado_morosos))
                else:
                    st.success("¡Todos los alumnos han respondido a sus formularios o no se han enviado aun!")
        else:
            st.success("¡Todos los alumnos han respondido a sus formularios o no se han enviado aun!")

    with col_p2:
        st.write("### ⚡ Acciones")
        st.info("Enviar recordatorio por correo a todos los alumnos pendientes de esta lista.")
        
        if st.button("🔔 Enviar Recordatorio Masivo", type="primary", use_container_width=True):
            if not df_pendientes.empty:
                with st.spinner("Ejecutando AppScript..."):
                    # Aquí llamarías a tu función de AppScript pasándole los emails
                    # Ejemplo: trigger_appscript_reminder(df_pendientes['email_destino'].tolist())
                    st.success(f"Recordatorios enviados a {len(df_pendientes)} alumnos.")
            else:
                st.warning("No hay nadie a quien reclamar.")

def seccion_detalle(alumno, empresa, p, oferta, gestores, tutores):
    with st.expander("Detalle"):
        col1, col2 = st.columns(2)
        with col1:
            st.write(f"**Alumno:** {alumno['nombre']} {alumno['apellido']}")
            st.write(f"**DNI:** {alumno['dni']}")
            st.write(f"**Email:** {alumno['email_alumno']}")
            st.write(f"**Ciclo:** {p.get('ciclo_formativo', '—')}")
            area = p.get("area") or "No especificado"
            st.write(f"**Área:** {area}")     
            proyecto = p.get("proyecto") or "No especificado"
            st.write(f"**Proyecto:** {proyecto}")      

        with col2:
            st.write(f"**Empresa:** {empresa['nombre']}")
            st.write(f"**CIF:** {empresa['CIF']}")
            direccion = oferta.get("direccion_empresa") or "No especificado"
            st.write(f"**Dirección práctica:** {direccion}")
            localidad = oferta.get("localidad_empresa") or "No especificado"
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
            if rol_usuario != 'admin':
                st.write(f"**Gestor:** {gestor_actual}")
            else:
                st.selectbox(
                    "**Gestor Asignado**",
                    options=lista_nombres_gestores,
                    index=indice_gestor,
                    key=clave_gestor,
                    on_change=handle_update,
                    # Pasamos la KEY en lugar del valor
                    args=(alumnosTabla, alumno['dni'], "gestor", "dni", clave_gestor, "Gestor")
                )
        
        lista_nombres_tutores = [g["nombre"] for g in tutores]
        if "No asignado" not in lista_nombres_tutores:
            lista_nombres_tutores.insert(0, "No asignado")
        tutor_actual = p.get("tutor") 
        indice_tutor = lista_nombres_tutores.index(tutor_actual) if tutor_actual in lista_nombres_tutores else 0
        with colTutor:
            clave_tutor = f"tutor_{alumno['id']}"
            if rol_usuario != 'admin':
                st.write(f"**Tutor Empresa:** {tutor_actual}")
            else:
                st.selectbox(
                    "**Tutor Empresa**",
                    options=lista_nombres_tutores,
                    index=indice_tutor,
                    key=clave_tutor,
                    on_change=handle_update,
                    args=(practicaTabla, p['id'], "tutor", "id", clave_tutor, "Tutor")
                )
        lista_nombres_tutoresCentro = [g["nombre"] for g in tutoresCentro]
        if "No asignado" not in lista_nombres_tutoresCentro:
            lista_nombres_tutoresCentro.insert(0, "No asignado")
        tutorc_actual = p.get("tutor_centro") 
        indice_tutorc = lista_nombres_tutoresCentro.index(tutorc_actual) if tutorc_actual in lista_nombres_tutoresCentro else 0
        with colTCentro:
            clave_tutorc = f"tutor_centro_{alumno['id']}"
            if rol_usuario != 'admin':
                st.write(f"**Tutor Centro:** {tutorc_actual}")
            else:
                st.selectbox(
                    "**Tutor Centro**",
                    options=lista_nombres_tutoresCentro,
                    index=indice_tutorc,
                    key=clave_tutorc,
                    on_change=handle_update,
                    args=(practicaTabla, p['id'], "tutor_centro", "id", clave_tutor, "TutorCentro")
                )

        pass

def seccion_seguimiento(practicaId, fasesPractica, faseColPractica, empresa, alumno):
    st.subheader("Seguimiento")
    estado_actual = st.session_state["estados"].get(practicaId, {})
    
    mostrar_fases(fasesPractica, faseColPractica, estado_actual)
    cols = st.columns(len(fasesPractica))
    if rol_usuario != 'tutor':
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

                upsert(practicaEstadosTabla, {"practicaId": int(practicaId), col: new_value}, keys=["practicaId"])
                estado_actual[col] = new_value

                if fase == fasesPractica[2] and checked:
                    payload_practica = {
                            "id": int(practicaId),
                            "fecha_inicio": new_value,
                        }
                    upsert(practicaTabla, payload_practica, keys=["id"])
                    dialog_fecha_fin(practicaId, alumno['email_alumno'])
                st.session_state["estados"][practicaId] = estado_actual
                st.toast(f"✅  Estado actualizado")
    
    
    feedbacks_forms = getEquals(feedbackFormsTabla, {"practica_id": practicaId})
    fechas = {f['tipo_form']: datetime.strptime(f['fecha_envio'], "%Y-%m-%d").strftime("%d/%m/%Y") for f in feedbacks_forms}
    if(estado_actual.get("en_progreso") is not None):
        st.info(f"ℹ️ **Estado:** Pasantía Iniciada: {estado_actual.get("en_progreso")}", icon="🚀")

        with st.container(border=True):
            st.markdown(f"""
            **Próximo Hito:**
            * 📅 **Envio Feedback Acogida:** : {fechas.get('feedback_inicial', '--')}
            * 🕒 **Envio Feedback Adaptación:** {fechas.get('feedback_adaptacion', '--')}
            * ⏲️ **Envio Feedback Cierre:** {fechas.get('feedback_cierre', '--')}
            """)
    pass

def seccion_feedback_candidato(practicaId, forms):
    st.subheader("¿Cómo se siente el candidato?")
    feedbacks_db = getEquals(feedbackResponseTabla, {"practica_id": practicaId})
    st.write(f"**Número de feedbacks enviados:** {len(feedbacks_db)}")
    progreso_feedback = {
        forms[0]: None,
        forms[1]: None,
        forms[2]: None,
    }

    for f in feedbacks_db:
        tipo = f["respuestas_json"].get("tipo")
        if tipo in progreso_feedback:
            progreso_feedback[tipo] = f["respuestas_json"]

    # 3. Crear las columnas y mostrar las cards
    col_ini, col_ada,col_cie = st.columns(3)

    with col_ini:
        render_feedback_card(progreso_feedback[forms[0]], "Acogida")

    with col_ada:
        render_feedback_card(progreso_feedback[forms[1]], "Adaptación")

    with col_cie:
        render_feedback_card(progreso_feedback[forms[2]], "Cierre")
    pass

def seccion_feedback_tutor(practicaId, p, tutor_actual):
    st.subheader("Seguimiento del Tutor")

    historial_feedback = p.get("feedback_tutor")
    if not isinstance(historial_feedback, list):
        historial_feedback = []

    # 2. ESPACIO PARA NUEVO FEEDBACK (Solo para Tutores)
    if rol_usuario == 'tutor':
        with st.container(border=True):
            st.markdown("##### Añadir nueva observación")
            nuevo_comentario = st.text_area(
                "Describe el progreso del alumno hoy:",
                placeholder="Ej: El alumno ha empezado a manejar las herramientas de diseño con autonomía...",
                key=f"input_fb_{practicaId}"
            )
            
            if st.button("💾 Publicar Comentario", use_container_width=True):
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
        st.markdown("##### Historial de observaciones")
        
        # Mostramos de más reciente a más antiguo para que lo último esté arriba
        for fb in reversed(historial_feedback):
            with st.chat_message("user", avatar="👨‍🏫"):
                st.markdown(f"**{fb['tutor']}** - <span style='color:gray; font-size:0.8rem;'>{fb['fecha']}</span>", unsafe_allow_html=True)
                st.write(fb['mensaje'])
    else:
        st.info("No hay feedback registrado todavía en esta práctica.")
    pass

def seccion_planificacion(alumno, empresa, practicaId):
        st.subheader("📅 Planificación de Prácticas")
        folder_name = f"{alumno['apellido']}_{alumno['nombre']}_{alumno['dni']}_practica_{empresa['nombre']}".strip()
        files = list_drive_files(folder_name)
        archivo_calendario = next((f for f in files[0] if "calendario" in f['name']), None)
        
        if rol_usuario == 'admin':
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
                    st.markdown(
                        """
                        <div style="border: 2px dashed #ccc; border-radius: 10px; height: 500px; display: flex; align-items: center; justify-content: center; color: #aaa;">
                            Esperando archivo de calendario (PNG/JPG)...
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
        if rol_usuario != 'admin':   
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
                    
                        st.link_button("Abrir imagen completa en Drive", archivo_calendario.get('webViewLink'), use_container_width=True)
            else:
                st.write("No han subido calendario aun")
        pass

def seccion_documentos(alumno, empresa, practicaId):
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
                        extension = Path(file.name).suffix
                        nombre_alumno_limpio = f"{alumno['nombre']}_{alumno['apellido']}".replace(" ", "_")
                        nuevo_nombre = f"{nombre_alumno_limpio}_{file.name}"
                        temp = Path("/tmp") / f"{uuid.uuid4()}_{nuevo_nombre}"
                        with open(temp, "wb") as f:
                            f.write(file.getbuffer())
                        upload_to_drive(str(temp), carpetaPractica, folder_name, nuevo_nombre)
                        st.success(f"Subido: {nuevo_nombre}")


    pass

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
    tutor_actual = p.get("tutor") 
    st.title(f"{alumno['nombre']} {alumno['apellido']} – {empresa['nombre']}")
    if rol_usuario == 'tutor':
        seccion_detalle(alumno, empresa, p, oferta, gestores, tutores)
        st.divider()
        seccion_feedback_tutor(practicaId, p, tutor_actual)
        st.divider()
        seccion_planificacion(alumno,empresa, practicaId)
        st.divider()
        seccion_seguimiento(practicaId, fasesPractica, faseColPractica,empresa, alumno)
        st.divider()
        seccion_feedback_candidato(practicaId, forms)
        # Los tutores quizás no ven la sección de documentos (según tu código previo)
        
    else:
        # ORDEN ADMIN/GESTOR: Detalle -> Seguimiento -> Feedback Tutor -> Feedback Candidato -> Documentos
        seccion_detalle(alumno, empresa, p, oferta, gestores, tutores)
        st.divider()
        seccion_seguimiento(practicaId, fasesPractica, faseColPractica,empresa, alumno)
        st.divider()
        seccion_planificacion(alumno,empresa, practicaId)
        st.divider()
        seccion_feedback_tutor(practicaId, p, tutor_actual)
        st.divider()
        seccion_feedback_candidato(practicaId, forms)
        st.divider()
        seccion_documentos(alumno, empresa, practicaId)

   
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

