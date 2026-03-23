import streamlit as st
from supabase import create_client, Client
from dotenv import load_dotenv
import os
import pandas as pd
import uuid
from datetime import datetime, timedelta
from variables import (
    practicaTabla,
    practicaEstadosTabla,
    alumnosTabla,
    alumnoEstadosTabla,
    estadosAlumno,
    necesidadFP,
    feedbackFormsTabla,
    forms,empresasTabla, practicaTabla, alumnosTabla,
    gestoresTabla,
    usuariosTabla,
    tutoresTabla,
    carpetaPractica,
    tutoresCentroTabla
)
load_dotenv()

url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_KEY")
env = os.getenv("SUPABASE_ENV")
supabase: Client = create_client(url, key)

# --- FUNCIÓN DE ACTUALIZACIÓN ---
def update_database(table_name, df_changes, pk_col="id"):
    """Procesa los cambios del data_editor y los sube a Supabase"""
    # Filas editadas
    for index, row in df_changes["edited_rows"].items():
        # Obtenemos el ID real desde el dataframe original usando el índice
        real_id = st.session_state[f"original_{table_name}"].iloc[index][pk_col]
        supabase.table(table_name).update(row).eq(pk_col, real_id).execute()
    
    # Filas eliminadas
    for index in df_changes["deleted_rows"]:
        real_id = st.session_state[f"original_{table_name}"].iloc[index][pk_col]
        supabase.table(table_name).delete().eq(pk_col, real_id).execute()

    # Filas añadidas
    if df_changes["added_rows"]:
        supabase.table(table_name).insert(df_changes["added_rows"]).execute()

def update_oferta_complex(oferta_id, df_editado, gestores_activos):    
    # 1. Obtenemos los valores de las columnas de gestores para esa fila
    # Nota: df_editado es la fila específica que se cambió
    nuevo_seguimiento = {}
    for g in gestores_activos:
        valor = df_editado.get(f"Prop. {g}", "")
        if valor: # Solo guardamos si hay texto
            nuevo_seguimiento[g] = valor
            
    # 2. Actualizamos en Supabase
    res = supabase.table(necesidadFP).update({
        "seguimiento_gestores": nuevo_seguimiento
        # Puedes añadir aquí otros campos como 'requisitos' o 'tutor'
    }).eq("id", oferta_id).execute()
    
    return res
def get_alumnos_con_practicas_consolidado():
    sinEmpresa = (
        supabase.table("alumnos")
        .select("""
        *,
        practicas_fp!left(
            id,
            alumno,
            status,
            area,
            tutor_centro,
            tutor,
            gestor,
            empresas(CIF, nombre, telefono, email_empresa)
        )
    """)
        .eq("estado", "Sin Empresa")
        .execute()
    )

    draft = (
        supabase.table("alumnos")
        .select("""
            *,
            practicas_fp!inner(
                id,
                alumno,
                status,
                area,
                tutor_centro,
                tutor,
                gestor,
                empresas(CIF, nombre, telefono, email_empresa)
            )
            """)
        .eq("practicas_fp.status", "Borrador")
        .execute()
    )

    ids = set()
    final = []
    for item in sinEmpresa.data + draft.data:
        if item["id"] not in ids:
            ids.add(item["id"])
            final.append(item)

    if not final:
        return pd.DataFrame()
    rows = []
    for item in final:
        practicas = item.get("practicas_fp", [])
        practica = practicas[0] if practicas else {}
        empresa = practica.get("empresas", {}) if practica else None
        row = {
            **item,
            "practica_id": practica.get("id") if practica else None,
            "id_empresa": empresa.get("CIF") if isinstance(empresa, dict) else "⚠️ SIN ASIGNAR",
            "nombre_empresa": empresa.get("nombre") if isinstance(empresa, dict) else "⚠️ SIN ASIGNAR",
            "email_empresa": empresa.get("email_empresa") if isinstance(empresa, dict) else None,
            "telefono_empresa": empresa.get("telefono") if isinstance(empresa, dict) else None,
            "area": practica.get("area") if practica else None,
            "tutor_centro": practica.get("tutor_centro") if practica else None,
            "tutor": practica.get("tutor") if practica else None,
            "gestor": practica.get("gestor") if practica else None,
        }
        # Eliminamos el objeto anidado para que no ensucie el DataFrame
        if "practicas_fp" in row: 
            del row["practicas_fp"]
            
        rows.append(row)

    return pd.DataFrame(rows)

def getGestore():
    gestores = supabase.table(gestoresTabla).select("*").order("nombre").execute()
    return pd.DataFrame(gestores.data)

def getGestores():
    gestores = supabase.table(gestoresTabla).select("id, email, nombre, ciclo").order("nombre").execute()
    usuarios = supabase.table(usuariosTabla).select("email, password").execute()

    df_gestores = pd.DataFrame(gestores.data)
    df_usuarios = pd.DataFrame(usuarios.data)
    
    if df_gestores.empty:
        return pd.DataFrame(columns=["id","nombre","email","ciclo"])
    else:
        df_final = pd.merge(df_gestores, df_usuarios, on="email", how="left")
        return df_final

def getTutoresEmpresa():
    tutores = supabase.table(tutoresTabla).select("id, email, nombre,telefono, empresas(nombre)").execute()
    return tutores
def getTutores():
    tutores = supabase.table(tutoresCentroTabla).select("id, email, nombre,telefono").order("nombre").execute()
    usuarios = supabase.table(usuariosTabla).select("email, password").execute()
    
    df_tutores = pd.DataFrame(tutores.data)
    df_usuarios = pd.DataFrame(usuarios.data)
    if df_tutores.empty:
        return pd.DataFrame(columns=["id","nombre","email","telefono"])
    else:
        df_final = pd.merge(df_tutores, df_usuarios, on="email", how="left")
        return df_final
def getEmpresasYOfertas():
    res = (
        supabase.table(empresasTabla)
        .select("*, oferta_fp(ciclos_formativos,puestos,tutores_por_puesto, tutores(nombre))")
        .order("nombre")
        .execute()
    )
    return res.data

def updateTutores(cambios, df_original, cif=None):
    for new_row in cambios["added_rows"]:
        nombre = new_row.get("nombre", "").strip()
        telefono = new_row.get("telefono", "").strip()
        nif=new_row.get("nif", "").strip()
        cif_final = cif or new_row.get("cif_empresa", "").strip()
        email = new_row.get("email", "").strip().lower()
        password = new_row.get("password_temp") or new_row.get("password", "123456")
        if email and nombre:
            try:
                add(tutoresTabla, {
                    "nif":nif,
                    "nombre": nombre,
                    "email": email,
                    "cif_empresa":cif_final,
                    "telefono":telefono
                })
                add("usuarios", {
                    "email": email,
                    "password": password,
                    "rol": "tutor"
                })
            except Exception as e:
                raise Exception(f"Error al crear el usuario {email}: {e}")

    # 2. MANEJAR EDICIONES (Edited)
    for idx, mods in cambios["edited_rows"].items():
        fila_orig = df_original.iloc[int(idx)]
        id_tutores = fila_orig["id"]
        email_orig = fila_orig["email"]
        
        try:
            cambios_tutor = {k: v for k, v in mods.items() if k in ["nombre", "email", "nif", "activo","telefono"]}
            cambios_usuario = {k: v for k, v in mods.items() if k in ["password", "email"]}
            if cambios_tutor:
                update(tutoresTabla, mods, {"id": id_tutores})
            if cambios_usuario:
                update("usuarios", cambios_usuario, {"email": email_orig})
                
        except Exception as e:
            raise Exception(f"Error al actualizar el gestor {id_tutores}: {e}")

    # 3. MANEJAR BORRADOS (Deleted)
    for idx in cambios["deleted_rows"]:
        fila_orig = df_original.iloc[int(idx)]
        id_tutor = fila_orig["id"]
        email_tutor = fila_orig["email"]
        
        try:
            delete(tutoresTabla, "id", id_tutor)
            delete("usuarios", "email", email_tutor)
        except Exception as e:
            st.error(f"Error al eliminar {email_tutor}: {e}")
        


def updateTutoresCentro(cambios, df_original):
    for new_row in cambios["added_rows"]:
        nombre = new_row.get("nombre", "").strip()
        telefono = new_row.get("telefono", "").strip()
        email = new_row.get("email", "").strip().lower()
        password = new_row.get("password_temp") or new_row.get("password", "123456")
        if email and nombre:
            try:
                add(tutoresCentroTabla, {
                    "nombre": nombre,
                    "email": email,
                    "telefono":telefono
                })
                add("usuarios", {
                    "email": email,
                    "password": password,
                    "rol": "tutorCentro"
                })
            except Exception as e:
                raise Exception(f"Error al crear el usuario {email}: {e}")

    # 2. MANEJAR EDICIONES (Edited)
    for idx, mods in cambios["edited_rows"].items():
        fila_orig = df_original.iloc[int(idx)]
        id_tutores = fila_orig["id"]
        email_orig = fila_orig["email"]
        
        try:
            cambios_tutor = {k: v for k, v in mods.items() if k in ["nombre", "email", "nif", "activo","telefono"]}
            cambios_usuario = {k: v for k, v in mods.items() if k in ["password", "email"]}
            if cambios_tutor:
                update(tutoresCentroTabla, mods, {"id": id_tutores})
            if cambios_usuario:
                update("usuarios", cambios_usuario, {"email": email_orig})
                
        except Exception as e:
            raise Exception(f"Error al actualizar el gestor {id_tutores}: {e}")

    # 3. MANEJAR BORRADOS (Deleted)
    for idx in cambios["deleted_rows"]:
        fila_orig = df_original.iloc[int(idx)]
        id_tutor = fila_orig["id"]
        email_tutor = fila_orig["email"]
        
        try:
            delete(tutoresCentroTabla, "id", id_tutor)
            delete("usuarios", "email", email_tutor)
        except Exception as e:
            st.error(f"Error al eliminar {email_tutor}: {e}")
        

def updateGestores(cambios, df_original):
    for new_row in cambios["added_rows"]:
        nombre = new_row.get("nombre", "").strip()
        email = new_row.get("email", "").strip().lower()
        password = new_row.get("password_temp") 
        ciclo = new_row.get("ciclo", "").strip()
        if email and nombre:
            try:
                add(gestoresTabla, {
                    "nombre": nombre,
                    "email": email,
                    "ciclo":ciclo,
                    "activo": new_row.get("activo", True)
                })

                # Insertamos en la tabla de USUARIOS
                add("usuarios", {
                    "email": email,
                    "password": password,
                    "rol": "gestor"
                })
            except Exception as e:
                raise Exception(f"Error al crear el usuario {email}: {e}")

    # 2. MANEJAR EDICIONES (Edited)
    for idx, mods in cambios["edited_rows"].items():
        # Obtenemos los datos originales mediante el índice del DataFrame
        fila_orig = df_original.iloc[int(idx)]
        id_gestor = fila_orig["id"]
        email_orig = fila_orig["email"]

        try:
            # Actualizamos la tabla de gestores
            update(gestoresTabla, mods, {"id": id_gestor})
            
            # Si el email cambió, actualizamos también la tabla de usuarios
            if "email" in mods:
                nuevo_email = mods["email"].strip().lower()
                update("usuarios", {"email": nuevo_email}, {"email": email_orig})
                
            # Si se modificó el estado 'activo', podrías sincronizarlo con usuarios si fuera necesario
        except Exception as e:
            raise Exception(f"Error al actualizar el gestor {id_gestor}: {e}")

    # 3. MANEJAR BORRADOS (Deleted)
    for idx in cambios["deleted_rows"]:
        fila_orig = df_original.iloc[int(idx)]
        id_gestor = fila_orig["id"]
        email_gestor = fila_orig["email"]
        
        try:
            # Eliminamos de ambas tablas
            delete(gestoresTabla, "id", id_gestor)
            delete(usuariosTabla, "email", email_gestor)
        except Exception as e:
            raise Exception(f"Error al eliminar el gestor {email_gestor}: {e}")
        
def getOfertasTabla():
    response = supabase.table(necesidadFP).select("*, empresas(*, tutores(*))").execute()
    return pd.DataFrame(response.data)

def updateOfertasTabla(update_payload, id_oferta):
    response = supabase.table(necesidadFP).update(update_payload).eq("id", id_oferta).execute()
    return pd.DataFrame(response.data)

def get(tableName):
    response = supabase.table(tableName).select('*').execute()
    return response.data

def getEqual(tableName, variable, value):
    response = supabase.table(tableName).select('*').eq(variable, value).execute()
    return response.data
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
# def update(tableName, data,searchFor, searchValue):
#     response = supabase.table(tableName).update(data).eq(searchFor, searchValue).execute()
#     return response

#tabla = "feedback_forms"
# body = {"estado": "completado", "token": "nuevo_token_123"}
# filtros = {"practica_id": "123", "tipo_form": "feedback_inicial"}
def update(tabla: str, body: dict, filtros: dict):
    query = supabase.table(tabla).update(body)
    for col, val in filtros.items():
        query = query.eq(col, val)

    response = query.execute()
    return response
    
def delete(tableName,searchFor, searchValue):
    response = supabase.table(tableName).delete().eq(searchFor, searchValue).execute()
    return response


def actualizar_cupo(cif_empresa, ciclo, cambio):
    # 1. Traer la oferta actual
    res = supabase.table(necesidadFP).select("id, ciclos_formativos").eq("empresa", cif_empresa).execute()

    # 2. Modificar el JSON en Python
    if res.data and len(res.data) > 0:
        oferta_dict = res.data[0]
        ciclos = oferta_dict.get('ciclos_formativos', {})
        if ciclo in ciclos:
                # Modificamos el valor de disponibles
                actual = ciclos[ciclo].get('disponibles', 0)
                
                # Calculamos el nuevo valor (sin bajar de 0)
                nuevo_valor = max(0, actual + cambio)
                
                # Actualizamos el diccionario localmente
                ciclos[ciclo]['disponibles'] = nuevo_valor
                
                # Update en la tabla de ofertas usando el ID del diccionario extraído
                supabase.table(necesidadFP) \
                    .update({"ciclos_formativos": ciclos}) \
                    .eq("id", oferta_dict['id']) \
                    .execute()

def getOrdered(tableName, searchFor, searchValue, orderByColumn):
    response = supabase.table(tableName).select('*').eq(searchFor, searchValue).order(orderByColumn).execute()
    return response.data

def upsert(tableName, data,keys):
    response = supabase.table(tableName).upsert(data, on_conflict=keys).execute()
    return response

def upsertCustome(tableName, data, keys):
    query = supabase.table(tableName).select("*")

    for key in keys:
        query = query.eq(key, data[key])
    
    existing_record = query.execute()

    # 2. Lógica de decisión
    if existing_record.data:
        # Si existe, actualizamos
        # Filtramos para asegurarnos de actualizar el registro correcto
        update_query = supabase.table(tableName).update(data)
        for key in keys:
            update_query = update_query.eq(key, data[key])
        
        response = update_query.execute()
    else:
        response = supabase.table(tableName).insert(data).execute()
        
    return response
def saveAuthToken(data):
    return supabase.table('auth_tokens').insert(data).execute()

def getAuthToken(email):
    response = supabase.table('auth_tokens').select('*').eq('email', email).execute()
    if response.data:
        return response.data[0]  # ✅ Devolvemos el primer resultado como dict
    return None

def getPracticaByToken(token, tipo_form):
    try:
        fb_res = (
            supabase
            .table(feedbackFormsTabla)
            .select("*")
            .eq("token", token)
            .eq("tipo_form", tipo_form)
            .maybe_single()
            .execute()
        )
        if not fb_res.data:
            return None

        feedback = fb_res.data
        practica_id = feedback["practica_id"]

        # 2️⃣ Traer la práctica
        practica_res = (
            supabase
            .table(practicaTabla)
            .select("ciclo_formativo, area, fecha_inicio, empresa, alumno")
            .eq("id", practica_id)
            .single()
            .execute()
        )
        if not practica_res.data: return None           
        practica = practica_res.data

        # 3️⃣ Traer empresa
        empresa_res = (
            supabase
            .table(empresasTabla)
            .select("nombre")
            .eq("CIF", practica["empresa"])
            .single()
            .execute()
        )

        empresa = empresa_res.data

        # 4️⃣ Traer alumno
        alumno_res = (
            supabase
            .table(alumnosTabla)
            .select("nombre","apellido")
            .eq("dni", practica["alumno"])
            .single()
            .execute()
        )

        alumno = alumno_res.data

        # 5️⃣ Combinar todo en un dict final
        return {
            "feedback_form_id": feedback["id"],
            "practica_id": practica_id,
            "ciclo": practica["ciclo_formativo"],
            "area": practica["area"],
            "fecha_inicio": practica["fecha_inicio"],
            "empresa": empresa["nombre"],
            "alumno": alumno["nombre"] + " " + alumno["apellido"],
        }
    except Exception as e:
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
    e.created_at as "Creada",
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

    ORDER BY e.created_at desc, o.id, cf.key
    """

    response = supabase.rpc("exec_sql", {"sql": query}).execute()
    return response.data

def guardar_cambios_alumnos(df_updated, df_original, mapa_nombres_id):
    original_dict = df_original.set_index('dni').to_dict('index')
    for _, row in df_updated.iterrows():
        dni = row['dni']
        practicaId = None

        if pd.notna(row.get('practica_id')):
            practicaId = int(float(row['practica_id']))
        if dni not in original_dict:
            continue
        row_orig = original_dict[dni]
        def clean_str(val):
            if pd.isna(val) or val is None: return ""
            return str(val).strip()

        def clean_int(val):
            try:
                if pd.isna(val) or str(val).strip() == "": return 0
                return int(float(val))
            except:
                return 0

        # 3. EXTRAER VALORES ACTUALES
        curr_comentarios = clean_str(row.get('comentarios_centro'))
        curr_obs = clean_str(row.get('observaciones_seguimiento'))
        curr_nombre = clean_str(row.get('nombre'))
        curr_apellido = clean_str(row.get('apellido'))
        curr_horas = clean_int(row.get('horas_totales'))
        curr_gestor = clean_str(row.get('gestor'))
        curr_asignado = clean_str(row.get('asignado'))
        curr_practica = clean_str(row.get('practica_id'))
        # 4. EXTRAER VALORES ORIGINALES
        orig_comentarios = clean_str(row_orig.get('comentarios_centro'))
        orig_obs = clean_str(row_orig.get('observaciones_seguimiento'))
        orig_nombre = clean_str(row_orig.get('nombre'))
        orig_apellido = clean_str(row_orig.get('apellido'))
        orig_horas = clean_int(row_orig.get('horas_totales'))
        orig_gestor = clean_str(row_orig.get('gestor'))
        orig_asignado = clean_str(row_orig.get('asignado'))
        # 5. DETECCIÓN DE CAMBIOS EXPLÍCITA
        # He añadido curr_horas != orig_horas aquí para que el IF se active si cambian las horas
        hubo_cambio_alumno = (curr_nombre != orig_nombre or 
                      curr_apellido != orig_apellido or
                      curr_horas != orig_horas or
                      curr_comentarios != orig_comentarios or
                      curr_obs != orig_obs or
                      curr_gestor != orig_gestor)

        if hubo_cambio_alumno:
            datos_alumno = {
                "dni": dni,
                "nombre": curr_nombre,
                "apellido": curr_apellido,
                "horas_totales": curr_horas,
                "comentarios_centro": curr_comentarios,
                "observaciones_seguimiento": curr_obs,
                "gestor": curr_gestor
            }
            upsert(alumnosTabla, datos_alumno, keys=["dni"])


        # 6. LÓGICA DE ASIGNACIÓN DE EMPRESA
        nueva_empresa = row.get('nombre_empresa')
        empresa_antigua = row_orig.get('nombre_empresa')
        nuevo_puesto = row.get('puesto')
        antiguo_puesto= row_orig.get('puesto')
        nueva_direccion = row.get('direccion')
        nueva_localidad= row.get('localidad')
        nuevo_tutorCentro = row.get('tutor_centro')
        antiguo_tutorCentro = row_orig.get('tutor_centro')
        cambio_logistica = (nueva_empresa != empresa_antigua or 
                    nuevo_puesto != antiguo_puesto or 
                    nuevo_tutorCentro != antiguo_tutorCentro or
                    curr_gestor != orig_gestor)
        if cambio_logistica:
            cif_empresa = mapa_nombres_id.get(nueva_empresa) if nueva_empresa != "⚠️ SIN ASIGNAR" else None
        
            if nueva_empresa != empresa_antigua:
                if empresa_antigua != "⚠️ SIN ASIGNAR":
                    actualizar_cupo(empresa_antigua, row['ciclo_formativo'], +1)
                else:
                    datos_alumno = {
                        "dni": dni,
                        "estado":"Sin Empresa"}
                    upsert(alumnosTabla, datos_alumno, keys=["dni"])
                if cif_empresa:
                    actualizar_cupo(cif_empresa, row['ciclo_formativo'], -1)
            
            practica_res = crearDraftPractica(
                empresaCif=cif_empresa,
                alumnoDni=dni,
                ciclo=row['ciclo_formativo'], 
                area=nuevo_puesto if nuevo_puesto else "General",
                proyecto= "No asignado aun",
                tutorCentro= nuevo_tutorCentro if nuevo_tutorCentro else "Sin asignar",
                fecha=datetime.now().isoformat(),
                ciclos_info=None, 
                cupos_disp=0, 
                oferta_id=row.get('oferta_id'),
                status="Borrador",
                practicaId=practicaId,
                gestor=curr_gestor,
                direccion=nueva_direccion,
                localidad=nueva_localidad
            )
            practicaId = practica_res[0].get("id")
        if curr_asignado != orig_asignado:
            if practicaId and nueva_empresa != "⚠️ SIN ASIGNAR":
                datos_alumno = {
                "dni": dni,
                "estado":"Asignado"}
                upsert(alumnosTabla, datos_alumno, keys=["dni"])
                update(practicaTabla, {"status": "Nuevo"}, {"id": practicaId})
                upsert(practicaEstadosTabla, {"practicaId": practicaId}, keys=["practicaId"])
            else:
                st.warning(f"No se puede confirmar la práctica de {curr_nombre} sin una empresa asignada.")

def crearDraftPractica(empresaCif, alumnoDni, ciclo, area, proyecto, tutorCentro, fecha,ciclos_info,cupos_disp,oferta_id, status, 
                       practicaId=None, gestor=None,direccion=None, localidad=None):
        payload_practica = {
            "empresa": empresaCif,
            "alumno": alumnoDni,
            "ciclo_formativo": ciclo,
            "area": area,
            "tutor_centro": tutorCentro,
            "proyecto": proyecto,
            "oferta": oferta_id,
            "status": status,
            "gestor": gestor,
            "direccion": direccion,
            "localidad": localidad
        }
        if practicaId:
            payload_practica["id"] = practicaId
        response = upsert(practicaTabla, payload_practica, keys=["id"])
        upsert(
        alumnosTabla,
        {"dni": alumnoDni, "estado": estadosAlumno[1]},
        keys=["dni"])

        if ciclos_info != None:
            ciclos_info[ciclo]["disponibles"] = max(cupos_disp - 1, 0)
            upsert(
                necesidadFP,
                {
                    "id": oferta_id,
                    "empresa": empresaCif,
                    "ciclos_formativos": ciclos_info,
                },
                keys=["id"],
            )
        upsert(
            alumnoEstadosTabla,
            {"alumno": alumnoDni, 'match_fp': fecha, 'fp_asignada': fecha},
            keys=["alumno"]
        )
        return response.data
        #create_drive_folder_practica(alumnoDni,alumnoNombre,alumnoApellido, empresaCif,carpetaPractica)

def cancelarPractica(practicaId, alumnoDni, motivo):
    payload_practica = {"id": int(practicaId),"status": "CANCELADA","motivo": motivo}
    try:
        resp = upsert(practicaTabla, payload_practica, keys=["id"])
        dateToday = datetime.now().isoformat()
        if resp:
                respAl = update(alumnosTabla,{"estado": "Sin Empresa"},{"dni":alumnoDni})
                if respAl:
                 upsert(
                    alumnoEstadosTabla,
                    {"alumno": alumnoDni, 'fp_cancelada': dateToday, 'fp_asignada': None,'match_fp': None, 'email_enviado': None,'fp_enprogreso': None,'fp_finalizada': None},
                    keys=["alumno"])

    except Exception as e:
            st.error(f"Error procesando la cancelación de la práctica: {e}")


def crearPractica(empresaCif, alumnoDni, ciclo, area, proyecto, fecha,ciclos_info,cupos_disp,oferta_id, status:None):
    registro_existente = getEquals(practicaTabla, {"alumno": alumnoDni})
    payload_practica = {
        "empresa": empresaCif,
        "alumno": alumnoDni,
        "ciclo_formativo": ciclo,
        "area": area,
        "proyecto": proyecto,
        "oferta": oferta_id,
        "status":status
    }

    if registro_existente:
        practicaId = registro_existente[0]["id"]
        payload_practica["id"] = practicaId
        res_practica = upsert(practicaTabla, payload_practica, keys=["id"])
    else:
        res_practica = add(practicaTabla, payload_practica)
        practicaId = res_practica.data[0]["id"]
        upsert(practicaEstadosTabla, {"practicaId": practicaId}, keys=["practicaId"])
        upsert(
        alumnosTabla,
        {"dni": alumnoDni, "estado": estadosAlumno[1]},
        keys=["dni"])

        
        if ciclos_info != None:
            ciclos_info[ciclo]["disponibles"] = max(cupos_disp - 1, 0)
            upsert(
                necesidadFP,
                {
                    "id": oferta_id,
                    "empresa": empresaCif,
                    "ciclos_formativos": ciclos_info,
                },
                keys=["id"],
            )
    upsert(
        alumnoEstadosTabla,
        {"alumno": alumnoDni, 'match_fp': fecha, 'fp_asignada': fecha},
        keys=["alumno"]
    )

    
def asignarFechasFormsFeedback(practica_id, fecha_inicio, email_destino, fecha_fin):
    for i, tipo in enumerate(forms):
        if i == len(forms) - 1:
            fecha_envio = fecha_fin.isoformat()
        else:
            dias_a_sumar = 7 if tipo == forms[0] else 30 if tipo == forms[1] else 32 if tipo == forms[2] else 0
            fecha_envio = (fecha_inicio + timedelta(days=dias_a_sumar)).isoformat()
    
        try:
            registro_existente = getEquals(feedbackFormsTabla, {"practica_id": int(practica_id), "tipo_form":tipo})

            token = uuid.uuid4().hex
            data_feedback = {
                "practica_id": int(practica_id),
                "fecha_envio": fecha_envio,
                "email_destino": email_destino,
                "tipo_form": tipo,
                "token": token,
                "estado": "pendiente",
            }
            if registro_existente:
                id_registro = registro_existente[0]['id']
                update(feedbackFormsTabla, data_feedback, {"id": id_registro})
            else:
                add(feedbackFormsTabla, data_feedback)       
        except Exception as e:
            st.error(f"Error procesando feedback para {tipo}: {e}")