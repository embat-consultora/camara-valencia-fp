import streamlit as st
import pandas as pd
import plotly.express as px
from io import BytesIO
import sys
import os
import re
from datetime import datetime
from variables import alumnosTabla, empresasTabla, tutoresTabla, practicaTabla, practicaEstadosTabla
# 1. CONFIGURACIÓN DE RUTAS Y UTILIDADES
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from page_utils import apply_page_config
from navigation import make_sidebar
from modules.data_base import get

# Colores Corporativos Cámara Valencia
AZUL_CAMARA = "#004b93"
CIAN_CAMARA = "#7ab9c2"
PALETA_GRAFICOS = [AZUL_CAMARA, CIAN_CAMARA, "#b3d4d8", "#003366", "#e0f2f1"]

st.set_page_config(page_title="Dashboard Cámara MSA", layout="wide")
apply_page_config()
make_sidebar()

# --- ESTILO CSS PARA KPIs (KNEPE) ATRACTIVOS ---
st.markdown(f"""
    <style>
    [data-testid="stMetric"] {{
        background-color: #ffffff;
        padding: 20px;
        border-radius: 15px;
        border-left: 5px solid {AZUL_CAMARA};
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        transition: transform 0.3s ease;
    }}
    [data-testid="stMetric"]:hover {{
        transform: translateY(-5px);
        border-left: 5px solid {CIAN_CAMARA};
    }}
    [data-testid="stMetricLabel"] p {{
        font-size: 16px !important;
        font-weight: bold;
        color: #555;
    }}
    </style>
    """, unsafe_allow_html=True)

# --- FUNCIONES DE LIMPIEZA Y SOPORTE ---
def limpiar_nombre(t):
    if pd.isna(t) or t == "": return "No definido"
    return str(t).strip().title()

def limpiar_localidad(nombre):
    """Estandariza municipios eliminando redundancias"""
    if pd.isna(nombre) or nombre == "": return "No definido"
    nombre = str(nombre).strip().title().replace(" Valencia", "").replace(" (Valencia)", "")
    return re.sub(r'[^a-zA-ZáéíóúÁÉÍÓÚñÑ ]', '', nombre).strip()

def exportar_excel(df):
    """Generación de Excel en memoria para evitar errores OSError en Windows"""
    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='Datos_Dashboard')
    return output.getvalue()

@st.cache_data
def load_all_data():
    """Motor de carga blindado contra errores de 'unpack' y 'KeyError'"""
    df_alu = pd.DataFrame(get(alumnosTabla))
    df_emp = pd.DataFrame(get(empresasTabla))
    df_tut = pd.DataFrame(get(tutoresTabla))
    df_est = pd.DataFrame(get(practicaEstadosTabla)) # Ajustado a tabla real
    df_pra = pd.DataFrame(get(practicaTabla))
    try:
        df_vw_ofe = pd.DataFrame(get("vw_empresas_ofertas"))
    except:
        df_vw_ofe = pd.DataFrame()

    if not df_pra.empty:
        col_alu_pra = 'alumno' if 'alumno' in df_pra.columns else ('alumno_id' if 'alumno_id' in df_pra.columns else None)
        col_tut_pra = 'tutor' if 'tutor' in df_pra.columns else ('tutor_id' if 'tutor_id' in df_pra.columns else None)

        if col_alu_pra:
            df_pra[col_alu_pra] = df_pra[col_alu_pra].astype(str)
            df_alu['id'] = df_alu['id'].astype(str)
        if col_tut_pra:
            df_pra[col_tut_pra] = df_pra[col_tut_pra].astype(str)
            df_tut['id'] = df_tut['id'].astype(str)

        # Merge para tener todos los datos cruzados (df_master)
   
        df_m = df_pra.merge(df_alu[['dni', 'nombre', 'apellido', 'localidad', 'sexo', 'ciclo_formativo', 'estado', 'vehiculo']], 
                            left_on=col_alu_pra, right_on='dni', how='left')
        
        if col_tut_pra:
            df_m = df_m.merge(df_tut[['id', 'nombre']], 
                                left_on=col_tut_pra, right_on='id', how='left', suffixes=('', '_tutor'))
        
        if 'nombre_tutor' in df_m.columns:
            df_m['nombre_tutor'] = df_m['nombre_tutor'].apply(limpiar_nombre)
    else:
        df_m = pd.DataFrame()

    return df_alu, df_est, df_emp, df_pra, df_vw_ofe, df_m

@st.cache_data
def load_feedback_data():
    try:
        df_stats = pd.DataFrame(get("vw_feedback_stats"))
        df_det = pd.DataFrame(get("vw_feedback_detalle_alumnos"))
        return df_stats, df_det
    except:
        return pd.DataFrame(), pd.DataFrame()

# --- EJECUCIÓN DE CARGA Y FILTROS ---
df_alu_raw, df_est, df_emp_raw, df_pra, df_vw_ofe, df_master = load_all_data()
df_stats, df_detalle = load_feedback_data()

st.sidebar.title("🔍 Filtros Panel")
df_alu = pd.DataFrame()
if df_alu_raw.empty:
    
    st.sidebar.info("No hay datos de alumnos disponibles para filtrar.")
else:
    ciclos_list = sorted(df_alu_raw['ciclo_formativo'].dropna().unique()) if 'ciclo_formativo' in df_alu_raw.columns else []
    f_ciclo = st.sidebar.multiselect("Ciclo Formativo", options=ciclos_list)
    f_loc = st.sidebar.multiselect("Localidad", options=sorted(df_alu_raw['localidad'].apply(limpiar_localidad).unique()))
    f_estado = st.sidebar.multiselect("Estatus Alumno", options=df_alu_raw['estado'].unique() if 'estado' in df_alu_raw.columns else [])

df_alu = df_alu_raw.copy()
if f_ciclo: df_alu = df_alu[df_alu['ciclo_formativo'].isin(f_ciclo)]
if f_loc: df_alu = df_alu[df_alu['localidad'].apply(limpiar_localidad).isin(f_loc)]
if f_estado: df_alu = df_alu[df_alu['estado'].isin(f_estado)]

# --- RENDERIZADO VISUAL ---
try:
    st.title("Panel Estratégico CÁMARA FP")

    # A. BLOQUE SUPERIOR: KPIs
    k1, k2, k3, k4 = st.columns(4)
    k1.metric("🎓 Alumnos Filtrados", len(df_alu))
    k2.metric("🏢 Empresas Activas", len(df_emp_raw))
    k3.metric("🤝 Match Realizados", len(df_pra))
    movilidad = (df_alu['vehiculo'].isin(['Sí', True])).mean() * 100 if len(df_alu) > 0 else 0
    k4.metric("🚗 Tasa Movilidad", f"{movilidad:.1f}%")

    st.divider()

    # B. PESTAÑAS
    t_alu, t_ofe, t_gest, t_emp, t_feed = st.tabs(["🎓 Alumnos", "🏢 Ofertas", "⚙️ Gestión", "📍 Empresas", "📩 Feedback"])

    with t_alu:
        c1, c2, c3 = st.columns(3)
        if not df_alu.empty:
            with c1:
                sex_df = df_alu['sexo'].fillna("N/E").value_counts().reset_index(name='total')
                st.plotly_chart(px.pie(sex_df, names='sexo', values='total', hole=0.5, title="Género", color_discrete_sequence=PALETA_GRAFICOS), use_container_width=True, key="pie_sexo")
                
                veh_df = df_alu['vehiculo'].fillna("No").value_counts().reset_index(name='total')
                st.plotly_chart(px.pie(veh_df, names='vehiculo', values='total', hole=0.5, title="Vehículo", color_discrete_sequence=[CIAN_CAMARA, AZUL_CAMARA]), use_container_width=True, key="pie_vehiculo")
            
            with c2:
                loc_df = df_alu['localidad'].apply(limpiar_localidad).value_counts().reset_index(name='alumnos').head(10)
                st.plotly_chart(px.bar(loc_df, x='alumnos', y='localidad', orientation='h', text_auto=True, title="Top 10 Ubicaciones", color_discrete_sequence=[AZUL_CAMARA]), use_container_width=True, key="bar_loc")
                
                if 'ciclo_formativo' in df_alu.columns:
                    cic_df = df_alu['ciclo_formativo'].value_counts().reset_index(name='total')
                    st.plotly_chart(px.bar(cic_df, x='total', y='ciclo_formativo', orientation='h', text_auto=True, title="Ciclos", color_discrete_sequence=[CIAN_CAMARA]), use_container_width=True, key="bar_ciclo")
            
            with c3:
                if 'estado' in df_alu.columns:
                    est_df = df_alu['estado'].value_counts().reset_index(name='total')
                    st.plotly_chart(px.bar(est_df, x='estado', y='total', text_auto=True, title="Estatus", color_discrete_sequence=[AZUL_CAMARA]), use_container_width=True, key="bar_estatus")
                
                if 'tipoPractica' in df_alu.columns:
                    tp_df = df_alu['tipoPractica'].value_counts().reset_index(name='total')
                    st.plotly_chart(px.bar(tp_df, x='tipoPractica', y='total', text_auto=True, title="Formación", color_discrete_sequence=[CIAN_CAMARA]), use_container_width=True, key="bar_tipo")

    with t_ofe:
        st.subheader("Análisis de Disponibilidad por Ciclo")

        if not df_vw_ofe.empty:
            ciclos_disponibles = sorted(df_vw_ofe['ciclo_formativo'].unique())
            ciclo_seleccionado = st.selectbox("Selecciona un Ciclo Formativo:", ciclos_disponibles, key="select_ciclo_ofe")
            
            df_filtrado = df_vw_ofe[df_vw_ofe['ciclo_formativo'] == ciclo_seleccionado]
            df_plot = df_filtrado.groupby('nombre', as_index=False)['cupos_disponibles'].sum()
            df_plot = df_plot.sort_values(by='cupos_disponibles', ascending=True) 

            fig_ofe = px.bar(
                df_plot, 
                x='cupos_disponibles', 
                y='nombre', 
                orientation='h',
                title=f"Plazas disponibles en: {ciclo_seleccionado}",
                labels={'cupos_disponibles': 'Nº de Plazas', 'nombre': ''},
                text_auto=True, 
                color_discrete_sequence=['#b3d4d8']
            )

            altura_dinamica = max(400, len(df_plot) * 40)
            fig_ofe.update_layout(
                showlegend=False, 
                xaxis_title="Cantidad de Plazas",
                yaxis_title=None,
                height=altura_dinamica, 
                margin=dict(l=20, r=20, t=50, b=20),
                hovermode="y unified"
            )
            st.plotly_chart(fig_ofe, use_container_width=True, key="grafico_cupos_filtrado")
            
        else:
            st.info("No hay datos de ofertas registradas en este momento.")

    with t_gest:
        st.subheader("Supervisión de Gestión y Cuellos de Botella")
        
        # Usamos df_master porque ahí ya cruzamos las formaciones con los nombres de los alumnos
        df_gestion = df_master if not df_master.empty else df_pra
        if not df_gestion.empty:
            st.markdown("#### ⚠️ Alertas Documentales (Formaciones en curso)")
            a1, a2, a3 = st.columns(3)
            
            # Identificamos los pendientes
            df_anexos_faltantes = df_gestion[df_gestion['anexos_firmados'] != True]
            df_sao_faltante = df_gestion[df_gestion['doc_sao_entregada'] != True]
            
            a1.metric("Anexos SIN Firmar", len(df_anexos_faltantes), delta="Atención requerida", delta_color="inverse")
            a2.metric("Doc. SAO Pendiente", len(df_sao_faltante), delta="Prioridad alta", delta_color="inverse")
            a3.metric("Total Formaciones Activas", len(df_gestion))
            
            # Tabla desplegable para el Director
            if not df_anexos_faltantes.empty or not df_sao_faltante.empty:
                with st.expander("🔍 DETALLE DE INCIDENCIAS: ¿A quién reclamar?"):
                    df_pendientes = df_gestion[(df_gestion['anexos_firmados'] != True) | (df_gestion['doc_sao_entregada'] != True)].copy()
                    
                    # Unimos nombre y apellido si existen en el df_master
                    if 'nombre' in df_pendientes.columns and 'apellido' in df_pendientes.columns:
                        df_pendientes['nombre'] = df_pendientes['nombre'].fillna('')
                        df_pendientes['apellido'] = df_pendientes['apellido'].fillna('')
                        df_pendientes['Alumno Completo'] = df_pendientes['nombre'] + " " + df_pendientes['apellido']
                    else:
                        df_pendientes['Alumno Completo'] = df_pendientes['alumno'] 
                    
                    columnas_check = {
                        'Alumno Completo': 'Alumno',
                        'empresa': 'Empresa',
                        'gestor': 'Gestor Responsable',
                        'anexos_firmados': 'Anexos OK',
                        'doc_sao_entregada': 'SAO OK'
                    }
                    
                    cols_finales = [c for c in columnas_check.keys() if c in df_pendientes.columns]
                    df_final = df_pendientes[cols_finales].rename(columns=columnas_check)
                    
                    st.warning("El siguiente listado muestra las formaciones que requieren intervención inmediata de sus gestores.")
                    st.dataframe(df_final, use_container_width=True, hide_index=True)

            st.divider()

        g1, g2 = st.columns(2)
        with g1:
            if not df_gestion.empty and 'gestor' in df_gestion.columns:
                carga_gestor = df_gestion['gestor'].fillna('Sin asignar').value_counts().reset_index()
                carga_gestor.columns = ['Gestor', 'Nº Formaciones']
                
                fig_gest = px.bar(
                    carga_gestor, 
                    x='Nº Formaciones', 
                    y='Gestor', 
                    orientation='h', 
                    text_auto=True,
                    title="Carga de Trabajo por Gestor",
                    color_discrete_sequence=[AZUL_CAMARA]
                )
                st.plotly_chart(fig_gest, use_container_width=True, key="bar_carga_gestores")
            else:
                st.info("No hay datos de gestores asignados a formaciones.")

        with g2:
            if not df_pra.empty and 'created_at' in df_pra.columns:
                df_pra['mes_grafico'] = pd.to_datetime(df_pra['created_at']).dt.to_period('M').dt.to_timestamp()
                evol_df = df_pra.groupby('mes_grafico').size().reset_index(name='total')
                
                fig_linea = px.line(
                    evol_df, 
                    x='mes_grafico', 
                    y='total', 
                    markers=True, 
                    title="Ritmo de Formalización de Formaciones",
                    color_discrete_sequence=[CIAN_CAMARA]
                )
                fig_linea.update_xaxes(dtick="M1", tickformat="%b %Y")
                st.plotly_chart(fig_linea, use_container_width=True, key="line_evolucion_final")
            else:
                st.info("Datos cronológicos insuficientes.")

    with t_emp:
        st.subheader("Mapa de Empresas y Progreso FP")
        e1, e2 = st.columns(2)
        with e1:
            if not df_emp_raw.empty and 'localidad' in df_emp_raw.columns:
                emp_loc = df_emp_raw['localidad'].apply(limpiar_localidad).value_counts().reset_index(name='total').head(10)
                st.plotly_chart(px.bar(emp_loc, x='total', y='localidad', orientation='h', text_auto=True, title="Ubicación Empresas", color_discrete_sequence=[CIAN_CAMARA]), use_container_width=True, key="bar_emp_loc")
            else:
                st.info("Aún no hay empresas registradas.")
                
        with e2:
            if not df_est.empty:
                pipe_data = {
                    "Asignadas": df_est['documentacion_firmada'].notna().sum(),
                    "En Progreso": df_est['en_progreso'].notna().sum(),
                    "Finalizadas": df_est['finalizada'].notna().sum()
                }
                df_p = pd.DataFrame(pipe_data.items(), columns=['Estado', 'Total'])
                st.plotly_chart(px.bar(df_p, x='Estado', y='Total', text_auto=True, title="Pipeline FP", color='Estado', color_discrete_sequence=[CIAN_CAMARA, AZUL_CAMARA, "#002b56"]), use_container_width=True, key="bar_pipeline")
            else:
                st.info("El Pipeline de estados se generará cuando comiencen las Formaciones.")

    with t_feed:
        st.subheader("📩 Feedback")
        if not df_stats.empty:
            f1, f2, f3 = st.columns(3)
            recibidas = df_stats['total_respuestas_recibidas'].sum()
            enviadas = df_stats['total_alumnos_asignados'].sum()
            f1.metric("📉 Tasa Respuesta", f"{(recibidas/enviadas*100):.1f}%" if enviadas > 0 else "0%")
            f2.metric("✅ Total Recibidas", int(recibidas))
            f3.metric("📅 Mes Actual", int(df_stats['respuestas_mes_actual'].sum()))
            
            st.plotly_chart(px.bar(df_stats.sort_values('porcentaje_completado'), x='porcentaje_completado', y='empresa_nombre', orientation='h', text_auto=True, title="Compromiso (%)", color_discrete_sequence=[AZUL_CAMARA]), use_container_width=True, key="bar_feedback")
        else:
            st.info("Aún no hay formularios de feedback respondidos por las empresas o tutores.")

    st.divider()
    if not df_alu.empty:
        st.download_button("📥 Exportar Excel", data=exportar_excel(df_alu), file_name=f"alumnos_fp_{datetime.now().strftime('%Y%m%d')}.xlsx")

except Exception as e:
    st.error(f"Error crítico al renderizar el dashboard: {e}")