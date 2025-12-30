import streamlit as st
import pandas as pd # Corregido: Importación estándar para evitar errores de Pylance
import plotly.express as px
import sys
import os
import re

# 1. CONFIGURACIÓN DE RUTAS Y UTILIDADES
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from page_utils import apply_page_config
from navigation import make_sidebar
from modules.data_base import get

# Definición de utilidad Excel para evitar error 'is not defined'
def df_to_excel(df):
    from io import BytesIO
    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='Sheet1')
    return output.getvalue()

# Colores Corporativos Cámara
AZUL_CAMARA = "#004b93"
CIAN_CAMARA = "#7ab9c2"

st.set_page_config(page_title="Dashboard Cámara MSA", layout="wide")
apply_page_config()
make_sidebar()

# --- FUNCIONES DE LIMPIEZA ---
def limpiar_localidad(nombre):
    if pd.isna(nombre) or nombre == "": return "No definido"
    nombre = str(nombre).strip().title()
    nombre = nombre.replace(" Valencia", "").replace(" (Valencia)", "")
    return re.sub(r'[^a-zA-ZáéíóúÁÉÍÓÚñÑ ]', '', nombre).strip()

@st.cache_data
def load_all_data():
    """Motor de carga coordinado para evitar errores de desempaquetado"""
    df_alu = pd.DataFrame(get("alumnos"))
    df_est = pd.DataFrame(get("empresa_estados"))
    df_emp = pd.DataFrame(get("empresas"))
    df_pra = pd.DataFrame(get("practicas_fp"))
    
    # INTENTAR TRAER LA VISTA ESPECÍFICA
    try:
        df_vw = pd.DataFrame(get("vw_empresas_ofertas"))
    except Exception:
        df_vw = pd.DataFrame() # Fallback si hay error de permisos
        
    # Sincronizamos los IDs para evitar errores de 'merge'
    for df in [df_alu, df_pra]:
        if 'id' in df.columns: df['id'] = df['id'].astype(str)
        if 'alumno' in df.columns: df['alumno'] = df['alumno'].astype(str)

    return df_alu, df_est, df_emp, df_pra, df_vw

# --- RENDERIZADO DEL DASHBOARD ---
try:
    # Recibimos exactamente los 5 valores devueltos por la función
    df_alu, df_est, df_emp, df_pra, df_vw = load_all_data()

    st.title("Dashboard Cámara FP")

    # A. BLOQUE SUPERIOR: KPIs con diseño mejorado
    with st.container():
        m1, m2, m3, m4 = st.columns(4)
    
    # Alumnos Totales (60 alumnos registrados)
    m1.metric("🎓 Alumnos Totales", len(df_alu))
    
    # Empresas (43 empresas colaboradoras)
    m2.metric("🏢 Empresas Colaboradoras", len(df_emp))
    
    # Documentación (Suma de documentos completados)
    docs_ready = df_est['documentacion_completa'].notna().sum() if 'documentacion_completa' in df_est.columns else 0
    m3.metric("📝 Docs. Completos", docs_ready)
    
    # Movilidad (Tasa calculada de vehículos disponibles: 73.3%)
    tasa_val = (df_alu['vehiculo'].isin(['Sí', True])).mean() * 100 if len(df_alu) > 0 else 0
    m4.metric("🚗 Tasa Movilidad", f"{tasa_val:.1f}%")

    st.divider()

    # B. PESTAÑAS
    tab_alu, tab_ofertas, tab_operativa = st.tabs(["🎓 Alumnos", "🏢 Ofertas y Cupos", "⚙️ Gestión Operativa"])

    with tab_alu:
        col1, col2 = st.columns(2)
        with col1:
            # Distribución por Sexo corregida
            sex_df = df_alu['sexo'].fillna("No Especificado").value_counts().reset_index()
            sex_df.columns = ['sexo', 'count'] # Renombrado para evitar error de 'index'
            st.plotly_chart(px.pie(sex_df, names='sexo', values='count', hole=0.5, color_discrete_sequence=[AZUL_CAMARA, CIAN_CAMARA]), use_container_width=True)
        with col2:
            loc_df = df_alu['localidad'].apply(limpiar_localidad).value_counts().reset_index().head(10)
            loc_df.columns = ['municipio', 'total']
            st.plotly_chart(px.bar(loc_df, x='total', y='municipio', orientation='h', color_discrete_sequence=[AZUL_CAMARA]), use_container_width=True)

    with tab_ofertas:
        st.subheader("📋 Análisis de la Vista: vw_empresas_ofertas")
        if not df_vw.empty:
            # Mostramos las columnas clave que vemos en Supabase
            cols_interes = ['nombre', 'alumnos_pedidos', 'cupos_disponibles', 'puestos']
            st.dataframe(df_vw[[c for c in cols_interes if c in df_vw.columns]], use_container_width=True)
            
            # Gráfico de cupos por empresa
            fig_cupos = px.bar(df_vw.head(10), x='cupos_disponibles', y='nombre', orientation='h', 
                               title="Capacidad de Cupos por Empresa", color_discrete_sequence=[CIAN_CAMARA])
            st.plotly_chart(fig_cupos, use_container_width=True)
        else:
            st.warning("⚠️ Los datos de la vista de ofertas no están disponibles o no tienen permisos.")

    with tab_operativa:
        # SOLUCIÓN AL ERROR 'tutor'
        # Verificamos dónde está la columna de tutor (en la vista es 'tutor_nombre')
        st.subheader("👨‍🏫 Gestión de Tutores")
        col_tutor = 'tutor_nombre' if 'tutor_nombre' in df_vw.columns else ('tutor' if 'tutor' in df_vw.columns else None)
        
        if col_tutor and not df_vw.empty:
            tut_df = df_vw[col_tutor].value_counts().reset_index()
            tut_df.columns = ['tutor', 'cantidad']
            st.plotly_chart(px.bar(tut_df, x='cantidad', y='tutor', orientation='h', color_discrete_sequence=[AZUL_CAMARA]), use_container_width=True)
        else:
            st.info("No se encontraron datos de tutores asignados en la vista.")

    # C. BOTÓN DE DESCARGA
    st.divider()
    if not df_alu.empty:
        st.download_button("📥 Descargar Listado de Alumnos (Excel)", data=df_to_excel(df_alu), file_name="alumnos_camara.xlsx")

except Exception as e:
    st.error(f"Error cargando los componentes del dashboard: {e}")