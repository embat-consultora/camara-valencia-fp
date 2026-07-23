import streamlit as st
import pandas as pd
from modules.data_base import updateCiclosFormativos, get,getEqual,upsert
from page_utils import apply_page_config
from navigation import make_sidebar
from variables import ciclosFormativosTablas,emailImportantesTabla,formTabla,aniosList
import os
# Configuración inicial
apply_page_config()
make_sidebar()
st.set_page_config(page_title="Configuraciones", page_icon="🚀")

st.markdown("<h2 style='text-align: center;'>Configuraciones</h2>", unsafe_allow_html=True)

# 1. Función simple para traer datos
def fetch_ciclos():
    datos = get(ciclosFormativosTablas)
    if datos:
        return pd.DataFrame(datos)
    # Si no hay datos, devolvemos el "molde" con las columnas necesarias
    return pd.DataFrame(columns=["id", "nombre", "abreviatura", "areas"])
def fetch_email_pymes():
    email = getEqual(emailImportantesTabla, "seccion", "pymes")
    if email:
        email = email[0]
        st.session_state.email_pymes_id = email.get("id")
        return email.get("email", "")
    return ""

def fetch_formularios():
    datos = get(formTabla)
    if datos:
        return pd.DataFrame(datos)
    return pd.DataFrame(columns=["id", "nombre","tipo", "titulo", "subtitulo", "descripcion"])

# 2. Inicializar el estado de los datos una sola vez
if "df_ciclos" not in st.session_state:
    st.session_state.df_ciclos = fetch_ciclos()
if "email_pymes_id" not in st.session_state:
    st.session_state.email_pymes_id = None
if "email_pymes" not in st.session_state:
    st.session_state.email_pymes = fetch_email_pymes()

if "df_formularios" not in st.session_state:
    st.session_state.df_formularios = fetch_formularios()

tabCiclos, tabCorreos, tabFormularios = st.tabs(["Ciclos Formativos", "Correos Importantes", "Formularios"])
with tabCiclos:
    
    # Formulario para capturar los cambios del editor
    with st.form("form_gestion_ciclos"):
        # El editor siempre recibe el DataFrame del session_state

        st.info("Agrega o elimina los ciclos formativos. IMPORTANTE: Las áreas deben estar separadas por comas y luego de realizar algún cambio presiona Enter")
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

with tabCorreos:
    st.subheader("Email Contacto Pymes")
    
    with st.form("form_email_pymes"):
        email_input = st.text_input(
            "Email de Pymes",
            value=st.session_state.email_pymes,
            key="input_email_pymes",
            placeholder="ejemplo@pymes.com"
        )
        submit_email = st.form_submit_button("Guardar Email")
    if submit_email:
            try:
                upsert(
                        emailImportantesTabla, 
                        { "email": email_input, 'seccion': "pymes"},keys=["seccion"])
                    
                st.session_state.email_pymes = email_input
                st.toast("✅ Email guardado correctamente.")
            except Exception as e:
                st.error(f"Error al guardar email: {e}")


with tabFormularios:
    st.subheader("Editar Formularios")
    tipos_disponibles = st.session_state.df_formularios['tipo'].unique().tolist()
    
    # Selectbox para elegir tipo
    tipo_seleccionado = st.selectbox(
        "Selecciona el tipo de formulario",
        options=tipos_disponibles,
        key="select_tipo_formulario"
    )
    
    if tipo_seleccionado:
        # Filtrar datos del tipo seleccionado
        formulario_actual = st.session_state.df_formularios[
            st.session_state.df_formularios['tipo'] == tipo_seleccionado
        ].iloc[0].to_dict()
        
        with st.form(f"form_editar_formulario_{tipo_seleccionado}"):
            st.caption(f"Editando: {formulario_actual.get('nombre', 'Formulario')}")
            
            titulo_input = st.text_input(
                "Título",
                value=formulario_actual.get('titulo', '')
            )
            subtitulo_input = st.text_input(
                "Subtítulo",
                value=formulario_actual.get('subtitulo', '')
            )
            
            descripcion_input = st.text_area(
                "Descripción",
                value=formulario_actual.get('descripcion', '')
            )
            
            submit_form = st.form_submit_button("Guardar Cambios")
        
        if submit_form:
            try:
                # Preparar datos para upsert
                datos_actualizar = {
                    "tipo": tipo_seleccionado,
                    "titulo": titulo_input,
                    "subtitulo": subtitulo_input,
                    "descripcion": descripcion_input
                }
                
                upsert(formTabla, datos_actualizar, keys=["tipo"])
                
                st.success("✅ Formulario actualizado correctamente.")
                st.session_state.df_formularios = fetch_formularios()
                st.rerun()
                
            except Exception as e:
                st.error(f"Error al guardar: {e}")
        
        if(tipo_seleccionado == "alumnos"):
            st.info(f"Link del formulario: {os.getenv('FORM_ALUMNO')}")
        elif(tipo_seleccionado == "empresa"):
            col1, col2 = st.columns([1, 2], vertical_alignment="bottom")
            with col1:
                st.selectbox(
                    "Seleccione curso académico", 
                    options=aniosList[1:], 
                    key="selector_curso_ac_doc"
                )
            with col2:  
                st.info(f"Link del formulario:  {os.getenv('FORM_EMPRESA')}?curso_academico={st.session_state['selector_curso_ac_doc']}")