import io
import re
import pandas as pd
import streamlit as st
from variables import idiomasRequisitos, nivelesIdioma, skillsRequisitos, provincias, provinciaDefecto, localidadesPorProvincia, provincia_de_localidad

def slug(s: str) -> str:
    s = str(s or "")
    s = s.strip().lower()
    s = re.sub(r"\s+", "_", s)
    s = re.sub(r"[^a-z0-9_]+", "", s)
    return s[:80]

def file_size_bytes(f):
    if f is None:
        return 0
    size = getattr(f, "size", None)
    return size if size is not None else len(f.getbuffer())

def required_ok(val) -> bool:
    if val is None:
        return False
    if isinstance(val, str):
        return val.strip() != ""
    return True

def requisitos_a_estado(key_prefix, texto):
    """Inverse of render_requisitos: turns saved text into widget values so an
    existing offer can be edited. Anything not in the lists goes to "otros"."""
    idiomas, skills, otros, estado = [], [], [], {}
    for parte in [p.strip() for p in str(texto or "").split(",") if p.strip()]:
        idioma, _, nivel = parte.rpartition(" ")
        if parte in skillsRequisitos:
            if parte not in skills:
                skills.append(parte)
        elif idioma in idiomasRequisitos and nivel in nivelesIdioma:
            if idioma not in idiomas:
                idiomas.append(idioma)
            estado[f"{key_prefix}_nivel_{slug(idioma)}"] = nivel
        elif parte in idiomasRequisitos:
            if parte not in idiomas:
                idiomas.append(parte)
        else:
            otros.append(parte)
    estado[f"{key_prefix}_idiomas"] = idiomas
    estado[f"{key_prefix}_skills"] = skills
    estado[f"{key_prefix}_otros"] = ", ".join(otros)
    return estado


def render_requisitos(key_prefix, idiomas_label, skills_label, otros_label):
    """Languages (+ level each), skills and free text. Returns the comma-separated text
    stored in `requisitos` (the matching SQL splits it on commas)."""
    partes = []
    idiomas = st.multiselect(
        idiomas_label, idiomasRequisitos,
        key=f"{key_prefix}_idiomas", placeholder="Selecciona idiomas",
    )
    for idioma in idiomas:
        nivel = st.selectbox(
            f"Nivel de {idioma}", nivelesIdioma, index=None,
            key=f"{key_prefix}_nivel_{slug(idioma)}", placeholder="Selecciona el nivel",
        )
        partes.append(f"{idioma} {nivel}" if nivel else idioma)

    partes.extend(st.multiselect(
        skills_label, skillsRequisitos,
        key=f"{key_prefix}_skills", placeholder="Selecciona skills",
    ))

    otros = st.text_input(otros_label, key=f"{key_prefix}_otros").strip()
    if otros:
        partes.append(otros)
    return ", ".join(partes)


def leer_csv(archivo, columnas_esperadas):
    """Lee el CSV aceptando , ; o tabulador como separador y UTF-8, UTF-8 con BOM o Windows-1252 (Excel)."""
    contenido = archivo.getvalue()
    try:
        texto = contenido.decode("utf-8-sig")
    except UnicodeDecodeError:
        texto = contenido.decode("cp1252")

    cabecera = texto.splitlines()[0] if texto else ""
    separador = max([",", ";", "\t"], key=cabecera.count)
    if cabecera.count(separador) == 0:
        separador = ","

    df = pd.read_csv(io.StringIO(texto), dtype=str, sep=separador).fillna("")

    # Nombres de columna sin espacios y sin importar mayúsculas (Dni, DNI, nia → dni, NIA)
    canonicas = {c.lower(): c for c in columnas_esperadas}
    df.columns = [canonicas.get(str(c).strip().lower(), str(c).strip()) for c in df.columns]
    return df


# --- Provincia + localidad ---
def _localidad_canonica(provincia, localidad):
    """The list's spelling of a saved town ("El Campello" -> "EL CAMPELLO")."""
    actual = str(localidad or "").strip()
    lista = localidadesPorProvincia.get(provincia, [])
    return actual.upper() if actual.upper() in lista else actual


def opciones_localidad(provincia, localidad_actual=None):
    """Towns of a province. A saved town that isn't in the list (old or typed by hand)
    is kept as the first option so editing a record doesn't lose it."""
    opciones = list(localidadesPorProvincia.get(provincia, []))
    actual = _localidad_canonica(provincia, localidad_actual)
    if actual and actual not in opciones and provincia_de_localidad(actual) in (None, provincia):
        opciones.insert(0, actual)
    return opciones


def selector_provincia(key, provincia_actual=None, localidad_actual=None, label="Provincia *", disabled=False):
    """Province selectbox. Starts on the saved province, else the province of the saved
    town, else Valencia."""
    if key not in st.session_state or st.session_state[key] not in provincias:
        inicial = provincia_actual if provincia_actual in provincias else None
        st.session_state[key] = inicial or provincia_de_localidad(localidad_actual) or provinciaDefecto
    return st.selectbox(label, provincias, key=key, disabled=disabled)


def selector_localidad(key, provincia, localidad_actual=None, label="Localidad *", disabled=False):
    """Town selectbox for `provincia`. Returns "" while nothing is picked."""
    opciones = opciones_localidad(provincia, localidad_actual)
    actual = _localidad_canonica(provincia, localidad_actual)
    # Province changed (or first draw): drop a town that doesn't belong to it
    if key in st.session_state and st.session_state[key] not in opciones:
        del st.session_state[key]
    if key not in st.session_state and actual in opciones:
        st.session_state[key] = actual
    extra = {} if key in st.session_state else {"index": None}
    valor = st.selectbox(
        label, opciones, key=key, disabled=disabled,
        placeholder="Selecciona una localidad", **extra,
    )
    return valor or ""


def selector_provincia_localidad(key, provincia_actual=None, localidad_actual=None,
                                 label_localidad="Localidad *", disabled=False):
    """Province and town side by side. Returns (provincia, localidad).
    Not for use inside st.form: the town list only refreshes outside a form."""
    col_prov, col_loc = st.columns(2)
    with col_prov:
        provincia = selector_provincia(f"{key}_provincia", provincia_actual, localidad_actual, disabled=disabled)
    with col_loc:
        localidad = selector_localidad(f"{key}_localidad", provincia, localidad_actual,
                                       label=label_localidad, disabled=disabled)
    return provincia, localidad
