import smtplib
from email.mime.text import MIMEText

def send_email(sender: str, password: str, recipients: list, subject: str, body: str) -> bool:
    """
    Envía un email usando SMTP de Gmail con los destinatarios en BCC (ocultos).
    Retorna True si fue exitoso, False en caso contrario.
    """
    if not recipients:
        raise ValueError("La lista de destinatarios está vacía.")

    try:
        msg = MIMEText(body, "plain", "utf-8")
        msg['From'] = sender
        msg['To'] = sender              # 👈 en pantalla, solo aparece el remitente
        msg['Subject'] = subject

        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender, password)
        server.sendmail(sender, recipients, msg.as_string())
        server.quit()

        return True
    except Exception as e:
        print(f"Error enviando email: {e}")
        return False
