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
    tutoresTabla
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
    response = (
        supabase.table(alumnosTabla)
        .select("*, practicas_fp(alumno, empresas(CIF, nombre,telefono, email_empresa), area, tutor)")
        .eq("estado", "Sin Empresa")
        .is_("practicas_fp.fecha_inicio", "null")
        .order("ciclo_formativo")
        .execute()
    )

    if not response.data:
        return pd.DataFrame()
    rows = []
    for item in response.data:
        # Extraemos la primera práctica si existe
        practicas = item.get("practicas_fp", [])
        practica = practicas[0] if practicas else {}
        empresa = practica.get("empresas", {}) if practica else {}
        
        row = {
            **item,  # Incluye todos los campos de alumnos (dni, nombre, ciclo, etc.)
            "practica_id": practica.get("id"),
            "id_empresa": empresa.get("CIF"),
            "nombre_empresa": empresa.get("nombre", "⚠️ SIN ASIGNAR"),
            "email_empresa": empresa.get("email_empresa"),
            "telefono_empresa": empresa.get("telefono"),
            "area": practica.get("area"),
            "tutor": practica.get("tutor")
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
    gestores = supabase.table(gestoresTabla).select("email, nombre").order("nombre").execute()
    usuarios = supabase.table(usuariosTabla).select("email, password").execute()
    
    df_gestores = pd.DataFrame(gestores.data)
    df_usuarios = pd.DataFrame(usuarios.data)
    
    df_final = pd.merge(df_gestores, df_usuarios, on="email", how="inner")
    return df_final

def getTutores():
    tutores = supabase.table(tutoresTabla).select("id, email, nombre").order("nombre").execute()
    usuarios = supabase.table(usuariosTabla).select("email, password").execute()
    
    df_tutores = pd.DataFrame(tutores.data)
    df_usuarios = pd.DataFrame(usuarios.data)
    
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

def updateTutores(cambios, df_original):
    for new_row in cambios["added_rows"]:
        nombre = new_row.get("nombre", "").strip()
        email = new_row.get("email", "").strip().lower()
        password = new_row.get("password_temp") or new_row.get("password", "123456")
        nif = "00000000"
        if email and nombre:
            try:
                add(tutoresTabla, {
                    "nif":nif,
                    "nombre": nombre,
                    "email": email,
                })

                # Insertamos en la tabla de USUARIOS
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
            cambios_tutor = {k: v for k, v in mods.items() if k in ["nombre", "email", "nif", "activo"]}
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
        

def updateGestores(cambios, df_original):
    for new_row in cambios["added_rows"]:
        nombre = new_row.get("nombre", "").strip()
        email = new_row.get("email", "").strip().lower()
        password = new_row.get("password_temp") 
        
        if email and nombre:
            try:
                add(gestoresTabla, {
                    "nombre": nombre,
                    "email": email,
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
    response = supabase.table(necesidadFP).select("*, empresas(*), tutores(*)").execute()
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
    # 1. Aseguramos que el original sea un diccionario indexado por DNI para acceso rápido
    original_dict = df_original.set_index('dni').to_dict('index')
    
    for _, row in df_updated.iterrows():
        dni = row['dni']
        
        # Si por alguna razón el DNI no está en el original, saltamos
        if dni not in original_dict:
            continue
            
        row_orig = original_dict[dni]

        # 2. LIMPIEZA Y NORMALIZACIÓN DE VALORES
        def clean_str(val):
            if pd.isna(val) or val is None: return ""
            return str(val).strip()

        def clean_bool(val):
            if isinstance(val, str):
                return "true" in val.lower() or "✅" in val
            return bool(val)

        def clean_int(val):
            try:
                # Maneja nulos, strings vacíos y decimales antes de convertir a entero
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
        # 4. EXTRAER VALORES ORIGINALES
        orig_comentarios = clean_str(row_orig.get('comentarios_centro'))
        orig_obs = clean_str(row_orig.get('observaciones_seguimiento'))
        orig_nombre = clean_str(row_orig.get('nombre'))
        orig_apellido = clean_str(row_orig.get('apellido'))
        orig_horas = clean_int(row_orig.get('horas_totales'))
        orig_gestor = clean_str(row_orig.get('gestor'))
        # 5. DETECCIÓN DE CAMBIOS EXPLÍCITA
        # He añadido curr_horas != orig_horas aquí para que el IF se active si cambian las horas
        hubo_cambio_texto = (curr_comentarios != orig_comentarios or 
                            curr_obs != orig_obs or
                            curr_nombre != orig_nombre or 
                            curr_apellido != orig_apellido or
                            curr_horas != orig_horas or
                            curr_gestor != orig_gestor 
                            )
        
        # Comparación de booleanos (anexos)
        hubo_cambio_anexos = any(
            clean_bool(row[col]) != clean_bool(row_orig[col]) 
            for col in ["anexos_creados", "anexos_enviados", "anexos_firmados", "doc_sao_entregada"]
        )

        if hubo_cambio_texto or hubo_cambio_anexos:
            datos_alumno = {
                "dni": dni,
                "nombre": curr_nombre,
                "apellido": curr_apellido,
                "horas_totales": curr_horas,
                "anexos_creados": clean_bool(row['anexos_creados']),
                "anexos_enviados": clean_bool(row['anexos_enviados']),
                "anexos_firmados": clean_bool(row['anexos_firmados']),
                "doc_sao_entregada": clean_bool(row['doc_sao_entregada']),
                "comentarios_centro": curr_comentarios,
                "observaciones_seguimiento": curr_obs,
                "gestor": curr_gestor
            }
            
            # Ejecutar el guardado
            upsert(alumnosTabla, datos_alumno, keys=["dni"])

        # 6. LÓGICA DE ASIGNACIÓN DE EMPRESA
        nueva_empresa = row.get('nombre_empresa')
        empresa_antigua = row_orig.get('nombre_empresa')
        nuevo_puesto = row.get('puesto')
        antiguo_puesto= row_orig.get('puesto')
        nuevo_tutor = row.get('tutor')
        antiguo_tutor = row_orig.get('tutor')
        if nueva_empresa != empresa_antigua or nuevo_puesto != antiguo_puesto or nuevo_tutor != antiguo_tutor:
            if nueva_empresa == "⚠️ SIN ASIGNAR":
                delete(practicaTabla, "alumno", dni)
                upsert(alumnosTabla, {"dni": dni, "estado": "Sin Empresa"}, keys=["dni"])
            else:
                cif_empresa = mapa_nombres_id.get(nueva_empresa)
                if cif_empresa:
                    crearDraftPractica(
                        empresaCif=cif_empresa,
                        alumnoDni=dni,
                        ciclo=row['ciclo_formativo'], 
                        area=nuevo_puesto if nuevo_puesto else "General",
                        proyecto= "No asignado aun",
                        tutor= nuevo_tutor if nuevo_tutor else "Nin asignar",
                        fecha=datetime.now().isoformat(),
                        ciclos_info=None, 
                        cupos_disp=0, 
                        oferta_id=row.get('oferta_id') 
                    )

def crearDraftPractica(empresaCif, alumnoDni, ciclo, area, proyecto, tutor, fecha,ciclos_info,cupos_disp,oferta_id):
        payload_practica = {
            "empresa": empresaCif,
            "alumno": alumnoDni,
            "ciclo_formativo": ciclo,
            "area": area,
            "tutor": tutor,
            "proyecto": proyecto,
            "oferta": oferta_id
        }
        add(practicaTabla, payload_practica)

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


def crearPractica(empresaCif, alumnoDni, ciclo, area, proyecto, fecha,ciclos_info,cupos_disp,oferta_id):
    registro_existente = getEquals(practicaTabla, {"alumno": alumnoDni})
    payload_practica = {
        "empresa": empresaCif,
        "alumno": alumnoDni,
        "ciclo_formativo": ciclo,
        "area": area,
        "proyecto": proyecto,
        "oferta": oferta_id
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