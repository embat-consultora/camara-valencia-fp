import streamlit as st
import pandas as pd
from modules.data_base import getEqual, get_alumnos_con_practicas_consolidado, getOfertasTabla, guardar_cambios_alumnos, getGestores, updateOfertasTabla, updateGestores, getEmpresas
from page_utils import apply_page_config
from navigation import make_sidebar
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode, DataReturnMode, JsCode
from datetime import datetime, timedelta
from variables import gestoresTabla
# Configuración inicial
apply_page_config()
make_sidebar()

# --- LÓGICA DE USUARIO (Simulada, aquí extraes tus datos de sesión) ---
rol_usuario = st.session_state.get("rol") 
email_usuario = st.session_state.get("username")

st.title("🚀 Panel de Gestión de Prácticas FP")

# 1. Definimos qué pestañas se muestran según el rol
nombres_tabs = ["🎓 Alumnos", "🏢 Ofertas por Ciclo"]
if rol_usuario == "admin":
    nombres_tabs.append("⚙️ Configuración")

tabs = st.tabs(nombres_tabs)

# Asignamos las pestañas a variables para facilitar el acceso
tab_alumnos = tabs[0]
tab_ofertas = tabs[1]
if rol_usuario == "admin":
    tab_config = tabs[2]

# --- TAB ALUMNOS ---
with tab_alumnos:
    df_raw = get_alumnos_con_practicas_consolidado()
    
    # 1. Obtener lista de gestores para el desplegable del Grid
    try:
        df_gestores_lista = getGestores()
        # Solo gestores activos para asignar
        nombres_gestores = df_gestores_lista[df_gestores_lista['activo'] == True]['nombre'].tolist()
    except:
        nombres_gestores = []

    # --- FILTRO POR GESTOR (Visualización) ---
    if rol_usuario == "gestor":
        
        if 'gestor' in df_raw.columns:
            gestorDb = getEqual(gestoresTabla, 'email', email_usuario)
            df_raw = df_raw[df_raw['gestor'] == gestorDb[0]['nombre']]
        else:
            st.warning("No se encontró columna de asignación para filtrar tus alumnos.")

    df_empresas_raw = getEmpresas()
    lista_empresas_db = ["⚠️ SIN ASIGNAR"] + df_empresas_raw["nombre"].tolist()
    mapa_nombres_id = dict(zip(df_empresas_raw['nombre'], df_empresas_raw['CIF']))

    if not df_raw.empty:
        def crear_acronimo(nombre):
            if not nombre or pd.isna(nombre): return ""
            palabras = [w for w in nombre.split() if len(w) > 2 or w.isupper()]
            return "".join([w[0].upper() for w in palabras])

        df_raw['ciclo_acronimo'] = df_raw['ciclo_formativo'].apply(crear_acronimo)

        cols_visibles = [
            "ciclo_acronimo", "apellido", "nombre", "horas_totales", 
            "nombre_empresa", "gestor", "comentarios_centro", "anexos_creados", 
            "anexos_enviados", "anexos_firmados", "doc_sao_entregada", "observaciones_seguimiento"
        ]
        
        cols_tecnicas = ["dni", "ciclo_formativo", "oferta_id", "ciclos_info", "cupos_disponibles"]
        cols_finales = cols_visibles + [c for c in cols_tecnicas if c in df_raw.columns]
        df_display = df_raw[cols_finales].copy()

        gb = GridOptionsBuilder.from_dataframe(df_display)
        gb.configure_default_column(editable=True, filter=True, resizable=True)

        si_no_js = JsCode("""
            function(params) {
                if (params.value === true || params.value === 'true') return '✅ SÍ';
                if (params.value === false || params.value === 'false') return '';
                return params.value;
            }
        """)

        gb.configure_column("ciclo_acronimo", headerName="Ciclo", pinned='left', width=80, editable=False)
        gb.configure_column("apellido", headerName="Apellidos", width=150)
        gb.configure_column("nombre", headerName="Nombre", width=120)
        
        # --- COLUMNA GESTOR CON DESPLEGABLE ---
        gb.configure_column("gestor", 
            headerName="Gestor", 
            width=120,
            cellEditor='agSelectCellEditor',
            cellEditorParams={'values': nombres_gestores},
            # Solo el admin puede reasignar gestores, o el gestor si quieres permitirlo
            editable=(rol_usuario == "admin") 
        )

        gb.configure_column("horas_totales", headerName="Hrs", width=70)
        gb.configure_column("nombre_empresa", 
            headerName="Empresa",
            cellEditor='agSelectCellEditor',
            cellEditorParams={'values': lista_empresas_db},
            cellStyle=JsCode("""
                function(params) {
                    if (params.value === '⚠️ SIN ASIGNAR') return {'backgroundColor': '#d63031', 'color': 'white', 'fontWeight': 'bold'};
                    return {'backgroundColor': '#55efc4', 'color': 'black'};
                }
            """),
            width=200
        )

        checkbox_cols = ["anexos_creados", "anexos_enviados", "anexos_firmados", "doc_sao_entregada"]
        for col in checkbox_cols:
            gb.configure_column(col, cellRenderer='checkboxRenderer', valueFormatter=si_no_js, width=100)

        for col in cols_tecnicas:
            if col in df_display.columns:
                gb.configure_column(col, hide=True)

        gridOptions = gb.build()

        grid_response = AgGrid(
            df_display,
            gridOptions=gridOptions,
            allow_unsafe_jscode=True,
            update_mode=GridUpdateMode.MODEL_CHANGED,
            theme='balham',
            height=600,
            key="grid_alumnos_master_v1"
        )
        
        if st.button("💾 Guardar Cambios Alumnos", type="primary", use_container_width=True):
            df_grid = grid_response['data']
            with st.spinner("Guardando datos"):
                try:
                    # Esta función debe estar preparada para recibir la columna 'gestor' y guardarla en la tabla alumnos
                    guardar_cambios_alumnos(df_grid, df_display, mapa_nombres_id)
                    st.success("✅ ¡Cambios guardados correctamente!")
                    st.rerun()
                except Exception as e:
                    st.error(f"Error técnico: {e}")

# --- TAB OFERTAS (Todo el código igual, visible para ambos) ---
with tab_ofertas:
    try:
        df_gestores_all = getGestores()
        gestores_activos = df_gestores_all[df_gestores_all['activo'] == True]['nombre'].tolist()
    except:
        st.error("No se pudo cargar la lista de gestores.")
        gestores_activos = []
        
    df_raw_ofertas = getOfertasTabla() # Renombrado para no chocar con df_raw de alumnos
    
    if df_raw_ofertas.empty:
        st.info("No hay ofertas registradas.")
    else:
        rows_list = []
        for _, record in df_raw_ofertas.iterrows():
            ciclos_info = record.get('ciclos_formativos', {}) or {}
            puestos_info = record.get('puestos', {}) or {}
            empresa = record.get('empresas', {}) or {}
            seguimiento_full = record.get('seguimiento_gestores', {}) or {}
            tutores_full = record.get('tutores_por_puesto', {}) or {}
            
            for nombre_ciclo, datos_alumnos in ciclos_info.items():
                areas_del_ciclo = puestos_info.get(nombre_ciclo, [{"area": "General", "proyecto": ""}])
                for area_item in areas_del_ciclo:
                    nombre_area = area_item.get('area', 'General')
                    seg_especifico = seguimiento_full.get(nombre_ciclo, {}).get(nombre_area, {})
                    tutor_especifico = tutores_full.get(nombre_ciclo, {}).get(nombre_area, {})

                    fila = {
                        "id": record.get('id'),
                        "Empresa": empresa.get('nombre', 'N/A'),
                        "Teléfono": empresa.get('telefono', ''),
                        "Dirección": empresa.get('direccion', ''),
                        "Localidad": empresa.get('localidad', ''),
                        "Ciclo": nombre_ciclo,
                        "Alumnos Pedidos": datos_alumnos.get('alumnos', 0),
                        "Área": nombre_area,
                        "Proyecto": area_item.get('proyecto', ''),
                        "Requisitos": record.get('requisitos', ''),
                        "Contrato": record.get('contrato', ''),
                        "Vehículo": record.get('vehiculo', ''),
                        "Nombre Tutor": tutor_especifico.get('nombre', record.get('nombre_tutor', '')),
                        "Email Tutor": tutor_especifico.get('email', record.get('email_tutor', '')),
                    }
                    for gestor in gestores_activos:
                        fila[f"Prop. {gestor}"] = seg_especifico.get(gestor, "")
                    rows_list.append(fila)

        df_final = pd.DataFrame(rows_list)
        lista_ciclos = sorted(df_final['Ciclo'].unique())
        if lista_ciclos:
            sub_tabs = st.tabs(lista_ciclos)
            for i, nombre_ciclo in enumerate(lista_ciclos):
                with sub_tabs[i]:
                    df_ciclo_tab = df_final[df_final['Ciclo'] == nombre_ciclo].reset_index(drop=True)
                    col_config_oferta = {
                        "id": None, 
                        "Empresa": st.column_config.TextColumn(disabled=True),
                        "Teléfono": st.column_config.TextColumn(disabled=True),
                        "Localidad": st.column_config.TextColumn(disabled=True),
                        "Alumnos Pedidos": st.column_config.NumberColumn("Cant.", disabled=True),
                        "Área": st.column_config.TextColumn(disabled=True),
                    }
                    for g in gestores_activos:
                        col_config_oferta[f"Prop. {g}"] = st.column_config.TextColumn(f"🙋 {g}")

                    edited_data = st.data_editor(
                        df_ciclo_tab,
                        column_config=col_config_oferta,
                        key=f"editor_ofertas_{nombre_ciclo}",
                        use_container_width=True,
                        num_rows="fixed",
                        hide_index=True
                    )

                    if st.button(f"💾 Guardar Cambios {nombre_ciclo}", key=f"btn_save_{nombre_ciclo}"):
                        cambios = st.session_state[f"editor_ofertas_{nombre_ciclo}"].get("edited_rows", {})
                        if cambios:
                            df_db_actual = getOfertasTabla() 
                            for row_idx, nuevos_valores in cambios.items():
                                fila_editor = df_ciclo_tab.iloc[int(row_idx)]
                                id_oferta = fila_editor['id']
                                area_actual = fila_editor['Área']
                                registro_db = df_db_actual[df_db_actual['id'] == id_oferta].iloc[0]
                                seguimiento_db = registro_db.get('seguimiento_gestores', {}) or {}
                                tutores_db = registro_db.get('tutores_por_puesto', {}) or {}

                                if nombre_ciclo not in seguimiento_db: seguimiento_db[nombre_ciclo] = {}
                                if area_actual not in seguimiento_db[nombre_ciclo]: seguimiento_db[nombre_ciclo][area_actual] = {}
                                if nombre_ciclo not in tutores_db: tutores_db[nombre_ciclo] = {}
                                if area_actual not in tutores_db[nombre_ciclo]: tutores_db[nombre_ciclo][area_actual] = {}

                                for g in gestores_activos:
                                    col_name = f"Prop. {g}"
                                    val = nuevos_valores.get(col_name, fila_editor.get(col_name, ""))
                                    seguimiento_db[nombre_ciclo][area_actual][g] = val

                                seguimiento_db[nombre_ciclo][area_actual]['tutor'] = nuevos_valores.get("Nombre Tutor", fila_editor["Nombre Tutor"])
                                seguimiento_db[nombre_ciclo][area_actual]['email'] = nuevos_valores.get("Email Tutor", fila_editor["Email Tutor"])

                                update_payload = {
                                    "seguimiento_gestores": seguimiento_db,
                                    "tutores_por_puesto": tutores_db,
                                    "requisitos": nuevos_valores.get("Requisitos", fila_editor["Requisitos"]),
                                    "contrato": nuevos_valores.get("Contrato", fila_editor["Contrato"]),
                                    "vehiculo": nuevos_valores.get("Vehículo", fila_editor["Vehículo"]),
                                }
                                try:
                                    updateOfertasTabla(update_payload, id_oferta)
                                    st.success(f"Actualizada oferta {id_oferta}")
                                except Exception as e:
                                    st.error(f"Error: {e}")
                            st.rerun()

# --- TAB CONFIGURACIÓN (Solo Admin) ---
if rol_usuario == "admin":
    with tab_config:
        st.subheader("Configuración de Gestores")
        df_gestores = getGestores()
        edited_g = st.data_editor(
                df_gestores,
                column_config={"id": None, "password": None, "nombre": "Nombre", "email": "Email", "activo": "Visible"},
                num_rows="dynamic",
                key="editor_gestores",
                use_container_width=True
            )
        if st.button("Actualizar Gestores"):
            cambios = st.session_state["editor_gestores"]
            if cambios["edited_rows"] or cambios["added_rows"] or cambios["deleted_rows"]:
                try:
                    for row in cambios["added_rows"]:
                        nombre = row.get("nombre", "Sin Nombre").strip()
                        email = row.get("email", "").strip()
                        if not email or "@" not in email:
                            st.error(f"Email inválido para {nombre}"); st.stop()
                        anio_actual = datetime.now().year
                        password_auto = f"{nombre.replace(' ', '')}{anio_actual}"
                        row["password_temp"] = password_auto
                    
                    updateGestores(cambios, df_gestores)
                    if cambios["added_rows"]:
                        st.warning("Usuarios creados:")
                        for row in cambios["added_rows"]:
                            st.code(f"Gestor: {row['nombre']} | Usuario: {row['email']} | Pass: {row['password_temp']}")
                        if st.button("Continuar"): st.rerun()
                    else:
                        st.success("✅ Guardado"); st.rerun()
                except Exception as e:
                    st.error(f"Error: {e}")