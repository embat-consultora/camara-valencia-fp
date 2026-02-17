import streamlit as st
import pandas as pd
from modules.data_base import getEquals, getEqual, upsert, updateTutores
from page_utils import apply_page_config
from navigation import make_sidebar
from variables import empresasTabla, necesidadFP, estados, localidades, tutoresTabla
from datetime import datetime
apply_page_config()
make_sidebar()

st.set_page_config(page_title="Mi Empresa", page_icon="🏢")
st.markdown(
    "<h2 style='text-align: center;'>MI EMPRESA</h2>",
    unsafe_allow_html=True
)

# -- aca el "email" es el CIF de la empresa
cif = st.session_state.get("username", "000000")
if "df_tutores" not in st.session_state:
    st.session_state.df_tutores = None
# --- Traer todas las empresas ---
empresas = getEquals(empresasTabla, {"CIF": cif})
if not empresas:
    st.warning("No encontramos tu empresa")
    st.stop()

df_empresas = pd.DataFrame(empresas)
df_empresas = df_empresas[df_empresas["CIF"] != "00000000"]
# --- Tabs principales ---
tab1, tab2 = st.tabs(["Mi Empresa", "Tutores"])

# -------------------------------------------------------------------
# TAB 1: Buscar y visualizar empresas
# -------------------------------------------------------------------
with tab1:

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
        

with tab2:
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
