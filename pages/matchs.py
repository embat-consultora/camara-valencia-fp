import streamlit as st
import pandas as pd
import json
from modules.data_base import getMatches, upsert, add, getOfertaEmpresas,getEquals,crearPractica
from page_utils import apply_page_config
from navigation import make_sidebar
from variables import alumnosTabla, tutoresTabla, necesidadFP, estadosAlumno, practicaTabla, alumnoEstadosTabla, verdeOk, estados,practicaEstadosTabla
from datetime import datetime
from modules.text_helper import st_custom_message
import os
now = datetime.now().isoformat()

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
            keys=["id"],
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
ofertas = getOfertaEmpresas(necesidadFP, {}) 
alumnosList = getEquals(alumnosTabla, {"estado": "Sin Empresa"})
if not ofertas:
    st.info("No se encontraron ofertas registradas.")
    st.stop()
base_url = os.getenv("URL")

empresas_disponibles = []
for o in ofertas:
    empresa_info = o.get("empresas", {})
    if empresa_info and empresa_info.get("CIF"):
        empresas_disponibles.append({
            "nombre": empresa_info.get("nombre", "Sin nombre"),
            "CIF": empresa_info.get("CIF")
        })

# Eliminar duplicados (por CIF)
empresas_unicas = {e["CIF"]: e["nombre"] for e in empresas_disponibles}
empresa_opciones = ["Todas"] + [f"{nombre} ({cif})" for cif, nombre in empresas_unicas.items()]
col1,col2 = st.columns([2,3])
with col1:
    empresa_seleccionada = st.selectbox("🏢 Filtrar por Empresa", options=empresa_opciones)
    
# Filtrar ofertas según selección
if empresa_seleccionada != "Todas":
    cif_seleccionado = empresa_seleccionada.split("(")[-1].replace(")", "")
    ofertas = [o for o in ofertas if o.get("empresas", {}).get("CIF") == cif_seleccionado]

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
    tutores=getEquals(tutoresTabla,{"id":oferta_data.get("tutor")})

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
            st.write(f"**Requisitos:**", oferta_data.get("requisitos"), "Ninguno especificado")
            st.write(f"**Vehículo:**", oferta_data.get("vehiculo", "Ninguno especificado"))
            st.write(f"**Contrato:**", oferta_data.get("contrato", "Ninguno especificado"))
            st.write(f"**CP:**", oferta_data.get("cp_empresa", "Ninguno especificado"))
        with col2:
            st.write(f"**Dirección:**", oferta_data.get("direccion_empresa", "Ninguno especificado"))
            st.write(f"**Localidad:**", oferta_data.get("localidad_empresa", "Ninguno especificado"))
            #tutores = oferta_data.get("tutores", [])
            if tutores:
                st.write(f"**Tutor:**", tutores[0].get("nombre"))
                st.write(f"**Email:**", tutores[0].get("email"))
            else:
                st.write(f"**Tutor:**",  "Ninguno asignado")
                st.write(f"**Email:**", "Sin email")
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
                proyecto = (
                    oferta_data.get("puestos", {})
                    .get(ciclo, [{}])[0]
                    .get("proyecto")
                    or "No completado"
                )
                area = (
                    oferta_data.get("puestos", {})
                    .get('area', [{}])[0]
                    .get("proyecto")
                    or "No completado"
                )
                st.write(f"**Proyectos:**",proyecto  )
                st.write(f"📦 Cupos disponibles: {cupos_disp}/{cupos_total}")

                if cupos_disp <= 0:
                    st_custom_message("La oferta está cogida", color=verdeOk, emoji="✅")
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
                                        f"- Preferencias: {row['pts_pref']} {'✅' if row['pts_pref'] > 0 else ''}\n"
                                        f"- Requisitos: {row['pts_requisitos']} {'✅' if row['pts_requisitos'] > 0 else ''}"
                                    )

                                with col3:
                                    if cupos_disp > 0:
                                        if st.button("Asignar", key=f"match_{oferta_id}_{row['alumno_id']}"):
                                            try:
                                                crearPractica(empresa.get("CIF"), row['alumno_dni'], ciclo, area,proyecto, fecha=now,ciclos_info=ciclos_info ,cupos_disp=cupos_disp,oferta_id=row["oferta_id"])
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
                                st.write(f"**Requisitos:** {alumno_info.get('requisitos', 'No especificado')}")


                    with colMatch:  
                        if alumnoSeleccionado != "Selecciona":
                            dni_alumno = alumnoSeleccionado.split("(")[-1].replace(")", "")
                            if st.button("Asignar Alumno", key=f"match_manual_{oferta_id}_{ciclo}_{dni_alumno}"):
                                try:
                                    matchAlumno(empresa.get("CIF"), dni_alumno, oferta_id, ciclo, ciclos_info, cupos_disp, proyecto, area)
                                    checkEstadoOferta(oferta_id)
                                    st.success(f"✅ Match creado con {alumnoSeleccionado} 🎉")
                                    st.rerun()
                                except Exception as e:
                                    st.error(f"❌ Error al crear el match: {e}")
