import streamlit as st
import pandas as pd
from modules.data_base import get_alumnos_con_practicas_consolidado, getOfertasTabla,guardar_cambios_alumnos, getGestores,updateOfertasTabla, updateGestores,getEmpresas
from page_utils import apply_page_config
from navigation import make_sidebar
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode, DataReturnMode, JsCode

# Configuración inicial
apply_page_config()
make_sidebar()


st.title("🚀 Panel de Gestión de Prácticas FP")

tab_alumnos, tab_ofertas, tab_config = st.tabs(["🎓 Alumnos", "🏢 Ofertas por Ciclo", "⚙️ Configuración"])

# --- TAB CONFIGURACIÓN ---
with tab_config:
    st.subheader("Configuración de Gestores")
    df_gestores = getGestores()
    
    edited_g = st.data_editor(
            df_gestores,
            # Ocultamos el ID para que el usuario no lo toque
            column_config={
                "id": None, 
                "nombre": "Nombre del Gestor", 
                "activo": "Visible"
            },
            num_rows="dynamic",
            key="editor_gestores"
        )

    if st.button("Actualizar Gestores"):
        # Obtenemos los cambios crudos del session_state
        cambios = st.session_state["editor_gestores"]
        
        if cambios["edited_rows"] or cambios["added_rows"] or cambios["deleted_rows"]:
            try:
                updateGestores(cambios, df_gestores)
                st.success("✅ Configuración guardada correctamente")
                st.rerun() # Recargamos para ver los IDs asignados a los nuevos
            except Exception as e:
                st.error(f"Error al actualizar: {e}")
        else:
            st.info("No hay cambios para guardar.")
# --- TAB ALUMNOS ---
with tab_alumnos:
    # 1. Obtener datos (Asegúrate que esta función traiga 'ciclo_formativo', 'oferta_id', etc.)
    df_raw = get_alumnos_con_practicas_consolidado()
    df_empresas_raw = getEmpresas()
    lista_empresas_db = ["⚠️ SIN ASIGNAR"] + df_empresas_raw["nombre"].tolist()
    
    # IMPORTANTE: Crear el mapa aquí para que esté disponible en el botón
    mapa_nombres_id = dict(zip(df_empresas_raw['nombre'], df_empresas_raw['CIF']))

    if not df_raw.empty:
        # --- FUNCIÓN PARA CREAR ACRÓNIMOS ---
        def crear_acronimo(nombre):
            if not nombre or pd.isna(nombre): return ""
            palabras = [w for w in nombre.split() if len(w) > 2 or w.isupper()]
            return "".join([w[0].upper() for w in palabras])

        # Preparamos el DataFrame con la columna visual del acrónimo
        df_raw['ciclo_acronimo'] = df_raw['ciclo_formativo'].apply(crear_acronimo)

        # --- GESTIÓN DE COLUMNAS PARA EL GRID ---
        # Columnas que el usuario VERÁ
        cols_visibles = [
            "ciclo_acronimo", "apellido", "nombre", "horas_totales", 
            "nombre_empresa", "comentarios_centro", "anexos_creados", 
            "anexos_enviados", "anexos_firmados", "doc_sao_entregada", "observaciones_seguimiento"
        ]
        
        # Columnas que el método GUARDAR necesita (pero el usuario NO verá)
        # Necesitamos 'ciclo_formativo' porque crearPractica usa el nombre largo
        cols_tecnicas = ["dni", "ciclo_formativo", "oferta_id", "ciclos_info", "cupos_disponibles"]

        # Creamos el DataFrame final con AMBAS
        # Usamos df_raw completo o filtramos solo las necesarias para no pesar tanto
        cols_finales = cols_visibles + [c for c in cols_tecnicas if c in df_raw.columns]
        df_display = df_raw[cols_finales].copy()

        gb = GridOptionsBuilder.from_dataframe(df_display)
        gb.configure_default_column(editable=True, filter=True, resizable=True)

        # JS para transformar True/False en SÍ/NO
        si_no_js = JsCode("""
            function(params) {
                if (params.value === true || params.value === 'true') return '✅ SÍ';
                if (params.value === false || params.value === 'false') return '';
                return params.value;
            }
        """)

        # --- CONFIGURACIÓN DE COLUMNAS VISIBLES ---
        gb.configure_column("ciclo_acronimo", headerName="Ciclo", pinned='left', width=80, editable=False)
        gb.configure_column("apellido", headerName="Apellidos", width=150)
        gb.configure_column("nombre", headerName="Nombre", width=120)
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
            gb.configure_column(col, cellRenderer='checkboxRenderer', valueFormatter=si_no_js, width=80)

        # --- CONFIGURACIÓN DE COLUMNAS OCULTAS (Mantenemos los datos pero no la vista) ---
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
        
        # --- LÓGICA DEL BOTÓN ---
        if st.button("💾 Guardar Cambios Alumnos", type="primary", use_container_width=True):
            df_grid = grid_response['data']
            
            with st.spinner("Guardando datos"):
                try:
                    guardar_cambios_alumnos(df_grid, df_display, mapa_nombres_id)
                    st.success("✅ ¡Cambios guardados correctamente!")
                    #st.rerun()
                except Exception as e:
                    st.error(f"Error técnico: {e}  - consulte con el administrador.")
# --- TAB OFERTAS ---
with tab_ofertas:
    try:
        df_gestores_all = getGestores()
        gestores_activos = df_gestores_all[df_gestores_all['activo'] == True]['nombre'].tolist()
    except:
        st.error("No se pudo cargar la lista de gestores.")
        gestores_activos = []
        
    df_raw = getOfertasTabla()
    
    if df_raw.empty:
        st.info("No hay ofertas registradas en la base de datos.")
    else:
        rows_list = []
        for _, record in df_raw.iterrows():
            ciclos_info = record.get('ciclos_formativos', {}) or {}
            puestos_info = record.get('puestos', {}) or {}
            empresa = record.get('empresas', {}) or {}
            # Cargamos el JSON de seguimiento completo
            seguimiento_full = record.get('seguimiento_gestores', {}) or {}
            
            for nombre_ciclo, datos_alumnos in ciclos_info.items():
                areas_del_ciclo = puestos_info.get(nombre_ciclo, [{"area": "General", "proyecto": ""}])
                
                for area_item in areas_del_ciclo:
                    nombre_area = area_item.get('area', 'General')
                    
                    # Extraemos los comentarios específicos para este Ciclo y esta Área
                    # Estructura esperada: { "Ciclo": { "Area": { "Gestor": "Comentario" } } }
                    seg_especifico = seguimiento_full.get(nombre_ciclo, {}).get(nombre_area, {})

                    fila = {
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
                        "Nombre Tutor": record.get('nombre_tutor', ''),
                        "Email Tutor": record.get('email_tutor', ''),
                    }
                    
                    # Rellenamos las columnas de gestores con su comentario específico de esa row
                    for gestor in gestores_activos:
                        fila[f"Prop. {gestor}"] = seg_especifico.get(gestor, "")
                    
                    rows_list.append(fila)

        df_final = pd.DataFrame(rows_list)
        
        # 4. Crear pestañas por Ciclo Formativo
        lista_ciclos = sorted(df_final['Ciclo'].unique())
        if lista_ciclos:
            sub_tabs = st.tabs(lista_ciclos)
            
            for i, nombre_ciclo in enumerate(lista_ciclos):
                with sub_tabs[i]:
                    df_ciclo_tab = df_final[df_final['Ciclo'] == nombre_ciclo].reset_index(drop=True)
                    
                    # Configuración de columnas (basada en tu código original)
                    col_config_oferta = {
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
                        num_rows="fixed",hide_index=True
                    )

                    if st.button(f"💾 Guardar Cambios {nombre_ciclo}", key=f"btn_save_{nombre_ciclo}"):
                        cambios = st.session_state[f"editor_ofertas_{nombre_ciclo}"].get("edited_rows", {})
                        
                        if cambios:
                            exitos = 0
                            for row_idx, nuevos_valores in cambios.items():
                                fila_original = df_ciclo_tab.iloc[int(row_idx)]
                                id_oferta = int(fila_original['id'])
                                area_actual = fila_original['Área']
                                
                                # Recuperamos el registro original de df_raw para no perder datos de otros ciclos/áreas
                                registro_raw = df_raw[df_raw['id'] == id_oferta].iloc[0]
                                seguimiento_db = registro_raw.get('seguimiento_gestores', {}) or {}

                                # Aseguramos la jerarquía en el JSON
                                if nombre_ciclo not in seguimiento_db:
                                    seguimiento_db[nombre_ciclo] = {}
                                if area_actual not in seguimiento_db[nombre_ciclo]:
                                    seguimiento_db[nombre_ciclo][area_actual] = {}

                                # Actualizamos los comentarios de los gestores para ESTA fila
                                for g in gestores_activos:
                                    col_name = f"Prop. {g}"
                                    # Si el gestor cambió en el editor, tomamos el nuevo; si no, el que ya tenía la fila
                                    val = nuevos_valores.get(col_name, fila_original.get(col_name, ""))
                                    seguimiento_db[nombre_ciclo][area_actual][g] = val

                                update_payload = {
                                    "seguimiento_gestores": seguimiento_db,
                                    "requisitos": nuevos_valores.get("Requisitos", fila_original["Requisitos"]),
                                    "contrato": nuevos_valores.get("Contrato", fila_original["Contrato"]),
                                    "vehiculo": nuevos_valores.get("Vehículo", fila_original["Vehículo"]),
                                    "nombre_tutor": nuevos_valores.get("Nombre Tutor", fila_original["Nombre Tutor"]),
                                    "email_tutor": nuevos_valores.get("Email Tutor", fila_original["Email Tutor"]),
                                }

                                try:
                                    updateOfertasTabla(update_payload, id_oferta)
                                    exitos += 1
                                except Exception as e:
                                    st.error(f"Error en fila {id_oferta}: {e}")

                            if exitos > 0:
                                st.success(f"¡Se han actualizado {exitos} registros!")
                                st.rerun()