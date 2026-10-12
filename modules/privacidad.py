import streamlit as st
from variables import urlPoliticaPrivacidad

# ---------------------------------------------------------------
# Datos del Responsable del tratamiento.
# ---------------------------------------------------------------
RESPONSABLE_NOMBRE = "Cámara Oficial de Comercio, Industria, Servicios y Navegación de Valencia (Cámara Valencia)"
EMAIL_PRIVACIDAD = "avicente@campuscamarafp.com"
URL_POLITICA = urlPoliticaPrivacidad
# Subir la versión cada vez que cambie el texto de la política o de los avisos
POLITICA_VERSION = "1.0"

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

DESTINATARIOS = {
    "alumno": (
        "Las empresas colaboradoras a las que se proponga o asigne tu candidatura (datos de perfil y CV), "
        "el centro educativo y, cuando exista obligación legal, la Administración educativa competente. "
        "Proveedores tecnológicos que actúan como encargados del tratamiento."
    ),
    "empresa": (
        "El centro educativo, los alumnos asignados (datos de contacto del tutor y del centro de trabajo) y, "
        "cuando exista obligación legal, la Administración educativa competente. "
        "Proveedores tecnológicos que actúan como encargados del tratamiento."
    ),
}


def render_info_basica(tipo):
    """Primera capa de información (art. 13 RGPD) que se muestra junto al formulario."""
    st.markdown(
        f"""
        <div style="background-color: #f8f9fa; border-left: 4px solid #1E90FF; padding: 12px 16px; border-radius: 4px; font-size: 0.85rem; color: #333; margin-bottom: 12px;">
            <strong style="font-size: 0.95rem;">Información básica sobre protección de datos</strong>
            <ul style="margin-bottom: 6px;">
                <li><strong>Responsable:</strong> {RESPONSABLE_NOMBRE}.</li>
                <li><strong>Finalidad:</strong> {FINALIDADES[tipo]}</li>
                <li><strong>Legitimación:</strong> La gestión del programa de formación en el que solicitas participar y el cumplimiento de las funciones públicas atribuidas a las Cámaras en materia de formación profesional.</li>
                <li><strong>Destinatarios:</strong> {DESTINATARIOS[tipo]}</li>
                <li><strong>Conservación:</strong> Durante tu participación en el programa y, después, durante los plazos legalmente exigidos.</li>
                <li><strong>Derechos:</strong> Acceder, rectificar y suprimir los datos, así como otros derechos, escribiendo a <a href="mailto:{EMAIL_PRIVACIDAD}">{EMAIL_PRIVACIDAD}</a>. También puedes reclamar ante la Agencia Española de Protección de Datos (www.aepd.es).</li>
            </ul>
            Información adicional: <a href="{URL_POLITICA}" target="_blank">Política de Privacidad</a>.
        </div>
        """,
        unsafe_allow_html=True,
    )


AVISO_ENVIO = {
    "alumno": (
        "Al pulsar <strong>Enviar</strong> declaras que has leído la información sobre protección de datos y la "
        f'<a href="{URL_POLITICA}" target="_blank">Política de Privacidad</a>, que los datos facilitados son veraces '
        "y que eres mayor de 14 años (o cuentas con la autorización de tu padre, madre o tutor legal). Tu perfil y tu CV "
        "se compartirán con las empresas colaboradoras a las que se proponga tu candidatura, y recibirás por email las "
        "comunicaciones necesarias para la gestión del programa (accesos, formularios de seguimiento, avisos y recordatorios)."
    ),
    "empresa": (
        "Al pulsar <strong>Enviar formulario</strong> declaras que has leído la información sobre protección de datos y la "
        f'<a href="{URL_POLITICA}" target="_blank">Política de Privacidad</a>, que los datos facilitados son veraces, '
        "que tienes capacidad para actuar en nombre de la empresa y que has informado a las personas cuyos datos "
        "facilitas (persona de contacto, responsable legal y tutor/a) sobre este tratamiento. La empresa y el tutor/a "
        "recibirán por email las comunicaciones necesarias para la gestión del programa (accesos, formularios de "
        "seguimiento, avisos y recordatorios)."
    ),
}


def datos_aceptacion(tipo):
    """Campos que registran la aceptación de la política al enviar el formulario."""
    from datetime import datetime, timezone
    return {
        "privacidad_aceptada_at": datetime.now(timezone.utc).isoformat(),
        "privacidad_version": POLITICA_VERSION,
        "privacidad_origen": f"formulario_{tipo}",
    }


def render_aviso_envio(tipo):
    """Aviso de aceptación de la política al enviar el formulario (sin checks)."""
    st.markdown(
        f"<p style='font-size:0.8rem; color:#555; margin-top:4px;'>{AVISO_ENVIO[tipo]}</p>",
        unsafe_allow_html=True,
    )
