import streamlit as st
import pandas as pd
import json
from modules.data_base import getMatches, upsert, add, getOfertaEmpresas,getEquals
from page_utils import apply_page_config
from navigation import make_sidebar
from variables import alumnosTabla, necesidadFP, estadosAlumno, practicaTabla, alumnoEstadosTabla, verdeOk, estados
from datetime import datetime
from modules.text_helper import st_custom_message
import os
now = datetime.now().isoformat()
def matchAlumno(empresaCif, alumnoDni, ofertaId, ciclo,ciclos_info,cupos_disp):
    add(
        practicaTabla,
        {
            "empresa": empresaCif,
            "alumno": alumnoDni,
            "oferta": ofertaId,
            "estado": "Nueva"
        },
    )

    upsert(
        alumnosTabla,
        {"dni": alumnoDni, "estado": estadosAlumno[1]},
        keys=["dni"],
    )

    upsert(
        alumnoEstadosTabla,
        {"alumno": alumnoDni, 'match_fp': now, 'fp_asignada': now},
        keys=["alumno"]
    )

    ciclos_info[ciclo]["disponibles"] = max(cupos_disp - 1, 0)
    upsert(
        necesidadFP,
        {
            "id": oferta_id,
            "empresa": empresaCif,
            "ciclos_formativos": ciclos_info,
        },
        keys=["id"],
    )

def checkEstadoOferta(ofertaId):
    oferta = getOfertaEmpresas(necesidadFP, {"id": ofertaId})
    if not oferta:
        return
    oferta = oferta[0]
    ciclos_info = oferta.get("ciclos_formativos", {})
    if isinstance(ciclos_info, str):
        try:
            ciclos_info = json.loads(ciclos_info)
        except json.JSONDecodeError:
            ciclos_info = {}
    todos_completos = all(
        (info.get("disponibles", 0) <= 0) for info in ciclos_info.values()
    )
    if todos_completos:
        upsert(
            necesidadFP,
            {
                "id": ofertaId,
                "estado": estados[1],
                "empresa": oferta.get("empresa"),
            },
            keys=["empresa"],
        )
# ---------------------------------
# Configuración inicial
# ---------------------------------
apply_page_config()
make_sidebar()
st.set_page_config(page_title="Match", page_icon="🚀")
st.title("🚀 MATCH")

# ---------------------------------
# Traer todas las ofertas (necesidadFP)
# ---------------------------------
ofertas = getOfertaEmpresas(necesidadFP, {})  # trae todas las filas
alumnosList = getEquals(alumnosTabla, {"estado": "Sin Empresa"})
if not ofertas:
    st.info("No se encontraron ofertas registradas.")
    st.stop()
base_url = os.getenv("URL")
# ---------------------------------
# Obtener datos del ranking SQL (posibles matches)
# ---------------------------------
ranking = getMatches()
df_matches = pd.DataFrame(ranking) if ranking else pd.DataFrame()

# ---------------------------------
# Iterar sobre cada oferta
# ---------------------------------

for oferta_data in ofertas:
    empresa = oferta_data.get("empresas")
    nombre_empresa = oferta_data.get("nombre", "Empresa sin nombre")
    oferta_id = oferta_data.get("id")

    # Cargar ciclos formativos
    ciclos_info = oferta_data.get("ciclos_formativos", {})
    if isinstance(ciclos_info, str):
        try:
            ciclos_info = json.loads(ciclos_info)
        except json.JSONDecodeError:
            ciclos_info = {}

    ciclos = list(ciclos_info.keys())
    todos_completos = all(
        (info.get("disponibles", 0) <= 0) for info in ciclos_info.values()
    )
    # Filtrar posibles candidatos para esta oferta
    df_oferta = df_matches[df_matches["oferta_id"] == oferta_id] if not df_matches.empty else pd.DataFrame()

    # Contar matches posibles
    candidatos_count = len(df_oferta)
    if todos_completos:
        continue
    with st.expander(f"🏢 {empresa.get("nombre", "Empresa sin nombre")} — CIF: {empresa.get("CIF", "Sin CIF")} — Oferta #{oferta_id} ({candidatos_count} candidatos)"):
        col1, col2 = st.columns(2)
        with col1:
            st.write(f"**Requisitos:**", oferta_data.get("requisitos", "Ninguno especificado"))
            st.write(f"**Vehículo:**", oferta_data.get("vehiculo", "Ninguno especificado"))
            st.write(f"**Contrato:**", oferta_data.get("contrato", "Ninguno especificado"))
            st.write(f"**CP:**", oferta_data.get("cp_empresa", "Ninguno especificado"))
        with col2:
            st.write(f"**Dirección:**", oferta_data.get("direccion_empresa", "Ninguno especificado"))
            st.write(f"**Localidad:**", oferta_data.get("localidad_empresa", "Ninguno especificado"))
            st.write(f"**Tutor:**", oferta_data.get("nombre_tutor", "Ninguno especificado"))
            st.write(f"**Email:**", oferta_data.get("email_tutor", "Ninguno especificado"))

        if not ciclos:
            st.warning("⚠️ Esta oferta no tiene ciclos formativos asignados.")
            continue

        tab_objs = st.tabs(ciclos)

        for i, ciclo in enumerate(ciclos):
            with tab_objs[i]:
                st.subheader(f"🎓 {ciclo}")
                cupo_data = ciclos_info.get(ciclo, {"alumnos": 0, "disponibles": 0})
                cupos_total = cupo_data.get("alumnos", 0)
                cupos_disp = cupo_data.get("disponibles", 0)
                st.write(f"**Proyectos:**",  oferta_data["puestos"][ciclo][0]["proyecto"])
                st.write(f"**Area:**",  oferta_data["puestos"][ciclo][0]["area"])
                st.write(f"📦 Cupos disponibles: {cupos_disp}/{cupos_total}")

                if cupos_disp <= 0:
                    st_custom_message("Este Ciclo está completo!", color=verdeOk, emoji="✅")
                else:
                    df_ciclo = df_oferta[df_oferta["ciclo"] == ciclo] if not df_oferta.empty else pd.DataFrame()
                    st.write("Alumnos propuestos para este ciclo:")
                    if df_ciclo.empty:
                        st.info("No hay candidatos en el ranking para este ciclo.")
                    else:
                        with st.container(height=300):
                            df_ciclo = df_ciclo.sort_values("puntaje", ascending=False).reset_index(drop=True)
                            for _, row in df_ciclo.iterrows():
                                col1, col2, col3 = st.columns([4, 3, 2])

                                with col1:
                                    st.markdown(
                                        f"👤 [**{row['alumno_nombre']} {row['alumno_apellido']}**]({base_url}?alumno={row['alumno_dni']})",
                                        unsafe_allow_html=True
                                    )

                                with col2:
                                    st.write(
                                        f"Puntaje total: {row['puntaje']}\n"
                                        f"- Ciclo: {row['pts_ciclo']} {'✅' if row['pts_ciclo'] > 0 else ''}\n"
                                        f"- Vehículo: {row['pts_vehiculo']} {'✅' if row['pts_vehiculo'] > 0 else ''}\n"
                                        f"- Localidad: {row['pts_localidad']} {'✅' if row['pts_localidad'] > 0 else ''}\n"
                                        f"- Preferencias: {row['pts_pref']} {'✅' if row['pts_pref'] > 0 else ''}"
                                    )

                                with col3:
                                    if cupos_disp > 0:
                                        if st.button("Asignar", key=f"match_{oferta_id}_{row['alumno_id']}"):
                                            try:
                                                matchAlumno(empresa.get("CIF"), row['alumno_dni'], row["oferta_id"], ciclo,ciclos_info,cupos_disp)
                                                st.success(f"✅ Match creado con {row['alumno_nombre']} ({row['alumno_dni']}) 🎉")
                                                st.rerun()
                                            except Exception as e:
                                                st.error(f"❌ Error al crear el match: {e}")
                                    else:
                                        st.info("Cupos completos para este ciclo.")
                                
                    #asignar alumnos manualmente
                    colAlumno, colMatch = st.columns([3, 1])
                    with colAlumno:
                        opciones_alumnos = ["Selecciona"] + [f"{a['nombre']} {a['apellido']} ({a['dni']})" for a in alumnosList]
                        alumnoSeleccionado = st.selectbox(
                            "Asignar alumno manualmente",
                            options=opciones_alumnos,
                            key=f"select_manual_{oferta_id}_{ciclo}"
                        )

                        if alumnoSeleccionado != "Selecciona":
                            # Obtener el DNI desde la opción seleccionada
                            dni_alumno = alumnoSeleccionado.split("(")[-1].replace(")", "")
                            # Buscar información del alumno
                            alumno_info = next((a for a in alumnosList if a["dni"] == dni_alumno), None)
                            if alumno_info:
                                st.write(f"**Ciclo formativo:** {', '.join(alumno_info.get('ciclo_formativo', [])) if isinstance(alumno_info.get('ciclo_formativo'), list) else alumno_info.get('ciclo_formativo', 'No especificado')}")
                                st.write(f"**Preferencias FP:** {', '.join(alumno_info.get('preferencias_fp', [])) if isinstance(alumno_info.get('preferencias_fp'), list) else alumno_info.get('preferencias_fp', 'No especificado')}")
                                st.write(f"**Vehículo:** {alumno_info.get('vehiculo', 'No especificado')}")
                                st.write(f"**Localidad:** {alumno_info.get('localidad', 'No especificado')}")

                    with colMatch:  
                        if alumnoSeleccionado != "Selecciona":
                            dni_alumno = alumnoSeleccionado.split("(")[-1].replace(")", "")
                            if st.button("Asignar Alumno", key=f"match_manual_{oferta_id}_{ciclo}_{dni_alumno}"):
                                try:
                                    matchAlumno(empresa.get("CIF"), dni_alumno, oferta_id, ciclo, ciclos_info, cupos_disp)
                                    checkEstadoOferta(oferta_id)
                                    st.success(f"✅ Match creado con {alumnoSeleccionado} 🎉")
                                    st.rerun()
                                except Exception as e:
                                    st.error(f"❌ Error al crear el match: {e}")
