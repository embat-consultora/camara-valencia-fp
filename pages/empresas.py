import streamlit as st
import pandas as pd
import os
from modules.data_base import get, getEqual, update, upsert,getEquals
from page_utils import apply_page_config
from pathlib import Path
from navigation import make_sidebar
from variables import empresasTabla, necesidadFP, estados,fasesEmpresa,formFieldsTabla, empresaEstadosTabla,fase2colEmpresa,opciones_motivo,bodyEmailsEmpresa,contactoEmpresaTabla
from datetime import datetime
from modules.emailSender import send_email
from modules.grafico_helper import mostrar_fases
import re
apply_page_config()
make_sidebar()

st.set_page_config(page_title="Empresas", page_icon="🏢")
st.markdown(
    "<h2 style='text-align: center;'>EMPRESAS</h2>",
    unsafe_allow_html=True
)

base_url = os.getenv("URL")

# --- Traer todas las empresas ---
empresas = get(empresasTabla)
if not empresas:
    st.warning("No hay empresas registradas")
    st.stop()

df_empresas = pd.DataFrame(empresas)

# --- Tabs principales ---
tab1, tab2, tab3 = st.tabs(["🏢 Buscar/Visualizar", "➕ Nueva Empresa", "📨 Formularios & Contacto"])

# -------------------------------------------------------------------
# TAB 1: Buscar y visualizar empresas
# -------------------------------------------------------------------
with tab1:
    col1, col2, col3= st.columns([3, 2,2])
    with col1:
        search = st.text_input("🔍 Buscar por nombre de empresa")
    with col2:
        st.metric("Total Empresas", len(df_empresas))
    with col3:
        temp_path = Path("/tmp") / f"empresas_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
        df_empresas.to_excel(temp_path, index=False)
        with open(temp_path, "rb") as f:
            st.download_button(
                label="⬇️ Descargar empresas (.xlsx)",
                data=f,
                file_name=temp_path.name,
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
    if search:
        df_empresas = df_empresas[df_empresas["nombre"].str.contains(search, case=False, na=False)]

    cols_map = {
        "CIF": "CIF",
        "nombre": "Nombre",
        "direccion": "Dirección",
        "localidad": "Localidad",
        "telefono": "Teléfono",
        "email_empresa": "Email"
    }
    df_view = df_empresas[list(cols_map.keys())].rename(columns=cols_map)
    st.dataframe(df_view, hide_index=True, use_container_width=True)

    if not df_empresas.empty:
        empresa_options = {row["nombre"]: row["id"] for _, row in df_empresas.iterrows()}
        selected_name = st.selectbox("Seleccionar empresa", list(empresa_options.keys()))
        empresa_id = empresa_options[selected_name]
        empresa = df_empresas[df_empresas["id"] == empresa_id].iloc[0].to_dict()

        with st.expander(f"✏️ Editar empresa: {empresa['nombre']}", expanded=False):
            new_nombre = st.text_input("Nombre", empresa.get("nombre", ""))
            new_direccion = st.text_input("Dirección", empresa.get("direccion", ""))
            new_localidad = st.text_input("Localidad", empresa.get("localidad", ""))
            new_cif = st.text_input("CIF", empresa.get("CIF", ""))
            new_telefono = st.text_input("Teléfono", empresa.get("telefono", ""))
            new_email = st.text_input("Email", empresa.get("email_empresa", ""))

            if st.button("💾 Actualizar empresa"):
                update(
                    empresasTabla,
                    {
                        "nombre": new_nombre,
                        "direccion": new_direccion,
                        "localidad": new_localidad,
                        "CIF": new_cif,
                        "telefono": new_telefono,
                        "email_empresa": new_email
                    },
                    "id",
                    empresa_id
                )
                st.success("Empresa actualizada correctamente")
                st.rerun()

        estadosEmpresa = getEqual(empresaEstadosTabla, "empresa", empresa["CIF"])
        st.subheader(f"Seguimiento - {empresa['nombre']}")

        if not estadosEmpresa:
            mostrar_fases(fasesEmpresa, fase2colEmpresa, None)
            estado_actual = {}
        else:
            mostrar_fases(fasesEmpresa, fase2colEmpresa, estadosEmpresa[0])
            estado_actual = estadosEmpresa[0]

        # --- Checkboxes dinámicos para cada fase ---
        cols = st.columns(len(fasesEmpresa))

        for i, fase in enumerate(fasesEmpresa):
            col = fase2colEmpresa[fase]
            valor_actual = True if estado_actual.get(col) else False

            with cols[i]:
                checked = st.checkbox(fase, value=valor_actual, key=f"{empresa['CIF']}_{col}")

            if checked != valor_actual:  # solo si cambió
                if checked:
                    new_value = datetime.now().isoformat()
                else:
                    new_value = None

                upsert(
                    empresaEstadosTabla,
                    {"empresa": empresa["CIF"], col: new_value},
                    keys=["empresa"]
                )
                st.success(f"Estado actualizado: {fase} → {new_value if new_value else '❌'}")
                st.rerun()
        
        # --- Mostrar FP asociadas ---
        fps = getEqual(necesidadFP, "empresa", empresa["CIF"])
        st.subheader(f"Oferta FP - {empresa['nombre']}")
        if fps:
            for i, fp in enumerate(fps, start=1):
                estado_actual = fp.get("estado") or "Nuevo"
                bg_color = "🟢" if estado_actual == "Nuevo" else "🔴"

                with st.expander(
                    f"Oferta #{i} | Fecha: {pd.to_datetime(fp.get('created_at')).strftime('%d/%m/%Y')} | {estado_actual} {bg_color}",
                    expanded=False
                ):
                    ciclos = fp.get("ciclos_formativos")
                    puestos = fp.get("puestos")

                    if ciclos:
                        st.write("🎓 Ciclos formativos y cantidad de alumnos:")
                        data = [
                            {"Ciclo": ciclo, "Alumnos": valores["alumnos"], "Disponibles": valores["disponibles"]}
                            for ciclo, valores in ciclos.items()]
                        df_ciclos = pd.DataFrame(data, columns=["Ciclo",  "Alumnos", "Disponibles"])
                        st.dataframe(df_ciclos, hide_index=True, use_container_width=True)

                    if puestos:
                        st.write("🧩 Puestos por ciclo formativo:")
                        for ciclo, lista_puestos in puestos.items():
                            cantidad_alumnos = None
                            if ciclos and ciclo in ciclos:
                                cantidad_alumnos = ciclos[ciclo]["alumnos"]

                            with st.expander(f"{ciclo} ({cantidad_alumnos if cantidad_alumnos else 'Sin datos'} alumnos)"):
                                if lista_puestos:
                                     for p in lista_puestos:
                                        st.write(f"- Área: {p['area']} — Proyecto: {p['proyecto']}")
                                else:
                                    st.markdown("_Sin áreas o proyectos registrados_")


                    proyectos = fp.get("proyectos")
                    requisitos = fp.get("requisitos")
                    if proyectos:
                        st.markdown(f"**Proyectos:** {proyectos}")
                    if requisitos:
                        st.markdown(f"**Requisitos:** {requisitos}")

                    contrato = fp.get("contrato")
                    vehiculo = fp.get("vehiculo")
                    st.write(f"**Contrato:** {'Sí' if contrato else 'No'}")
                    st.write(f"**Vehículo:** {'Sí' if vehiculo else 'No'}")

                    if estado_actual in estados:
                        default_index = estados.index(estado_actual)
                    else:
                        default_index = 0
                    estado = st.selectbox("Estado", options=estados, index=default_index, key=f"estado_{fp['id']}")
                    motivo_seleccionado = None
                    if estado == "Cancelado":
                        st.write("Motivo de cancelación:")
                        motivo_seleccionado = st.selectbox(
                            "Selecciona el motivo",
                            options=opciones_motivo,
                            index=opciones_motivo.index(fp.get("motivo")) if fp.get("motivo") in opciones_motivo else 0,
                            key=f"motivo_select_{fp['id']}")
                        if motivo_seleccionado == "Otros":
                                motivo_otro = st.text_area(
                                    "Especifica el motivo",
                                    value=fp.get("motivo_otro") or "",
                                    key=f"motivo_otro_{fp['id']}"
                                )
                                motivo_final = motivo_otro
                        else:
                                motivo_final = motivo_seleccionado
                    if st.button("Guardar cambios", key=f"guardar_{fp['id']}"):
                        upsert(
                            necesidadFP,
                            {"empresa": empresa["CIF"], "estado": estado, "motivo": motivo_final, "id": fp["id"]},
                            keys=["id"]
                        )
                        st.success("Oferta FP actualizada")
                        st.rerun()
        else:
            st.info(
                'No hay necesidades FP registradas para esta empresa. '
                f"Mandale el link para que nos avise: [Formulario]({base_url}forms?form=1)"
            )
            # if st.button("Crear Oferta Autogestionada"):
            #     contrato = st.radio("Contrato Laboral",["Sí", "No"],horizontal=True)
            #     vehiculo = st.radio("Vehiculo",["Sí", "No"],horizontal=True)
            #     form_fields = getEquals(formFieldsTabla, {"category": "Alumno", "type": "Opciones"})
            #     ciclo_field = next((f for f in form_fields if f["columnName"] == "ciclo_formativo"), None)
            #     pref_field = next((f for f in form_fields if f["columnName"] == "preferencias_fp"), None)
            #     ofertaPayload={
            #             "contrato": contrato,
            #             "vehiculo": vehiculo,
            #             "ciclos_formativos": cantidades,
            #             "puestos": puestos_seleccionados,
            #             "requisitos": requisitos.strip(),
            #             "estado": estados[0],
            #             "nombre_tutor": nombre_tutor.strip(),
            #             "nif_tutor": nif_tutor.strip(),
            #             "email_tutor": email_tutor.strip().lower(),
            #             "telefono_tutor": telefono_tutor.strip(),
            #             "direccion_empresa": direccion.strip() if not direccion_centro.strip() else direccion_centro.strip(),
            #             "cp_empresa": cp.strip() if not cp_centro.strip() else cp_centro.strip(),
            #             "localidad_empresa": localidad.strip() if not localidad_centro.strip() else localidad_centro.strip(),
            #             "nombre_rellena_form": nombre_contacto.strip(),
            #             "cupo_alumnos": sum(v["alumnos"] for v in cantidades.values()) if cantidades else 0,
            #         }
            #     try:
            #         upsert(
            #             necesidadFP,
            #             {
            #                 "empresa": empresa["CIF"],
            #                 "estado": "Nuevo"
            #             },
            #             keys=["empresa", "created_at"]
            #         )
            #         st.success("Oferta FP creada correctamente")
            #         st.rerun()
            #     except Exception as e:
            #         st.error(f"Error al crear la oferta FP: {e}")



# -------------------------------------------------------------------
# TAB 2: Crear nueva empresa
# -------------------------------------------------------------------
with tab2:
    st.subheader("➕ Nueva Empresa")
    with st.form("nueva_empresa_form"):
        nombre_empresa = st.text_input("Nombre de la empresa")
        direccion = st.text_input("Dirección")
        cp = st.text_input("Código Postal")
        localidad = st.text_input("Localidad")
        cif = st.text_input("CIF *")
        nombre_contacto = st.text_input("Nombre de la persona que rellena el formulario")
        telefono_contacto = st.text_input("Teléfono de contacto")
        email_contacto = st.text_input("Email de contacto")
        nombre_responsable = st.text_input("Nombre del responsable legal")
        nie_responsable = st.text_input("NIF del responsable legal")
        horario = st.text_input("Horario Empresa")
        pagina_web = st.text_input("Página web")
        col1, col2 = st.columns(2)
        submitted = st.form_submit_button("Crear Empresa")
        if submitted:
            if not cif or cif.strip() == "":
                st.warning("⚠️ El campo CIF es obligatorio")
            else:
                try:
                    upsert(
                        empresasTabla,
                        {
                            "nombre": nombre_empresa,
                            "direccion": direccion,
                            "localidad": localidad,
                            "codigo_postal": cp,
                            "CIF": cif.strip(),
                            "telefono": telefono_contacto,
                            "email_empresa": email_contacto,
                            "nombre_rellena": nombre_contacto,
                            "responsable_legal": nombre_responsable,
                            "nif_responsable_legal": nie_responsable,
                            "horario": horario,
                            "pagina_web": pagina_web,
                        },
                        keys=["CIF"],
                    )
                    st.success("✅ Empresa creada correctamente")
                    st.rerun()
                except Exception as e:
                    st.error(f"❌ Error al crear la empresa: {e}")

# -------------------------------------------------------------------
# TAB 3: Formularios & Contacto
# -------------------------------------------------------------------
formUrl = os.getenv("FORM_EMPRESA")
can_send = True
with tab3:
    if "emailsList" not in st.session_state:
        st.session_state.emailsList = []
    st.write("🎓 Contactar Empresas")
    
    if not empresas:
        st.warning("No hay empresas registrados")
        st.stop()

    df_empresas = pd.DataFrame(empresas)[["CIF", "nombre", "email_empresa"]]
    emailsEmpresasClean =df_empresas["email_empresa"].dropna().unique().tolist()
    
    col1, col2 = st.columns([3, 2])
    with col2:
        checked = st.checkbox("Seleccionar todos", value=False, key="select_all_empresas")
    with col1:
        emails_empresas = st.multiselect(
            "Selecciona empresas (emails)", placeholder="Selecciona un valor",
            options=emailsEmpresasClean,disabled=st.session_state.select_all_empresas
        )
    emails_manual_empresas = st.text_area(
        "Agregar emails manualmente (separados por coma)",
        placeholder="ejemplo1@mail.com, ejemplo2@mail.com",
        key="emails_manual_empresas"
    )
    EMAIL_REGEX = re.compile(r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$")
    valid_emails = []
    invalid_emails = []
    if emails_manual_empresas.strip():
        raw_list = [e.strip() for e in emails_manual_empresas.split(",") if e.strip()]
        for e in raw_list:
            if EMAIL_REGEX.match(e):
                valid_emails.append(e.lower())
            else:
                invalid_emails.append(e)

        valid_emails = list(dict.fromkeys(valid_emails))

        if invalid_emails:
            can_send = False
            st.warning(f"Puede que falte alguna coma o que tengas correos inválidos: {', '.join(invalid_emails)}")
    
    if checked:
        allEmails = emailsEmpresasClean.copy()
        final_list = list(set(allEmails + valid_emails))
    else:
        final_list = list(set(emails_empresas + valid_emails))

    st.session_state.emailsList = final_list
    
    st.write("**Destinatarios seleccionados:**")
    for e in st.session_state.emailsList:
        st.markdown(f"- {e}")

    subject_al = st.text_input("Asunto del email", value="Pasantías FP 2025/2026", key="subj_al")
    body_al = st.text_area(
        "Cuerpo del email",
        height=200,
        value=bodyEmailsEmpresa.replace("{{form_link}}", formUrl),
        key="body_al"
    )

    email_sender = st.secrets['email']['gmail']
    email_password = st.secrets['email']['password']

    if st.button("📨 Enviar Emails a Empresas", disabled=not can_send):
        try:
            if send_email(email_sender, email_password, final_list, subject_al, body_al):
                fecha_envio = datetime.now().isoformat()

                for email in final_list:
                    empresa = df_empresas[df_empresas["email_empresa"] == email]

                    if not empresa.empty:
                        cif = empresa["CIF"].values[0]
                        upsert(
                            empresaEstadosTabla,
                            {"empresa": cif, "email_enviado": fecha_envio},
                            keys=["empresa"]
                        )
                    else:
                        upsert(
                            contactoEmpresaTabla,
                            {"email_empresa": email, "email_enviado": fecha_envio},
                            keys=["email_empresa"]
                        )
                st.success("Emails enviados correctamente! 🚀")
        except Exception as e:
            st.error(f"Falló el envío de mail: {e}")

