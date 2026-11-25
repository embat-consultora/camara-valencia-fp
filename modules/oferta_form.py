import streamlit as st
from modules.data_base import crearOfertaEmpresa, eliminarOferta, actualizarOfertaEmpresa, ofertaSinAsignaciones, minimoAlumnosPorCiclo
from modules.forms_helper import render_requisitos, requisitos_a_estado, slug
from variables import aniosList


def _prefijo(cif):
    return f"nueva_oferta_{slug(cif)}"


def nueva_oferta_abierta(cif):
    return bool(st.session_state.get(f"{_prefijo(cif)}_abierta"))


def abrir_nueva_oferta(cif):
    st.session_state[f"{_prefijo(cif)}_abierta"] = True


def cerrar_nueva_oferta(cif):
    k = _prefijo(cif)
    for key in [key for key in st.session_state if str(key).startswith(f"{k}_")]:
        del st.session_state[key]


def nueva_oferta(empresa, ciclos_lista, areas_map, tutores_empresa, anio_actual):
    """Form that creates a training offer for `empresa` from scratch."""
    cif = empresa["CIF"]
    k = _prefijo(cif)
    with st.container(border=True):
        st.markdown("#### ➕ Nueva oferta")

        anios = list(aniosList[1:])
        anio = st.selectbox(
            "Curso académico *", anios,
            index=anios.index(anio_actual) if anio_actual in anios else 0, key=f"{k}_anio",
        )

        tutor_id = None
        if tutores_empresa:
            opciones_tutor = {t["id"]: f"{t.get('nombre', '')} ({t.get('email', '')})" for t in tutores_empresa}
            tutor_id = st.selectbox(
                "Tutor de empresa", list(opciones_tutor), format_func=opciones_tutor.get,
                index=None, placeholder="Selecciona un tutor", key=f"{k}_tutor",
            )
        else:
            st.caption("No tienes tutores cargados, dirigete a la pestaña de Tutores para cargarlos.")

        st.markdown("**Ciclos formativos y puestos**")
        ciclos_sel = st.multiselect(
            "Ciclos formativos *", ciclos_lista, key=f"{k}_ciclos", placeholder="Selecciona ciclos",
        )
        alumnos, puestos = {}, {}
        for ciclo in ciclos_sel:
            st.markdown(f"🎓 **{ciclo}**")
            alumnos[ciclo] = st.number_input(
                "Cantidad de alumnos *", min_value=1, max_value=50, value=1, step=1,
                key=f"{k}_alumnos_{slug(ciclo)}",
            )
            areas = st.multiselect(
                "Puestos / áreas *", areas_map.get(ciclo, []),
                key=f"{k}_areas_{slug(ciclo)}", placeholder="Selecciona áreas",
            )
            puestos[ciclo] = [
                {"area": area, "proyecto": st.text_input(
                    f"Proyecto relacionado ({area})", key=f"{k}_proy_{slug(ciclo)}_{slug(area)}",
                ).strip()}
                for area in areas
            ]

        st.markdown("**Dirección del centro de trabajo**")
        direccion = st.text_input("Dirección", value=empresa.get("direccion") or "", key=f"{k}_dir")
        col_cp, col_loc = st.columns(2)
        with col_cp:
            cp = st.text_input("Código Postal", value=empresa.get("codigo_postal") or "", key=f"{k}_cp")
        with col_loc:
            localidad = st.text_input("Localidad", value=empresa.get("localidad") or "", key=f"{k}_loc")

        st.markdown("**Requisitos adicionales**")
        requisitos = render_requisitos(
            f"{k}_req", idiomas_label="Idiomas", skills_label="Skills",
            otros_label="Otros requisitos (por ejemplo, residencia)",
        )

        st.markdown("**Información adicional**")
        contrato = st.radio(
            "Si el alumno cubre las expectativas, ¿habría posibilidad de hacerle un contrato laboral? *",
            ["Sí", "No"], index=None, horizontal=True, key=f"{k}_contrato",
        )
        vehiculo = st.radio(
            "¿Se necesita vehículo propio para acceder a las instalaciones? *",
            ["Sí", "No"], index=None, horizontal=True, key=f"{k}_vehiculo",
        )

        faltan = []
        if not ciclos_sel:
            faltan.append("ciclos formativos")
        faltan += [f"área en {c}" for c in ciclos_sel if not puestos.get(c)]
        if contrato is None:
            faltan.append("posible contrato")
        if vehiculo is None:
            faltan.append("vehículo")
        if faltan:
            st.info("Completa los campos obligatorios: " + ", ".join(faltan))

        col_ok, col_no = st.columns([1, 1])
        with col_ok:
            guardar = st.button("💾 Crear oferta", type="primary", key=f"{k}_guardar", disabled=bool(faltan))
        with col_no:
            if st.button("Cancelar", key=f"{k}_cancelar"):
                cerrar_nueva_oferta(cif)
                st.rerun()

        if guardar:
            campos = {
                "anio": anio,
                "puestos": puestos,
                "direccion_empresa": direccion.strip(),
                "cp_empresa": cp.strip(),
                "localidad_empresa": localidad.strip(),
                "requisitos": requisitos,
                "contrato": contrato,
                "vehiculo": vehiculo,
            }
            if tutor_id is not None:
                campos["tutor"] = tutor_id
            try:
                crearOfertaEmpresa(cif, alumnos, campos)
            except Exception as e:
                st.error(f"No se pudo crear la oferta: {e}")
                return
            cerrar_nueva_oferta(cif)
            st.toast("Oferta creada", icon="✅")
            st.rerun()


def _si_no(valor):
    """contrato/vehiculo are saved as "Sí"/"No" (older rows may be booleans)."""
    if isinstance(valor, str):
        return "Sí" if valor.strip().lower() in ("sí", "si", "true") else "No"
    return "Sí" if valor else "No"


@st.dialog("Eliminar oferta")
def dialog_eliminar_oferta(fp, numero):
    st.warning(f"Vas a eliminar la **Oferta #{numero}** por completo. Esta acción no se puede deshacer.")
    col_ok, col_no = st.columns(2)
    with col_ok:
        if st.button("Eliminar", type="primary", key=f"confirmar_eliminar_oferta_{fp['id']}"):
            try:
                eliminarOferta(fp["id"])
            except Exception as e:
                st.error(str(e))
                return
            st.toast("Oferta eliminada", icon="✅")
            st.rerun()
    with col_no:
        if st.button("Volver", key=f"volver_eliminar_oferta_{fp['id']}"):
            st.rerun()


def editar_oferta(fp, areas_map):
    oid = fp["id"]
    k = f"oferta_{oid}"
    ciclos = fp.get("ciclos_formativos") or {}
    puestos = fp.get("puestos") or {}

    # Load the saved requirements into the widgets once
    if not st.session_state.get(f"{k}_req_cargado"):
        for key, value in requisitos_a_estado(f"{k}_req", fp.get("requisitos")).items():
            st.session_state[key] = value
        st.session_state[f"{k}_req_cargado"] = True

    st.markdown("**Ciclos formativos y puestos**")
    minimos = minimoAlumnosPorCiclo(fp)
    nuevos_alumnos, nuevos_puestos = {}, {}
    for ciclo, valores in ciclos.items():
        total = valores.get("alumnos") or 0
        inscriptos = minimos.get(ciclo, 0)
        st.markdown(f"🎓 **{ciclo}**")
        nuevos_alumnos[ciclo] = st.number_input(
            "Cantidad de alumnos", min_value=max(inscriptos, 1), max_value=50,
            value=max(total, inscriptos, 1), step=1, key=f"{k}_alumnos_{slug(ciclo)}",
            help=f"Ya hay {inscriptos} alumno(s) inscripto(s): no puede ser menor." if inscriptos else None,
        )
        if inscriptos:
            st.caption(f"Alumnos inscriptos: {inscriptos}. La cantidad no puede ser menor.")
        actuales = {p.get("area"): p.get("proyecto", "") for p in (puestos.get(ciclo) or []) if p.get("area")}
        opciones = list(dict.fromkeys(list(areas_map.get(ciclo, [])) + list(actuales)))
        areas = st.multiselect(
            "Puestos / áreas", opciones, default=list(actuales),
            key=f"{k}_areas_{slug(ciclo)}", placeholder="Selecciona áreas",
        )
        nuevos_puestos[ciclo] = [
            {"area": area, "proyecto": st.text_input(
                f"Proyecto relacionado ({area})", value=actuales.get(area, ""),
                key=f"{k}_proy_{slug(ciclo)}_{slug(area)}",
            ).strip()}
            for area in areas
        ]

    st.markdown("**Dirección del centro de trabajo**")
    direccion = st.text_input("Dirección", value=fp.get("direccion_empresa") or "", key=f"{k}_dir")
    col_cp, col_loc = st.columns(2)
    with col_cp:
        cp = st.text_input("Código Postal", value=fp.get("cp_empresa") or "", key=f"{k}_cp")
    with col_loc:
        localidad = st.text_input("Localidad", value=fp.get("localidad_empresa") or "", key=f"{k}_loc")

    st.markdown("**Requisitos adicionales**")
    requisitos = render_requisitos(
        f"{k}_req", idiomas_label="Idiomas", skills_label="Skills",
        otros_label="Otros requisitos (por ejemplo, residencia)",
    )

    st.markdown("**Información adicional**")
    contrato = st.radio(
        "Si el alumno cubre vuestras expectativas, ¿habría posibilidad de hacerle un contrato laboral?",
        ["Sí", "No"], index=["Sí", "No"].index(_si_no(fp.get("contrato"))),
        horizontal=True, key=f"{k}_contrato",
    )
    vehiculo = st.radio(
        "¿Se necesita vehículo propio para acceder a vuestras instalaciones?",
        ["Sí", "No"], index=["Sí", "No"].index(_si_no(fp.get("vehiculo"))),
        horizontal=True, key=f"{k}_vehiculo",
    )

    sin_area = [c for c, lista in nuevos_puestos.items() if not lista]
    if sin_area:
        st.markdown(
            f"<span style='color:red;'>Selecciona al menos un área en: {', '.join(sin_area)}</span>",
            unsafe_allow_html=True,
        )
    if st.button("💾 Guardar cambios", type="primary", key=f"{k}_guardar", disabled=bool(sin_area)):
        try:
            actualizarOfertaEmpresa(oid, nuevos_alumnos, {
                "puestos": nuevos_puestos,
                "direccion_empresa": direccion.strip(),
                "cp_empresa": cp.strip(),
                "localidad_empresa": localidad.strip(),
                "requisitos": requisitos,
                "contrato": contrato,
                "vehiculo": vehiculo,
            })
        except Exception as e:
            st.error(str(e))
            return
        st.session_state[f"{k}_cerrar_edicion"] = True
        st.session_state.pop(f"{k}_req_cargado", None)
        st.toast("Oferta actualizada", icon="✅")
        st.rerun()


def acciones_oferta(fp, numero, areas_map):
    """Edit toggle + delete button for one offer. Delete is only enabled while no
    students are assigned (alumnos == disponibles in every cycle)."""
    puede_eliminar = ofertaSinAsignaciones(fp)
    col_edit, col_del = st.columns([3, 1])
    with col_edit:
        # Close the editor after a save (the toggle can only be reset before it's drawn)
        if st.session_state.pop(f"oferta_{fp['id']}_cerrar_edicion", False):
            st.session_state[f"oferta_{fp['id']}_editar"] = False
        editando = st.toggle("✏️ Editar oferta", key=f"oferta_{fp['id']}_editar")
    with col_del:
        if st.button(
            "🗑️ Eliminar oferta", key=f"eliminar_oferta_{fp['id']}",
            disabled=not puede_eliminar,
            help=None if puede_eliminar else "No se puede eliminar: ya hay alumnos asignados a esta oferta.",
        ):
            dialog_eliminar_oferta(fp, numero)
    if editando:
        editar_oferta(fp, areas_map)
