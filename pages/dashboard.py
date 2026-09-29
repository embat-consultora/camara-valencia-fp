import streamlit as st
import pandas as pd
import plotly.express as px
from io import BytesIO
import sys
import os
import re
from datetime import datetime
from variables import alumnosTabla, empresasTabla, tutoresTabla, practicaTabla, practicaEstadosTabla, aniosList, cursoList
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


def empresas_con_practicas_en_filtro(df_practicas, df_empresas):
    """Devuelve solo empresas que tienen al menos una práctica dentro del filtro actual."""
    if df_practicas is None or df_practicas.empty:
        return df_empresas.iloc[0:0].copy() if isinstance(df_empresas, pd.DataFrame) else pd.DataFrame()

    empresas_validas = set()

    for col in ["empresa", "cif_empresa", "empresa_id", "CIF", "cif"]:
        if col in df_practicas.columns:
            empresas_validas.update(
                str(v).strip()
                for v in df_practicas[col].dropna().tolist()
                if str(v).strip() not in ["", "nan", "None", "null"]
            )

    if "empresas" in df_practicas.columns:
        for item in df_practicas["empresas"].dropna().tolist():
            if isinstance(item, dict):
                for key in ["CIF", "cif", "id"]:
                    valor = item.get(key)
                    if pd.notna(valor) and str(valor).strip() not in ["", "nan", "None", "null"]:
                        empresas_validas.add(str(valor).strip())

    if not empresas_validas:
        return df_empresas.iloc[0:0].copy() if isinstance(df_empresas, pd.DataFrame) else pd.DataFrame()

    if isinstance(df_empresas, pd.DataFrame) and "CIF" in df_empresas.columns:
        return df_empresas[df_empresas["CIF"].astype(str).isin(empresas_validas)].copy()

    if isinstance(df_empresas, pd.DataFrame) and "cif" in df_empresas.columns:
        return df_empresas[df_empresas["cif"].astype(str).isin(empresas_validas)].copy()

    if isinstance(df_empresas, pd.DataFrame):
        return df_empresas.head(0).copy()

    return pd.DataFrame()


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


def filtrar_por_curso_academico_y_curso(df, anio_filtro=None, curso_filtro=None):
    """Aplica el filtro global del sidebar (curso académico y curso) si existe."""
    if df is None or df.empty:
        return df

    df_filtrado = df.copy()

    anio_filtro = anio_filtro or st.session_state.get("selector_curso_ac_global", aniosList[0])
    curso_filtro = curso_filtro or st.session_state.get("selector_curso_global", cursoList[0])

    if anio_filtro and anio_filtro != aniosList[0]:
        columnas_anio = [col for col in ["anio", "anio_alumno", "anio_practica"] if col in df_filtrado.columns]
        if columnas_anio:
            df_filtrado = df_filtrado[df_filtrado[columnas_anio[0]].astype(str).str.strip() == str(anio_filtro).strip()]

    if curso_filtro and curso_filtro != cursoList[0]:
        columnas_curso = [col for col in ["curso", "curso_alumno", "curso_practica"] if col in df_filtrado.columns]
        if columnas_curso:
            df_filtrado = df_filtrado[df_filtrado[columnas_curso[0]].astype(str).str.strip() == str(curso_filtro).strip()]

    return df_filtrado


def aplicar_filtro_dashboard(df, ciclo_seleccionado=None, estado_seleccionado=None, localidad_seleccionada=None):
    """Filtra por los valores del dashboard: ciclo, estado y localidad."""
    if df is None or df.empty:
        return df

    df_filtrado = df.copy()

    if ciclo_seleccionado:
        ciclo_col = "ciclo_formativo" if "ciclo_formativo" in df_filtrado.columns else None
        if ciclo_col:
            df_filtrado = df_filtrado[df_filtrado[ciclo_col].astype(str).isin([str(v) for v in ciclo_seleccionado])]

    if estado_seleccionado:
        estado_col = "estado" if "estado" in df_filtrado.columns else "status" if "status" in df_filtrado.columns else None
        if estado_col:
            df_filtrado = df_filtrado[df_filtrado[estado_col].astype(str).isin([str(v) for v in estado_seleccionado])]

    if localidad_seleccionada:
        localidad_col = "localidad" if "localidad" in df_filtrado.columns else None
        if localidad_col:
            normalizada = df_filtrado[localidad_col].apply(lambda v: limpiar_localidad(v) if pd.notna(v) else "")
            df_filtrado = df_filtrado[normalizada.isin([limpiar_localidad(v) for v in localidad_seleccionada])]

    return df_filtrado


anioFiltro = st.session_state.get("selector_curso_ac_global", aniosList[0])
cursoFiltro = st.session_state.get("selector_curso_global", cursoList[0])

# Filtrado global del dashboard cuando el usuario cambia los selectores del sidebar
if "dashboard_ciclo_formativo" not in st.session_state:
    st.session_state["dashboard_ciclo_formativo"] = []
if "dashboard_estado_alumno" not in st.session_state:
    st.session_state["dashboard_estado_alumno"] = []
if "dashboard_localidad" not in st.session_state:
    st.session_state["dashboard_localidad"] = []

# Datos base ya cargados y filtrados por curso académico / curso desde el sidebar
base_alu = filtrar_por_curso_academico_y_curso(df_alu_raw, anioFiltro, cursoFiltro)
base_emp = filtrar_por_curso_academico_y_curso(df_emp_raw, anioFiltro, cursoFiltro)
base_pra = filtrar_por_curso_academico_y_curso(df_pra, anioFiltro, cursoFiltro)
base_vw_ofe = filtrar_por_curso_academico_y_curso(df_vw_ofe, anioFiltro, cursoFiltro)
base_master = filtrar_por_curso_academico_y_curso(df_master, anioFiltro, cursoFiltro)

# Filtros del dashboard bajo el título
if not base_alu.empty:
    ciclos_list = sorted(base_alu['ciclo_formativo'].dropna().astype(str).unique()) if 'ciclo_formativo' in base_alu.columns else []
    localidades_list = sorted(base_alu['localidad'].dropna().map(limpiar_localidad).unique()) if 'localidad' in base_alu.columns else []
    estados_list = sorted(base_alu['estado'].dropna().astype(str).unique()) if 'estado' in base_alu.columns else []
else:
    ciclos_list = []
    localidades_list = []
    estados_list = []

st.title("Panel Estratégico CÁMARA FP")

# Filtros debajo del título y encima de todos los tabs
if ciclos_list or localidades_list or estados_list:
    col_filtro_ciclo, col_filtro_localidad, col_filtro_estado = st.columns(3)

    with col_filtro_ciclo:
        filtro_ciclo = st.multiselect(
            "Ciclo Formativo",
            options=ciclos_list,
            default=st.session_state.get("dashboard_ciclo_formativo", []),
            key="dashboard_ciclo_formativo",
            placeholder="Selecciona una opción"
        )
    with col_filtro_localidad:
        filtro_localidad = st.multiselect(
            "Localidad",
            options=localidades_list,
            default=st.session_state.get("dashboard_localidad", []),
            key="dashboard_localidad",
            placeholder="Selecciona una opción"
        )
    with col_filtro_estado:
        filtro_estado = st.multiselect(
            "Estatus Alumno",
            options=estados_list,
            default=st.session_state.get("dashboard_estado_alumno", []),
            key="dashboard_estado_alumno",
            placeholder="Selecciona una opción"
        )
else:
    filtro_ciclo = []
    filtro_localidad = []
    filtro_estado = []

# Aplicación final de filtros a todos los datasets del dashboard
# Estos valores se usan en todas las tabs.
df_alu = aplicar_filtro_dashboard(base_alu, filtro_ciclo, filtro_estado, filtro_localidad)
df_emp_raw = aplicar_filtro_dashboard(base_emp, filtro_ciclo, filtro_estado, filtro_localidad)
df_pra = aplicar_filtro_dashboard(base_pra, filtro_ciclo, filtro_estado, filtro_localidad)
df_vw_ofe = aplicar_filtro_dashboard(base_vw_ofe, filtro_ciclo, filtro_estado, filtro_localidad)
df_master = aplicar_filtro_dashboard(base_master, filtro_ciclo, filtro_estado, filtro_localidad)

# --- RENDERIZADO VISUAL ---
try:
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
        st.subheader("Análisis de Disponibilidad")

        if not df_vw_ofe.empty:
            df_plot = df_vw_ofe.groupby('nombre', as_index=False)['cupos_disponibles'].sum()
            df_plot = df_plot.sort_values(by='cupos_disponibles', ascending=True)

            fig_ofe = px.bar(
                df_plot,
                x='cupos_disponibles',
                y='nombre',
                orientation='h',
                title="Plazas disponibles por empresa",
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

        df_empresas_con_practicas = empresas_con_practicas_en_filtro(df_pra, df_emp_raw)
        df_est_filtrado = df_est.copy()
        if not df_est_filtrado.empty and 'practicaId' in df_est_filtrado.columns and not df_pra.empty:
            practicas_validas = set(str(v) for v in df_pra['id'].dropna().astype(str).tolist())
            df_est_filtrado = df_est_filtrado[df_est_filtrado['practicaId'].astype(str).isin(practicas_validas)].copy()

        e1, e2 = st.columns(2)
        with e1:
            if not df_empresas_con_practicas.empty and 'localidad' in df_empresas_con_practicas.columns:
                emp_loc = df_empresas_con_practicas['localidad'].apply(limpiar_localidad).value_counts().reset_index(name='total').head(10)
                emp_loc.columns = ['localidad', 'total']
                st.plotly_chart(px.bar(emp_loc, x='total', y='localidad', orientation='h', text_auto=True, title="Ubicación Empresas con prácticas", color_discrete_sequence=[CIAN_CAMARA]), use_container_width=True, key="bar_emp_loc")
            else:
                st.info("No hay empresas con prácticas para los filtros actuales.")

        with e2:
            if not df_est_filtrado.empty:
                pipe_data = {
                    "Asignadas": df_est_filtrado['documentacion_firmada'].notna().sum(),
                    "En Progreso": df_est_filtrado['en_progreso'].notna().sum(),
                    "Finalizadas": df_est_filtrado['finalizada'].notna().sum()
                }
                df_p = pd.DataFrame(pipe_data.items(), columns=['Estado', 'Total'])
                st.plotly_chart(px.bar(df_p, x='Estado', y='Total', text_auto=True, title="Pipeline FP", color='Estado', color_discrete_sequence=[CIAN_CAMARA, AZUL_CAMARA, "#002b56"]), use_container_width=True, key="bar_pipeline")
            else:
                st.info("No hay prácticas activas con los filtros actuales.")

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