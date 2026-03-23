import streamlit as st
import pandas as pd
from modules.data_base import getTutores,getGestore, getTutoresEmpresa,updateTutoresCentro, get_alumnos_con_practicas_consolidado, getOfertasTabla, guardar_cambios_alumnos, getGestores, updateOfertasTabla, updateGestores, getEmpresasYOfertas
from page_utils import apply_page_config
from navigation import make_sidebar
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode, JsCode
from datetime import datetime
# Configuración inicial
apply_page_config()
make_sidebar()

import json

def extraer_ofertas_por_ciclo(df_empresas):
    mapping = {}
    
    # df_empresas es la lista de diccionarios (res.data)
    for empresa_dict in df_empresas:
        nombre_empresa = empresa_dict.get('nombre')
        dir_empresa = empresa_dict.get('direccion', '')
        loc_empresa = empresa_dict.get('localidad', '')
        ofertas_json = empresa_dict.get('oferta_fp', [])
        puestos_por_ciclo = {}
        
        mapping[nombre_empresa] = {
            "info_base": {"direccion": dir_empresa, "localidad": loc_empresa},
            "ciclos": {}
        }
        if not isinstance(ofertas_json, list) or len(ofertas_json) == 0:
            mapping[nombre_empresa] = {}
            continue

        for oferta in ofertas_json:
            # 1. Tutor General (Fallback)
            # Nota: Usamos 'tutores' porque así viene de tu select de Supabase
            t_data = oferta.get('tutores')
            if isinstance(t_data, dict):
                tutor_general = t_data.get('nombre', 'Sin tutor')
            elif isinstance(t_data, list) and len(t_data) > 0:
                tutor_general = t_data[0].get('nombre', 'Sin tutor')
            else:
                tutor_general = 'Sin tutor'

            # 2. Tutores específicos
            tutores_especificos = oferta.get('tutores_por_puesto')
            if not isinstance(tutores_especificos, dict):
                tutores_especificos = {}

            # 3. Puestos
            dir_oferta = oferta.get('direccion_empresa') or dir_empresa
            loc_oferta = oferta.get('localidad_empresa') or loc_empresa
            data_puestos = oferta.get('puestos', {})
            
            if isinstance(data_puestos, dict):
                for ciclo, lista_proyectos in data_puestos.items():
                    if ciclo not in puestos_por_ciclo:
                        puestos_por_ciclo[ciclo] = []
                    
                    for p in lista_proyectos:
                        # Sacamos el nombre del puesto (prioridad 'area' luego 'proyecto')
                        nombre_puesto = p.get('area') or p.get('proyecto') or "General"
                        
                        # Buscamos el tutor específico en el JSONB
                        tutor_puesto = tutores_especificos.get(ciclo, {}).get(nombre_puesto, {}).get('nombre')
                        
                        # Añadimos el objeto limpio
                        puestos_por_ciclo[ciclo].append({
                            "nombre": nombre_puesto,
                            "tutor": tutor_puesto if tutor_puesto else tutor_general,
                            "direccion": dir_oferta,    # <--- Agregado
                            "localidad": loc_oferta
                        })

        # --- LIMPIEZA DE DUPLICADOS CON PRIORIDAD ---
        for ciclo in puestos_por_ciclo:
            mejores_puestos = {} # Usamos un dict para sobreescribir
            
            for item in puestos_por_ciclo[ciclo]:
                nombre = item['nombre']
                tutor = item['tutor']
                direccion = item['direccion']
                localidad = item['localidad']
                
                # Si el puesto no está, o si el nuevo tutor es mejor que "Sin tutor", lo guardamos
                if nombre not in mejores_puestos or (tutor != "Sin tutor" and mejores_puestos[nombre] == "Sin tutor"):
                    mejores_puestos[nombre] = {
                        "tutor": tutor,
                        "direccion": direccion,
                        "localidad": localidad
                    }
            
            # Convertimos de nuevo al formato de lista de dicts que espera el JS
            puestos_por_ciclo[ciclo] = [
                {
                    "nombre": n, 
                    "tutor": v['tutor'], 
                    "direccion": v['direccion'], 
                    "localidad": v['localidad']
                } for n, v in mejores_puestos.items()
            ]

        mapping[nombre_empresa] = puestos_por_ciclo
        
    return mapping

# --- LÓGICA DE USUARIO (Simulada, aquí extraes tus datos de sesión) ---
rol_usuario = st.session_state.get("rol") 
email_usuario = st.session_state.get("username")


if "df_gestores" not in st.session_state:
    st.session_state.df_gestores = None
if "df_tutores" not in st.session_state:
    st.session_state.df_tutores = None
if "practicas_data" not in st.session_state:
    st.session_state.practicas_data = None
if "data_loaded" not in st.session_state:
    st.session_state["data_loaded"] = False
if "force_reload" not in st.session_state:
    st.session_state["force_reload"] = False
if "grid_version" not in st.session_state:
    st.session_state.grid_version = 0

def load_data():
    if st.session_state["data_loaded"] or not st.session_state["force_reload"]:
        with st.spinner("Cargando datos desde la base..."):
            st.session_state["practicas_data"] = get_alumnos_con_practicas_consolidado()
            st.session_state["data_loaded"] = True
            st.session_state["force_reload"] = False

st.title("🚀 Panel de Gestión de Prácticas FP")
load_data()
nombres_tabs = ["🎓 Alumnos", "🏢 Ofertas por Ciclo"]
if rol_usuario == "admin":
    nombres_tabs.append("⚙️ Configuración")
tabs = st.tabs(nombres_tabs)

tab_alumnos = tabs[0]
tab_ofertas = tabs[1]
if rol_usuario == "admin":
    tab_config = tabs[2]

# --- TAB ALUMNOS ---
with tab_alumnos:
    df_raw = st.session_state.practicas_data

    df_raw = df_raw.rename(columns={'area': 'puesto', 'tutorCentro': 'tutor_centro'})
    if 'puesto' not in df_raw.columns:
        df_raw['puesto'] = None
    if 'asignado' not in df_raw.columns:
        df_raw['asignado'] = None
    if 'tutor_centro' not in df_raw.columns:
        df_raw['tutor_centro'] = None
    if 'cupos_disponibles' not in df_raw.columns:
            df_raw['cupos_disponibles'] = None
            
    df_raw['puesto'] = df_raw['puesto'].fillna("")
    df_raw['tutor_centro'] = df_raw['tutor_centro'].fillna("")
    try:
        df_gestores_lista = getGestores()
        nombres_gestores = df_gestores_lista['nombre'].tolist()
    except:
        nombres_gestores = []

    try:
        df_tutores_lista = getTutores() # Esta es la función que ya tienes
        nombres_tutores_centro = sorted(df_tutores_lista['nombre'].unique().tolist())
    except:
        nombres_tutores_centro = []
    df_empresas = getEmpresasYOfertas()

    if df_empresas is None or len(df_empresas) == 0:
        st.info("No hay empresas cargadas aun.")
    else:
        df_empresas_raw = pd.DataFrame(df_empresas)
        lista_empresas_db = ["⚠️ SIN ASIGNAR"] + df_empresas_raw["nombre"].tolist()
        mapa_nombres_id = dict(zip(df_empresas_raw['nombre'], df_empresas_raw['CIF']))

            # Generamos el JSON para el JS del Grid
        dict_mapeo = extraer_ofertas_por_ciclo(df_empresas)
        json_mapeo = json.dumps(dict_mapeo)

        mapeo_ciclo_empresas = {}

        for row in df_empresas:
            nombre_empresa = row['nombre']
            # Accedemos a la relación de oferta_fp
            ofertas = row.get('oferta_fp', [])
            
            for oferta in ofertas:
                # Extraemos el JSON de ciclos_formativos
                ciclos_data = oferta.get('ciclos_formativos', {})
                
                for ciclo, info in ciclos_data.items():
                    disponibles = info.get('disponibles', 0)
                    
                    if ciclo not in mapeo_ciclo_empresas:
                        mapeo_ciclo_empresas[ciclo] = []
                    
                    mapeo_ciclo_empresas[ciclo].append({
                        "nombre": nombre_empresa,
                        "disponibles": disponibles
                    })

        json_ciclo_empresas = json.dumps(mapeo_ciclo_empresas)

        if not df_raw.empty:
            def crear_acronimo(nombre):
                if not nombre or pd.isna(nombre): return ""
                palabras = [w for w in nombre.split() if len(w) > 2 or w.isupper()]
                return "".join([w[0].upper() for w in palabras])

            df_raw['ciclo_acronimo'] = df_raw['ciclo_formativo'].apply(crear_acronimo)
            cols_visibles = [
                "ciclo_acronimo", "apellido", "nombre","localidad", "vehiculo", "horas_totales", 
                "nombre_empresa","asignado", "puesto","cupos_disponibles","tutor_centro", "gestor", "comentarios_centro", "observaciones_seguimiento","telefono", "email_empresa"
            ]
        
            cols_tecnicas = ["dni", "ciclo_formativo", "oferta_id", "ciclos_info","practica_id", "direccion_practica","localidad_practica"]
            cols_finales = cols_visibles + [c for c in cols_tecnicas if c in df_raw.columns]
            df_display = df_raw[cols_finales].copy()
            if "direccion_practica" not in df_display.columns:
                df_display["direccion_practica"] = None
            if "localidad_practica" not in df_display.columns:
                df_display["localidad_practica"] = None
            def calcular_cupo_actual(row, dict_mapeo):
                empresa = row.get('nombre_empresa')
                ciclo = row.get('ciclo_formativo')
                
                # Si no tiene empresa o es la marca de "Sin asignar"
                if not empresa or empresa == "⚠️ SIN ASIGNAR":
                    return None
                
                # Buscamos en el mapeo de ofertas (dict_mapeo que ya generaste)
                # Estructura esperada: dict_mapeo[empresa][ciclo] -> { "disponibles": X, ... }
                try:
                    if empresa in dict_mapeo and ciclo in dict_mapeo[empresa]:
                        # Accedemos al primer puesto o sumamos disponibles si hay varios
                        puestos = dict_mapeo[empresa][ciclo]
                        if isinstance(puestos, list) and len(puestos) > 0:
                            # Si tu dict_mapeo tiene la estructura de puestos:
                            return puestos[0].get('disponibles', 0) 
                except Exception as e:
                    return None
                return None

            # Creamos la columna físicamente en el DataFrame
            df_display['cupos_disponibles'] = df_display.apply(lambda x: calcular_cupo_actual(x, dict_mapeo), axis=1)

            # Ahora sí, asegúrate de incluirla en la lista de columnas visibles
            if "cupos_disponibles" not in cols_visibles:
                cols_visibles.append("cupos_disponibles")
            if rol_usuario == "admin":
                st.info("Si no encontrás la empresa y ya tenes al alumno para asignar, dirigite a la sección de  Prácticas -> Carga Rápida")
            gb = GridOptionsBuilder.from_dataframe(df_display)
            gb.configure_default_column(editable=True, filter=True, resizable=True)

            si_no_js = JsCode("""
                function(params) {
                    if (params.value === true || params.value === 'true') return '✅ SÍ';
                    if (params.value === false || params.value === 'false') return '';
                    return params.value;
                }
            """)

            gb.configure_column("ciclo_acronimo", headerName="Ciclo", pinned='left', width=150, editable=False)
            gb.configure_column("apellido", headerName="Apellidos", width=200)
            gb.configure_column("nombre", headerName="Nombre", width=200)
            gb.configure_column("telefono", headerName="Telefono", width=200)
            gb.configure_column("email_empresa", headerName="Email Empresa", width=200)
            gb.configure_column("comentarios_centro", headerName="Comentarios", width=200)

            gb.configure_column("gestor", 
                headerName="Gestor", 
                width=120,
                cellEditor='agSelectCellEditor',
                cellEditorParams={'values': nombres_gestores},
                editable=(rol_usuario == "admin") 
            )

            gb.configure_column("horas_totales", headerName="Hrs", width=100)
            gb.configure_column("nombre_empresa", 
                headerName="Empresa",
                cellEditor='agSelectCellEditor',
                cellEditorParams=JsCode(f"""
                    function(params) {{
                        const mapeoCiclos = {json_ciclo_empresas};
                        const cicloAlumno = params.data.ciclo_formativo;
                        const empresaActual = params.data.nombre_empresa;
                        
                        let datosEmpresas = mapeoCiclos[cicloAlumno] || [];
                        
                        // Filtrar: dejamos las que tienen cupo O la que ya tiene el alumno asignada
                        let empresasValidas = datosEmpresas
                            .filter(e => e.disponibles > 0 || e.nombre === empresaActual)
                            .map(e => e.nombre);
                        
                        return {{
                            values: ['⚠️ SIN ASIGNAR', ...empresasValidas]
                        }};
                    }}
                """),
                cellStyle=JsCode("""
                    function(params) {
                        if (params.value === '⚠️ SIN ASIGNAR') return {'backgroundColor': '#d63031', 'color': 'white', 'fontWeight': 'bold'};
                        return {'backgroundColor': '#55efc4', 'color': 'black'};
                    }
                """),
                onCellValueChanged=JsCode(f"""
                        function(params) {{
                            // Usamos el JSON de ciclos que tiene los disponibles
                            const mapeoCiclos = {json_ciclo_empresas}; 
                            const nuevaEmpresa = params.data.nombre_empresa;
                            const ciclo = params.data.ciclo_formativo;

                            let totalCupos = 0;
                            if (mapeoCiclos[ciclo]) {{
                                const empData = mapeoCiclos[ciclo].find(e => e.nombre === nuevaEmpresa);
                                if (empData) totalCupos = empData.disponibles;
                            }}

                            // Actualizamos el valor en la fila (esto dispara el cellRenderer de la otra columna)
                            params.data.cupos_disponibles = totalCupos;
                            params.data.puesto = null; 

                            // Refrescamos ambas celdas para que el usuario vea el cambio visual
                            params.api.refreshCells({{
                                rowNodes: [params.node], 
                                columns: ['cupos_disponibles', 'puesto']
                            }});
                        }}
                    """),
                editable=True,
                width=200
            )

            gb.configure_column("asignado", 
                headerName="Asignar", 
                editable=True,
                width=200,
                cellEditor='agSelectCellEditor',
                cellEditorParams={'values': ["Asignar"]},
                cellStyle={'color': '#0984e3', 'fontWeight': 'bold'}
            )
            gb.configure_column("tutor_centro", 
                headerName="Tutor Centro", 
                editable=True,
                width=200,
                cellEditor='agSelectCellEditor',
                cellEditorParams={'values': nombres_tutores_centro}, # Pasamos la lista aquí
                cellStyle={'color': '#0984e3', 'fontWeight': 'bold'}
            )
            gb.configure_column("puesto",
                headerName="Puesto/Area",
                editable=True,
                cellEditor='agSelectCellEditor',
                cellEditorParams=JsCode(f"""
                function(params) {{
                    // Usamos || {{}} para asegurar que si el JSON falla, sea un objeto vacío y no 'null'
                    const mapeo = {json_mapeo} || {{}}; 
                    const empresa = params.data.nombre_empresa;
                    const ciclo = params.data.ciclo_formativo;
                    
                    // Verificamos existencia antes de iterar/mapear
                    if (mapeo[empresa] && mapeo[empresa][ciclo]) {{
                        const opciones = mapeo[empresa][ciclo];
                        return {{ values: Array.isArray(opciones) ? opciones.map(p => p.nombre) : [] }};
                    }}
                    return {{ values: [] }};
                }}
            """),

            onCellValueChanged=JsCode(f"""
            function(params) {{
                const mapeo = {json_mapeo} || {{}};
                const empresa = params.data.nombre_empresa;
                const ciclo = params.data.ciclo_formativo;
                const puestoNombre = params.data.puesto;

                if (mapeo[empresa] && mapeo[empresa][ciclo]) {{
                    const listaPuestos = mapeo[empresa][ciclo];
                    // Buscamos el objeto que coincide con el nombre seleccionado
                    const puestoEncontrado = listaPuestos.find(p => p.nombre === puestoNombre);
                    
                    if (puestoEncontrado) {{
                        // ASIGNAMOS EL TUTOR AL CAMPO 'tutor'
                        console.log("¡Puesto encontrado! Info:", puestoEncontrado);
                        params.data.tutor = puestoEncontrado.tutor;
                        params.data.direccion = puestoEncontrado.direccion;
                        params.data.localidad = puestoEncontrado.localidad;

                    }} else {{
                        params.data.tutor = null;
                        const infoBase = mapeo[empresa]["info_base"];
                        params.data.direccion_practica = infoBase ? infoBase.direccion : null;
                        params.data.localidad_practica = infoBase ? infoBase.localidad : null;
                    }}
                }}
                
                // Forzamos el refresco de la celda del tutor para que se vea el cambio
                params.api.refreshCells({{
                    rowNodes: [params.node], 
                    columns: ['tutor']
                }});
            }}
        """),
                width=250
            )
                    
            gb.configure_column(
                "cupos_disponibles",
                headerName="Plazas Libres",
                width=130,
                editable=False,
                # 1. Definimos el estilo (Colores de fondo y texto)
                cellStyle=JsCode("""
                    function(params) {
                        if (params.value === null || params.value === undefined) return null;
                        if (params.value <= 0) {
                            return {'backgroundColor': '#ff7675', 'color': 'white', 'fontWeight': 'bold'};
                        } else if (params.value <= 2) {
                            return {'backgroundColor': '#fab1a0', 'color': 'black', 'fontWeight': 'bold'};
                        } else {
                            return {'backgroundColor': '#55efc4', 'color': 'black', 'fontWeight': 'bold'};
                        }
                    }
                """),
                # 2. Definimos el texto con el icono (Sin HTML, solo strings)
                valueFormatter=JsCode("""
                    function(params) {
                        if (params.value === null || params.value === undefined) return '-';
                        if (params.value <= 0) return '🔴 Agotado';
                        if (params.value <= 2) return '🟠 ' + params.value + ' disp.';
                        return '🟢 ' + params.value + ' disp.';
                    }
                """)
            )

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
                key=f"grid_alumnos_v_{st.session_state.grid_version}"
                
            )
            if st.button("💾 Guardar Cambios Alumnos", type="primary", use_container_width=True):
                df_grid = grid_response['data']
                with st.spinner("Guardando datos"):
                    try:
                        guardar_cambios_alumnos(df_grid, df_display, mapa_nombres_id)
                        st.success("✅ ¡Cambios guardados correctamente!")
                        st.session_state["force_reload"] = True
                        load_data()
                        st.session_state.grid_version += 1
                        st.rerun()
                    except Exception as e:
                        st.error(f"Error técnico: {e}")
        else:
            st.info("No tienes sugerencias de prácticas por el momento")
# --- TAB OFERTAS (Todo el código igual, visible para ambos) ---
with tab_ofertas:
    try:
        df_gestores_all = getGestore()
        gestores_activos_df = pd.DataFrame(columns=['nombre', 'ciclo', 'activo'])
        
        if df_gestores_all.empty:
            st.info("No hay gestores registrados.")
        else:
            gestores_activos_df = df_gestores_all[df_gestores_all['activo'] == True]
    except:
        st.error("No se pudo cargar la lista de gestores.")
        gestores_activos_df = []
        
    df_raw_ofertas = getOfertasTabla()
    if df_raw_ofertas.empty:
        st.info("No hay ofertas registradas.")
    else:
        rows_list = []
        for _, record in df_raw_ofertas.iterrows():
            ciclos_info = record.get('ciclos_formativos', {}) or {}
            puestos_info = record.get('puestos', {}) or {}
            empresa = record.get('empresas', {}) or {}
            seguimiento_full = record.get('seguimiento_gestores', {}) or {}
            tutores_full = empresa.get("tutores", {}) or {}
            for nombre_ciclo, datos_alumnos in ciclos_info.items():
                gestores_ciclo = gestores_activos_df[
                    gestores_activos_df['ciclo'].str.upper() == nombre_ciclo
                ]['nombre'].tolist()
                areas_del_ciclo = puestos_info.get(nombre_ciclo, [{"area": "General", "proyecto": ""}])
                for area_item in areas_del_ciclo:
                    nombre_area = area_item.get('area', 'General')
                    seg_especifico = seguimiento_full.get(nombre_ciclo, {}).get(nombre_area, {})
                    
                    fila = {
                        "id": record.get('id'),
                        "Empresa": empresa.get('nombre', 'N/A'),
                        "Teléfono": empresa.get('telefono', ''),
                        "Dirección": empresa.get('direccion', ''),
                        "Localidad": empresa.get('localidad', ''),
                        "Horario": empresa.get('horario', ''),
                        "Ciclo": nombre_ciclo,
                        "Alumnos Pedidos": datos_alumnos.get('alumnos', 0),
                        "Área": nombre_area,
                        "Proyecto": area_item.get('proyecto', ''),
                        "Requisitos": record.get('requisitos', ''),
                        "Contrato": record.get('contrato', ''),
                        "Vehículo": record.get('vehiculo', ''),
                        "Nombre Tutor": tutores_full[0].get('nombre', record.get('nombre_tutor', '')) if (isinstance(tutores_full, list) and len(tutores_full) > 0) else record.get('nombre_tutor', ''),
                        "Email Tutor": tutores_full[0].get('email', record.get('email_tutor', '')) if (isinstance(tutores_full, list) and len(tutores_full) > 0) else record.get('email_tutor', ''),
                        "Telefono Tutor": tutores_full[0].get('telefono', record.get('telefono', '')) if (isinstance(tutores_full, list) and len(tutores_full) > 0) else record.get('telefono', ''),
                    }
                    for gestor in gestores_ciclo:
                        fila[f"Prop. {gestor}"] = seg_especifico.get(gestor, "")
                    rows_list.append(fila)

        df_final = pd.DataFrame(rows_list)
        lista_ciclos = sorted(df_final['Ciclo'].unique())
        if lista_ciclos:
            sub_tabs = st.tabs(lista_ciclos)
            for i, nombre_ciclo in enumerate(lista_ciclos):
                with sub_tabs[i]:
                    # 1. Filtramos las filas que pertenecen a este ciclo
                    df_ciclo_raw = df_final[df_final['Ciclo'] == nombre_ciclo].copy()
                    
                    columnas_fijas = [
                        "id", "Empresa", "Teléfono", "Localidad", "Horario"
                        "Alumnos Pedidos", "Área", "Proyecto", "Requisitos", 
                        "Contrato", "Vehículo", "Nombre Tutor", "Email Tutor","Telefono Tutor"
                    ]
                    
                    # 3. Identificamos SOLO los gestores de este ciclo específico
                    gestores_del_ciclo = gestores_activos_df[
                        gestores_activos_df['ciclo'].str.upper() == nombre_ciclo.upper()
                    ]['nombre'].tolist()
                    
                    # Creamos la lista de nombres de columnas de gestores permitidos
                    columnas_gestores_permitidas = [f"Prop. {g}" for g in gestores_del_ciclo]
                    
                    # 4. FILTRADO CRÍTICO DE COLUMNAS: Solo las fijas + los gestores de este ciclo
                    # Esto elimina cualquier columna de "Prop. Gestor" que no sea de este ciclo
                    columnas_finales = [c for c in columnas_fijas if c in df_ciclo_raw.columns] + \
                                    [c for c in columnas_gestores_permitidas if c in df_ciclo_raw.columns]
                    
                    # Re-creamos el DataFrame solo con esas columnas
                    df_ciclo_tab = df_ciclo_raw[columnas_finales].reset_index(drop=True)

                    # 5. Configuración de columnas para el editor
                    col_config_oferta = {
                        "id": None, # Ocultamos el ID
                        "Empresa": st.column_config.TextColumn(disabled=True),
                        "Teléfono": st.column_config.TextColumn(disabled=True),
                        "Localidad": st.column_config.TextColumn(disabled=True),
                        "Horarios": st.column_config.TextColumn(disabled=True),
                        "Nombre Tutor": st.column_config.TextColumn(disabled=True),
                        "Email Tutor": st.column_config.TextColumn(disabled=True),
                        "Telefono Tutor": st.column_config.TextColumn(disabled=True),
                        "Alumnos Pedidos": st.column_config.NumberColumn("Cant.", disabled=True),
                        "Área": st.column_config.TextColumn(disabled=True),
                    }
                    
                    # Formateamos solo las columnas de los gestores que SI están presentes
                    for g in gestores_del_ciclo:
                        col_name = f"Prop. {g}"
                        if col_name in df_ciclo_tab.columns:
                            col_config_oferta[col_name] = st.column_config.TextColumn(f"🙋 {g}")

                    # 6. Renderizado
                    edited_data = st.data_editor(
                        df_ciclo_tab,
                        column_config=col_config_oferta,
                        key=f"editor_ofertas_{nombre_ciclo}",
                        use_container_width=True,
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

                                for g in gestores_ciclo:
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
        tabs = st.tabs(["Gestores", "Tutores Centro"])
        with tabs[0]:
            if st.session_state.df_gestores is None:
                st.session_state.df_gestores = getGestores()
            edited_g = st.data_editor(
                    st.session_state.df_gestores,
                    column_config={"id": None, "password": "Password", "nombre": "Nombre", "email": "Email", "ciclo": st.column_config.SelectboxColumn(
                        "Ciclo",
                        options=["Comercio Internacional","Desarrollo Aplicaciones Multiplataforma", "Desarrollo Aplicaciones Web", "Marketing y Publicidad", "Transporte y Logística"], 
                        required=False
                    ),"activo": "Visible"},
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
                        
                        des= updateGestores(cambios, st.session_state.df_gestores)
                        if cambios["added_rows"]:
                            st.warning("Usuarios creados:")
                            for row in cambios["added_rows"]:
                                st.code(f"Gestor: {row['nombre']} | Usuario: {row['email']} | Pass: {row['password_temp']}")
                            if st.button("Continuar"): 
                                st.session_state.df_gestores = None
                                st.rerun()
                        else:
                            st.success("✅ Guardado"); st.rerun()
                    except Exception as e:
                        st.error(f"Error: {e}")
         
        with tabs[1]:
            if st.session_state.df_tutores is None:
                st.session_state.df_tutores = getTutores()
            edited_g = st.data_editor(
                    st.session_state.df_tutores,
                    column_config={"id": None, "nombre": "Nombre", "email": "Email","telefono": "Teléfono"},
                    num_rows="dynamic",
                    key="editor_tutores",
                    use_container_width=True
                )
            if st.button("Actualizar Tutores"):
                cambios = st.session_state["editor_tutores"]
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
                        
                        res = updateTutoresCentro(cambios, st.session_state.df_tutores)
                        
                        if cambios["added_rows"]:
                            st.warning("Usuarios creados:")
                            for row in cambios["added_rows"]:
                                st.code(f"Tutor: {row['nombre']} | Usuario: {row['email']} | Pass: {row['password_temp']}")
                            if st.button("Continuar"): 
                                st.session_state.df_tutores = None
                                st.rerun()
                        else:
                            st.toast("✅ Guardado"); st.rerun()
                    except Exception as e:
                        error_msg = str(e)
                        if "23503" in error_msg:
                            st.error("❌ Error: El CIF de la empresa no existe en la base de datos.")
                            st.info("Asegúrate de que la empresa esté creada antes de asignar un tutor.")     
                        else:
                            st.error(f"⚠️ Ha ocurrido un error inesperado: {error_msg}")


