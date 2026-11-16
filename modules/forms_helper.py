import re
import streamlit as st
from variables import idiomasRequisitos, nivelesIdioma, skillsRequisitos

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
