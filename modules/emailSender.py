import streamlit as st
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
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
