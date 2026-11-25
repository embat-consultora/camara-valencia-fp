"""Approximate distance between a student and an offer's workplace.

Uses the centre point of each postal code (or, if there's no postal code, of the town).
Coordinates come from GeoNames postal codes for Spain (https://www.geonames.org,
CC BY 4.0), saved in modules/data/geo_es.csv. Accuracy is at town level: two addresses
in the same town (e.g. any two postal codes in Valencia city) come out as "same town".
"""
import csv
import math
import re
import unicodedata
from pathlib import Path

import streamlit as st

_ARCHIVO = Path(__file__).parent / "data" / "geo_es.csv"
_ARTICULOS = ("L ", "EL ", "LA ", "LOS ", "LAS ", "ELS ", "LES ")


def _normalizar_localidad(valor):
    s = unicodedata.normalize("NFKD", str(valor or "")).encode("ascii", "ignore").decode().upper()
    s = " ".join(s.replace("'", " ").replace("-", " ").split())
    for articulo in _ARTICULOS:
        if s.startswith(articulo):
            s = s[len(articulo):]
    return s


def _normalizar_cp(valor):
    digitos = re.sub(r"\D", "", re.sub(r"\.0+$", "", str(valor or "").strip()))
    # Excel drops the leading zero (03001 -> 3001)
    return digitos.zfill(5) if 4 <= len(digitos) <= 5 else ""


@st.cache_data(show_spinner=False)
def _cargar():
    por_cp, por_localidad = {}, {}
    with open(_ARCHIVO, encoding="utf-8") as f:
        for fila in csv.DictReader(f):
            destino = por_cp if fila["tipo"] == "cp" else por_localidad
            destino[fila["clave"]] = (float(fila["lat"]), float(fila["lon"]))
    return por_cp, por_localidad


def coordenadas(cp=None, localidad=None):
    """(lat, lon) for a postal code, falling back to the town name. None if unknown."""
    por_cp, por_localidad = _cargar()
    punto = por_cp.get(_normalizar_cp(cp))
    if punto is None and localidad:
        punto = por_localidad.get(_normalizar_localidad(localidad))
    return punto


def distancia_km(punto_a, punto_b):
    """Straight-line distance in km between two (lat, lon) points."""
    lat1, lon1 = map(math.radians, punto_a)
    lat2, lon2 = map(math.radians, punto_b)
    h = math.sin((lat2 - lat1) / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin((lon2 - lon1) / 2) ** 2
    return 2 * 6371 * math.asin(math.sqrt(h))


def texto_distancia(punto_alumno, punto_empresa):
    """Short label for the match screen."""
    if punto_alumno is None or punto_empresa is None:
        return "sin datos (falta CP o localidad)"
    km = distancia_km(punto_alumno, punto_empresa)
    if km < 1:
        return "mismo municipio (entre 1 y 10 km)"
    return f"≈ {round(km)} km en línea recta"
