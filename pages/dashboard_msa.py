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
    estadosAlumno,
    feedbackResponseTabla,
    necesidadFP,
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

    df_ofertas = pd.DataFrame(get(necesidadFP))

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
            columnas_alumno = [
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
            datos_alumnos = df_alumnos[columnas_alumno].rename(
                columns={
                    "localidad": "localidad_alumno",
                    "ciclo_formativo": "ciclo_formativo_alumno",
                }
            )
            df_master = df_practicas.merge(
                datos_alumnos,
                left_on=columna_alumno,
                right_on="dni",
                how="left",
            )
            if "localidad_alumno" in df_master.columns:
                df_master["localidad"] = df_master["localidad_alumno"]
            if "ciclo_formativo_alumno" in df_master.columns:
                df_master["ciclo_formativo"] = df_master["ciclo_formativo_alumno"]
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


@st.cache_data
def load_feedback_respuestas():
    return pd.DataFrame(get(feedbackResponseTabla))


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


def ofertas_activas_por_ciclo(df_ofertas, df_empresas):
    if df_ofertas.empty:
        return pd.DataFrame(
            columns=[
                "id",
                "empresa",
                "nombre",
                "ciclo_formativo",
                "cupos_disponibles",
                "localidad",
                "created_at",
                "anio",
            ]
        )

    empresas_por_cif = {}
    if not df_empresas.empty and "CIF" in df_empresas.columns:
        empresas_por_cif = {
            str(empresa["CIF"]): empresa
            for empresa in df_empresas.to_dict("records")
        }

    ofertas_ciclos = []
    for oferta in df_ofertas.to_dict("records"):
        ciclos_oferta = oferta.get("ciclos_formativos")
        if not isinstance(ciclos_oferta, dict):
            continue

        empresa = empresas_por_cif.get(str(oferta.get("empresa")), {})
        for ciclo, datos_ciclo in ciclos_oferta.items():
            if not isinstance(datos_ciclo, dict):
                continue
            disponibles = pd.to_numeric(
                datos_ciclo.get("disponibles"), errors="coerce"
            )
            if pd.isna(disponibles) or disponibles <= 0:
                continue

            ofertas_ciclos.append(
                {
                    "id": oferta.get("id"),
                    "empresa": oferta.get("empresa"),
                    "nombre": empresa.get("nombre", "Sin empresa"),
                    "ciclo_formativo": ciclo,
                    "cupos_disponibles": disponibles,
                    "localidad": oferta.get("localidad_empresa")
                    or empresa.get("localidad"),
                    "created_at": oferta.get("created_at"),
                    "anio": oferta.get("anio"),
                }
            )

    return pd.DataFrame(ofertas_ciclos)


def es_verdadero(valor):
    if isinstance(valor, bool):
        return valor
    return str(valor).strip().lower() in {"sí", "si", "true", "1"}


def datos_feedback_cierre_alumno(df_respuestas, df_practicas):
    columnas = ["curso", "valoracion", "happy"]
    if df_respuestas.empty or df_practicas.empty or "id" not in df_practicas.columns:
        return pd.DataFrame(columns=columnas)

    practicas_por_id = {
        str(practica["id"]): practica
        for practica in df_practicas.to_dict("records")
    }
    resultados = []
    for respuesta in df_respuestas.to_dict("records"):
        respuestas_json = respuesta.get("respuestas_json")
        if not isinstance(respuestas_json, dict):
            continue
        if respuestas_json.get("tipo") != "feedback_cierre":
            continue

        practica = practicas_por_id.get(str(respuesta.get("practica_id")))
        evaluacion = respuestas_json.get("evaluacion_global") or {}
        if practica is None or not isinstance(evaluacion, dict):
            continue

        valoracion = pd.to_numeric(evaluacion.get("positiva"), errors="coerce")
        if pd.isna(valoracion):
            continue
        resultados.append(
            {
                "curso": practica.get("curso", "Sin definir"),
                "valoracion": valoracion,
                "happy": valoracion >= 4,
            }
        )

    return pd.DataFrame(resultados, columns=columnas)


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
df_feedback_respuestas = load_feedback_respuestas()

anio_filtro = st.session_state.get("selector_curso_ac_global", aniosList[0])
curso_filtro = st.session_state.get("selector_curso_global", cursoList[0])

df_feedback_base = filtrar_por_curso(df_feedback_stats, anio_filtro, curso_filtro)
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
df_practicas_dashboard = df_master
df_ofertas = filtrar_por_curso(
    ofertas_activas_por_ciclo(df_ofertas_raw, df_empresas_raw),
    anio_filtro,
    curso_filtro,
)
if ciclos_seleccionados and "ciclo_formativo" in df_ofertas.columns:
    df_ofertas = df_ofertas[
        df_ofertas["ciclo_formativo"].astype(str).isin(ciclos_seleccionados)
    ]
if localidades_seleccionadas and "localidad" in df_ofertas.columns:
    localidades_limpias = {
        limpiar_localidad(localidad) for localidad in localidades_seleccionadas
    }
    df_ofertas = df_ofertas[
        df_ofertas["localidad"].map(limpiar_localidad).isin(localidades_limpias)
    ]
if estados_seleccionados:
    ciclos_alumnos_filtrados = set(
        df_alumnos["ciclo_formativo"].dropna().astype(str)
    ) if "ciclo_formativo" in df_alumnos.columns else set()
    if "ciclo_formativo" in df_ofertas.columns:
        df_ofertas = df_ofertas[
            df_ofertas["ciclo_formativo"].astype(str).isin(ciclos_alumnos_filtrados)
        ]

if not df_ofertas.empty:
    df_ofertas["cupos_disponibles"] = pd.to_numeric(
        df_ofertas["cupos_disponibles"], errors="coerce"
    ).fillna(0)
    df_ofertas = df_ofertas[df_ofertas["cupos_disponibles"] > 0]

if not df_ofertas.empty and "empresa" in df_ofertas.columns:
    empresas_con_ofertas_activas = df_ofertas["empresa"].dropna().astype(str).nunique()
else:
    empresas_con_ofertas_activas = (
        df_ofertas["nombre"].nunique() if "nombre" in df_ofertas.columns else 0
    )

if not df_alumnos.empty and "vehiculo" in df_alumnos.columns:
    vehiculos = df_alumnos["vehiculo"].astype(str).str.strip().str.lower()
    tasa_movilidad = vehiculos.isin({"sí", "si", "true", "1"}).mean() * 100
else:
    tasa_movilidad = 0

st.subheader("Resumen")
kpi_1, kpi_2, kpi_3, kpi_4 = st.columns(4)
card(kpi_1, "🎓", "Alumnos totales", len(df_alumnos), AZUL_CAMARA)
card(kpi_2, "🏢", "Empresas con ofertas activas", empresas_con_ofertas_activas, CIAN_CAMARA)
card(kpi_3, "🤝", "Formaciones Iniciadas", len(df_practicas_dashboard), "#003366")
card(kpi_4, "🚗", "Tasa de movilidad", f"{tasa_movilidad:.1f}%", "#5B8C5A")

st.divider()
tab_alumnos, tab_ofertas, tab_feedback = st.tabs(
    ["🎓 Alumnos", "🏢 Ofertas", "📩 Formaciones"]
)

with tab_alumnos:
    st.subheader("Detalle de alumnos")
    if df_alumnos.empty:
        st.info("No hay alumnos para los filtros seleccionados.")
    else:
        col_1, col_2 = st.columns(2)
        with col_1:
            if "sexo" in df_alumnos.columns:
                sexo = df_alumnos["sexo"].astype("string").str.strip()
                sin_especificar = (
                    sexo.isna()
                    | sexo.eq("")
                    | sexo.str.casefold().isin(
                        {"none", "null", "nan", "Prefiero No especificar"}
                    )
                )
                sexo = sexo.mask(sin_especificar, "Prefiero No especificar")

                datos_sexo = sexo.value_counts().rename_axis("Sexo").reset_index(name="Alumnos")
                datos_sexo.columns = ["Sexo", "Alumnos"]
                st.plotly_chart(
                    px.pie(
                        datos_sexo,
                        names="Sexo",
                        values="Alumnos",
                        hole=0.5,
                        title="Alumnos por sexo",
                        color_discrete_sequence=PALETA_GRAFICOS,
                    ),
                    use_container_width=True,
                )
            if "vehiculo" in df_alumnos.columns:
                def movilidad_label(valor):
                    if pd.isna(valor):
                        return "Sin definir"
                    return "Sí" if es_verdadero(valor) else "No"

                datos_movilidad = (
                    df_alumnos["vehiculo"]
                    .map(movilidad_label)
                    .value_counts()
                    .rename_axis("Movilidad")
                    .reset_index(name="Alumnos")
                )
                st.plotly_chart(
                    px.pie(
                        datos_movilidad,
                        names="Movilidad",
                        values="Alumnos",
                        hole=0.5,
                        title="Alumnos con movilidad",
                        color_discrete_sequence=[CIAN_CAMARA, AZUL_CAMARA],
                    ),
                    use_container_width=True,
                )
        with col_2:
            if "tipoPractica" in df_alumnos.columns:
                datos_tipo_formacion = (
                    df_alumnos["tipoPractica"]
                    .fillna("Sin definir")
                    .value_counts()
                    .rename_axis("Tipo de formación")
                    .reset_index(name="Alumnos")
                )
                st.plotly_chart(
                    px.pie(
                        datos_tipo_formacion,
                        names="Tipo de formación",
                        values="Alumnos",
                        hole=0.5,
                        title="Alumnos por tipo de formación",
                        color_discrete_sequence=PALETA_GRAFICOS,
                    ),
                    use_container_width=True,
                )
            if "localidad" in df_alumnos.columns:
                datos_localidad = (
                    df_alumnos["localidad"]
                    .map(limpiar_localidad)
                    .value_counts()
                    .rename_axis("Localidad")
                    .reset_index(name="Alumnos")
                    .sort_values("Alumnos", ascending=True)
                )
                st.plotly_chart(
                    px.bar(
                        datos_localidad,
                        x="Localidad",
                        y="Alumnos",
                        text_auto=True,
                        title="Alumnos por localidad",
                        color_discrete_sequence=[AZUL_CAMARA],
                    ),
                    use_container_width=True,
                )

with tab_ofertas:
    st.subheader("Ofertas disponibles por ciclo")
    columnas_match = {"oferta", "created_at"}
    if (
        columnas_match.issubset(df_practicas_dashboard.columns)
        and {"id", "created_at"}.issubset(df_ofertas_raw.columns)
    ):
        practicas_match = df_practicas_dashboard[
            ["oferta", "created_at"]
        ].copy()
        ofertas_match = df_ofertas_raw[["id", "created_at"]].copy()

        practicas_match["oferta_id_match"] = pd.to_numeric(
            practicas_match["oferta"], errors="coerce"
        ).astype("Int64")
        ofertas_match["oferta_id_match"] = pd.to_numeric(
            ofertas_match["id"], errors="coerce"
        ).astype("Int64")
        practicas_match["fecha_practica"] = pd.to_datetime(
            practicas_match["created_at"], errors="coerce", utc=True
        )
        ofertas_match["fecha_oferta"] = pd.to_datetime(
            ofertas_match["created_at"], errors="coerce", utc=True
        )

        tiempos_match_df = practicas_match.dropna(
            subset=["oferta_id_match", "fecha_practica"]
        ).merge(
            ofertas_match.dropna(subset=["oferta_id_match", "fecha_oferta"])[
                ["oferta_id_match", "fecha_oferta"]
            ],
            on="oferta_id_match",
            how="inner",
            validate="many_to_one",
        )
        tiempos_match_df["dias_match"] = (
            tiempos_match_df["fecha_practica"]
            - tiempos_match_df["fecha_oferta"]
        ).dt.total_seconds() / 86400
    else:
        tiempos_match_df = pd.DataFrame(columns=["dias_match"])

    if df_ofertas.empty:
        st.info("No hay ofertas para los filtros seleccionados.")
    else:
        ofertas_disponibles = (
            df_ofertas["id"].nunique() if "id" in df_ofertas.columns else len(df_ofertas)
        )
        plazas_disponibles = int(df_ofertas["cupos_disponibles"].sum())
        df_alumnos_disponibles = df_alumnos
        if "estado" in df_alumnos_disponibles.columns:
            df_alumnos_disponibles = df_alumnos_disponibles[
                df_alumnos_disponibles["estado"].astype(str).str.casefold()
                == estadosAlumno[0].casefold()
            ]

        oferta_1, oferta_2 = st.columns(2)
        oferta_1.metric("Ofertas disponibles", ofertas_disponibles)
        oferta_2.metric("Plazas disponibles", plazas_disponibles)

        ofertas_por_ciclo = (
            df_ofertas.groupby("ciclo_formativo")
            .agg({"id": "nunique", "cupos_disponibles": "sum"})
            .rename(
                columns={
                    "id": "Ofertas disponibles",
                    "cupos_disponibles": "Plazas disponibles",
                }
            )
            .reset_index()
        )
        alumnos_por_ciclo = (
            df_alumnos_disponibles.groupby("ciclo_formativo")["dni"]
            .nunique()
            .rename("Alumnos disponibles")
            if "ciclo_formativo" in df_alumnos_disponibles.columns
            and "dni" in df_alumnos_disponibles.columns
            else pd.Series(dtype="int64", name="Alumnos disponibles")
        )
        datos_ciclo = ofertas_por_ciclo[["ciclo_formativo", "Ofertas disponibles"]].merge(
            alumnos_por_ciclo,
            left_on="ciclo_formativo",
            right_index=True,
            how="outer",
        )
        for columna in ("Ofertas disponibles", "Alumnos disponibles"):
            if columna in datos_ciclo.columns:
                datos_ciclo[columna] = datos_ciclo[columna].fillna(0)
        datos_ciclo["ciclo_formativo"] = datos_ciclo["ciclo_formativo"].fillna(
            "Sin definir"
        )
        grafico_ofertas, grafico_alumnos = st.columns(2)
        with grafico_ofertas:
            st.plotly_chart(
                px.bar(
                    datos_ciclo.sort_values("Ofertas disponibles"),
                    x="ciclo_formativo",
                    y="Ofertas disponibles",
                    text_auto=True,
                    title="Ofertas disponibles por ciclo",
                    color_discrete_sequence=[CIAN_CAMARA],
                    labels={
                        "Ofertas disponibles": "Cantidad de ofertas",
                        "ciclo_formativo": "Ciclo formativo",
                    },
                ),
                use_container_width=True,
            )
        with grafico_alumnos:
            st.plotly_chart(
                px.bar(
                    datos_ciclo.sort_values("Alumnos disponibles"),
                    x="ciclo_formativo",
                    y="Alumnos disponibles",
                    text_auto=True,
                    title="Alumnos disponibles por ciclo",
                    color_discrete_sequence=[AZUL_CAMARA],
                    labels={
                        "Alumnos disponibles": "Cantidad de alumnos",
                        "ciclo_formativo": "Ciclo formativo",
                    },
                ),
                use_container_width=True,
            )

        if "nombre" in df_ofertas.columns:
            datos_ofertas = (
                df_ofertas.groupby("nombre", as_index=False)["cupos_disponibles"]
                .sum()
                .sort_values("cupos_disponibles", ascending=True)
            )
            st.plotly_chart(
                px.bar(
                    datos_ofertas,
                    x="nombre",
                    y="cupos_disponibles",
                    text_auto=True,
                    color_discrete_sequence=[CIAN_CAMARA],
                    labels={"cupos_disponibles": "Plazas disponibles", "nombre": ""},
                    title="Plazas disponibles por empresa",
                ),
                use_container_width=True,
            )

    if not tiempos_match_df.empty:
        match_tiempo, match_total = st.columns(2)
        match_tiempo.metric(
            "Tiempo medio entre creación de oferta y formaciones",
            f"{tiempos_match_df['dias_match'].mean():.1f} días",
        )
        match_total.metric(
            "Formaciones enlazadas con ofertas",
            len(tiempos_match_df)
        )
    else:
        st.info(
            "No hay formaciones enlazadas por ID de oferta con fechas de creación "
            "válidas para calcular el tiempo medio."
        )

with tab_feedback:
  st.subheader("Formaciones")

  if df_feedback_base.empty:
    st.info("Aún no hay datos de feedback para los filtros seleccionados.")
  else:
    # 1. Cálculo de métricas
    recibidas = (
        df_feedback_base["total_respuestas_recibidas"].sum()
        if "total_respuestas_recibidas" in df_feedback_base.columns
        else 0
    )
    enviadas = (
        df_feedback_base["total_alumnos_asignados"].sum()
        if "total_alumnos_asignados" in df_feedback_base.columns
        else 0
    )
    tasa_respuesta = recibidas / enviadas * 100 if enviadas else 0
    respuestas_mes = (
        int(df_feedback_base["respuestas_mes_actual"].sum())
        if "respuestas_mes_actual" in df_feedback_base.columns
        else 0
    )

    # 2. Cards estilizadas con CSS
    feedback_1, feedback_2, feedback_3 = st.columns(3)

    with feedback_1:
      st.markdown(
          f"""
            <div style="background-color: #f0f8ff; border-left: 5px solid #1E88E5; padding: 15px; border-radius: 8px; text-align: center;">
                <p style="margin: 0; font-size: 13px; color: #555; font-weight: 600;">TASA DE RESPUESTA</p>
                <h2 style="margin: 5px 0 0 0; color: #1E88E5; font-size: 26px;">{tasa_respuesta:.1f}%</h2>
            </div>
            """,
          unsafe_allow_html=True,
      )

    with feedback_2:
      st.markdown(
          f"""
            <div style="background-color: #f4fbf7; border-left: 5px solid #2ECC71; padding: 15px; border-radius: 8px; text-align: center;">
                <p style="margin: 0; font-size: 13px; color: #555; font-weight: 600;">RESPUESTAS RECIBIDAS</p>
                <h2 style="margin: 5px 0 0 0; color: #2ECC71; font-size: 26px;">{int(recibidas)}</h2>
            </div>
            """,
          unsafe_allow_html=True,
      )

    with feedback_3:
      st.markdown(
          f"""
            <div style="background-color: #fbf5fc; border-left: 5px solid #9B59B6; padding: 15px; border-radius: 8px; text-align: center;">
                <p style="margin: 0; font-size: 13px; color: #555; font-weight: 600;">RESPUESTAS DEL MES</p>
                <h2 style="margin: 5px 0 0 0; color: #9B59B6; font-size: 26px;">{respuestas_mes}</h2>
            </div>
            """,
          unsafe_allow_html=True,
      )

  st.markdown("<br>", unsafe_allow_html=True)
  st.subheader("Resultados de Formaciones")

  # --- A. VALORACIONES POSITIVAS Y CIERRES DE ALUMNOS (PRIMERO) ---
  cierres_alumno = datos_feedback_cierre_alumno(
      df_feedback_respuestas, df_practicas_dashboard
  )

  if cierres_alumno.empty:
    st.info(
        "No hay valoraciones de cierre de alumnos para los filtros"
        " seleccionados."
    )
  else:
    felicidad = cierres_alumno["happy"].mean() * 100
    feedback_cierre_1, feedback_cierre_2 = st.columns(2)
    feedback_cierre_1.metric(
        "% valoraciones positivas (4–5)", f"{felicidad:.1f}%"
    )
    feedback_cierre_2.metric(
        "Total de cierres valorados", len(cierres_alumno)
    )

    promedio_por_curso = cierres_alumno.groupby("curso", as_index=False).agg(
        cierres=("valoracion", "count"),
        promedio=("valoracion", "mean"),
        valoraciones_positivas=("happy", "mean"),
    )
    promedio_por_curso["% valoraciones positivas"] = (
        promedio_por_curso["valoraciones_positivas"] * 100
    )
    promedio_por_curso = promedio_por_curso.drop(
        columns="valoraciones_positivas"
    )

  st.markdown("<hr>", unsafe_allow_html=True)

  # --- B. GRÁFICOS DE TORTA EN 2 COLUMNAS ---
  graf_col1, graf_col2 = st.columns(2)

  # 1. Gráfico de Contratación
  with graf_col1:
    datos_cierre = []
    for practica in df_practicas_dashboard.to_dict("records"):
      cierre = practica.get("datos_cierre")
      if not isinstance(cierre, dict) or not cierre:
        continue
      contratado = es_verdadero(cierre.get("contratado", False))
      otra_empresa = es_verdadero(cierre.get("contratadoOtraEmpresa", False))
      datos_cierre.append({
          "contratacion": (
              "Contratado por la empresa"
              if contratado
              else (
                  "Contratado por otra empresa"
                  if otra_empresa
                  else "No contratado"
              )
          ),
      })

    if datos_cierre:
      df_cierre = pd.DataFrame(datos_cierre)
      conteo_cierre = df_cierre["contratacion"].value_counts().reset_index()
      conteo_cierre.columns = ["Estado", "Cantidad"]

      fig_cierre = px.pie(
          conteo_cierre,
          names="Estado",
          values="Cantidad",
          title="Estado de Contratación al Cierre",
          color="Estado",
          color_discrete_map={
              "Contratado por la empresa": "#2ecc71",  # Verde
              "No contratado": "#e74c3c",  # Rojo
              "Contratado por otra empresa": "#3498db",  # Azul
          },
          hole=0.35,
      )
      fig_cierre.update_traces(
          textinfo="percent+label",
          hovertemplate="%{label}: %{value} (%{percent})",
      )
      fig_cierre.update_layout(
          legend=dict(
              orientation="h",
              yanchor="bottom",
              y=-0.3,
              xanchor="center",
              x=0.5,
          )
      )

      st.plotly_chart(fig_cierre, use_container_width=True)
    else:
      st.info("Sin datos de cierre disponibles.")

  # 2. Gráfico de Participación FP Pyme
  with graf_col2:

    def mapear_estado(val):
      if pd.isna(val) or val is None or str(val).strip() == "":
        return "SIN DEFINIR"
      if isinstance(val, bool):
        return "SI" if val else "NO"
      if str(val).lower() in ["true", "1", "1.0", "si", "sí"]:
        return "SI"
      if str(val).lower() in ["false", "0", "0.0", "no"]:
        return "NO"
      return "SIN DEFINIR"

    if (
        "fp_dual_cogido" in df_practicas_dashboard.columns
        and not df_practicas_dashboard.empty
    ):
      df_grafico = df_practicas_dashboard.copy()
      df_grafico["estado_fp"] = df_grafico["fp_dual_cogido"].apply(
          mapear_estado
      )

      conteo_fp = df_grafico["estado_fp"].value_counts().reset_index()
      conteo_fp.columns = ["Estado", "Cantidad"]

      fig_fp = px.pie(
          conteo_fp,
          names="Estado",
          values="Cantidad",
          title="Participación FP Pyme",
          color="Estado",
          color_discrete_map={
              "SI": "#2ecc71",  # Verde
              "NO": "#e74c3c",  # Rojo
              "SIN DEFINIR": "#95a5a6",  # Gris
          },
          hole=0.35,
      )
      fig_fp.update_traces(
          textinfo="percent+label",
          hovertemplate="%{label}: %{value} (%{percent})",
      )
      fig_fp.update_layout(
          legend=dict(
              orientation="h",
              yanchor="bottom",
              y=-0.3,
              xanchor="center",
              x=0.5,
          )
      )

      st.plotly_chart(fig_fp, use_container_width=True)
    else:
      st.info("Sin datos disponibles para la columna FP Dual.")

