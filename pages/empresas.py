import streamlit as st
import pandas as pd
import os
from modules.data_base import get, getEqual, update, upsert
from page_utils import apply_page_config
from navigation import make_sidebar
from variables import empresasTabla, necesidadFP, estados,fasesEmpresa, empresaEstadosTabla,fase2colEmpresa
from modules.grafico_helper import mostrar_fases

apply_page_config()
make_sidebar()

st.set_page_config(page_title="Empresas", page_icon="🏢")
st.markdown(
    "<h2 style='text-align: center;'>EMPRESAS</h2>",
    unsafe_allow_html=True
)

base_url = os.getenv("URL")

# --- Traer todas las empresas ---
empresas = get(empresasTabla)
if not empresas:
    st.warning("No hay empresas registradas")
    st.stop()

df_empresas = pd.DataFrame(empresas)

# --- Tabs principales ---
tab1, tab2, tab3 = st.tabs(["🏢 Buscar/Visualizar", "➕ Nueva Empresa", "📨 Formularios & Contacto"])

# -------------------------------------------------------------------
# TAB 1: Buscar y visualizar empresas
# -------------------------------------------------------------------
with tab1:
    col1, col2 = st.columns([3, 2])
    with col1:
        search = st.text_input("🔍 Buscar por nombre de empresa")
    with col2:
        st.metric("Total Empresas", len(df_empresas))

    if search:
        df_empresas = df_empresas[df_empresas["nombre"].str.contains(search, case=False, na=False)]

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

    if not df_empresas.empty:
        empresa_options = {row["nombre"]: row["id"] for _, row in df_empresas.iterrows()}
        selected_name = st.selectbox("Seleccionar empresa", list(empresa_options.keys()))
        empresa_id = empresa_options[selected_name]
        empresa = df_empresas[df_empresas["id"] == empresa_id].iloc[0].to_dict()

        with st.expander(f"✏️ Editar empresa: {empresa['nombre']}", expanded=False):
            new_nombre = st.text_input("Nombre", empresa.get("nombre", ""))
            new_direccion = st.text_input("Dirección", empresa.get("direccion", ""))
            new_localidad = st.text_input("Localidad", empresa.get("localidad", ""))
            new_cif = st.text_input("CIF", empresa.get("CIF", ""))
            new_telefono = st.text_input("Teléfono", empresa.get("telefono", ""))
            new_email = st.text_input("Email", empresa.get("email_empresa", ""))

            if st.button("💾 Actualizar empresa"):
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

        # --- Mostrar FP asociadas ---
        fps = getEqual(necesidadFP, "empresa", empresa["CIF"])
        estadosEmpresa = getEqual(empresaEstadosTabla, "empresa", empresa["CIF"])
        st.subheader(f"Seguimiento - {empresa['nombre']}")
        if estadosEmpresa is None or len(estadosEmpresa) == 0:
            mostrar_fases(fasesEmpresa, fase2colEmpresa, None)
        else:
            mostrar_fases(fasesEmpresa, fase2colEmpresa, estadosEmpresa[0])
        st.subheader(f"Oferta FP - {empresa['nombre']}")

        if fps:
            for i, fp in enumerate(fps, start=1):
                estado_actual = fp.get("estado") or "Activo"
                bg_color = "🟢" if estado_actual == "Activo" else "🔴"

                with st.expander(
                    f"Oferta #{i} | Fecha: {pd.to_datetime(fp.get('created_at')).strftime('%d/%m/%Y')} | {estado_actual} {bg_color}",
                    expanded=False
                ):
                    ciclos = fp.get("ciclos_formativos")
                    if ciclos:
                        st.markdown("**Ciclos formativos y cantidad de alumnos:**")
                        df_ciclos = pd.DataFrame(list(ciclos.items()), columns=["Ciclo", "Cantidad Alumnos"])
                        st.dataframe(df_ciclos, hide_index=True, use_container_width=True)

                    areas = fp.get("areas")
                    if areas:
                        st.markdown("**Áreas:**")
                        for area in areas:
                            st.markdown(f"- {area}")

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
                    estado = st.selectbox("Estado", options=estados, index=default_index, key=f"estado_{fp['id']}")
                    motivo_cancelacion = None
                    if estado == "Cancelado":
                        motivo_cancelacion = st.text_area("Motivo de cancelación", value=fp.get("motivo") or "", key=f"motivo_{fp['id']}")

                    if st.button("Guardar cambios", key=f"guardar_{fp['id']}"):
                        upsert(
                            necesidadFP,
                            {"empresa": empresa["CIF"], "estado": estado, "motivo": motivo_cancelacion, "id": fp["id"]},
                            keys=["id"]
                        )
                        st.success("Oferta FP actualizada")
                        st.rerun()
        else:
            st.info(
                'No hay necesidades FP registradas para esta empresa. '
                f"Mandale el link para que nos avise: [Formulario]({base_url}forms?form=1)"
            )

# -------------------------------------------------------------------
# TAB 2: Crear nueva empresa
# -------------------------------------------------------------------
with tab2:
    st.subheader("➕ Nueva Empresa")
    with st.form("nueva_empresa_form"):
        nombre = st.text_input("Nombre")
        direccion = st.text_input("Dirección")
        localidad = st.text_input("Localidad")
        cif = st.text_input("CIF")
        telefono = st.text_input("Teléfono")
        email = st.text_input("Email")

        submitted = st.form_submit_button("Crear Empresa")
        if submitted:
            upsert(
                empresasTabla,
                {"nombre": nombre, "direccion": direccion, "localidad": localidad, "CIF": cif, "telefono": telefono, "email_empresa": email},
                keys=["CIF"]
            )
            st.success("Empresa creada correctamente")
            st.rerun()

# -------------------------------------------------------------------
# TAB 3: Formularios & Contacto
# -------------------------------------------------------------------
with tab3:
    st.subheader("📨 Formularios & Contacto")
    formUrl = os.getenv("FORM_EMPRESA")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"📋 [Formulario Empresa]({formUrl})")
    with col2:
        st.page_link("pages/emails.py", label="✉️ Contactar Empresas")
