import streamlit as st
import pandas as pd
import json
from page_utils import apply_page_config
from navigation import make_sidebar
from modules.data_base import get, getEqual, getEquals, getTodosEmpresaOfertas
from modules.utils import df_to_excel
from variables import (
    empresasTabla,
    alumnosTabla,
    practicaTabla,
    practicaEstadosTabla,
    necesidadFP,
    tutoresTabla,
    fasesPractica,
    faseColPractica,
    formFieldsTabla,
    azul
)

# CONFIG
st.session_state["current_page"] = "dashboard"
st.set_page_config(page_title="Dashboard", page_icon="📊", layout="wide")
apply_page_config()
make_sidebar()

st.markdown(
    "<h2 style='text-align: center;'>📊 DASHBOARD OPERATIVO</h2>",
    unsafe_allow_html=True
)

# -------------------------------------------------------------------
# 1. LOAD DATA
# -------------------------------------------------------------------

df_emp = pd.DataFrame(get(empresasTabla))
df_al = pd.DataFrame(get(alumnosTabla))
df_prac = pd.DataFrame(get(practicaTabla))
df_ofe = pd.DataFrame(get(necesidadFP))
df_tut = pd.DataFrame(get(tutoresTabla))

# -------------------------------------------------------------------
# LOAD ALL CICLOS DESDE formFieldsTabla
# -------------------------------------------------------------------

form_fields = getEquals(formFieldsTabla, {"category": "Alumno", "type": "Opciones"})
ciclo_field = next((f for f in form_fields if f["columnName"] == "ciclo_formativo"), None)
ciclos_opts = json.loads(ciclo_field["options"]) if ciclo_field else []

# -------------------------------------------------------------------
# 2. CALCULAR ESTADO PRÁCTICA
# -------------------------------------------------------------------
if df_prac.empty:
    df_prac["estado_actual"] = None
    df_prac["empresa"] = None
    df_prac["alumno"] = None
    df_prac["ciclo_formativo"] = None
else:
    estado_por_practica = {}

    for _, p in df_prac.iterrows():
        pid = p["id"]
        estados = getEqual(practicaEstadosTabla, "practicaId", pid)

        if not estados:
            estado_actual = fasesPractica[0]
        else:
            registro = estados[0]
            estado_actual = fasesPractica[0]
            for fase in fasesPractica:
                col = faseColPractica[fase]
                if registro.get(col):
                    estado_actual = fase

        estado_por_practica[pid] = estado_actual

    df_prac["estado_actual"] = df_prac["id"].map(estado_por_practica)

    # Join empresa + alumno
df_prac = df_prac.merge(df_emp, left_on="empresa", right_on="CIF", suffixes=("", "_empresa"))
df_prac = df_prac.merge(df_al, left_on="alumno", right_on="dni", suffixes=("", "_alumno"))

# -------------------------------------------------------------------
# 3. KPIs — BALLS
# -------------------------------------------------------------------

total_empresas = len(df_emp)
empresas_con_practicas = df_prac["empresa"].nunique()

total_alumnos = len(df_al)
alumnos_con_practica = df_prac["alumno"].nunique()

practicas_in_progress = len(df_prac[df_prac["estado_actual"] == "Pasantía en progreso"])

def kpi_ball(title, value, color_bg="#013d5f", color_text="#FECA1D"):
    st.markdown(
        f"""
        <div style='text-align: center; color: black; font-size: 16px;font-weight: bold; margin-bottom: 8px;'>
            {title}
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown(
        f"""
        <div style="
            background-color: {color_bg};
            padding: 10px;
            border-radius: 50%;
            text-align: center;
            width: 100px;
            height: 100px;
            line-height: 80px;
            margin: 0 auto;">
            <span style="color: {color_text}; font-size: 24px; font-weight: bold;">
                {value}
            </span>
        </div>
        """,
        unsafe_allow_html=True,
    )

kpis = [
    ("Total Empresas", total_empresas),
    ("Empresas con práctica", empresas_con_practicas),
    ("Total Alumnos", total_alumnos),
    ("Alumnos con práctica", alumnos_con_practica),
    ("Prácticas en curso", practicas_in_progress),
]

st.subheader("Indicadores")
cols = st.columns(len(kpis))
for col, (title, value) in zip(cols, kpis):
    with col:
        kpi_ball(title, value)

# -------------------------------------------------------------------
# CREAR MASTER: EMPRESAS + OFERTAS + PRACTICAS
# -------------------------------------------------------------------

# Preparar OFERTAS con columnas limpias
df_ofe_clean = df_ofe.copy()
df_ofe_clean.rename(columns={"empresa": "CIF"}, inplace=True)

# Unir OFERTAS con EMPRESAS
df_master = df_ofe_clean.merge(
    df_emp,
    on="CIF",
    how="left",
    suffixes=("_oferta", "_empresa")
)

# Unir PRACTICAS
df_master = df_master.merge(
    df_prac[["id", "empresa", "estado_actual", "alumno", "ciclo_formativo"]],
    left_on="CIF",
    right_on="empresa",
    how="left"
)
df_al_ren = df_al.rename(columns={
    "nombre": "nombre_alumno",
    "apellido": "apellido_alumno",
})

df_master = df_master.merge(
    df_al_ren[["dni", "nombre_alumno", "apellido_alumno"]],
    left_on="alumno",
    right_on="dni",
    how="left"
)

df_master.rename(columns={"id": "practica_id"}, inplace=True)

# -------------------------------------------------------------------
# 4. FILTROS EMPRESAS
# --------s----------------------------------------------------------
st.subheader("")
tab2, tab1 = st.tabs(["🚀 Ofertas", " 💼 Prácticas"])

with tab1:
    c1, c2, c3 = st.columns(3)

    empresa_filter = c1.multiselect("Empresa", df_emp["nombre"].unique(), placeholder="Empresa")
    ciclo_filter = c2.multiselect("Ciclo Formativo", ciclos_opts, placeholder="Ciclo Formativo")
    estado_practica_filter = c3.multiselect("Estado práctica", fasesPractica, placeholder="Estado Práctica")


    df_f = df_master.copy()
    # FILTRO empresa
    if empresa_filter:
        df_f = df_f[df_f["nombre"].isin(empresa_filter)]

    # FILTRO ciclo
    if ciclo_filter:
        mask_prac = df_f["ciclo_formativo"].isin(ciclo_filter)
        df_f = df_f[mask_prac]

    # FILTRO estado práctica
    if estado_practica_filter:
        df_f = df_f[df_f["estado_actual"].isin(estado_practica_filter)]


    # -------------------------------------------------------------------
    # 5. TABLA PRINCIPAL EMPRESAS
    # -------------------------------------------------------------------
    st.subheader("📋 Empresas")
    cols_emp = [
        "nombre",
        "CIF",
        "telefono",
        "email_empresa",
        "direccion",
        "localidad",
        "responsable_legal",
        "horario"
    ]

    rename_map = {
        "nombre": "Nombre",
        "CIF": "CIF",
        "telefono": "Teléfono",
        "email_empresa": "Email",
        "direccion": "Dirección",
        "localidad": "Localidad",
        "responsable_legal": "Responsable Legal",
        "horario": "Horario"
    }

    # Filas únicas + columnas limpias
    df_emp_display = (
        df_f[cols_emp]
        .rename(columns=rename_map)
        .drop_duplicates()
        .reset_index(drop=True)
    )

    # Mostrar tabla
    if df_emp_display.empty:
        st.info("No hay empresas que coincidan con este filtro.")
    else:
        st.dataframe(
            df_emp_display,
            use_container_width=True,
            hide_index=True
        )


    # -------------------------------------------------------------------
    # 6. TABS: PRÁCTICAS
    # -------------------------------------------------------------------

    st.markdown("#### 🎓 Prácticas por Empresa")
    df_prac_display = df_f[df_f["practica_id"].notna()].copy()

    # Construimos el nombre del alumno correctamente
    df_prac_display["Alumno"] = (
        df_prac_display["nombre_alumno"].fillna("") + " " +
        df_prac_display["apellido_alumno"].fillna("")
    ).str.strip()
    # Seleccionamos las columnas correctas
    df_prac_display = df_prac_display[
        ["practica_id", "Alumno", "ciclo_formativo", "CIF","nombre", "estado_actual"]
    ].drop_duplicates()

    cols_practicas = [
        "practica_id",
        "Alumno",
        "ciclo_formativo",
        "CIF",
        "nombre",
        "estado_actual"
    ]

    rename_map_prac = {
        "practica_id":"Id",
        "Alumno":"Alumno",
        "ciclo_formativo": "Ciclo Formativo",
        "CIF":"CIF",
        "nombre": "Empresa",
        "estado_actual":"Estado Práctica"
    }

    # Filas únicas + columnas limpias
    df_prac_display = (
        df_prac_display[cols_practicas]
        .rename(columns=rename_map_prac)
        .drop_duplicates()
        .reset_index(drop=True)
    )


    # Mostrar
    if df_prac_display.empty:
        st.info("No hay prácticas para esta empresa.")
    else:
            st.dataframe(df_prac_display, use_container_width=True, hide_index=True)

st.divider()
with tab2:
    st.markdown("### 📥 Descargar datos")
    col1 , col2 = st.columns([1, 5])

    with col1:
        if st.button("⬇️ Descargar", use_container_width=True):

            # 1) Traer datos desde Supabase
            data_ofertas = getTodosEmpresaOfertas()
            if not data_ofertas:
                st.warning("No se encontraron ofertas para descargar.")
            else:
                df_ofertas = pd.DataFrame(data_ofertas)
                column_order = [
                "CIF", "Empresa", "telefono", "direccion", "localidad", "CP",
                "Email Empresa", "Nombre Responsable Legal", "NIF Responsable Legal",
                "horario", "pagina_web", "nombre_rellena",

                "ciclo_formativo", "alumnos_pedidos", "cupos_disponibles",
                "areas_puestos",

                "requisitos", "contrato", "vehiculo", "cupo_alumnos_totales_oferta",

                "Nombre Tutor", "Email Tutor", "Telefono Tutor",
            ]
                df_ofertas = df_ofertas[column_order]
                # 2) Exportar a Excel
                excel_bytes = df_to_excel(df_ofertas)
                st.download_button(
                    label="📄 Descargar archivo Excel",
                    data=excel_bytes,
                    file_name="ofertas_fp.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    use_container_width=True
                )

    c1, c2, c3 = st.columns(3)

    empresa_filter = c1.multiselect("Empresa", df_emp["nombre"].unique(), placeholder="Empresa",key="ofertaEmp")
    ciclo_filter = c2.multiselect("Ciclo Formativo", ciclos_opts, placeholder="Ciclo Formativo",key="ofertaCiclo")
    completa_filter = c3.multiselect("Oferta completa", ["Sí", "No"], placeholder="Completa?")


    df_f = df_master.copy()

    def oferta_completa(ciclos_json):
        if not ciclos_json:
            return False
        if isinstance(ciclos_json, dict):
            ciclos = ciclos_json
        else:
            try:
                ciclos = json.loads(ciclos_json)
            except:
                return False

        return all(v.get("disponibles", 0) == 0 for v in ciclos.values())

    df_f["completa"] = df_f["ciclos_formativos"].apply(oferta_completa)
    # FILTRO empresa
    if empresa_filter:
        df_f = df_f[df_f["nombre"].isin(empresa_filter)]

    # FILTRO ciclo
    if ciclo_filter:
        def oferta_tiene_ciclo(ciclos_json):
        # Si ciclos_json ya ES un dict → usarlo directo
            if isinstance(ciclos_json, dict):
                ciclos = ciclos_json
            else:
                try:
                    ciclos = json.loads(ciclos_json)
                except:
                    return False

            keys = [k.strip().lower() for k in ciclos.keys()]
            return any(c.lower().strip() in keys for c in ciclo_filter)


        mask_ofe = df_f["ciclos_formativos"].apply(oferta_tiene_ciclo)

        # 3) Combinar resultados → si cae por prácticas o por ofertas, pasa
        df_f = df_f[mask_ofe]
    if completa_filter:
        if "Sí" in completa_filter and "No" not in completa_filter:
            df_f = df_f[df_f["completa"] == True]
        elif "No" in completa_filter and "Sí" not in completa_filter:
            df_f = df_f[df_f["completa"] == False]
    # si tiene ambas → no se filtra
    # -------------------------------------------------------------------
    # 5. TABLA PRINCIPAL EMPRESAS
    # -------------------------------------------------------------------
    st.subheader("📋 Empresas")
    cols_emp = [
        "nombre",
        "CIF",
        "telefono",
        "email_empresa",
        "direccion",
        "localidad",
        "responsable_legal",
        "horario"
    ]

    rename_map = {
        "nombre": "Nombre",
        "CIF": "CIF",
        "telefono": "Teléfono",
        "email_empresa": "Email",
        "direccion": "Dirección",
        "localidad": "Localidad",
        "responsable_legal": "Responsable Legal",
        "horario": "Horario"
    }

    # Filas únicas + columnas limpias
    df_emp_display = (
        df_f[cols_emp]
        .rename(columns=rename_map)
        .drop_duplicates()
        .reset_index(drop=True)
    )

    # Mostrar tabla
    if df_emp_display.empty:
        st.info("No hay empresas que coincidan con este filtro.")
    else:
        st.dataframe(
            df_emp_display,
            use_container_width=True,
            hide_index=True,
            
        )


    # -------------------------------------------------------------------
    # 6. TABS: OFERTAS 
    # -------------------------------------------------------------------

    # OFERTAS
    st.markdown("#### 📄 Ofertas de FP")
    fps = df_f[["CIF","nombre", "ciclos_formativos", "puestos", "estado","vehiculo", "contrato","requisitos"]].copy()

    if not fps.empty:
        for i, (idx, fp) in enumerate(fps.iterrows(), start=1):
            estado_actual = fp["estado"] or "Nuevo"
            completa = False
            if fp["ciclos_formativos"]:
                completa = all(valores["disponibles"] == 0 for valores in fp["ciclos_formativos"].values())

            estado_visual = "Completa" if completa else estado_actual
            bg_color = "✅" if completa else ("🟧" if estado_actual == "Nuevo" else "✅")
            estado_actual =estado_visual

            with st.expander(
                f"Oferta #{i} | {fp['nombre']} - {fp['CIF']} - {estado_actual} {bg_color}",
                expanded=False
            ):

                ciclos = fp["ciclos_formativos"]
                puestos = fp["puestos"]

                if ciclos:
                    st.write("🎓 Ciclos formativos y cantidad de alumnos:")
                    data = [
                        {"Ciclo": ciclo, "Alumnos": valores["alumnos"], "Disponibles": valores["disponibles"]}
                        for ciclo, valores in ciclos.items()
                    ]
                    df_ciclos = pd.DataFrame(data, columns=["Ciclo", "Alumnos", "Disponibles"])
                    st.dataframe(df_ciclos, hide_index=True, use_container_width=True)

                if puestos:
                    st.write("🧩 Puestos por ciclo formativo:")
                    for ciclo, lista_puestos in puestos.items():
                        cantidad_alumnos = ciclos[ciclo]["alumnos"] if ciclos and ciclo in ciclos else None

                        with st.expander(f"{ciclo} ({cantidad_alumnos if cantidad_alumnos else 'Sin datos'} alumnos)"):
                            if lista_puestos:
                                for p in lista_puestos:
                                    st.write(f"- Área: {p['area']} — Proyecto: {p['proyecto'] if p['proyecto'] else "No mencionado" }")
                            else:
                                st.markdown("_Sin áreas o proyectos registrados_")

                requisitos = fp.get("requisitos")

                st.write(f"**Requisitos:** {requisitos if requisitos else 'No mencionados'}")

                st.write(f"**Contrato:** {'Sí' if fp['contrato'] else 'No'}")
                st.write(f"**Vehículo:** {'Sí' if fp['vehiculo'] else 'No'}")


