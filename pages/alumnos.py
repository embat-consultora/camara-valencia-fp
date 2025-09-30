import streamlit as st
import pandas as pd
import os
import json
from modules.data_base import get, update, upsert, getEquals,getEqual
from page_utils import apply_page_config
from navigation import make_sidebar
from variables import alumnosTabla, estadosAlumno, formFieldsTabla,fasesAlumno,alumnoEstadosTabla,fase2colEmpresa
from datetime import datetime
from modules.grafico_helper import mostrar_fases
apply_page_config()
make_sidebar()

st.set_page_config(page_title="Alumnos", page_icon="🧑‍🎓")
st.markdown(
    "<h2 style='text-align: center;'>ALUMNOS</h2>",
    unsafe_allow_html=True
)

base_url = os.getenv("URL")

# --- Traer alumnos ---
alumnos = get(alumnosTabla)
if not alumnos:
    st.warning("No hay alumnos registrados")
    st.stop()

df_alumnos = pd.DataFrame(alumnos)

# --- Tabs principales ---
tab1, tab2, tab3 = st.tabs(["🔍 Buscar / Visualizar", "➕ Nuevo Alumno", "📋 Formulario & Contacto"])

# -------------------------------------------------------------------
# TAB 1: Buscar / Visualizar / Editar
# -------------------------------------------------------------------
with tab1:
    col1, col2 = st.columns([3, 2])
    with col1:
        search = st.text_input("Buscar alumnos")
    with col2:
        st.metric("Total alumnos", len(df_alumnos))

    if search:
        mask = df_alumnos.astype(str).apply(
            lambda row: row.str.contains(search, case=False, na=False).any(),
            axis=1
        )
        df_alumnos = df_alumnos[mask]

    # Vista resumida
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

    # Selección de alumno
    if not df_alumnos.empty:
        alumnos_options = {"Ninguno": None}
        for _, row in df_alumnos.iterrows():
            alumnos_options[f"{row['apellido']}, {row['nombre']}"] = row["id"]

        selected_name = st.selectbox("Seleccionar alumno", list(alumnos_options.keys()), index=0)

        if alumnos_options[selected_name]:
            alumno_id = alumnos_options[selected_name]
            alumno = df_alumnos[df_alumnos["id"] == alumno_id].iloc[0].to_dict()
            estadosAlumnos = getEqual(alumnoEstadosTabla, "alumno", alumno["NIA"])
            st.subheader(f"Seguimiento - {alumno['nombre']}")
            if not estadosAlumnos:
                mostrar_fases(fasesAlumno, fase2colEmpresa, None)
                estado_actual = {}
            else:
                mostrar_fases(fasesAlumno, fase2colEmpresa, estadosAlumnos[0])
                estado_actual = estadosAlumnos[0]

            # --- Checkboxes dinámicos para cada fase ---
            cols = st.columns(len(fasesAlumno))

            for i, fase in enumerate(fasesAlumno):
                col = fase2colEmpresa[fase]
                valor_actual = True if estado_actual.get(col) else False

                with cols[i]:
                    checked = st.checkbox(fase, value=valor_actual, key=f"{alumno['NIA']}_{col}")

                if checked != valor_actual:  # solo si cambió
                    if checked:
                        new_value = datetime.now().isoformat()
                    else:
                        new_value = None

                    upsert(
                        alumnoEstadosTabla,
                        {"alumno": alumno["NIA"], col: new_value},
                        keys=["alumno"]
                    )
                    st.success(f"Estado actualizado: {fase} → {new_value if new_value else '❌'}")
                    st.rerun()
            subtab1, subtab2 = st.tabs([f"✏️ Detalle: {alumno['nombre']} {alumno['apellido']}",
                                        "📌 Preferencias FP"])

            # --- Detalle / edición ---
            with subtab1:
                st.write("Edita los datos y guarda para actualizar:")

                new_nombre = st.text_input("Nombre", alumno.get("nombre", ""))
                new_apellido = st.text_input("Apellido", alumno.get("apellido", ""))
                new_direccion = st.text_input("Dirección", alumno.get("direccion", ""))
                new_localidad = st.text_input("Localidad", alumno.get("localidad", ""))
                new_nia = st.text_input("NIA", alumno.get("NIA", ""))
                new_telefono = st.text_input("Teléfono", alumno.get("telefono", ""))
                new_email = st.text_input("Email", alumno.get("email_alumno", ""))

                vehiculo_val = alumno.get("vehiculo")
                vehiculo_bool = True if vehiculo_val == "Sí" else False
                new_vehiculo = st.checkbox("Vehículo", value=vehiculo_bool)

                if st.button("💾 Actualizar alumno"):
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

            # --- Preferencias FP ---
            with subtab2:
                estado_actual = alumno.get("estado") or "Activo"
                estado_map = {
                    "Activo": "⚪",
                    "Cancelado": "🔴",
                    "En progreso": "🟢",
                    "Finalizado": "🔵"
                }
                icono = estado_map.get(estado_actual, "⚪")
                st.write(f"**Estado actual:** {icono} {estado_actual}")

                # Obtener opciones de form_fields
                form_fields = getEquals(formFieldsTabla, {"category": "Alumno", "type": "Opciones"})
                ciclo_field = next((f for f in form_fields if f["columnName"] == "ciclo_formativo"), None)
                pref_field = next((f for f in form_fields if f["columnName"] == "preferencias_fp"), None)

                ciclos_opts = json.loads(ciclo_field["options"]) if ciclo_field else []
                prefs_opts_dict = json.loads(pref_field["options"]) if pref_field else {}

                current_ciclos = alumno.get("ciclo_formativo") or []
                current_prefs = alumno.get("preferencias_fp") or []

                selected_ciclos = st.multiselect(
                    "Ciclo Formativo",
                    options=ciclos_opts,
                    default=current_ciclos,
                    placeholder="Selecciona uno o más ciclos"
                )
                selected_prefs = []
                for ciclo in selected_ciclos:
                    if ciclo in prefs_opts_dict:
                        selected_prefs.extend(
                            st.multiselect(
                                f"Preferencias para {ciclo}",
                                options=prefs_opts_dict[ciclo],
                                default=[p for p in current_prefs if p in prefs_opts_dict[ciclo]]
                            )
                        )

                vehiculo_selected = st.checkbox("Vehículo", value=vehiculo_bool,key="vehiculo_pref")

                if estado_actual in estadosAlumno:
                    default_index = estadosAlumno.index(estado_actual)
                else:
                    default_index = 0

                estado = st.selectbox("Estado", options=estadosAlumno, index=default_index)
                motivo_cancelacion = None
                if estado == "Cancelado":
                    motivo_cancelacion = st.text_area("Motivo de cancelación", value=alumno.get("motivo") or "")

                if st.button("💾 Guardar preferencias"):
                    data_to_update = {
                        "NIA": alumno["NIA"],
                        "estado": estado,
                        "motivo": motivo_cancelacion,
                        "ciclo_formativo": selected_ciclos,
                        "preferencias_fp": selected_prefs,
                        "vehiculo": "Sí" if vehiculo_selected else "No"
                    }
                    upsert(alumnosTabla, data_to_update, keys=["NIA"])
                    st.success("Preferencias actualizadas")
                    st.rerun()

# -------------------------------------------------------------------
# TAB 2: Nuevo Alumno
# -------------------------------------------------------------------
with tab2:
    st.subheader("➕ Nuevo Alumno")

    with st.form("form_nuevo_alumno"):
        new_nombre = st.text_input("Nombre")
        new_apellido = st.text_input("Apellido")
        new_direccion = st.text_input("Dirección")
        new_localidad = st.text_input("Localidad")
        new_nia = st.text_input("NIA")
        new_telefono = st.text_input("Teléfono")
        new_email = st.text_input("Email")
        new_vehiculo = st.checkbox("Vehículo")

        submitted = st.form_submit_button("Crear Alumno")
        if submitted:
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
                }, keys=["NIA"]
            )
            st.success("Nuevo alumno agregado correctamente")
            st.rerun()

# -------------------------------------------------------------------
# TAB 3: Formulario Alumno
# -------------------------------------------------------------------
with tab3:
    st.subheader("📨 Formularios & Contacto")
    col1, col2 = st.columns(2)
    formUrlAlumno = os.getenv("FORM_ALUMNO")
    with col1:
        st.markdown(f"📋 [Formulario Alumno]({formUrlAlumno})")
    with col2:
        st.page_link("pages/emails.py", label="✉️ Contactar Alumnos")
