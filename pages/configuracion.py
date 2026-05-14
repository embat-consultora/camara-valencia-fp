import streamlit as st
import pandas as pd
from modules.data_base import updateCiclosFormativos, get
from page_utils import apply_page_config
from navigation import make_sidebar
from variables import ciclosFormativosTablas,coloresCiclos

# Configuración inicial
apply_page_config()
make_sidebar()

st.markdown("<h2 style='text-align: center;'>Configuraciones</h2>", unsafe_allow_html=True)

# 1. Función simple para traer datos
def fetch_ciclos():
    datos = get(ciclosFormativosTablas)
    if datos:
        return pd.DataFrame(datos)
    # Si no hay datos, devolvemos el "molde" con las columnas necesarias
    return pd.DataFrame(columns=["id", "nombre", "abreviatura", "areas", "color"])

# 2. Inicializar el estado de los datos una sola vez
if "df_ciclos" not in st.session_state:
    st.session_state.df_ciclos = fetch_ciclos()

tabCiclos, tabCorreos = st.tabs(["Ciclos Formativos", "Correos Importantes"])

with tabCiclos:
    
    # Formulario para capturar los cambios del editor
    with st.form("form_gestion_ciclos"):
        # El editor siempre recibe el DataFrame del session_state

        st.caption("Agrega o elimina los ciclos formativos. IMPORTANTE: Las áreas deben estar separadas por comas")
        edited_df = st.data_editor(
            st.session_state.df_ciclos,
            column_config={
                "id": None, # Ocultamos el ID para que no estorbe
                "created_at":None,
                "nombre": st.column_config.TextColumn("Nombre del Ciclo", required=True),
                "abreviatura": st.column_config.TextColumn("Abreviatura", required=True),
                "areas": st.column_config.TextColumn("Áreas", required=True)
            },
            num_rows="dynamic",
            key="editor_tabla_ciclos", # Esta es la clave interna del widget
            width='stretch',
            hide_index=True
        )
        
        submit_btn = st.form_submit_button("Guardar Cambios")

    if submit_btn:
        # Obtenemos los cambios directamente desde la KEY del widget
        cambios = st.session_state.editor_tabla_ciclos
        
        # Si hay cualquier tipo de cambio (edición, suma o borrado)
        if cambios["edited_rows"] or cambios["added_rows"] or cambios["deleted_rows"]:
            try:
                # Pasamos los cambios y la lista original (convertida de DF a dict)
                lista_original = st.session_state.df_ciclos.to_dict('records')
                updateCiclosFormativos(cambios, lista_original)
                
                st.success("✅ Cambios guardados correctamente.")
                
                # Refrescamos los datos para mostrar la tabla actualizada
                st.session_state.df_ciclos = fetch_ciclos()
                st.rerun()
                
            except Exception as e:
                st.error(f"Error al guardar: {e}")
        else:
            st.info("No se realizaron cambios.")