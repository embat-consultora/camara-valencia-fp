import streamlit as st
import re
import smtplib
from html import unescape
from email.utils import formatdate, make_msgid
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from modules.data_base import logError,actualizarFeedbackRecordatorio
from modules.email_templates import render_feedback_tutor_email, render_welcome_email

# def send_email_outlook( recipients: list, subject: str, body: str):
#     sender = st.secrets["emailOutlook"]["EMAIL_USER"]
#     password = st.secrets["emailOutlook"]["EMAIL_PASS"]
#     if not recipients:
#         raise ValueError("Lista de destinatarios vacía.")

#     try:
#         msg = MIMEText(body, "plain", "utf-8")
#         msg['From'] = sender
#         msg['To'] = sender 
#         msg['Subject'] = subject

#         # Configuración específica para Outlook/Office 365
#         server = smtplib.SMTP('smtp.office365.com', 587)
#         server.starttls() # Obligatorio para Outlook
#         server.login(sender, password)
#         server.sendmail(sender, recipients, msg.as_string())
#         server.quit()
        
#         return True
#     except Exception as e:
#         # Re-lanzamos para que Streamlit capture el error como vimos antes
#         raise e
    
def _html_a_texto(html_body: str) -> str:
    """Plain-text version of an HTML email (sent alongside the HTML; spam filters
    penalize HTML-only messages with little text)."""
    texto = re.sub(r"(?is)<(head|style|script)\b.*?</\1>", "", html_body)
    # Keep link targets: <a href="url">text</a> -> text (url)
    texto = re.sub(r'(?is)<a\b[^>]*href="([^"]+)"[^>]*>(.*?)</a>', r"\2 (\1)", texto)
    texto = re.sub(r"\s+", " ", texto)  # source line breaks aren't real line breaks in HTML
    texto = re.sub(r"(?i)<br\s*/?>", "\n", texto)
    texto = re.sub(r"(?i)</(p|h[1-6])>", "\n\n", texto)
    texto = re.sub(r"(?i)</(div|li|tr)>", "\n", texto)
    texto = unescape(re.sub(r"<[^>]+>", "", texto))
    lineas = [" ".join(linea.split()) for linea in texto.splitlines()]
    return re.sub(r"\n{3,}", "\n\n", "\n".join(lineas)).strip() + "\n"


def _crear_mensaje(sender, recipient, subject, body, html, adjuntos):
    msg = MIMEMultipart("mixed")
    msg["From"] = sender
    msg["To"] = recipient
    msg["Subject"] = subject
    msg["Date"] = formatdate(localtime=True)
    msg["Message-ID"] = make_msgid(domain=sender.split("@")[-1])

    if html:
        cuerpo = MIMEMultipart("alternative")  # plain text first, HTML preferred
        cuerpo.attach(MIMEText(_html_a_texto(body), "plain", "utf-8"))
        cuerpo.attach(MIMEText(body, "html", "utf-8"))
        msg.attach(cuerpo)
    else:
        msg.attach(MIMEText(body, "plain", "utf-8"))

    for nombre, contenido in adjuntos:
        part = MIMEBase("application", "octet-stream")
        part.set_payload(contenido)
        encoders.encode_base64(part)
        part.add_header("Content-Disposition", "attachment", filename=nombre)
        msg.attach(part)
    return msg


def send_email(
    sender: str,
    password: str,
    recipients: list,
    subject: str,
    body: str,
    attachments=None,
    html: bool = False,
) -> bool:
    """
    Envía un email con adjuntos usando SMTP de Gmail.
    Se envía un mensaje por destinatario, con el destinatario en "To" (no en BCC):
    los correos con el destinatario oculto en BCC suelen ir a spam, y así nadie ve
    las direcciones de los demás en los envíos masivos.
    """
    if not recipients:
        raise ValueError("La lista de destinatarios está vacía.")

    # Read attachments once (Streamlit UploadedFile), then rewind them so a rerun can read them again
    adjuntos = []
    for uploaded_file in attachments or []:
        adjuntos.append((uploaded_file.name, uploaded_file.read()))
        uploaded_file.seek(0)

    fallidos = []
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender, password)
        try:
            for recipient in recipients:
                try:
                    msg = _crear_mensaje(sender, recipient, subject, body, html, adjuntos)
                    server.sendmail(sender, [recipient], msg.as_string())
                except smtplib.SMTPException as e:
                    print(f"Error enviando email a {recipient}: {e}")
                    fallidos.append(recipient)
        finally:
            server.quit()
    except Exception as e:
        print(f"Error enviando email: {e}")
        raise e

    if fallidos:
        raise RuntimeError(
            f"No se pudo enviar a {len(fallidos)} de {len(recipients)} destinatarios: {', '.join(fallidos)}"
        )
    return True


def send_welcome_email(email: str, usuario: str, password:str,  nombre:str) -> bool:
    """Envía el email de bienvenida al alumno con su usuario/contraseña (el DNI)."""
    email_sender = st.secrets['email']['gmail']
    email_password = st.secrets['email']['password']
    url = st.secrets['urls']['URL']

    subject = "Bienvenido a la plataforma FP MATCH - Ciclos Formativos"
    body = render_welcome_email(nombre, usuario, password, url)
    return send_email(email_sender, email_password, [email], subject, body, [], html=True)


def send_feedback_tutor_email(
    email: str,
    alumno: str,
    fecha_fin_real: str,
    link: str,
) -> bool:
    """Envía al tutor el formulario de cierre de la formación en empresa."""
    email_sender = st.secrets['email']['gmail']
    email_password = st.secrets['email']['password']
    subject = "Formulario de cierre de la formación en empresa"
    body = render_feedback_tutor_email(alumno, fecha_fin_real, link)

    return send_email(email_sender, email_password, [email], subject, body, [], html=True)


def enviarRecordatoriosMasivos(listado_morosos):
    try:
        email_sender = st.secrets['email']['gmail']
        email_password = st.secrets['email']['password']

        emails_enviados = 0
        errores = []

        for item in listado_morosos:
            link = item['Link'].split('href="')[1].split('"')[0]  # extraemos la url del hyperlink
            tipo_label = item['Formulario']
            subject = f"Recordatorio: Completa tu formulario de {tipo_label}"
            body = f"""Hola,

            Te recordamos que aún tienes pendiente completar el formulario de {tipo_label}.

            Por favor, accede al siguiente enlace para completarlo:
            {link}

            Muchas gracias por tu colaboración.
            """
            if send_email(email_sender, email_password, [item['Email']], subject, body, []):
                actualizarFeedbackRecordatorio(item['Email'], item['_tipo_form'], item['Id'])
                emails_enviados += 1
            else:
                errores.append(item['Email'])
        return emails_enviados, errores


    except Exception as e:
        error_msg = f"{type(e).__name__}: {str(e)}"
        logError(error_msg, "Feedback - Recordatorio Masivo")
        st.error(f"Error al enviar recordatorios: {e}")