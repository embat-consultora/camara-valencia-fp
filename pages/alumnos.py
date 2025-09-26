import streamlit as st
import pandas as pd
import os
import json
from modules.data_base import get, update, upsert,getEquals
from page_utils import apply_page_config
from navigation import make_sidebar
from variables import alumnosTabla, estadosAlumno, formFieldsTabla

apply_page_config()
make_sidebar()

st.set_page_config(page_title="Alumnos", page_icon="🧑‍⚕️")
st.title("Alumnos")
base_url = os.getenv("URL")

# --- Inicializar estado ---
if "show_add_form" not in st.session_state:
    st.session_state.show_add_form = False

alumnos = get(alumnosTabla)
if not alumnos:
    st.warning("No hay alumnos registrados")
    st.stop()

df_alumnos = pd.DataFrame(alumnos)

# --- Filtro por nombre ---
col1, col2, col3 = st.columns([2, 3, 2])
with col1:
    search = st.text_input("Buscar alumnos")
with col3:
    if st.button("➕ Agregar Alumno"):
        st.session_state.show_add_form = True
if search:
    mask = df_alumnos.astype(str).apply(
        lambda row: row.str.contains(search, case=False, na=False).any(),
        axis=1
    )
    df_alumnos = df_alumnos[mask]

# --- Columnas a mostrar con nombres bonitos ---
cols_map = {
    "NIA": "NIA",
    "nombre": "Nombre",
    "apellido": "Apellido",
    "direccion": "Dirección",
    "localidad": "Localidad",
    "telefono": "Teléfono",
    "email_alumno": "Email",
    "vehiculo": "Vehículo"
}
df_view = df_alumnos[list(cols_map.keys())].rename(columns=cols_map)
st.dataframe(df_view, hide_index=True, use_container_width=True)

# --- Formulario de nuevo alumno ---
if st.session_state.show_add_form:
    st.subheader("Nuevo Alumno")
    new_nombre = st.text_input("Nombre")
    new_apellido = st.text_input("Apellido")
    new_direccion = st.text_input("Dirección")
    new_localidad = st.text_input("Localidad")
    new_nia = st.text_input("NIA")
    new_telefono = st.text_input("Teléfono")
    new_email = st.text_input("Email")
    new_vehiculo = st.checkbox("Vehículo")
    col_guardar, col_cancelar = st.columns(2)
    with col_guardar:
        if st.button("Guardar Nuevo Alumno"):
            upsert(
                alumnosTabla,
                {
                    "nombre": new_nombre,
                    "apellido": new_apellido,
                    "direccion": new_direccion,
                    "localidad": new_localidad,
                    "NIA": new_nia,
                    "telefono": new_telefono,
                    "email_alumno": new_email,
                    "vehiculo": "Sí" if new_vehiculo else "No",
                    "estado": "Activo"
                }
            )
            st.success("Nuevo alumno agregado correctamente")
            st.session_state.show_add_form = False
            st.rerun()
    with col_cancelar:
        if st.button("Cancelar"):
            st.session_state.show_add_form = False
            st.rerun()

# --- Selección de alumno existente ---
if not df_alumnos.empty and not st.session_state.show_add_form:
    alumnos_options = {"Ninguno": None}
    for _, row in df_alumnos.iterrows():
        alumnos_options[f"{row['apellido']}, {row['nombre']}"] = row["id"]

    col1, col2, col3 = st.columns([2, 3, 3])
    with col1:
        selected_name = st.selectbox("Ver detalle alumno", list(alumnos_options.keys()), index=0)

    if alumnos_options[selected_name]:
        alumno_id = alumnos_options[selected_name]
        alumno = df_alumnos[df_alumnos["id"] == alumno_id].iloc[0].to_dict()

        tab1, tab2 = st.tabs([f"Detalle: {alumno['nombre']} {alumno['apellido']}",
                              f"Preferencias FP"])

        with tab1:
            st.write("Edita los datos y guarda para actualizar:")
            new_nombre = st.text_input("Nombre", alumno.get("nombre", ""))
            new_apellido = st.text_input("Apellido", alumno.get("apellido", ""))
            new_direccion = st.text_input("Dirección", alumno.get("direccion", ""))
            new_localidad = st.text_input("Localidad", alumno.get("localidad", ""))
            new_nia = st.text_input("NIA", alumno.get("NIA", ""))
            new_telefono = st.text_input("Teléfono", alumno.get("telefono", ""))
            new_email = st.text_input("Email", alumno.get("email_alumno", ""))

            if st.button("Actualizar alumno"):
                update(
                    alumnosTabla,
                    {
                        "nombre": new_nombre,
                        "apellido": new_apellido,
                        "direccion": new_direccion,
                        "localidad": new_localidad,
                        "NIA": new_nia,
                        "telefono": new_telefono,
                        "email_alumno": new_email,
                        "vehiculo": "Sí" if new_vehiculo else "No",
                    },
                    "id",
                    alumno_id
                )
                st.success("Alumno actualizado correctamente")
                st.rerun()

        with tab2:
            estado_actual = alumno.get("estado") or "Activo"
            estado_map = {
                "Activo": "⚪",
                "Cancelado": "🔴",
                "En progreso": "🟢",
                "Finalizado": "🔵"
            }
            icono = estado_map.get(estado_actual, "⚪")
            st.write(f"**Estado actual:** {icono} {estado_actual}")

            # --- Obtener campos de preferencias desde form_fields ---
            form_fields = getEquals(formFieldsTabla, {"category": "Alumno", "type": "Opciones"})

            # Parsear ciclos y preferencias
            ciclo_field = next((f for f in form_fields if f["columnName"] == "ciclo_formativo"), None)
            pref_field = next((f for f in form_fields if f["columnName"] == "preferencias_fp"), None)

            ciclos_opts = json.loads(ciclo_field["options"]) if ciclo_field else []
            prefs_opts_dict = json.loads(pref_field["options"]) if pref_field else {}

            # Valores actuales del alumno
            current_ciclos = alumno.get("ciclo_formativo") or []
            current_prefs = alumno.get("preferencias_fp") or []

            # Selección de ciclos
            selected_ciclos = st.multiselect(
                "Ciclo Formativo",
                options=ciclos_opts,
                default=current_ciclos,placeholder=
                "Selecciona uno o más ciclos"
            )
            st.markdown("**Seleccionados:**")
            for c in selected_ciclos:
                st.markdown(f"- {c}")
            # Preferencias filtradas según los ciclos seleccionados
            opciones_pref_filtradas = []
            for ciclo in selected_ciclos:
                if ciclo in prefs_opts_dict:
                    opciones_pref_filtradas.extend(prefs_opts_dict[ciclo])

            selected_prefs = st.multiselect(
                "Preferencias profesionales",
                options=opciones_pref_filtradas,
                default=[p for p in current_prefs if p in opciones_pref_filtradas],
                placeholder="Selecciona las preferencias"
            )
            st.markdown("**Preferencias seleccionadas:**")
            for p in selected_prefs:
                st.markdown(f"- {p}")
            # Vehículo
            vehiculo_val = alumno.get("vehiculo")
            vehiculo_bool = True if vehiculo_val == "Sí" else False

            vehiculo_selected = st.checkbox("Vehículo", value=vehiculo_bool)

            # Estado
            if estado_actual in estadosAlumno:
                default_index = estadosAlumno.index(estado_actual)
            else:
                default_index = 0

            col1, col2, col3 = st.columns(3)
            with col1:
                estado = st.selectbox("Estado", options=estadosAlumno, index=default_index)
                motivo_cancelacion = None
                if estado == "Cancelado":
                    motivo_cancelacion = st.text_area("Motivo de cancelación", value=alumno.get("motivo") or "")

            if st.button("Guardar"):
                data_to_update = {
                    "NIA": alumno["NIA"],
                    "estado": estado,
                    "motivo": motivo_cancelacion,
                    "ciclo_formativo": selected_ciclos,
                    "preferencias_fp": selected_prefs,
                    "vehiculo": "Sí" if vehiculo_selected else "No"
                }
                upsert(alumnosTabla, data_to_update)
                st.success("Actualizado")
                st.rerun()
