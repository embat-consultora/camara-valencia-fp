import streamlit as st
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from modules.data_base import logError,actualizarFeedbackRecordatorio

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
    
def send_email(sender: str, password: str, recipients: list, subject: str, body: str, attachments=None) -> bool:
    """
    Envía un email con adjuntos usando SMTP de Gmail con los destinatarios en BCC.
    """
    if not recipients:
        raise ValueError("La lista de destinatarios está vacía.")

    try:
        # 1. Cambiamos a MIMEMultipart para soportar adjuntos
        msg = MIMEMultipart()
        msg['From'] = sender
        msg['To'] = sender  # Se envía a uno mismo para que los demás vayan en BCC
        msg['Subject'] = subject

        # 2. Adjuntamos el cuerpo del mensaje
        msg.attach(MIMEText(body, "plain", "utf-8"))

        # 3. Lógica para los archivos adjuntos
        if attachments:
            for uploaded_file in attachments:
                # Creamos la parte del adjunto
                part = MIMEBase("application", "octet-stream")
                # Leemos el contenido del archivo de Streamlit
                part.set_payload(uploaded_file.read())
                # Codificamos en base64 para el envío
                encoders.encode_base64(part)
                
                # Añadimos la cabecera con el nombre del archivo
                part.add_header(
                    "Content-Disposition",
                    f"attachment; filename={uploaded_file.name}",
                )
                msg.attach(part)
                
                # IMPORTANTE: Volver al inicio del archivo para que Streamlit 
                # no lo dé por "leído" si se re-ejecuta el script
                uploaded_file.seek(0)

        # 4. Envío del correo
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender, password)
        
        # Enviamos a la lista completa de recipients (irán como BCC ocultos)
        server.sendmail(sender, recipients, msg.as_string())
        server.quit()

        return True

    except Exception as e:
        print(f"Error enviando email: {e}")
        raise e


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