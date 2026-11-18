import streamlit as st
import pandas as pd
from page_utils import apply_page_config
from modules.data_base import getEquals, upsert, updateTutores,getEquals, getPracticas,logError, getCiclosYAreas, eliminarOferta, actualizarOfertaEmpresa, ofertaSinAsignaciones, crearOfertaEmpresa
from navigation import make_sidebar
from modules.forms_helper import file_size_bytes, render_requisitos, requisitos_a_estado, slug
from variables import empresasTabla, max_file_size, necesidadFP, estados, aniosList, localidades,estados as estadosPractica, tutoresTabla,practicaTabla,linkCalendar,carpetaPractica,locale_tabla_principal
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode, DataReturnMode
from modules.drive_helper import list_drive_files, upload_to_drive,folderNamePractica,archivoNombre

from pathlib import Path
import uuid
apply_page_config()
make_sidebar()

st.set_page_config(page_title="Mi Empresa", page_icon="🏢")
st.markdown(
    "<h2 style='text-align: center;'>MI EMPRESA</h2>",
    unsafe_allow_html=True
)


def _si_no(valor):
    """contrato/vehiculo are saved as "Sí"/"No" (older rows may be booleans)."""
    if isinstance(valor, str):
        return "Sí" if valor.strip().lower() in ("sí", "si", "true") else "No"
    return "Sí" if valor else "No"


@st.dialog("Eliminar oferta")
def dialog_eliminar_oferta(fp, numero):
    st.warning(f"Vas a eliminar la **Oferta #{numero}** por completo. Esta acción no se puede deshacer.")
    col_ok, col_no = st.columns(2)
    with col_ok:
        if st.button("Eliminar", type="primary", key=f"confirmar_eliminar_oferta_{fp['id']}"):
            try:
                eliminarOferta(fp["id"])
            except Exception as e:
                st.error(str(e))
                return
            st.toast("Oferta eliminada", icon="✅")
            st.rerun()
    with col_no:
        if st.button("Volver", key=f"volver_eliminar_oferta_{fp['id']}"):
            st.rerun()


def editar_oferta(fp, areas_map):
    oid = fp["id"]
    k = f"oferta_{oid}"
    ciclos = fp.get("ciclos_formativos") or {}
    puestos = fp.get("puestos") or {}

    # Load the saved requirements into the widgets once
    if not st.session_state.get(f"{k}_req_cargado"):
        for key, value in requisitos_a_estado(f"{k}_req", fp.get("requisitos")).items():
            st.session_state[key] = value
        st.session_state[f"{k}_req_cargado"] = True

    st.markdown("**Ciclos formativos y puestos**")
    nuevos_alumnos, nuevos_puestos = {}, {}
    for ciclo, valores in ciclos.items():
        total = valores.get("alumnos") or 0
        ocupadas = max(total - (valores.get("disponibles") or 0), 0)
        st.markdown(f"🎓 **{ciclo}**")
        nuevos_alumnos[ciclo] = st.number_input(
            "Cantidad de alumnos", min_value=max(ocupadas, 1), max_value=50,
            value=max(total, ocupadas, 1), step=1, key=f"{k}_alumnos_{slug(ciclo)}",
            help=f"Ya hay {ocupadas} alumno(s) asignado(s): no puede ser menor." if ocupadas else None,
        )
        actuales = {p.get("area"): p.get("proyecto", "") for p in (puestos.get(ciclo) or []) if p.get("area")}
        opciones = list(dict.fromkeys(list(areas_map.get(ciclo, [])) + list(actuales)))
        areas = st.multiselect(
            "Puestos / áreas", opciones, default=list(actuales),
            key=f"{k}_areas_{slug(ciclo)}", placeholder="Selecciona áreas",
        )
        nuevos_puestos[ciclo] = [
            {"area": area, "proyecto": st.text_input(
                f"Proyecto relacionado ({area})", value=actuales.get(area, ""),
                key=f"{k}_proy_{slug(ciclo)}_{slug(area)}",
            ).strip()}
            for area in areas
        ]

    st.markdown("**Dirección del centro de trabajo**")
    direccion = st.text_input("Dirección", value=fp.get("direccion_empresa") or "", key=f"{k}_dir")
    col_cp, col_loc = st.columns(2)
    with col_cp:
        cp = st.text_input("Código Postal", value=fp.get("cp_empresa") or "", key=f"{k}_cp")
    with col_loc:
        localidad = st.text_input("Localidad", value=fp.get("localidad_empresa") or "", key=f"{k}_loc")

    st.markdown("**Requisitos adicionales**")
    requisitos = render_requisitos(
        f"{k}_req", idiomas_label="Idiomas", skills_label="Skills",
        otros_label="Otros requisitos (por ejemplo, residencia)",
    )

    st.markdown("**Información adicional**")
    contrato = st.radio(
        "Si el alumno cubre vuestras expectativas, ¿habría posibilidad de hacerle un contrato laboral?",
        ["Sí", "No"], index=["Sí", "No"].index(_si_no(fp.get("contrato"))),
        horizontal=True, key=f"{k}_contrato",
    )
    vehiculo = st.radio(
        "¿Se necesita vehículo propio para acceder a vuestras instalaciones?",
        ["Sí", "No"], index=["Sí", "No"].index(_si_no(fp.get("vehiculo"))),
        horizontal=True, key=f"{k}_vehiculo",
    )

    sin_area = [c for c, lista in nuevos_puestos.items() if not lista]
    if sin_area:
        st.markdown(
            f"<span style='color:red;'>Selecciona al menos un área en: {', '.join(sin_area)}</span>",
            unsafe_allow_html=True,
        )
    if st.button("💾 Guardar cambios", type="primary", key=f"{k}_guardar", disabled=bool(sin_area)):
        try:
            actualizarOfertaEmpresa(oid, nuevos_alumnos, {
                "puestos": nuevos_puestos,
                "direccion_empresa": direccion.strip(),
                "cp_empresa": cp.strip(),
                "localidad_empresa": localidad.strip(),
                "requisitos": requisitos,
                "contrato": contrato,
                "vehiculo": vehiculo,
            })
        except Exception as e:
            st.error(str(e))
            return
        st.session_state[f"{k}_cerrar_edicion"] = True
        st.session_state.pop(f"{k}_req_cargado", None)
        st.toast("Oferta actualizada", icon="✅")
        st.rerun()



NUEVA = "nueva_oferta"


def _cerrar_nueva_oferta():
    st.session_state[f"{NUEVA}_abierta"] = False
    for key in [k for k in st.session_state if str(k).startswith(f"{NUEVA}_") and k != f"{NUEVA}_abierta"]:
        del st.session_state[key]


def nueva_oferta(empresa, ciclos_lista, areas_map, tutores_empresa, anio_actual):
    k = NUEVA
    with st.container(border=True):
        st.markdown("#### ➕ Nueva oferta")

        anios = list(aniosList[1:])
        anio = st.selectbox(
            "Curso académico *", anios,
            index=anios.index(anio_actual) if anio_actual in anios else 0, key=f"{k}_anio",
        )

        tutor_id = None
        if tutores_empresa:
            opciones_tutor = {t["id"]: f"{t.get('nombre', '')} ({t.get('email', '')})" for t in tutores_empresa}
            tutor_id = st.selectbox(
                "Tutor de empresa", list(opciones_tutor), format_func=opciones_tutor.get,
                index=None, placeholder="Selecciona un tutor", key=f"{k}_tutor",
            )
        else:
            st.caption("No tienes tutores registrados. Puedes agregarlos en la pestaña Tutores.")

        st.markdown("**Ciclos formativos y puestos**")
        ciclos_sel = st.multiselect(
            "Ciclos formativos *", ciclos_lista, key=f"{k}_ciclos", placeholder="Selecciona ciclos",
        )
        alumnos, puestos = {}, {}
        for ciclo in ciclos_sel:
            st.markdown(f"🎓 **{ciclo}**")
            alumnos[ciclo] = st.number_input(
                "Cantidad de alumnos *", min_value=1, max_value=50, value=1, step=1,
                key=f"{k}_alumnos_{slug(ciclo)}",
            )
            areas = st.multiselect(
                "Puestos / áreas *", areas_map.get(ciclo, []),
                key=f"{k}_areas_{slug(ciclo)}", placeholder="Selecciona áreas",
            )
            puestos[ciclo] = [
                {"area": area, "proyecto": st.text_input(
                    f"Proyecto relacionado ({area})", key=f"{k}_proy_{slug(ciclo)}_{slug(area)}",
                ).strip()}
                for area in areas
            ]

        st.markdown("**Dirección del centro de trabajo**")
        direccion = st.text_input("Dirección", value=empresa.get("direccion") or "", key=f"{k}_dir")
        col_cp, col_loc = st.columns(2)
        with col_cp:
            cp = st.text_input("Código Postal", value=empresa.get("codigo_postal") or "", key=f"{k}_cp")
        with col_loc:
            localidad = st.text_input("Localidad", value=empresa.get("localidad") or "", key=f"{k}_loc")

        st.markdown("**Requisitos adicionales**")
        requisitos = render_requisitos(
            f"{k}_req", idiomas_label="Idiomas", skills_label="Skills",
            otros_label="Otros requisitos (por ejemplo, residencia)",
        )

        st.markdown("**Información adicional**")
        contrato = st.radio(
            "Si el alumno cubre vuestras expectativas, ¿habría posibilidad de hacerle un contrato laboral? *",
            ["Sí", "No"], index=None, horizontal=True, key=f"{k}_contrato",
        )
        vehiculo = st.radio(
            "¿Se necesita vehículo propio para acceder a vuestras instalaciones? *",
            ["Sí", "No"], index=None, horizontal=True, key=f"{k}_vehiculo",
        )

        faltan = []
        if not ciclos_sel:
            faltan.append("ciclos formativos")
        faltan += [f"área en {c}" for c in ciclos_sel if not puestos.get(c)]
        if contrato is None:
            faltan.append("posible contrato")
        if vehiculo is None:
            faltan.append("vehículo")
        if faltan:
            st.info("Completa los campos obligatorios: " + ", ".join(faltan))

        col_ok, col_no = st.columns([1, 1])
        with col_ok:
            guardar = st.button("💾 Crear oferta", type="primary", key=f"{k}_guardar", disabled=bool(faltan))
        with col_no:
            if st.button("Cancelar", key=f"{k}_cancelar"):
                _cerrar_nueva_oferta()
                st.rerun()

        if guardar:
            campos = {
                "anio": anio,
                "puestos": puestos,
                "direccion_empresa": direccion.strip(),
                "cp_empresa": cp.strip(),
                "localidad_empresa": localidad.strip(),
                "requisitos": requisitos,
                "contrato": contrato,
                "vehiculo": vehiculo,
            }
            if tutor_id is not None:
                campos["tutor"] = tutor_id
            try:
                crearOfertaEmpresa(empresa["CIF"], alumnos, campos)
            except Exception as e:
                st.error(f"No se pudo crear la oferta: {e}")
                return
            _cerrar_nueva_oferta()
            st.toast("Oferta creada", icon="✅")
            st.rerun()


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
# --- Traer todas las empresas ---
anioFiltro = aniosList[st.session_state.get("index_academic", 0)]
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
    practicaTodas = getPracticas(practicaTabla, {"empresa": cif, "anio": anioFiltro})
    practicas = [
        p for p in practicaTodas 
        if p.get("status") not in [ estadosPractica[5]]
    ]
    tutores = getEquals(tutoresTabla, {'cif_empresa': cif})
    
    st.session_state["practicas"] = practicas
    st.session_state["tutores"] = tutores
    return practicas, tutores

@st.cache_data(ttl=180, show_spinner=False)
def list_drive_files_cached(folder_name):
    return list_drive_files(folder_name)

if not empresas:
    st.warning("No encontramos tu empresa")
    st.stop()

df_empresas = pd.DataFrame(empresas)
df_empresas = df_empresas[df_empresas["CIF"] != "00000000"]
fetch_practicas_tutores()
practicas = st.session_state["practicas"]
tutores = st.session_state["tutores"]

# --- Tabs principales ---
tabEmpresa, tabOferta,tabPractica, tabTutores = st.tabs(["Mi Empresa", "Ofertas", "Formaciones", "Tutores"])

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

                st.toast("Empresa actualizada correctamente",duration='short', icon="✅"); 

    
with tabOferta:
        CICLOS_LISTA, AREAS_MAP = getCiclosYAreas()
 # --- Mostrar FP asociadas ---
        anioFiltro = aniosList[st.session_state.get("index_academic", 0)]

        fps = getEquals(necesidadFP, {"empresa": empresa["CIF"], "anio": anioFiltro})
        if anioFiltro != aniosList[0]: 
            fps = [p for p in fps if p.get("anio") == anioFiltro]
        st.subheader(f"Formaciones ofrecidas")

        if not st.session_state.get(f"{NUEVA}_abierta"):
            if st.button("➕ Agregar oferta", type="primary", key="btn_agregar_oferta"):
                st.session_state[f"{NUEVA}_abierta"] = True
                st.rerun()
        else:
            if st.session_state.tutores is None:
                st.session_state.tutores = getEquals(tutoresTabla, {"cif_empresa": cif})
            nueva_oferta(empresa, CICLOS_LISTA, AREAS_MAP, st.session_state.tutores or [], anioFiltro)

        if str(anioFiltro).strip().lower() == "seleccionar":
                anioFiltroLink = aniosList[1]
        else:
                anioFiltroLink = anioFiltro
        if fps:
            for i, fp in enumerate(fps, start=1):
                with st.expander(
                    f"Oferta #{i} | Fecha: {pd.to_datetime(fp.get('created_at')).strftime('%d/%m/%Y')}",
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
                        st.dataframe(df_ciclos, hide_index=True, width='stretch')

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

                    st.write(f"**Contrato:** {_si_no(fp.get('contrato'))}")
                    st.write(f"**Vehículo:** {_si_no(fp.get('vehiculo'))}")

                    st.divider()
                    puede_eliminar = ofertaSinAsignaciones(fp)
                    col_edit, col_del = st.columns([3, 1])
                    with col_edit:
                        # Close the editor after a save (the toggle can only be reset before it's drawn)
                        if st.session_state.pop(f"oferta_{fp['id']}_cerrar_edicion", False):
                            st.session_state[f"oferta_{fp['id']}_editar"] = False
                        editando = st.toggle("✏️ Editar oferta", key=f"oferta_{fp['id']}_editar")
                    with col_del:
                        if st.button(
                            "🗑️ Eliminar oferta", key=f"eliminar_oferta_{fp['id']}",
                            disabled=not puede_eliminar,
                            help=None if puede_eliminar else "No se puede eliminar: ya hay alumnos asignados a esta oferta.",
                        ):
                            dialog_eliminar_oferta(fp, i)
                    if editando:
                        editar_oferta(fp, AREAS_MAP)

        else:
           st.info('No hay necesidades FP registradas para esta empresa o para el filtro seleccionado')     
  
with tabTutores:
        st.subheader("Tutores")
        st.caption('Aquí puedes administrar los tutores de tu empresa. Agrega, modifica o elimina usando la tabla, posiciona el ratón sobre la tabla y podrás ver las opciones. Luego preciona "Actualizar Tutores"')
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
                            width='stretch'
                        )
        with st.spinner("⏳ procesando tutores, por favor espera..."):
            if st.button("Actualizar Tutores"):
                cambios = st.session_state["editor_tutores"]
                if cambios["edited_rows"] or cambios["added_rows"] or cambios["deleted_rows"]:
                    try:
                        for row in cambios["added_rows"]:
                            nombre = row.get("nombre", "Sin Nombre").strip()
                            email = row.get("email", "").strip()
                            if not email or "@" not in email:
                                st.error(f"Email inválido para {nombre}, , corrobore que no tiene filas vacias, si las tiene eliminelas"); st.stop()
                        
                        res = updateTutores(cambios, df_tutores, cif=cif)
                        st.toast("Guardado",duration='short', icon="✅"); 
                        st.rerun()
                    except Exception as e:
                        st.error(f"Error: {e}")

def mostrarLista():
    if st.button("🔄 Actualizar", key="btn_refresh"):
            st.session_state["force_reload"] = True
            st.rerun()
    if not practicas:
        st.info("No tienes Formaciones asignadas aun o no existen para el curso académico o curso seleccionado.")
    else:
        data_for_grid = []
        for p in practicas:
            anioFiltro = aniosList[st.session_state.get("index_academic", 0)]
            if st.session_state.get("index_academic", 0)>0 and p.get("anio", []) != anioFiltro:
                continue
            pid = p["id"]
            estados_p =  p.get("status", [])
            data_for_grid.append({
                "ID": pid,
                "Alumno": f"{p.get('alumnos', {}).get('nombre')} {p.get('alumnos', {}).get('apellido')}",
                "Empresa": p.get('empresas', {}).get('nombre'),
                "Estado": estados_p,
                "Fecha Inicio": p.get('fecha_inicio', '—'),
                "Fecha Fin": p.get('fecha_fin', '—'),
                "Ciclo": p.get('ciclo_formativo', '—'),
                "Tutor Empresa": p.get('tutor', 'Sin asignar'),
                "Gestor": p.get('gestor', 'Sin asignar')
            })

        df = pd.DataFrame(data_for_grid)

        if df.empty:
            st.info("No hay Formaciones asignadas aun para el curso académico seleccionado.")
        else:
            # 2. Configurar AgGrid
            gb = GridOptionsBuilder.from_dataframe(df)
            gb.configure_grid_options(localeText=locale_tabla_principal)
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
                allow_unsafe_html=True
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
        st.session_state.page = "lista"
        st.rerun()
   

    p["oferta_fp"] = p.get("oferta_fp") or {}
    p["empresas"] = p.get("empresas") or {}
    p["alumnos"] = p.get("alumnos") or {}
    oferta = p["oferta_fp"]
    empresa = p["empresas"]
    alumno = p["alumnos"]
    folder_name= folderNamePractica(alumno['nombre'],alumno['apellido'], alumno['dni'], empresa['nombre'])
    st.title(f"{alumno['nombre']} {alumno['apellido']} – {empresa['nombre']}")
    seccion_detalle(alumno, empresa, p, oferta)
    seccion_planificacion(alumno, empresa, p)
    seccion_documentos(folder_name,alumno, p)
    if st.button("⬅ Volver",type="primary"):
        st.session_state.page = "lista"
        st.rerun()

def seccion_detalle(alumno, empresa, p, oferta):
        if p.get("status") == estadosPractica[3]:
            st.error(f"ℹ️ **Estado:** {p.get('status')} — **Motivo:** {p.get('motivo') or 'No especificado'}", icon="🚀")
            
        else:
            st.info(f"ℹ️ **Estado:** {p.get('status')}", icon="🚀")
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
            st.write(f"**Curso Académico:** {p.get('anio', '—')}")  
            st.write(f"**Curso:** {p.get('curso', '—')}")  
            gestor_actual = p.get("gestor")
            st.write(f"**Gestor:** {gestor_actual}")

        with col2:
            st.write(f"**Empresa:** {empresa['nombre']}")
            st.write(f"**CIF:** {empresa['CIF']}")
            direccion = oferta.get("direccion_empresa") or empresa['direccion']
            st.write(f"**Dirección formación:** {direccion}") 
            localidad = oferta.get("localidad_empresa") or empresa['localidad']
            st.write(f"**Localidad:** {localidad}")

            lista_nombres_tutores = [g["nombre"] for g in tutores]
            if "No asignado" not in lista_nombres_tutores:
                lista_nombres_tutores.insert(0, "No asignado")
            tutor_actual = p.get("tutor") 
            indice_tutor = lista_nombres_tutores.index(tutor_actual) if tutor_actual in lista_nombres_tutores else 0
            clave_tutor = f"tutor_{alumno['id']}"
            if p.get("status") in [ estadosPractica[3] , estadosPractica[2]]:
                st.write(f"**Tutor Empresa:** {tutor_actual or 'No asignado'}")
            else:
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

def seccion_planificacion(alumno, empresa, practica):
        st.subheader("📅 Planificación de Formaciones")
        practicaId = practica.get("id")
        cancelada_finalizada = practica.get("status") == estadosPractica[3] or practica.get("status") == estadosPractica[2]
        folder_name= folderNamePractica(alumno['nombre'],alumno['apellido'], alumno['dni'], empresa['nombre'])
        files = list_drive_files(folder_name)
        archivo_calendario = next((f for f in files[0] if "calendario" in f['name']), None)

        if cancelada_finalizada:
            if archivo_calendario and archivo_calendario.get('id'):
                preview_url = f"https://drive.google.com/file/d/{archivo_calendario.get('id')}/preview"
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
                st.info("No hay calendario subido para esta formación.")
            return

        with st.expander("Generar Calendario", expanded=False):
            col_cal1, col_cal2 = st.columns([1, 1.5]) # Ajustamos el ancho para la imagen
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
                            upload_to_drive(str(temp_path), carpetaPractica, folder_name,original_name)
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
                    
                    st.link_button("Abrir imagen completa", archivo_calendario.get('webViewLink'),width='stretch')
                else:
                    st.markdown(
                        """
                        <div style="border: 2px dashed #ccc; border-radius: 10px; height: 500px; display: flex; align-items: center; justify-content: center; color: #aaa;">
                            Esperando archivo de calendario (PNG/JPG)...
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
              
                # else:
                #     st.write("No han subido calendario aun")
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
with tabPractica:
    if st.session_state.page == "lista":
        mostrarLista()
    else:
        mostrar_detalle()

