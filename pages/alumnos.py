import streamlit as st
import pandas as pd
import os
import uuid
from pathlib import Path
from modules.data_base import get, update, upsert,getEqual,logError,getCiclosYAreas
from page_utils import apply_page_config
from navigation import make_sidebar
from variables import alumnosTabla, aniosList, cursoList, localidades, max_file_size,tipoPracticas,carpetaAlumnos,alumnoEstadosTabla,alumnosTabla, bodyEmailsAlumno, alumnoEstadosTabla
from datetime import datetime
from modules.emailSender import send_email
from modules.drive_helper import list_drive_files,upload_to_drive
from modules.forms_helper import  file_size_bytes
import re
apply_page_config()
make_sidebar()

st.set_page_config(page_title="Alumnos", page_icon="🧑‍🎓")
st.markdown(
    "<h2 style='text-align: center;'>ALUMNOS</h2>",
    unsafe_allow_html=True
)
if "uploader_key" not in st.session_state:
    st.session_state.uploader_key = 0
if "form_registro_key" not in st.session_state:
    st.session_state.form_registro_key = 0


base_url =  st.secrets["urls"]["URL"] 

# --- Traer alumnos ---
alumnos = get(alumnosTabla)
ciclos, areas = getCiclosYAreas()

if not alumnos:
    st.warning("No hay alumnos registrados")
    st.stop()

df_alumnos = pd.DataFrame(alumnos)


# --- Tabs principales ---
tab1, tab2, tab3 = st.tabs(["🔍 Buscar / Visualizar", "➕ Nuevo Alumno", "📋 Formulario & Contacto"])

# -------------------------------------------------------------------
# TAB 1: Buscar / Visualizar / Editar
# -------------------------------------------------------------------
with tab1:
    filtrarCF, filtroanio, filtrocurso, total,descargar= st.columns([2,2,2,2,2])
    with filtrarCF:
        cicloForm = sorted(df_alumnos["ciclo_formativo"].dropna().unique())
        selected_ciclo = st.selectbox("Filtrar por ciclo formativo", options=["Todos"] + cicloForm, index=0)
        if selected_ciclo != "Todos":
            df_alumnos = df_alumnos[df_alumnos["ciclo_formativo"] == selected_ciclo]     
    with filtroanio:
        selected_anio = st.selectbox("Filtrar por curso académico", options= aniosList, index=st.session_state.get("index_academic", 0))
        if selected_anio != "Seleccionar":
            df_alumnos = df_alumnos[df_alumnos["anio"] == selected_anio]     
    with filtrocurso:
        selected_curso = st.selectbox("Filtrar por curso", options= cursoList, index=st.session_state.get("index_curso",0))
        if selected_curso != "Seleccionar":
            df_alumnos = df_alumnos[df_alumnos["curso"] == selected_curso]
    with total:
        st.metric("Total alumnos", len(df_alumnos))
    with descargar:
        import tempfile
        from pathlib import Path

        # Esto funcionará en Windows, Linux y Mac automáticamente
        temp_dir = Path(tempfile.gettempdir())
        temp_path = temp_dir / f"alumnos_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
        df_alumnos.to_excel(temp_path, index=False)
        st.write("Exportar datos:")
        with open(temp_path, "rb") as f:
            st.download_button(
                label="⬇️",
                data=f,
                file_name=temp_path.name,
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
   

    search = st.text_input("Buscar alumnos", placeholder="Buscar alumno")
    if search:
        mask = df_alumnos.astype(str).apply(
            lambda row: row.str.contains(search, case=False, na=False).any(),
            axis=1
        )
        df_alumnos = df_alumnos[mask]
    # Vista resumida
    cols_map = {
        "dni": "DNI",
        "nombre": "Nombre",
        "apellido": "Apellido",
        "direccion": "Dirección",
        "localidad": "Localidad",
        "telefono": "Teléfono",
        "email_alumno": "Email",
        "vehiculo": "Vehículo",
        "tipoPractica": "Tipo Formación",
    }
    df_view = df_alumnos[list(cols_map.keys())].rename(columns=cols_map)
    st.dataframe(df_view, hide_index=True, width='stretch')

    # Selección de alumno
    if not df_alumnos.empty:
        alumnos_options = {"Ninguno": None}
        for _, row in df_alumnos.iterrows():
            alumnos_options[f"{row['apellido']}, {row['nombre']}"] = row["id"]

        selected_name = st.selectbox("Seleccionar alumno", list(alumnos_options.keys()), index=0)

        if alumnos_options[selected_name]:
            alumno_id = alumnos_options[selected_name]
            alumno = df_alumnos[df_alumnos["id"] == alumno_id].iloc[0].to_dict()
            estadosAlumnos = getEqual(alumnoEstadosTabla, "alumno", alumno["dni"])
            subtab1, subtab3 = st.tabs([f"✏️ Detalle: {alumno['nombre']} {alumno['apellido']}","📂 Documentos"])

            # --- Detalle / edición ---
            with subtab1:
                st.write("Edita los datos y guarda para actualizar:")
                col1, col2 = st.columns(2)
                with col1:
                    new_nombre = st.text_input("Nombre", alumno.get("nombre", ""))
                    new_apellido = st.text_input("Apellido", alumno.get("apellido", ""))
                    new_dni = st.text_input("DNI", alumno.get("dni", ""))
                    new_nia = st.text_input("NIA", alumno.get("NIA", ""))
                    new_nuss = st.text_input("NUSS", alumno.get("nuss", ""))
                  
                with col2:
                    new_telefono = st.text_input("Teléfono", alumno.get("telefono", ""))
                    new_email = st.text_input("Email", alumno.get("email_alumno", ""))
                    new_direccion = st.text_input("Dirección", alumno.get("direccion", ""))
                    new_codigoPostal = st.text_input("CP", alumno.get("codigo_postal", ""))
                    current_loc = alumno.get("localidad", "")
                    try:
                        default_index_loc = localidades.index(current_loc)
                    except (ValueError, TypeError):
                        default_index_loc = 10
                    new_localidad = st.selectbox("Localidad *", options=localidades, index=default_index_loc)
                    
                    tipo_opts = tipoPracticas
                st.divider()
                new_tipo_practica = st.selectbox(
                    "Tipo de Formación",
                    options=tipo_opts,
                    index=tipo_opts.index(alumno.get("tipoPractica")) if alumno.get("tipoPractica") in tipo_opts else 0
                )

                tipo_practica = alumno.get("tipoPractica") or "N/A"
                vehiculo_val = alumno.get("vehiculo")
                vehiculo_bool = True if vehiculo_val == "Sí" else False

                
                current_ciclo = alumno.get("ciclo_formativo") or ""
                current_pref = alumno.get("preferencias_fp") or "[]"

                selected_ciclo = st.selectbox(
                    "Ciclo Formativo",
                    options=[""] + ciclos,  # agrega una opción vacía
                    index=([""] + ciclos).index(current_ciclo) if current_ciclo in ciclos else 0,
                    placeholder="Selecciona un ciclo formativo"
                )

                selected_pref = []
                if selected_ciclo and selected_ciclo in areas:
                    prefs_options = areas[selected_ciclo]
                    selected_pref = st.multiselect(
                        f"Preferencia para {selected_ciclo}",
                        options=prefs_options,
                        default=[p for p in current_pref if p in prefs_options],
                        key=f"prefs_multiselect_{alumno['dni']}",placeholder="Selecciona preferencias"
                    )
                else:
                    st.info("Selecciona un ciclo formativo para ver las preferencias disponibles.")

                ano = st.selectbox("Curso Académico *", options= aniosList,index=aniosList.index(alumno.get("anio")) if alumno.get("anio") in aniosList else 0)
                curso = st.selectbox("Curso *", options= cursoList,index=cursoList.index(alumno.get("curso")) if alumno.get("curso") in cursoList else 0)
                
                vehiculo_selected = st.checkbox("Vehículo", value=vehiculo_bool,key=f"vehiculo_pref_{new_email}")
                val_requisitos = "" if pd.isna(alumno.get("requisitos")) else str(alumno.get("requisitos"))

                requisitos = st.text_input("Requisitos adicionales (separados por comas)", value=val_requisitos)
                raw_horas = alumno.get("horas_totales")
                if pd.isna(raw_horas) or raw_horas is None:
                    val_horas_totales = 0
                else:
                    try:
                        val_horas_totales = int(raw_horas)
                    except ValueError:
                        val_horas_totales = 7
                horas_totales = st.number_input("Horas Totales", value=val_horas_totales,step=1) 
                if st.button("💾 Actualizar alumno"):
                    data_alumnos = {
                            "nombre": new_nombre,
                            "apellido": new_apellido,
                            "direccion": new_direccion,
                            "localidad": new_localidad,
                            "codigo_postal": new_codigoPostal,
                            "dni": new_dni,
                            "NIA": new_nia,
                            "telefono": new_telefono,
                            "email_alumno": new_email,
                            "tipoPractica": new_tipo_practica,
                            "anio": ano.strip(),
                            "curso": curso.strip(),
                            "ciclo_formativo": selected_ciclo,
                            "preferencias_fp": selected_pref,
                            "vehiculo": "Sí" if vehiculo_selected else "No",
                            "requisitos": requisitos,
                            "horas_totales": horas_totales
                        }
                    update(
                        alumnosTabla,
                        data_alumnos,
                        {"id":alumno_id}
                    )
                    st.toast("Alumno actualizado correctamente")
                    st.rerun()


            with subtab3:
                folder_name = f"{alumno['nombre']}_{alumno['apellido']}_{alumno['dni']}".strip()
                files, folderId = list_drive_files(folder_name)

                if not files:
                    st.warning("No hay archivos en la carpeta del alumno.")
                else:
                    # if folderId:
                    #     folder_link = f"https://drive.google.com/drive/folders/{folderId}"
                    #     st.link_button("🔗 Abrir carpeta", folder_link)
                    st.write("Archivos del alumno:")
                    for f in files:
                                fecha = f.get("modifiedTime", "")[:10]
                                download_link = f.get("webContentLink") or f.get("webViewLink")
                                col1, col2, col3 = st.columns([5, 1, 1])
                                with col1:
                                    st.write(f"📥 [{f['name']}]({download_link}) _(modificado: {fecha})_")

                st.divider()
                st.write("📤 Subir archivos adicionales para el alumno:")

                uploaded_files = st.file_uploader(
                    "Selecciona uno o varios archivos (PDF/DOC/DOCX/ODT)",
                    type=["pdf", "doc", "docx", "odt"],
                    accept_multiple_files=True
                )

                if uploaded_files:
                    too_big_files = [f.name for f in uploaded_files if file_size_bytes(f) > max_file_size]

                    if too_big_files:
                        st.error(f"Los siguientes archivos superan los 20 MB: {', '.join(too_big_files)}")
                    else:
                        if st.button("Subir Archivos"):
                            try:
                                total = len(uploaded_files)
                                st.info(f"Subiendo {total} archivo(s), por favor espera...")

                                for i, file in enumerate(uploaded_files, start=1):
                                    extension = Path(file.name).suffix
                                    nombre_alumno_limpio = f"{alumno['nombre']}_{alumno['apellido']}".replace(" ", "_")
                                    nuevo_nombre = f"{nombre_alumno_limpio}_{file.name}"
                                    tmp_path = Path("/tmp") / f"{uuid.uuid4()}_{nuevo_nombre}"
                                    with open(tmp_path, "wb") as f:
                                        f.write(file.getbuffer())

                                    res = upload_to_drive(str(tmp_path), carpetaAlumnos, folder_name, nuevo_nombre)

                                    if isinstance(res, dict):
                                        link = res.get("webViewLink") or res.get("webContentLink")
                                    else:
                                        link = None

                                    st.success(f"✅ {i}/{total}: {nuevo_nombre} subido correctamente")
                                    if link:
                                        st.markdown(f"[Abrir]({link})")

                                st.success("🎉 Todos los archivos se subieron correctamente.")
                                st.rerun()

                            except Exception as e:
                                logError(f"{type(e).__name__}: {str(e)}", "Alumnos - Subida de Archivos")
                                st.error(f"❌ Error al subir los archivos: {e}")

# -------------------------------------------------------------------
# TAB 2: Nuevo Alumno
# -------------------------------------------------------------------
with tab2:
    tabNuevo, tabBulk = st.tabs(["Nuevo Alumno", "Carga Masiva (.csv)"])
    with tabNuevo:
        with st.form(key=f"nuevo_alumno_form_{st.session_state.form_registro_key}"):
            new_nombre = st.text_input("Nombre")
            new_apellido = st.text_input("Apellido")
            new_direccion = st.text_input("Dirección")
            new_codigoPostal = st.text_input("CP")
            new_localidad = st.selectbox("Localidad *", (localidades))
            new_dni = st.text_input("DNI")
            new_nia = st.text_input("NIA")
            new_nuss = st.text_input("NUSS")
            new_telefono = st.text_input("Teléfono")
            new_email = st.text_input("Email")
            tipo_opts = tipoPracticas
            new_tipo_practica = st.selectbox(
                "Tipo de Formación",
                options=tipo_opts,
                index=0
            )
            selected_ciclo = st.selectbox(
                    "Ciclo Formativo",
                    options=[""] + ciclos,  # agrega una opción vacía
                    index= 0,
                    placeholder="Selecciona un ciclo formativo"
                )
            ano = st.selectbox("Curso Académico *", options= aniosList)
            curso = st.selectbox("Curso *", options= cursoList, key="nuevo_curso")
            val_horas_totales = 10
            horas_totales = st.number_input("Horas Totales", value=val_horas_totales, step=1) 

            submitted = st.form_submit_button("Crear Alumno")

        if submitted:
            # --- SECCIÓN DE VALIDACIÓN ---
            campos_obligatorios = {
                "Nombre": new_nombre,
                "Apellido": new_apellido,
                "DNI": new_dni,
                "Email": new_email
            }
            
            # Filtramos cuáles están vacíos
            faltantes = [label for label, valor in campos_obligatorios.items() if not valor or valor.strip() == ""]
            
            if faltantes:
                st.error(f"⚠️ Los siguientes campos son obligatorios: {', '.join(faltantes)}")
            else:
                # Si pasa la validación, procedemos al guardado
                try:
                    upsert(
                        alumnosTabla,
                        {
                            "nombre": new_nombre,
                            "apellido": new_apellido,
                            "direccion": new_direccion,
                            "localidad": new_localidad,
                            "dni": new_dni,
                            "NIA": new_nia,
                            "nuss": new_nuss,
                            "codigo_postal": new_codigoPostal,
                            "telefono": new_telefono,
                            "email_alumno": new_email,
                            "estado": "Sin Empresa",
                            "tipoPractica": new_tipo_practica,
                            "anio": ano,
                            "curso": curso,
                            "ciclo_formativo": selected_ciclo,
                            "horas_totales": horas_totales
                        }, keys=["dni"]
                    )
                    st.success("✅ Nuevo alumno agregado correctamente")
                    st.session_state.form_registro_key += 1
                    st.rerun()
                except Exception as e:
                    logError(f"{type(e).__name__}: {str(e)}", "Alumnos - Nuevo Alumno")
                    st.error(f"Hubo un error al guardar: {e}")
    with tabBulk:
        st.write("📥 Cargar alumnos desde CSV")

        # 1. Excel de muestra
        sample_df = pd.DataFrame({
            "nombre": [""],
            "apellido": [""],
            "direccion": [""],
            "codigo_postal": [""],
            "localidad": [""],
            "dni": [""],  # obligatorio
            "NIA": [""],
            "telefono": [""],
            "email_alumno": [""],
            "anio": [aniosList[1:]],
            "curso": [cursoList[1:]],
            "ciclo": [ciclos],
            "tipoPractica": ["Autogestionada | Asignada por el Centro"],
            "horas_totales": [""]
        })
        sample_csv_path = Path(tempfile.gettempdir()) / "alumnos_muestra.csv"
        sample_df.to_csv(sample_csv_path, index=False, encoding="utf-8")

        with open(sample_csv_path, "rb") as f:
            st.download_button(
                label="⬇️ Descargar CSV de ejemplo",
                data=f,
                file_name="alumnos_muestra.csv",
                mime="text/csv"
            )

        st.info("Sube un archivo CSV. Solo el DNI es obligatorio. El resto de las columnas son opcionales.")

        # 2. File uploader
        uploaded_csv = st.file_uploader(
            "Subir archivo CSV (.csv)",
            type=["csv"],
            key=f"upload_csv_{st.session_state.uploader_key}"
        )

        if uploaded_csv:
            try:
                # Leer TODO como string siempre → adiós floats y NaNs
                df_csv = pd.read_csv(uploaded_csv, dtype=str, encoding="utf-8").fillna("")

                st.write("📄 **Vista previa del archivo cargado:**")
                st.dataframe(df_csv.head(), width='stretch')

                # Validar presencia de columna DNI
                if "dni" not in df_csv.columns:
                    st.error("❌ El archivo debe incluir la columna 'dni'.")
                    st.stop()

                with st.spinner(f"Procesando alumos."):
                    if st.button("🚀 Crear/Actualizar alumnos desde CSV"):
                        creados = 0
                        errores = []

                        # Iterar filas
                        for _, row in df_csv.iterrows():

                            # 1️⃣ Saltar fila completamente vacía
                            if not any(str(v).strip() for v in row.values):
                                continue

                            # 2️⃣ Normalizar DNI
                            dni_raw = row.get("dni", "").strip()
                            dni = re.sub(r"\.0+$", "", dni_raw)  # eliminar .0 si CSV viene de Excel
                            dni = dni.strip()

                            if not dni:
                                errores.append("Fila sin DNI — omitida.")
                                continue

                            horas_raw = row.get("horas_totales", "").strip()
                            try:
                                # Reemplazamos coma por punto por si el usuario escribió "350,5"
                                horas_float = float(horas_raw.replace(",", ".")) if horas_raw else 7.0
                            except ValueError:
                                # Si el usuario escribió texto no numérico, cae aquí
                                horas_float = 7.0
                            data = {
                                "dni": dni,
                                "nombre": row.get("nombre", "").strip(),
                                "apellido": row.get("apellido", "").strip(),
                                "direccion": row.get("direccion", "").strip(),
                                "codigo_postal": row.get("codigo_postal", "").strip(),
                                "localidad": row.get("localidad", "").strip().upper(),
                                "NIA": row.get("NIA", "").strip(),
                                "telefono": row.get("telefono", "").strip(),
                                "email_alumno": row.get("email_alumno", "").strip(),
                                "estado": "Sin Empresa",
                                "tipoPractica": row.get("tipoPractica", "").strip(),
                                "anio": re.sub(r"['\"]", "", row.get("anio", "")).strip(),
                                "curso": re.sub(r"['\"]", "", row.get("curso", "")).strip(),
                                "ciclo_formativo": re.sub(r"['\"]", "", row.get("ciclo", "")).strip(),
                                "horas_totales": horas_float,
                            }

                            # 4️⃣ Insert/update
                            try:
                                upsert(alumnosTabla, data, keys=["dni"])
                                creados += 1
                                    
                            except Exception as e:
                                errores.append(f"DNI {dni}: {e}")
                        
                        if errores:
                            st.warning("⚠️ Errores encontrados:")
                            for err in errores:
                                st.write("- " + err)
                        else:
                            st.toast(f"🎉 {creados} alumnos creados o actualizados correctamente.")
                            st.session_state.uploader_key += 1
                            st.rerun()

            except Exception as e:
                error_msg = f"{type(e).__name__}: {str(e)}"
                logError(error_msg,"Alumnos - Leyendo CSV")
                st.error(f"❌ Error leyendo el CSV: {e}")

# -------------------------------------------------------------------
# TAB 3: Formulario Alumno
# -------------------------------------------------------------------
formUrlAlumno = st.secrets["urls"]["FORM_ALUMNO"] 
can_send = True
with tab3:
    if "emailsList" not in st.session_state:
        st.session_state.emailsList = []
    st.write("🎓 Contactar Alumnos")
    
    if not alumnos:
        st.warning("No hay alumnos registrados")
        st.stop()

    df_alumnos = pd.DataFrame(alumnos)
    df_clean_al = df_alumnos.dropna(subset=["email_alumno", "nombre"]).copy()

    # Opcional: Eliminar también si el email es un string vacío "" (no solo nulo)
    df_clean_al = df_clean_al[df_clean_al["email_alumno"].str.strip() != ""]

    # 2. Creamos el nombre completo para mostrar
    df_clean_al["nombre_completo"] = df_clean_al["nombre"] + " " + df_clean_al["apellido"].fillna("")

    # 3. Preparamos las opciones del multiselect (solo con los que pasaron el filtro)
    nombreAlumnosClean = df_clean_al["nombre_completo"].unique().tolist()
    emailsAlumnosClean = df_clean_al["email_alumno"].unique().tolist()
    col1, col2 = st.columns([3, 2])
    with col2:
        checked = st.checkbox("Seleccionar todos", value=False, key="select_all_alumnos")

    with col1:
        # Mostramos los nombres completos
        alumnos_seleccionados = st.multiselect(
            "Selecciona alumnos", 
            placeholder="Selecciona un valor",
            options=nombreAlumnosClean,
            disabled=st.session_state.select_all_alumnos
        )

    emails_manual_alumnos = st.text_area(
        "Agregar emails manualmente (separados por coma)",
        placeholder="ejemplo1@mail.com, ejemplo2@mail.com",
        key="emails_manual_alumnos"
    )

    # --- Validación de emails manuales (tu lógica original corregida) ---
    EMAIL_REGEX = re.compile(r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$")
    valid_emails_manual = []
    invalid_emails = []

    if emails_manual_alumnos.strip():
        raw_list = [e.strip() for e in emails_manual_alumnos.split(",") if e.strip()]
        for e in raw_list:
            if EMAIL_REGEX.match(e):
                valid_emails_manual.append(e.lower())
            else:
                invalid_emails.append(e)
        valid_emails_manual = list(set(valid_emails_manual))

        if invalid_emails:
            st.warning(f"Correos inválidos: {', '.join(invalid_emails)}")

    # --- Lógica de filtrado para obtener la lista final de EMAILS ---
    if checked:
        # Si seleccionó todos, usamos la lista limpia de la DB
        emails_de_seleccion = emailsAlumnosClean.copy()
    else:
        # FILTRO: Buscamos los emails de los alumnos cuyo 'nombre_completo' esté en la selección
        emails_de_seleccion = df_clean_al[df_clean_al["nombre_completo"].isin(alumnos_seleccionados)]["email_alumno"].unique().tolist()

    # Combinamos ambos y guardamos en session_state
    final_list = list(set(emails_de_seleccion + valid_emails_manual))
    st.session_state.emailsList = final_list
    
    st.write("**Destinatarios seleccionados:**")
    for e in st.session_state.emailsList:
        st.markdown(f"- {e}")

    subject_al = st.text_input("Asunto del email", value="Formaciones", key="subj_al")
    body_al = st.text_area(
        "Cuerpo del email",
        height=200,
        value=bodyEmailsAlumno.replace("{{form_link}}", formUrlAlumno),
        key="body_al"
    )

    email_sender = st.secrets['email']['gmail']
    email_password = st.secrets['email']['password']
    
    adjuntos = st.file_uploader(
            label="Adjuntar archivos (opcional, máximo 10 MB por archivo)",
            accept_multiple_files=True, 
            key="adjuntos_alumnos"
        )
    st.html(
    """
    <style>

    [data-testid='stFileUploader'] [data-testid='stFileUploaderDropzoneInstructions'] > div > span {
    display: none;
    }

    [data-testid='stFileUploader'] [data-testid='stFileUploaderDropzoneInstructions'] > div::before {
    content: 'Arrastre aquí los archivos';
    }

    [data-testid='stFileUploader'] [data-testid='stBaseButton-secondary'] {
    text-indent: -9999px;
    line-height: 0;
    }
    [data-testid='stFileUploader'] [data-testid='stBaseButton-secondary']::after {
    line-height: initial;
    content: "Buscar";
    text-indent: 0;
    }

    [data-testid='stFileUploader'] [data-testid='stFileDropzoneInstructions'] {
    text-indent: -9999px;
    line-height: 0;
    }
    [data-testid='stFileUploader'] [data-testid='stFileDropzoneInstructions']::after {
    line-height: initial;
    content: "Límite 1MB por archivo";
    text-indent: 0;
    }

    </style>
    """
)
    if st.button("📨 Enviar Correo a Alumnos", disabled=not can_send):
        try:
            if send_email(email_sender, email_password, final_list, subject_al, body_al,adjuntos):
                fecha_envio = datetime.now().isoformat()
                for email in final_list:
                    alumno = df_alumnos[df_alumnos["email_alumno"] == email]
                    if not alumno.empty:
                        alumno_id = alumno["dni"].values[0]
                        upsert(
                            alumnoEstadosTabla,
                            {"alumno": alumno_id, "email_enviado": fecha_envio},
                            keys=["alumno"]
                        )
                st.success("Emails enviados correctamente! 🚀")
        except Exception as e:
            error_msg = f"{type(e).__name__}: {str(e)}"
            logError(error_msg,"Alumnos - Envío de Emails")
            st.error(f"Falló el envío de email: {e}. Por favor contacte a antopiscio@gmail.com (soporte técnico).")

