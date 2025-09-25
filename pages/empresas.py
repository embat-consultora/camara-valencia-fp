import streamlit as st
import pandas as pd
import os
from modules.data_base import get, getEqual, update,upsert
from page_utils import apply_page_config
from navigation import make_sidebar
from variables import empresasTabla, necesidadFP,estados

apply_page_config()
make_sidebar()

st.set_page_config(page_title="Empresas", page_icon="🏢")
st.title("Empresas")
base_url = os.getenv("URL")
# --- Traer todas las empresas ---
empresas = get(empresasTabla)
if not empresas:
    st.warning("No hay empresas registradas")
    st.stop()

df_empresas = pd.DataFrame(empresas)

# --- Filtro por nombre ---
col1, col2 = st.columns([2, 6])
with col1:
    search = st.text_input("Buscar por nombre de empresa")
if search:
    df_empresas = df_empresas[df_empresas["nombre"].str.contains(search, case=False, na=False)]

# --- Columnas a mostrar con nombres bonitos ---
cols_map = {
    "CIF": "CIF",
    "nombre": "Nombre",
    "direccion": "Dirección",
    "localidad": "Localidad",
    "telefono": "Teléfono",
    "email_empresa": "Email"
}
df_view = df_empresas[list(cols_map.keys())].rename(columns=cols_map)
st.dataframe(df_view, hide_index=True, use_container_width=True)

# --- Selección de empresa ---
if not df_empresas.empty:
    empresa_options = {row["nombre"]: row["id"] for _, row in df_empresas.iterrows()}
    col1, col2 = st.columns([3, 7])
    with col1: 
        selected_name = st.selectbox("Seleccionar empresa", list(empresa_options.keys()))
    empresa_id = empresa_options[selected_name]

    empresa = df_empresas[df_empresas["id"] == empresa_id].iloc[0].to_dict()

    with st.expander(f"Detalle de empresa: {empresa['nombre']}", expanded=False):
        st.write("Edita los datos y guarda para actualizar:")

        new_nombre = st.text_input("Nombre", empresa.get("nombre", ""))
        new_direccion = st.text_input("Dirección", empresa.get("direccion", ""))
        new_localidad = st.text_input("Localidad", empresa.get("localidad", ""))
        new_cif = st.text_input("CIF", empresa.get("CIF", ""))
        new_telefono = st.text_input("Teléfono", empresa.get("telefono", ""))
        new_email = st.text_input("Email", empresa.get("email_empresa", ""))

        if st.button("Actualizar empresa"):
            update(
                empresasTabla,
                {
                    "nombre": new_nombre,
                    "direccion": new_direccion,
                    "localidad": new_localidad,
                    "CIF": new_cif,
                    "telefono": new_telefono,
                    "email_empresa": new_email
                },
                "id",
                empresa_id
            )
            st.success("Empresa actualizada correctamente")
            st.rerun()

    # --- Mostrar FP asociadas por CIF ---
    fps = getEqual(necesidadFP, "empresa", empresa["CIF"])
    st.subheader(f"Oferta FP - {empresa['nombre']}")

    if fps:
        for i, fp in enumerate(fps, start=1):
            estado_actual = fp.get("estado") or "Activo"
            bg_color = "🟢" if estado_actual == "Activo" else "🔴"
          

            with st.expander(f"Oferta #{i}  - Fecha: {pd.to_datetime(fp.get("created_at")).strftime("%d/%m/%Y")}  - {estado_actual} - {bg_color}", expanded=False):
                ciclos = fp.get("ciclos_formativos")
                if ciclos:
                    st.markdown("**Ciclos formativos y cantidad de alumnos:**")
                    df_ciclos = pd.DataFrame(list(ciclos.items()), columns=["Ciclo", "Cantidad Alumnos"])
                    st.dataframe(df_ciclos, hide_index=True, use_container_width=True)

                # --- Áreas (lista de strings)
                areas = fp.get("areas")
                if areas:
                    st.markdown("**Áreas:**")
                    for area in areas:
                        st.markdown(f"- {area}")

                # --- Proyectos y requisitos (strings)
                proyectos = fp.get("proyectos")
                requisitos = fp.get("requisitos")
                if proyectos:
                    st.markdown(f"**Proyectos:** {proyectos}")
                if requisitos:
                    st.markdown(f"**Requisitos:** {requisitos}")

                # --- Contrato y vehículo (si/no)
                contrato = fp.get("contrato")
                vehiculo = fp.get("vehiculo")
                st.write(f"**Contrato:** {'Sí' if contrato else 'No'}")
                st.write(f"**Vehículo:** {'Sí' if vehiculo else 'No'}")

                if estado_actual in estados:
                    default_index = estados.index(estado_actual)
                else:
                    default_index = 0
                col1, col2, col3 = st.columns(3)
                with col1:
                    estado = st.selectbox("Estado", options=estados, index=default_index)
                    motivo_cancelacion = None
                    if estado == "Cancelado":
                        motivo_cancelacion = st.text_area("Motivo de cancelación", value=fp.get("motivo") or "")
                if st.button("Guardar"):
                    upsert(necesidadFP,{"empresa": empresa["CIF"],"estado": estado, "motivo": motivo_cancelacion, "id": fp["id"]})
                    st.success("Actualizado")
                    st.rerun()
    else:
        st.info(
            'No hay necesidades FP registradas para esta empresa. '
            f"Mandale el link para que nos avise de necesidades nuevas: [Formulario]({base_url}forms?form=1)"
        )
        
