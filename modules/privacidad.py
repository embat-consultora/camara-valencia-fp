import streamlit as st
from variables import urlPoliticaPrivacidad

# ---------------------------------------------------------------
# Datos del Responsable del tratamiento.
# ---------------------------------------------------------------
RESPONSABLE_NOMBRE = "Cámara Oficial de Comercio, Industria, Servicios y Navegación de Valencia (Cámara Valencia)"
EMAIL_PRIVACIDAD = "avicente@campuscamarafp.com"
URL_POLITICA = urlPoliticaPrivacidad
# Subir la versión cada vez que cambie el texto de la política o de los avisos
POLITICA_VERSION = "1.1"

FINALIDADES = {
    "alumno": (
        "Gestionar tu participación en el programa de Formación en Empresa (FP Dual): "
        "valorar tu perfil y preferencias, buscar y asignarte una empresa colaboradora, "
        "tramitar la documentación (convenios, anexos) y hacer el seguimiento y la evaluación de la formación."
    ),
    "empresa": (
        "Gestionar la participación de la empresa en el programa de Formación en Empresa (FP Dual): "
        "registro de la oferta formativa, asignación de alumnos, tramitación de convenios y anexos, "
        "y seguimiento de la formación a través del tutor de empresa."
    ),
}


def render_aviso_legal(tipo):
    """Aviso legal y de protección de datos con check de aceptación. Devuelve True si el usuario acepta."""
    finalidad = FINALIDADES[tipo][0].lower() + FINALIDADES[tipo][1:].rstrip(".")
    st.markdown(
        f"""
        <div style="background-color: #f8f9fa; border-left: 4px solid #1E90FF; padding: 12px 16px; border-radius: 4px; font-size: 0.85rem; color: #333; margin-bottom: 12px;">
            <p><strong>AVISO LEGAL Y CONFIDENCIALIDAD:</strong> Este mensaje y sus archivos adjuntos van dirigidos exclusivamente a su destinatario, pudiendo contener información confidencial sometida a secreto profesional. No está permitida su comunicación, reproducción o distribución sin la autorización expresa del remitente. Si usted no es el destinatario final, por favor elimínelo e infórmenos por esta misma vía.</p>
            <p style="margin-bottom: 0;"><strong>PROTECCIÓN DE DATOS:</strong> De conformidad con lo dispuesto en el Reglamento (UE) 2016/679 (RGPD) y la Ley Orgánica 3/2018 (LOPDGDD), le informamos que los datos personales que nos facilite serán tratados por {RESPONSABLE_NOMBRE} con la finalidad de {finalidad}. Puede ejercer sus derechos de acceso, rectificación, portabilidad, supresión, limitación y oposición enviando un correo a <a href="mailto:{EMAIL_PRIVACIDAD}">{EMAIL_PRIVACIDAD}</a>.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    return st.checkbox(
        "He leído y acepto el aviso legal y la información sobre protección de datos *",
        key=f"acepta_privacidad_{tipo}",
    )


def datos_aceptacion(tipo):
    """Campos que registran la aceptación de la política al enviar el formulario."""
    from datetime import datetime, timezone
    return {
        "privacidad_aceptada_at": datetime.now(timezone.utc).isoformat(),
        "privacidad_version": POLITICA_VERSION,
        "privacidad_origen": f"formulario_{tipo}",
    }

