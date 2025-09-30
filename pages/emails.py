import streamlit as st
import pandas as pd
import os
from datetime import datetime

from modules.emailSender import send_email
from modules.data_base import get, upsert
from page_utils import apply_page_config
from navigation import make_sidebar
from variables import (
    empresasTabla, bodyEmailsEmpresa, empresaEstadosTabla, contactoEmpresaTabla,
    alumnosTabla, bodyEmailsAlumno, alumnoEstadosTabla, contactoAlumnoTabla
)

apply_page_config()
make_sidebar()
st.set_page_config(page_title="Contactar", page_icon="📧")

st.markdown(
    "<h2 style='text-align: center;'>📧 Envío de Emails</h2>",
    unsafe_allow_html=True
)

formUrl = os.getenv("FORM_EMPRESA")
formUrlAlumno = os.getenv("FORM_ALUMNO")

# -------------------------------------------------------------------
# --- Tabs principales
# -------------------------------------------------------------------
tab_empresas, tab_alumnos = st.tabs(["🏢 Empresas", "🎓 Alumnos"])


# -------------------------------------------------------------------
# TAB 1: Empresas
# -------------------------------------------------------------------
with tab_empresas:
    st.subheader("🏢 Contactar Empresas")

    empresas = get(empresasTabla)
    if not empresas:
        st.warning("No hay empresas registradas")
        st.stop()
    df_empresas = pd.DataFrame(empresas)[["CIF", "nombre", "email_empresa"]]

    emails_empresas = st.multiselect(
        "Selecciona empresas (emails)", placeholder="Selecciona un valor",
        options=df_empresas["email_empresa"].dropna().unique().tolist()
    )

    emails_manual = st.text_area(
        "Agregar emails manualmente (separados por coma)",
        placeholder="ejemplo1@mail.com, ejemplo2@mail.com"
    )

    all_emails = emails_empresas.copy()
    if emails_manual.strip():
        all_emails.extend([e.strip() for e in emails_manual.split(",") if e.strip()])

    st.write("**Destinatarios seleccionados:**")
    for e in all_emails:
        st.markdown(f"- {e}")

    subject = st.text_input("Asunto del email", value="Formaciones Profesionales 2025/26", key="subj_emp")
    body = st.text_area(
        "Cuerpo del email",
        height=200,
        value=bodyEmailsEmpresa.replace("{{form_link}}", formUrl),
        key="body_emp"
    )

    email_sender = st.secrets['email']['gmail']
    email_password = st.secrets['email']['password']

    if st.button("📨 Enviar Emails a Empresas"):
        try:
            if send_email(email_sender, email_password, all_emails, subject, body):
                fecha_envio = datetime.now().isoformat()

                for email in all_emails:
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


# -------------------------------------------------------------------
# TAB 2: Alumnos
# -------------------------------------------------------------------
with tab_alumnos:
    st.subheader("🎓 Contactar Alumnos")

    alumnos = get(alumnosTabla)
    if not alumnos:
        st.warning("No hay alumnos registrados")
        st.stop()
    df_alumnos = pd.DataFrame(alumnos)[["id","NIA", "nombre", "email_alumno"]]

    emails_alumnos = st.multiselect(
        "Selecciona alumnos (emails)", placeholder="Selecciona un valor",
        options=df_alumnos["email_alumno"].dropna().unique().tolist()
    )

    emails_manual_alumnos = st.text_area(
        "Agregar emails manualmente (separados por coma)",
        placeholder="ejemplo1@mail.com, ejemplo2@mail.com",
        key="emails_manual_alumnos"
    )

    all_emails_alumnos = emails_alumnos.copy()
    if emails_manual_alumnos.strip():
        all_emails_alumnos.extend([e.strip() for e in emails_manual_alumnos.split(",") if e.strip()])

    st.write("**Destinatarios seleccionados:**")
    for e in all_emails_alumnos:
        st.markdown(f"- {e}")

    subject_al = st.text_input("Asunto del email", value="Pasantías FP 2025/2026", key="subj_al")
    body_al = st.text_area(
        "Cuerpo del email",
        height=200,
        value=bodyEmailsAlumno.replace("{{form_link}}", formUrlAlumno),
        key="body_al"
    )

    email_sender = st.secrets['email']['gmail']
    email_password = st.secrets['email']['password']

    if st.button("📨 Enviar Emails a Alumnos"):
        try:
            if send_email(email_sender, email_password, all_emails_alumnos, subject_al, body_al):
                fecha_envio = datetime.now().isoformat()

                for email in all_emails_alumnos:
                    alumno = df_alumnos[df_alumnos["email_alumno"] == email]

                    if not alumno.empty:
                        alumno_id = alumno["NIA"].values[0]
                        upsert(
                            alumnoEstadosTabla,
                            {"alumno": alumno_id, "email_enviado": fecha_envio},
                            keys=["alumno"]
                        )
                    else:
                        upsert(
                            contactoAlumnoTabla,
                            {"email_alumno": email, "email_enviado": fecha_envio},
                            keys=["email_alumno"]
                        )
                st.success("Emails enviados correctamente! 🚀")
        except Exception as e:
            st.error(f"Falló el envío de mail: {e}")
