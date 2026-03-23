import streamlit as st
import pandas as pd
from modules.data_base import getEquals, getEqual, upsert, updateTutores,getEquals, getPracticas
from page_utils import apply_page_config
from navigation import make_sidebar
from variables import empresasTabla, necesidadFP, estados, localidades, tutoresTabla,practicaTabla,practicaEstadosTabla,linkCalendar,carpetaPractica
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode, DataReturnMode
from modules.drive_helper import list_drive_files, upload_to_drive
from pathlib import Path
import uuid
apply_page_config()
make_sidebar()

st.set_page_config(page_title="Mi Empresa", page_icon="🏢")
st.markdown(
    "<h2 style='text-align: center;'>MI EMPRESA</h2>",
    unsafe_allow_html=True
)

# -- aca el "email" es el CIF de la empresa
cif = st.session_state.get("username", "000000")

if "tutores" not in st.session_state:
    st.session_state.tutores = None
if "page" not in st.session_state:
    st.session_state.page = "lista"
if "practicas" not in st.session_state:
    st.session_state["practicas"] = []
if "practica_seleccionada" not in st.session_state:
    st.session_state.practica_seleccionada = None
if "estados" not in st.session_state:
    st.session_state["estados"] = []
# --- Traer todas las empresas ---
empresas = getEquals(empresasTabla, {"CIF": cif})
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

def fetch_practicas_tutores():
    practicas = getPracticas(practicaTabla, {"empresa": cif})
    estados = getEquals(practicaEstadosTabla, {})
    tutores = getEquals(tutoresTabla, {'cif_empresa': cif})
    
    st.session_state["practicas"] = practicas
    st.session_state["tutores"] = tutores
    st.session_state["estados"] = estados
    return practicas, tutores

if not empresas:
    st.warning("No encontramos tu empresa")
    st.stop()

df_empresas = pd.DataFrame(empresas)
df_empresas = df_empresas[df_empresas["CIF"] != "00000000"]
fetch_practicas_tutores()
practicas = st.session_state["practicas"]
tutores = st.session_state["tutores"]

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
# --- Tabs principales ---
tabEmpresa, tabOferta,tabPractica, tabTutores = st.tabs(["Mi Empresa", "Ofertas", "Prácticas", "Tutores"])

# -------------------------------------------------------------------
# TAB 1: Buscar y visualizar empresas
# -------------------------------------------------------------------
with tabEmpresa:
    if not df_empresas.empty:
        empresa = df_empresas.iloc[0].to_dict()
        with st.expander(f"Empresa: {empresa['nombre']}", expanded=True):
            new_nombre = st.text_input("Nombre", empresa.get("nombre", ""))
            new_direccion = st.text_input("Dirección", empresa.get("direccion", ""))
            try:
                indice_default = localidades.index(empresa.get("localidad", ""))
            except ValueError:
                indice_default = 0

            new_localidad = st.selectbox(
                "Localidad *", 
                localidades, 
                index=indice_default, 
                key="localidad"
            )
            st.write("**CIF**")
            st.info(empresa.get("CIF", "N/A"))
            new_telefono = st.text_input("Teléfono", empresa.get("telefono", ""))
            new_email = st.text_input("Email", empresa.get("email_empresa", ""))

            if st.button("💾 Actualizar empresa"):
                upsert(empresasTabla, {
                        "nombre": new_nombre,
                        "CIF": cif,
                        "direccion": new_direccion,
                        "localidad": new_localidad,
                        "telefono": new_telefono,
                        "email_empresa": new_email
                    }, keys=["CIF"])

                st.toast("Empresa actualizada correctamente")
                st.rerun()
    
with tabOferta:
 # --- Mostrar FP asociadas ---
        fps = getEqual(necesidadFP, "empresa", empresa["CIF"])
        st.subheader(f"Prácticas ofrecidas")
        st.caption('Oferta de prácticas actuales ')
        if fps:
            for i, fp in enumerate(fps, start=1):
                estado_actual = fp.get("estado") or "Nuevo"
                bg_color = "🟢" if estado_actual == "Nuevo" else "🔴"

                with st.expander(
                    f"Oferta #{i} | Fecha: {pd.to_datetime(fp.get('created_at')).strftime('%d/%m/%Y')} | {estado_actual} {bg_color}",
                    expanded=False
                ):
                    ciclos = fp.get("ciclos_formativos")
                    puestos = fp.get("puestos")

                    if ciclos:
                        st.write("🎓 Ciclos formativos y cantidad de alumnos:")
                        data = [
                            {"Ciclo": ciclo, "Alumnos": valores["alumnos"], "Disponibles": valores["disponibles"]}
                            for ciclo, valores in ciclos.items()]
                        df_ciclos = pd.DataFrame(data, columns=["Ciclo",  "Alumnos", "Disponibles"])
                        st.dataframe(df_ciclos, hide_index=True, use_container_width=True)

                    if puestos:
                        st.write("🧩 Puestos por ciclo formativo:")
                        for ciclo, lista_puestos in puestos.items():
                            cantidad_alumnos = None
                            if ciclos and ciclo in ciclos:
                                cantidad_alumnos = ciclos[ciclo]["alumnos"]

                            with st.expander(f"{ciclo} ({cantidad_alumnos if cantidad_alumnos else 'Sin datos'} alumnos)"):
                                if lista_puestos:
                                     for p in lista_puestos:
                                        st.write(f"- Área: {p['area']} — Proyecto: {p['proyecto']}")
                                else:
                                    st.markdown("_Sin áreas o proyectos registrados_")


                    proyectos = fp.get("proyectos")
                    requisitos = fp.get("requisitos")
                    if proyectos:
                        st.markdown(f"**Proyectos:** {proyectos}")
                    if requisitos:
                        st.markdown(f"**Requisitos:** {requisitos}")

                    contrato = fp.get("contrato")
                    vehiculo = fp.get("vehiculo")
                    st.write(f"**Contrato:** {'Sí' if contrato else 'No'}")
                    st.write(f"**Vehículo:** {'Sí' if vehiculo else 'No'}")

                    if estado_actual in estados:
                        default_index = estados.index(estado_actual)
                    else:
                        default_index = 0
                   
        else:
            st.info('No hay necesidades FP registradas para esta empresa.')     

with tabTutores:
        st.subheader("Tutores")
        st.caption('Aquí puedes administrar los tutores de tu empresa. Agrega, modifica o elimina usando la tabla, posiciona el mouse sobre la tabla y podrás ver las opciones. Luego preciona "Actualizar Tutores"')
        if st.session_state.tutores is None:
            st.session_state.tutores = getEquals(tutoresTabla,{"cif_empresa": cif})
        if not st.session_state.tutores:
            columnas = ["id", "created_at", "nombre", "email", "nif", "cif_empresa","telefono"]
            df_tutores = pd.DataFrame(columns=columnas)
        else:
            df_tutores = pd.DataFrame(st.session_state.tutores)
        
        edited_t = st.data_editor(
                        df_tutores,
                        column_config={
                                "id": None, 
                                "created_at": None, 
                                "nombre": "Nombre", 
                                "email": "Email",
                                "telefono": "telefono",  
                                "oferta":None,
                                "nif": "NIF",
                                "cif_empresa":None
                            },
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
                    
                    res = updateTutores(cambios, df_tutores, cif=cif)
                    st.toast("✅ Guardado"); 
                    st.rerun()
                except Exception as e:
                    st.error(f"Error: {e}")

def mostrarLista():
    if st.button("🔄 Actualizar", key="btn_refresh"):
            st.session_state["force_reload"] = True
            st.rerun()
    if not practicas:
        st.info("No tienes prácticas asignadas aun.")
    else:
        data_for_grid = []
        for p in practicas:
            pid = p["id"]
            estados_p =  p.get("status", [])

            data_for_grid.append({
                "ID": pid,
                "Alumno": f"{p.get('alumnos', {}).get('nombre')} {p.get('alumnos', {}).get('apellido')}",
                "Empresa": p.get('empresas', {}).get('nombre'),
                "Estado": estados_p,
                "Ciclo": p.get('ciclo_formativo', '—'),
                "Gestor": p.get('alumnos', {}).get('gestor', 'Sin asignar')
            })

        df = pd.DataFrame(data_for_grid)

        if df.empty:
            st.info("No hay prácticas asignadas aun")

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
            if isinstance(selected_rows, pd.DataFrame):
                selected_id = selected_rows.iloc[0]['ID']
            else:
                selected_id = selected_rows[0]['ID']

            # Seteamos el estado y redirigimos
            st.session_state.practica_seleccionada = selected_id
            st.session_state.page = "detalle"
            st.rerun()
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
    seccion_detalle(alumno, empresa, p, oferta)
    seccion_planificacion(alumno, empresa, p)
    if st.button("⬅️ Volver"):
        st.session_state.page = "lista"
        st.rerun()

def seccion_detalle(alumno, empresa, p, oferta):
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
            gestor_actual = alumno.get("gestor")
            st.write(f"**Gestor:** {gestor_actual}")

        with col2:
            st.write(f"**Empresa:** {empresa['nombre']}")
            st.write(f"**CIF:** {empresa['CIF']}")
            direccion = oferta.get("direccion_empresa") or empresa['direccion']
            st.write(f"**Dirección práctica:** {direccion}") 
            localidad = oferta.get("localidad_empresa") or empresa['localidad']
            st.write(f"**Localidad:** {localidad}")

            lista_nombres_tutores = [g["nombre"] for g in tutores]
            if "No asignado" not in lista_nombres_tutores:
                lista_nombres_tutores.insert(0, "No asignado")
            tutor_actual = p.get("tutor") 
            indice_tutor = lista_nombres_tutores.index(tutor_actual) if tutor_actual in lista_nombres_tutores else 0
            clave_tutor = f"tutor_{alumno['id']}"
            st.selectbox(
                "**Tutor Empresa**",
                options=lista_nombres_tutores,
                index=indice_tutor,
                key=clave_tutor,
                on_change=handle_update,
                args=(practicaTabla, p['id'], "tutor", "id", clave_tutor, "Tutor")
            )

            tutorc_actual = p.get("tutor_centro") 
            st.write(f"**Tutor Centro:** {tutorc_actual}")
        
        pass

def seccion_planificacion(alumno, empresa, practicaId):
        st.subheader("📅 Planificación de Prácticas")
        folder_name = f"{alumno['apellido']}_{alumno['nombre']}_{alumno['dni']}_practica_{empresa['nombre']}".strip()
        files = list_drive_files(folder_name)
        archivo_calendario = next((f for f in files[0] if "calendario" in f['name']), None)
        
        with st.expander("Generar Calendario", expanded=False):
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

with tabPractica:
    if st.session_state.page == "lista":
        mostrarLista()
    else:
        mostrar_detalle()

