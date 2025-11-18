import streamlit as st
from supabase import create_client, Client
from dotenv import load_dotenv
import os

load_dotenv()

url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_KEY")
env = os.getenv("SUPABASE_ENV")
supabase: Client = create_client(url, key)
@st.cache_data(ttl=3600) 
def get(tableName):
    response = supabase.table(tableName).select('*').execute()
    return response.data
@st.cache_data(ttl=3600) 
def getEqual(tableName, variable, value):
    response = supabase.table(tableName).select('*').eq(variable, value).execute()
    return response.data
@st.cache_data(ttl=3600) 
def getEquals(tableName, conditions: dict, in_filters: dict = None):
    query = supabase.table(tableName).select("*")
    if conditions:
        for key, value in conditions.items():
            query = query.eq(key, value)
    if in_filters:
        for key, values in in_filters.items():
            query = query.in_(key, values)
    response = query.execute()
    return response.data
@st.cache_data(ttl=3600) 
def getOfertaEmpresas(tableName, conditions: dict, in_filters: dict = None):
    query = supabase.table(tableName).select("*, empresas(*),tutores(*)")
    if conditions:
        for key, value in conditions.items():
            query = query.eq(key, value)
    if in_filters:
        for key, values in in_filters.items():
            query = query.in_(key, values)
    response = query.execute()
    return response.data
@st.cache_data(ttl=3600) 
def getPracticas(tableName, conditions: dict, in_filters: dict = None):
    query = supabase.table(tableName).select("*, empresas(*),alumnos(*), oferta_fp(*), practica_estados(*)")
    if conditions:
        for key, value in conditions.items():
            query = query.eq(key, value)
    if in_filters:
        for key, values in in_filters.items():
            query = query.in_(key, values)
    response = query.execute()
    return response.data
def add(tableName, data):
    response = supabase.table(tableName).insert(data).execute()
    return response
def update(tableName, data,searchFor, searchValue):
    response = supabase.table(tableName).update(data).eq(searchFor, searchValue).execute()
    return response
def delete(tableName,searchFor, searchValue):
    response = supabase.table(tableName).delete().eq(searchFor, searchValue).execute()
    return response

def getOrdered(tableName, searchFor, searchValue, orderByColumn):
    response = supabase.table(tableName).select('*').eq(searchFor, searchValue).order(orderByColumn).execute()
    return response.data

def upsert(tableName, data,keys):
    response = supabase.table(tableName).upsert(data, on_conflict=keys).execute()
    return response
def saveAuthToken(data):
    return supabase.table('auth_tokens').insert(data).execute()

def getAuthToken(email):
    response = supabase.table('auth_tokens').select('*').eq('email', email).execute()
    if response.data:
        return response.data[0]  # ✅ Devolvemos el primer resultado como dict
    return None


def getMatches():
    """
    Ejecuta la query de coincidencias entre ofertas y alumnos (ranking de match),
    incluyendo el nombre de la empresa.
    Retorna una lista de dicts (rows) con el resultado.
    """
    query = """
    WITH ofertas_activas AS (
      SELECT
        of.*,
        of.ciclos_formativos::jsonb AS ciclos_js
      FROM oferta_fp of
      WHERE LOWER(of.estado) = 'nuevo'
        AND of.cupo_alumnos > 0
    ),
    alumnos_disponibles AS (
      SELECT a.*
      FROM alumnos a
      WHERE LOWER(a.estado) = 'sin empresa'
    ),
    oferta_ciclos AS (
      SELECT
        o.id AS oferta_id,
        o.empresa,
        e.nombre AS nombre_empresa,
        each.key::text AS ciclo_text,
        ((each.value ->> 'disponibles')::int) AS disponibles,
        o.vehiculo AS oferta_vehiculo,
        o.localidad_empresa,
        o.requisitos AS oferta_requisitos
      FROM ofertas_activas o
      JOIN empresas e ON e."CIF" = o.empresa
      CROSS JOIN LATERAL jsonb_each(o.ciclos_js) AS each(key, value)
      WHERE ((each.value ->> 'disponibles')::int) > 0
    ),
    candidatos AS (
      SELECT
        a.id AS alumno_id,
        a.nombre AS alumno_nombre,
        a.apellido AS alumno_apellido,
        a.dni AS alumno_dni,
        oc.oferta_id,
        oc.empresa,
        oc.nombre_empresa,
        oc.ciclo_text AS ciclo,
        a.ciclo_formativo,
        a.preferencias_fp,
        a.vehiculo AS alumno_vehiculo,
        a.localidad AS alumno_localidad,
        a.requisitos AS requisitos,
        oc.oferta_requisitos,
        oc.oferta_vehiculo,
        oc.localidad_empresa
      FROM alumnos_disponibles a
      JOIN oferta_ciclos oc
        ON a.ciclo_formativo::text ILIKE '%' || oc.ciclo_text || '%'
        OR oc.ciclo_text ILIKE '%' || a.ciclo_formativo::text || '%'
    ),
    ranking AS (
      SELECT
        c.*,
        1 AS pts_ciclo,
        CASE WHEN c.alumno_vehiculo = c.oferta_vehiculo THEN 1 ELSE 0 END AS pts_vehiculo,
        CASE WHEN LOWER(c.alumno_localidad::text) = LOWER(c.localidad_empresa::text) THEN 1 ELSE 0 END AS pts_localidad,

        -- Preferencias (área, proyecto o ciclo)
        CASE
          WHEN EXISTS (
            SELECT 1
            FROM oferta_fp of2,
                 jsonb_each(of2.puestos) AS ciclo(ciclo_text, puestos_array),
                 jsonb_array_elements(puestos_array) AS puesto_obj
            WHERE of2.id = c.oferta_id
              AND (
                LOWER(c.preferencias_fp::text) LIKE '%' || LOWER(puesto_obj ->> 'area') || '%'
                OR LOWER(c.preferencias_fp::text) LIKE '%' || LOWER(puesto_obj ->> 'proyecto') || '%'
                OR LOWER(c.preferencias_fp::text) LIKE '%' || LOWER(ciclo.ciclo_text) || '%'
              )
          )
          THEN 1 ELSE 0
        END AS pts_pref,

        -- Requisitos (comparación entre alumno y oferta, tolerante a tildes/espacios)
        CASE
          WHEN c.requisitos IS NOT NULL
               AND c.oferta_requisitos IS NOT NULL
               AND TRIM(c.requisitos) <> ''
               AND TRIM(c.oferta_requisitos) <> ''
               AND (
                 translate(LOWER(regexp_replace(c.requisitos, '\\s+', ' ', 'g')), 'áéíóúü', 'aeiouu')
                   ILIKE '%' || translate(LOWER(regexp_replace(c.oferta_requisitos, '\\s+', ' ', 'g')), 'áéíóúü', 'aeiouu') || '%'
                 OR
                 translate(LOWER(regexp_replace(c.oferta_requisitos, '\\s+', ' ', 'g')), 'áéíóúü', 'aeiouu')
                   ILIKE '%' || translate(LOWER(regexp_replace(c.requisitos, '\\s+', ' ', 'g')), 'áéíóúü', 'aeiouu') || '%'
               )
          THEN 1 ELSE 0
        END AS pts_requisitos

      FROM candidatos c
    )
    SELECT
      r.alumno_id,
      r.alumno_nombre,
      r.alumno_apellido,
      r.alumno_dni,
      r.oferta_id,
      r.empresa,
      r.nombre_empresa,
      r.ciclo,
      (r.pts_ciclo + r.pts_vehiculo + r.pts_localidad + r.pts_pref + r.pts_requisitos) AS puntaje,
      r.pts_ciclo,
      r.pts_vehiculo,
      r.pts_localidad,
      r.pts_pref,
      r.pts_requisitos
    FROM ranking r
    ORDER BY puntaje DESC, r.pts_pref DESC, r.pts_localidad DESC
    """
    response = supabase.rpc("exec_sql", {"sql": query}).execute()
    return response.data


def getTodosEmpresaOfertas():
    query = """SELECT 
    e."CIF",
    e."nombre" as "Empresa",
    e.telefono,
    e."direccion",
    e.localidad,
    e.codigo_postal as "CP",
    e.email_empresa as "Email Empresa",
    e.responsable_legal as "Nombre Responsable Legal",
    e.nif_responsable_legal as "NIF Responsable Legal",
    e.horario,
    e.pagina_web,
    e.nombre_rellena,

    cf.key AS ciclo_formativo,
    (cf.value ->> 'alumnos')::int AS alumnos_pedidos,
    (cf.value ->> 'disponibles')::int AS cupos_disponibles,

    (
        SELECT string_agg(
            CONCAT(
                pitem.value->>'area', 
                ' — ',
                pitem.value->>'proyecto'
            ),
            ' | '
        )
        FROM jsonb_each(o.puestos) AS px(key, value)
        JOIN jsonb_array_elements(px.value) AS pitem(value) ON TRUE
        WHERE px.key = cf.key
    ) AS areas_puestos,

    o.requisitos,
    o.contrato,
    o.vehiculo,
    o.cupo_alumnos AS cupo_alumnos_totales_oferta,

    t.nombre AS "Nombre Tutor",
    t.email AS "Email Tutor",
    t.telefono AS "Telefono Tutor"

    FROM empresas e
    JOIN oferta_fp o ON o.empresa = e."CIF"
    LEFT JOIN tutores t ON t.id = o.tutor
    LEFT JOIN LATERAL jsonb_each(o.ciclos_formativos) AS cf(key, value) ON TRUE

    ORDER BY e.nombre, o.id, cf.key
    """

    response = supabase.rpc("exec_sql", {"sql": query}).execute()
    return response.data
