import os
import re
import sys
from datetime import datetime
from io import BytesIO

import pandas as pd
import plotly.express as px
import streamlit as st

from variables import (
    alumnosTabla,
    aniosList,
    cursoList,
    empresasTabla,
    practicaEstadosTabla,
    practicaTabla,
    tutoresTabla,
)

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from modules.data_base import get
from navigation import make_sidebar
from page_utils import apply_page_config


AZUL_CAMARA = "#004b93"
CIAN_CAMARA = "#7ab9c2"
PALETA_GRAFICOS = [AZUL_CAMARA, CIAN_CAMARA, "#b3d4d8", "#003366", "#e0f2f1"]

st.set_page_config(page_title="Dashboard Cámara MSA", layout="wide")
apply_page_config()
make_sidebar()


def limpiar_nombre(valor):
    if pd.isna(valor) or valor == "":
        return "No definido"
    return str(valor).strip().title()


def limpiar_localidad(valor):
    if pd.isna(valor) or valor == "":
        return "No definido"
    localidad = (
        str(valor)
        .strip()
        .title()
        .replace(" Valencia", "")
        .replace(" (Valencia)", "")
    )
    return re.sub(r"[^a-zA-ZáéíóúÁÉÍÓÚñÑ ]", "", localidad).strip()


def exportar_excel(df):
    output = BytesIO()
    with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
        df.to_excel(writer, index=False, sheet_name="Datos_Dashboard")
    return output.getvalue()


@st.cache_data
def load_all_data():
    df_alumnos = pd.DataFrame(get(alumnosTabla))
    df_empresas = pd.DataFrame(get(empresasTabla))
    df_tutores = pd.DataFrame(get(tutoresTabla))
    df_estados = pd.DataFrame(get(practicaEstadosTabla))
    df_practicas = pd.DataFrame(get(practicaTabla))

    try:
        df_ofertas = pd.DataFrame(get("vw_empresas_ofertas"))
    except Exception:
        df_ofertas = pd.DataFrame()

    if df_practicas.empty:
        df_master = pd.DataFrame()
    else:
        columna_alumno = next(
            (
                columna
                for columna in ("alumno", "alumno_id")
                if columna in df_practicas.columns
            ),
            None,
        )
        if columna_alumno and "dni" in df_alumnos.columns:
            df_master = df_practicas.merge(
                df_alumnos[
                    [
                        columna
                        for columna in (
                            "dni",
                            "nombre",
                            "apellido",
                            "localidad",
                            "sexo",
                            "ciclo_formativo",
                            "estado",
                            "vehiculo",
                        )
                        if columna in df_alumnos.columns
                    ]
                ],
                left_on=columna_alumno,
                right_on="dni",
                how="left",
            )
        else:
            df_master = df_practicas.copy()

    return (
        df_alumnos,
        df_estados,
        df_empresas,
        df_practicas,
        df_ofertas,
        df_master,
    )


@st.cache_data
def load_feedback_data():
    try:
        return (
            pd.DataFrame(get("vw_feedback_stats")),
            pd.DataFrame(get("vw_feedback_detalle_alumnos")),
        )
    except Exception:
        return pd.DataFrame(), pd.DataFrame()


def filtrar_por_curso(df, anio, curso):
    if df is None or df.empty:
        return df.copy() if isinstance(df, pd.DataFrame) else pd.DataFrame()

    resultado = df.copy()
    if anio and anio != aniosList[0]:
        columna = next(
            (
                campo
                for campo in ("anio", "anio_alumno", "anio_practica")
                if campo in resultado.columns
            ),
            None,
        )
        if columna:
            resultado = resultado[
                resultado[columna].astype(str).str.strip() == str(anio).strip()
            ]

    if curso and curso != cursoList[0]:
        columna = next(
            (
                campo
                for campo in ("curso", "curso_alumno", "curso_practica")
                if campo in resultado.columns
            ),
            None,
        )
        if columna:
            resultado = resultado[
                resultado[columna].astype(str).str.strip() == str(curso).strip()
            ]

    return resultado


def aplicar_filtros(df, ciclos, localidades, estados):
    if df is None or df.empty:
        return df.copy() if isinstance(df, pd.DataFrame) else pd.DataFrame()

    resultado = df.copy()
    if ciclos and "ciclo_formativo" in resultado.columns:
        resultado = resultado[
            resultado["ciclo_formativo"].astype(str).isin(map(str, ciclos))
        ]

    columna_estado = next(
        (campo for campo in ("estado", "status") if campo in resultado.columns),
        None,
    )
    if estados and columna_estado:
        resultado = resultado[
            resultado[columna_estado].astype(str).isin(map(str, estados))
        ]

    if localidades and "localidad" in resultado.columns:
        localidades_limpias = {limpiar_localidad(valor) for valor in localidades}
        resultado = resultado[
            resultado["localidad"].map(limpiar_localidad).isin(localidades_limpias)
        ]

    return resultado


def valores_filtro(df, columna, transformador=str):
    if df is None or df.empty or columna not in df.columns:
        return []
    valores = df[columna].dropna().map(transformador)
    return sorted({valor for valor in valores if valor and valor != "No definido"})


def empresas_de_practicas(df_empresas, df_practicas):
    if df_empresas.empty or df_practicas.empty:
        return df_empresas.iloc[0:0].copy()

    identificadores = set()
    for columna in ("empresa", "cif_empresa", "empresa_id", "CIF", "cif"):
        if columna in df_practicas.columns:
            identificadores.update(
                str(valor).strip()
                for valor in df_practicas[columna].dropna()
                if str(valor).strip()
            )

    columna_empresa = next(
        (
            columna
            for columna in ("CIF", "cif", "id")
            if columna in df_empresas.columns
        ),
        None,
    )
    if not columna_empresa:
        return df_empresas.iloc[0:0].copy()

    return df_empresas[
        df_empresas[columna_empresa].astype(str).isin(identificadores)
    ].copy()


def card(contenedor, icono, titulo, valor, color):
    contenedor.markdown(
        f"""
        <div class="dashboard-card" style="border-top: 5px solid {color};">
            <div class="dashboard-card-icon">{icono}</div>
            <div class="dashboard-card-title">{titulo}</div>
            <div class="dashboard-card-value">{valor}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


df_alumnos_raw, df_estados, df_empresas_raw, df_practicas_raw, df_ofertas_raw, df_master_raw = load_all_data()
df_feedback_stats, df_feedback_detalle = load_feedback_data()

anio_filtro = st.session_state.get("selector_curso_ac_global", aniosList[0])
curso_filtro = st.session_state.get("selector_curso_global", cursoList[0])

df_alumnos_base = filtrar_por_curso(df_alumnos_raw, anio_filtro, curso_filtro)
df_practicas_base = filtrar_por_curso(df_practicas_raw, anio_filtro, curso_filtro)
df_master_base = filtrar_por_curso(df_master_raw, anio_filtro, curso_filtro)

st.markdown(
    f"""
    <style>
    .dashboard-card {{
        background: linear-gradient(135deg, #ffffff 0%, #f4f8fb 100%);
        border-radius: 16px;
        padding: 18px 20px;
        min-height: 130px;
        box-shadow: 0 5px 16px rgba(0, 75, 147, 0.12);
    }}
    .dashboard-card-icon {{ font-size: 28px; }}
    .dashboard-card-title {{ color: #5b6770; font-size: 14px; margin-top: 8px; }}
    .dashboard-card-value {{
        color: {AZUL_CAMARA};
        font-size: 30px;
        font-weight: 700;
        margin-top: 4px;
    }}
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("Panel Estratégico CÁMARA FP")
st.caption(f"Curso académico: **{anio_filtro}** · Curso: **{curso_filtro}**")

ciclos = valores_filtro(df_alumnos_base, "ciclo_formativo")
localidades = valores_filtro(df_alumnos_base, "localidad", limpiar_localidad)
estados = valores_filtro(df_alumnos_base, "estado")

filtro_ciclo, filtro_localidad, filtro_estado = st.columns(3)
with filtro_ciclo:
    ciclos_seleccionados = st.multiselect(
        "Ciclo Formativo",
        ciclos,
        key="dashboard_ciclo_formativo",
        placeholder="Todos",
    )
with filtro_localidad:
    localidades_seleccionadas = st.multiselect(
        "Localidad",
        localidades,
        key="dashboard_localidad",
        placeholder="Todas",
    )
with filtro_estado:
    estados_seleccionados = st.multiselect(
        "Estatus Alumno",
        estados,
        key="dashboard_estado_alumno",
        placeholder="Todos",
    )

df_alumnos = aplicar_filtros(
    df_alumnos_base,
    ciclos_seleccionados,
    localidades_seleccionadas,
    estados_seleccionados,
)
df_practicas = aplicar_filtros(
    df_practicas_base,
    ciclos_seleccionados,
    localidades_seleccionadas,
    estados_seleccionados,
)
df_master = aplicar_filtros(
    df_master_base,
    ciclos_seleccionados,
    localidades_seleccionadas,
    estados_seleccionados,
)
df_empresas = empresas_de_practicas(df_empresas_raw, df_practicas)

if not df_alumnos.empty and "vehiculo" in df_alumnos.columns:
    vehiculos = df_alumnos["vehiculo"].astype(str).str.strip().str.lower()
    tasa_movilidad = vehiculos.isin({"sí", "si", "true", "1"}).mean() * 100
else:
    tasa_movilidad = 0

st.subheader("Resumen")
kpi_1, kpi_2, kpi_3, kpi_4 = st.columns(4)
card(kpi_1, "🎓", "Alumnos totales", len(df_alumnos), AZUL_CAMARA)
card(kpi_2, "🏢", "Empresas", len(df_empresas), CIAN_CAMARA)
card(kpi_3, "🤝", "Matches realizados", len(df_practicas), "#003366")
card(kpi_4, "🚗", "Tasa de movilidad", f"{tasa_movilidad:.1f}%", "#5B8C5A")

st.divider()
tab_alumnos, tab_ofertas, tab_gestion, tab_empresas, tab_feedback = st.tabs(
    ["🎓 Alumnos", "🏢 Ofertas", "⚙️ Gestión", "📍 Empresas", "📩 Feedback"]
)

with tab_alumnos:
    st.subheader("Detalle de alumnos")
    if df_alumnos.empty:
        st.info("No hay alumnos para los filtros seleccionados.")
    else:
        col_1, col_2 = st.columns(2)
        with col_1:
            if "ciclo_formativo" in df_alumnos.columns:
                datos_ciclo = df_alumnos["ciclo_formativo"].fillna("Sin definir").value_counts().reset_index()
                datos_ciclo.columns = ["Ciclo", "Alumnos"]
                st.plotly_chart(
                    px.bar(
                        datos_ciclo,
                        x="Alumnos",
                        y="Ciclo",
                        orientation="h",
                        text_auto=True,
                        color_discrete_sequence=[AZUL_CAMARA],
                    ),
                    use_container_width=True,
                )
        with col_2:
            if "estado" in df_alumnos.columns:
                datos_estado = df_alumnos["estado"].fillna("Sin definir").value_counts().reset_index()
                datos_estado.columns = ["Estado", "Alumnos"]
                st.plotly_chart(
                    px.pie(
                        datos_estado,
                        names="Estado",
                        values="Alumnos",
                        hole=0.5,
                        color_discrete_sequence=PALETA_GRAFICOS,
                    ),
                    use_container_width=True,
                )
        columnas_alumnos = [
            columna
            for columna in (
                "dni",
                "nombre",
                "apellido",
                "localidad",
                "ciclo_formativo",
                "estado",
                "vehiculo",
            )
            if columna in df_alumnos.columns
        ]
        st.dataframe(df_alumnos[columnas_alumnos], hide_index=True, use_container_width=True)

with tab_ofertas:
    st.subheader("Detalle de ofertas y plazas")
    df_ofertas = filtrar_por_curso(df_ofertas_raw, anio_filtro, curso_filtro)
    if ciclos_seleccionados and "ciclo_formativo" in df_ofertas.columns:
        df_ofertas = df_ofertas[
            df_ofertas["ciclo_formativo"].astype(str).isin(ciclos_seleccionados)
        ]
    if localidades_seleccionadas and "localidad" in df_ofertas.columns:
        localidades_limpias = {limpiar_localidad(valor) for valor in localidades_seleccionadas}
        df_ofertas = df_ofertas[
            df_ofertas["localidad"].map(limpiar_localidad).isin(localidades_limpias)
        ]
    if df_ofertas.empty:
        st.info("No hay ofertas para los filtros seleccionados.")
    else:
        if "nombre" in df_ofertas.columns and "cupos_disponibles" in df_ofertas.columns:
            datos_ofertas = (
                df_ofertas.groupby("nombre", as_index=False)["cupos_disponibles"]
                .sum()
                .sort_values("cupos_disponibles", ascending=True)
            )
            st.plotly_chart(
                px.bar(
                    datos_ofertas,
                    x="cupos_disponibles",
                    y="nombre",
                    orientation="h",
                    text_auto=True,
                    color_discrete_sequence=[CIAN_CAMARA],
                    labels={"cupos_disponibles": "Plazas disponibles", "nombre": ""},
                ),
                use_container_width=True,
            )
        st.dataframe(df_ofertas, hide_index=True, use_container_width=True)

with tab_gestion:
    st.subheader("Gestión y documentación pendiente")
    df_gestion = df_master if not df_master.empty else df_practicas
    if df_gestion.empty:
        st.info("No hay formaciones para los filtros seleccionados.")
    else:
        anexos_pendientes = (
            int((df_gestion["anexos_firmados"] != True).sum())
            if "anexos_firmados" in df_gestion.columns
            else 0
        )
        sao_pendiente = (
            int((df_gestion["doc_sao_entregada"] != True).sum())
            if "doc_sao_entregada" in df_gestion.columns
            else 0
        )
        gestion_1, gestion_2, gestion_3 = st.columns(3)
        gestion_1.metric("Anexos sin firmar", anexos_pendientes)
        gestion_2.metric("Documentación SAO pendiente", sao_pendiente)
        gestion_3.metric("Formaciones", len(df_gestion))
        columnas_gestion = [
            columna
            for columna in (
                "nombre",
                "apellido",
                "empresa",
                "gestor",
                "anexos_firmados",
                "doc_sao_entregada",
            )
            if columna in df_gestion.columns
        ]
        st.dataframe(df_gestion[columnas_gestion], hide_index=True, use_container_width=True)

with tab_empresas:
    st.subheader("Empresas relacionadas")
    if df_empresas.empty:
        st.info("No hay empresas relacionadas con los filtros seleccionados.")
    else:
        empresas_1, empresas_2 = st.columns(2)
        with empresas_1:
            if "localidad" in df_empresas.columns:
                datos_localidad = df_empresas["localidad"].map(limpiar_localidad).value_counts().reset_index()
                datos_localidad.columns = ["Localidad", "Empresas"]
                st.plotly_chart(
                    px.bar(
                        datos_localidad,
                        x="Empresas",
                        y="Localidad",
                        orientation="h",
                        text_auto=True,
                        color_discrete_sequence=[CIAN_CAMARA],
                    ),
                    use_container_width=True,
                )
        with empresas_2:
            st.metric("Empresas relacionadas", len(df_empresas))
        columnas_empresas = [
            columna
            for columna in (
                "CIF",
                "nombre",
                "direccion",
                "localidad",
                "telefono",
                "email_empresa",
            )
            if columna in df_empresas.columns
        ]
        st.dataframe(df_empresas[columnas_empresas], hide_index=True, use_container_width=True)

with tab_feedback:
    st.subheader("Feedback")
    if df_feedback_stats.empty:
        st.info("Aún no hay datos de feedback para los filtros seleccionados.")
    else:
        recibidas = (
            df_feedback_stats["total_respuestas_recibidas"].sum()
            if "total_respuestas_recibidas" in df_feedback_stats.columns
            else 0
        )
        enviadas = (
            df_feedback_stats["total_alumnos_asignados"].sum()
            if "total_alumnos_asignados" in df_feedback_stats.columns
            else 0
        )
        tasa_respuesta = recibidas / enviadas * 100 if enviadas else 0
        feedback_1, feedback_2, feedback_3 = st.columns(3)
        feedback_1.metric("Tasa de respuesta", f"{tasa_respuesta:.1f}%")
        feedback_2.metric("Respuestas recibidas", int(recibidas))
        feedback_3.metric(
            "Respuestas del mes",
            int(df_feedback_stats["respuestas_mes_actual"].sum())
            if "respuestas_mes_actual" in df_feedback_stats.columns
            else 0,
        )
        st.dataframe(
            df_feedback_stats,
            hide_index=True,
            use_container_width=True,
        )

st.divider()
if not df_alumnos.empty:
    st.download_button(
        "📥 Exportar alumnos filtrados",
        data=exportar_excel(df_alumnos),
        file_name=f"alumnos_fp_{datetime.now().strftime('%Y%m%d')}.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )
