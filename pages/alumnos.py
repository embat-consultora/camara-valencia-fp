import streamlit as st
import pandas as pd
import os
from modules.data_base import get, update,upsert
from page_utils import apply_page_config
from navigation import make_sidebar
from variables import alumnosTabla,estadosAlumno

apply_page_config()
make_sidebar()

st.set_page_config(page_title="Alumnos", page_icon="🧑‍⚕️")
st.title("Alumnos")
base_url = os.getenv("URL")

alumnos = get(alumnosTabla)
if not alumnos:
    st.warning("No hay alumnos registrados")
    st.stop()

df_alumnos = pd.DataFrame(alumnos)

# --- Filtro por nombre ---
col1, col2 = st.columns([2, 6])
with col1:
    search = st.text_input("Buscar por nombre de alumnos")
if search:
    df_alumnos = df_alumnos[df_alumnos["nombre"].str.contains(search, case=False, na=False)]

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


if not df_alumnos.empty:
    alumnos_options = {row["apellido"]: row["id"] for _, row in df_alumnos.iterrows()}
    col1, col2 = st.columns([3, 7])
    with col1: 
        selected_name = st.selectbox("Seleccionar alumno", list(alumnos_options.keys()))
    alumno_id = alumnos_options[selected_name]

    alumno = df_alumnos[df_alumnos["id"] == alumno_id].iloc[0].to_dict()

    with st.expander(f"Detalle del alumno: {alumno['nombre']} {alumno['apellido']}", expanded=False):
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
                    "email_alumno": new_email
                },
                "id",
                alumno_id
            )
            st.success("Alumno actualizada correctamente")
            st.rerun()

    estado_actual = alumno.get("estado") or "Activo"
    estado_map = {
        "Activo": "⚪",        # amarillo
        "Cancelado": "🔴",     # rojo
        "En progreso": "🟢",   # verde
        "Finalizado": "🔵"     # azul
    }
    icono = estado_map.get(estado_actual, "⚪") 
    with st.expander(f"Preferencias FP - {alumno['nombre']} {alumno['apellido']} - {icono} "):
        ciclos = alumno.get("ciclo_formativo")
        if ciclos:
            st.markdown("**Ciclos Formativos:**")
            for ciclo in ciclos:
                st.markdown(f"- {ciclo}")

        # --- Áreas (lista de strings)
        areas = alumno.get("preferencias_fp")
        if areas:
            st.markdown("**Áreas:**")
            for area in areas:
                st.markdown(f"- {area}")

        vehiculo = alumno.get("vehiculo")
        st.write(f"**Vehículo:** {'Sí' if vehiculo else 'No'}")
        estado_actual = alumno.get("estado")
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
            upsert(alumnosTabla,{"estado": estado, "motivo": motivo_cancelacion, "NIA": alumno["NIA"]})
            st.success("Actualizado")
            st.rerun()

else:
    st.info(
        'Este alumno no tiene preferencias.'
        f"Mandale el link para que nos avise de preferencias nuevas: [Formulario]({base_url}forms?form=2)"
    )
    
