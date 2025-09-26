import streamlit as st
import pandas as pd
import os
from modules.data_base import get
from page_utils import apply_page_config
from navigation import make_sidebar
from variables import empresasTabla

apply_page_config()
make_sidebar()

st.set_page_config(page_title="Enviar Email a Empresas", page_icon="📧")
st.title("📧 Enviar Email a Empresas")

# 1. Traer empresas
empresas = get(empresasTabla)
if not empresas:
    st.warning("No hay empresas registradas")
    st.stop()

df_empresas = pd.DataFrame(empresas)[["CIF", "nombre", "email_empresa"]]

st.dataframe(df_empresas, use_container_width=True, hide_index=True)

# 2. Selección de emails
emails_empresas = st.multiselect(
    "Selecciona empresas (emails)",
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

# 3. Subject + Body
subject = st.text_input("Asunto del email")
body = st.text_area("Cuerpo del email", height=200)

# 4. Enviar
if st.button("Enviar Email"):
    if not all_emails:
        st.error("Debes seleccionar al menos un email")
    elif not subject or not body:
        st.error("Debes completar asunto y cuerpo")
    else:
        # --- Ejemplo con API Gmail ---
        # necesitas haber autenticado al usuario antes con OAuth
        from email.mime.text import MIMEText
        import base64
        from googleapiclient.discovery import build

        service = build("gmail", "v1", credentials=st.session_state["google_creds"])

        message = MIMEText(body)
        message["to"] = ", ".join(all_emails)
        message["subject"] = subject

        raw = base64.urlsafe_b64encode(message.as_bytes()).decode()
        service.users().messages().send(userId="me", body={"raw": raw}).execute()

        st.success(f"Correo enviado a {len(all_emails)} destinatarios")
