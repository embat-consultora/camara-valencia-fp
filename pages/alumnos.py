import streamlit as st
import pandas as pd
import os
import json, uuid
from pathlib import Path
from modules.data_base import get, update, upsert, getEquals,getEqual
from page_utils import apply_page_config
from navigation import make_sidebar
from variables import alumnosTabla,max_file_size,tipoPracticas,carpetaAlumnos,estadosAlumno, formFieldsTabla,fasesAlumno,alumnoEstadosTabla,fase2colEmpresa,alumnosTabla, bodyEmailsAlumno, alumnoEstadosTabla, contactoAlumnoTabla
from datetime import datetime
from modules.grafico_helper import mostrar_fases
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

base_url = os.getenv("URL")

# --- Traer alumnos ---
alumnos = get(alumnosTabla)
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
    col1, col2, col3= st.columns([3, 2,2])
    with col1:
        search = st.text_input("Buscar alumnos")
    with col2:
        st.metric("Total alumnos", len(df_alumnos))
    with col3:
        temp_path = Path("/tmp") / f"alumnos_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
        df_alumnos.to_excel(temp_path, index=False)
        with open(temp_path, "rb") as f:
            st.download_button(
                label="⬇️ Descargar alumnos (.xlsx)",
                data=f,
                file_name=temp_path.name,
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
    if search:
        mask = df_alumnos.astype(str).apply(
            lambda row: row.str.contains(search, case=False, na=False).any(),
            axis=1
        )
        df_alumnos = df_alumnos[mask]

    # Vista resumida
    cols_map = {
        "dni": "dni",
        "nombre": "Nombre",
        "apellido": "Apellido",
        "direccion": "Dirección",
        "localidad": "Localidad",
        "telefono": "Teléfono",
        "email_alumno": "Email",
        "vehiculo": "Vehículo",
        "tipoPractica": "Tipo Práctica",
    }
    df_view = df_alumnos[list(cols_map.keys())].rename(columns=cols_map)
    st.dataframe(df_view, hide_index=True, use_container_width=True)

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
            st.subheader(f"Seguimiento - {alumno['nombre']}")
            if not estadosAlumnos:
                mostrar_fases(fasesAlumno, fase2colEmpresa, None)
                estado_actual = {}
            else:
                mostrar_fases(fasesAlumno, fase2colEmpresa, estadosAlumnos[0])
                estado_actual = estadosAlumnos[0]

            # --- Checkboxes dinámicos para cada fase ---
            cols = st.columns(len(fasesAlumno))

            for i, fase in enumerate(fasesAlumno):
                col = fase2colEmpresa[fase]
                valor_actual = True if estado_actual.get(col) else False

                with cols[i]:
                    checked = st.checkbox(fase, value=valor_actual, key=f"{alumno['dni']}_{col}")

                if checked != valor_actual:  # solo si cambió
                    if checked:
                        new_value = datetime.now().isoformat()
                    else:
                        new_value = None

                    upsert(
                        alumnoEstadosTabla,
                        {"alumno": alumno["dni"], col: new_value},
                        keys=["alumno"]
                    )
                    st.success(f"Estado actualizado: {fase} → {new_value if new_value else '❌'}")
                    st.rerun()
            subtab1, subtab2, subtab3 = st.tabs([f"✏️ Detalle: {alumno['nombre']} {alumno['apellido']}",
                                        "📌 Preferencias FP","📂 Documentos"])

            # --- Detalle / edición ---
            with subtab1:
                st.write("Edita los datos y guarda para actualizar:")

                new_nombre = st.text_input("Nombre", alumno.get("nombre", ""))
                new_apellido = st.text_input("Apellido", alumno.get("apellido", ""))
                new_direccion = st.text_input("Dirección", alumno.get("direccion", ""))
                new_codigoPostal = st.text_input("CP", alumno.get("codigo_postal", ""))
                new_localidad = st.text_input("Localidad", alumno.get("localidad", ""))
                new_dni = st.text_input("dni", alumno.get("dni", ""))
                new_nia = st.text_input("NIA", alumno.get("NIA", ""))
                new_telefono = st.text_input("Teléfono", alumno.get("telefono", ""))
                new_email = st.text_input("Email", alumno.get("email_alumno", ""))
                tipo_opts = tipoPracticas
                new_tipo_practica = st.selectbox(
                    "Tipo de Práctica",
                    options=tipo_opts,
                    index=tipo_opts.index(alumno.get("tipoPractica")) if alumno.get("tipoPractica") in tipo_opts else 0
                )
                if st.button("💾 Actualizar alumno"):
                    update(
                        alumnosTabla,
                        {
                            "nombre": new_nombre,
                            "apellido": new_apellido,
                            "direccion": new_direccion,
                            "localidad": new_localidad,
                            "codigo_postal": new_codigoPostal,
                            "dni": new_dni,
                            "NIA": new_nia,
                            "telefono": new_telefono,
                            "email_alumno": new_email,
                            "tipoPractica": new_tipo_practica
                        },
                        "id",
                        alumno_id
                    )
                    st.success("Alumno actualizado correctamente")
                    st.rerun()

            # --- Preferencias FP ---
            with subtab2:
                tipo_practica = alumno.get("tipoPractica") or "N/A"
                vehiculo_val = alumno.get("vehiculo")
                vehiculo_bool = True if vehiculo_val == "Sí" else False
                estado_actual = alumno.get("estado") or "Activo"
                estado_map = {
                    "Activo": "⚪",
                    "Cancelado": "🔴",
                    "En progreso": "🟢",
                    "Finalizado": "🔵"
                }
                icono = estado_map.get(estado_actual, "⚪")
                st.write(f"**Estado actual:** {icono} {estado_actual}")
                st.write(f"**Tipo de Práctica:**  {tipo_practica}")
                # Obtener opciones de form_fields
                form_fields = getEquals(formFieldsTabla, {"category": "Alumno", "type": "Opciones"})
                ciclo_field = next((f for f in form_fields if f["columnName"] == "ciclo_formativo"), None)
                pref_field = next((f for f in form_fields if f["columnName"] == "preferencias_fp"), None)

                ciclos_opts = json.loads(ciclo_field["options"]) if ciclo_field else []
                prefs_opts_dict = json.loads(pref_field["options"]) if pref_field else {}

                current_ciclo = alumno.get("ciclo_formativo") or ""
                current_pref = alumno.get("preferencias_fp") or "[]"

                selected_ciclo = st.selectbox(
                    "Ciclo Formativo",
                    options=[""] + ciclos_opts,  # agrega una opción vacía
                    index=([""] + ciclos_opts).index(current_ciclo) if current_ciclo in ciclos_opts else 0,
                    placeholder="Selecciona un ciclo formativo"
                )

                selected_pref = []
                if selected_ciclo and selected_ciclo in prefs_opts_dict:
                    prefs_options = prefs_opts_dict[selected_ciclo]
                    selected_pref = st.multiselect(
                        f"Preferencia para {selected_ciclo}",
                        options=prefs_options,
                        default=[p for p in current_pref if p in prefs_options],
                        key=f"prefs_multiselect_{alumno['dni']}"
                    )
                else:
                    st.info("Selecciona un ciclo formativo para ver las preferencias disponibles.")


                vehiculo_selected = st.checkbox("Vehículo", value=vehiculo_bool,key=f"vehiculo_pref_{new_email}")
                requisitos = st.text_input("Requisitos adicionales (separados por comas)", value=alumno.get("requisitos") or "")
                if estado_actual in estadosAlumno:
                    default_index = estadosAlumno.index(estado_actual)
                else:
                    default_index = 0

                estado = st.selectbox("Estado", options=estadosAlumno, index=default_index)
                motivo_cancelacion = None
                if estado == "Cancelado":
                    motivo_cancelacion = st.text_area("Motivo de cancelación", value=alumno.get("motivo") or "")

                if st.button("💾 Guardar preferencias"):
                    data_to_update = {
                        "dni": alumno["dni"],
                        "estado": estado,
                        "motivo": motivo_cancelacion,
                        "ciclo_formativo": selected_ciclo,
                        "preferencias_fp": selected_pref,
                        "vehiculo": "Sí" if vehiculo_selected else "No",
                        "requisitos": requisitos
                    }
                    upsert(alumnosTabla, data_to_update, keys=["dni"])
                    st.success("Preferencias actualizadas")
                    st.rerun()

            with subtab3:
                folder_name = f"{alumno['nombre']}_{alumno['apellido']}_{alumno['dni']}".strip()
                files, folderId = list_drive_files(folder_name)

                if not files:
                    st.warning("No hay archivos en la carpeta del alumno.")
                else:
                    if folderId:
                        folder_link = f"https://drive.google.com/drive/folders/{folderId}"
                        st.link_button("🔗 Abrir carpeta en Drive", folder_link)
                    st.write("Archivos encontrados:")
                    for f in files:
                                fecha = f.get("modifiedTime", "")[:10]
                                col1, col2, col3 = st.columns([5, 1, 1])
                                with col1:
                                    st.write(f"- [{f['name']}]({f['webViewLink']}) _(última modificación: {fecha})_")

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
                                    original_name = file.name
                                    tmp_path = Path("/tmp") / f"{uuid.uuid4()}_{original_name}"
                                    with open(tmp_path, "wb") as f:
                                        f.write(file.getbuffer())

                                    res = upload_to_drive(str(tmp_path), carpetaAlumnos, folder_name, original_name)

                                    if isinstance(res, dict):
                                        link = res.get("webViewLink") or res.get("webContentLink")
                                    else:
                                        link = None

                                    st.success(f"✅ {i}/{total}: {original_name} subido correctamente")
                                    if link:
                                        st.markdown(f"[Abrir en Drive]({link})")

                                st.success("🎉 Todos los archivos se subieron correctamente.")
                                st.rerun()

                            except Exception as e:
                                st.error(f"❌ Error al subir los archivos: {e}")

# -------------------------------------------------------------------
# TAB 2: Nuevo Alumno
# -------------------------------------------------------------------
with tab2:
    tabNuevo, tabBulk = st.tabs(["Nuevo Alumno", "Carga Masiva (.csv)"])
    with tabNuevo:
        st.write("➕ Nuevo Alumno")
        
        with st.form("form_nuevo_alumno"):
            new_nombre = st.text_input("Nombre")
            new_apellido = st.text_input("Apellido")
            new_direccion = st.text_input("Dirección")
            new_codigoPostal = st.text_input("CP")
            new_localidad = st.text_input("Localidad")
            new_dni = st.text_input("dni")
            new_nia = st.text_input("NIA")
            new_telefono = st.text_input("Teléfono")
            new_email = st.text_input("Email")
            tipo_opts = tipoPracticas
            new_tipo_practica = st.selectbox(
                "Tipo de Práctica",
                options=tipo_opts,
                index=0
            )

            submitted = st.form_submit_button("Crear Alumno")
            if submitted:
                upsert(
                    alumnosTabla,
                    {
                        "nombre": new_nombre,
                        "apellido": new_apellido,
                        "direccion": new_direccion,
                        "localidad": new_localidad,
                        "dni": new_dni,
                        "NIA": new_nia,
                        "codigo_postal": new_codigoPostal,
                        "telefono": new_telefono,
                        "email_alumno": new_email,
                        "estado": "Activo",
                        "tipoPractica": new_tipo_practica
                    }, keys=["dni"]
                )
                st.success("Nuevo alumno agregado correctamente")
                st.rerun()
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
            "tipoPractica": ["Práctica Autogestionada | Práctica Asignada por el Centro"]
        })

        sample_csv_path = Path("/tmp") / "alumnos_muestra.csv"
        sample_df.to_csv(sample_csv_path, index=False, encoding="utf-8")

        with open(sample_csv_path, "rb") as f:
            st.download_button(
                label="⬇️ Descargar CSV de ejemplo",
                data=f,
                file_name="alumnos_muestra.csv",
                mime="text/csv"
            )

        st.info("Sube un archivo CSV. Solo el DNI es obligatorio. El resto de las columnas son opcionales. Intenta que ninguna fila quede vacia")

        # 2. File uploader
        uploaded_csv = st.file_uploader(
            "Subir archivo CSV (.csv)",
            type=["csv"],
            key="upload_csv_alumnos"
        )

        if uploaded_csv:
            try:
                # Leer TODO como string siempre → adiós floats y NaNs
                df_csv = pd.read_csv(uploaded_csv, dtype=str, encoding="utf-8").fillna("")

                st.write("📄 **Vista previa del archivo cargado:**")
                st.dataframe(df_csv.head(), use_container_width=True)

                # Validar presencia de columna DNI
                if "dni" not in df_csv.columns:
                    st.error("❌ El archivo debe incluir la columna 'dni'.")
                    st.stop()

                if st.button("🚀 Crear alumnos desde CSV"):
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

                        # 3️⃣ Construir payload limpio
                        data = {
                            "dni": dni,
                            "nombre": row.get("nombre", "").strip(),
                            "apellido": row.get("apellido", "").strip(),
                            "direccion": row.get("direccion", "").strip(),
                            "codigo_postal": row.get("codigo_postal", "").strip(),
                            "localidad": row.get("localidad", "").strip(),
                            "NIA": row.get("NIA", "").strip(),
                            "telefono": row.get("telefono", "").strip(),
                            "email_alumno": row.get("email_alumno", "").strip(),
                            "estado": "Activo",
                            "tipoPractica": row.get("tipoPractica", "").strip(),
                        }

                        # 4️⃣ Insert/update
                        try:
                            upsert(alumnosTabla, data, keys=["dni"])
                            creados += 1
                        except Exception as e:
                            errores.append(f"DNI {dni}: {e}")

                    # Resultado del proceso
                    st.success(f"🎉 {creados} alumnos creados o actualizados correctamente.")

                    if errores:
                        st.warning("⚠️ Errores encontrados:")
                        for err in errores:
                            st.write("- " + err)

                    st.rerun()

            except Exception as e:
                st.error(f"❌ Error leyendo el CSV: {e}")

# -------------------------------------------------------------------
# TAB 3: Formulario Alumno
# -------------------------------------------------------------------
formUrlAlumno = os.getenv("FORM_ALUMNO")
can_send = True
with tab3:
    if "emailsList" not in st.session_state:
        st.session_state.emailsList = []
    st.write("🎓 Contactar Alumnos")
    
    if not alumnos:
        st.warning("No hay alumnos registrados")
        st.stop()

    df_alumnos = pd.DataFrame(alumnos)[["id","NIA", "nombre", "email_alumno"]]
    emailsAlumnosClean =df_alumnos["email_alumno"].dropna().unique().tolist()
    
    col1, col2 = st.columns([3, 2])
    with col2:
        checked = st.checkbox("Seleccionar todos", value=False, key="select_all_alumnos")
    with col1:
        emails_alumnos = st.multiselect(
            "Selecciona alumnos (emails)", placeholder="Selecciona un valor",
            options=emailsAlumnosClean,disabled=st.session_state.select_all_alumnos
        )
    emails_manual_alumnos = st.text_area(
        "Agregar emails manualmente (separados por coma)",
        placeholder="ejemplo1@mail.com, ejemplo2@mail.com",
        key="emails_manual_alumnos"
    )
    EMAIL_REGEX = re.compile(r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$")
    valid_emails = []
    invalid_emails = []
    if emails_manual_alumnos.strip():
        # Separar y limpiar
        raw_list = [e.strip() for e in emails_manual_alumnos.split(",") if e.strip()]
        for e in raw_list:
            if EMAIL_REGEX.match(e):
                valid_emails.append(e.lower())
            else:
                invalid_emails.append(e)

        valid_emails = list(dict.fromkeys(valid_emails))

        if invalid_emails:
            can_send = False
            st.warning(f"Puede que falte alguna coma o que tengas correos inválidos: {', '.join(invalid_emails)}")
    
    if checked:
        allEmails = emailsAlumnosClean.copy()
        final_list = list(set(allEmails + valid_emails))
    else:
        final_list = list(set(emails_alumnos + valid_emails))

    st.session_state.emailsList = final_list
    
    st.write("**Destinatarios seleccionados:**")
    for e in st.session_state.emailsList:
        st.markdown(f"- {e}")

    subject_al = st.text_input("Asunto del email", value="Pasantías FP 2025/2026", key="subj_al")
    body_al = st.text_area(
        "Cuerpo del email",
        height=200,
        value=bodyEmailsAlumno.replace("{{form_link}}", formUrlAlumno),
        key="body_al"
    )

    email_sender = st.secrets['email']['gmail']
    email_password = st.secrets['email']['password']

    if st.button("📨 Enviar Emails a Alumnos", disabled=not can_send):
        try:
            if send_email(email_sender, email_password, final_list, subject_al, body_al):
                fecha_envio = datetime.now().isoformat()

                for email in final_list:
                    alumno = df_alumnos[df_alumnos["email_alumno"] == email]

                    if not alumno.empty:
                        alumno_id = alumno["NIA"].values[0]
                        upsert(
                            alumnoEstadosTabla,
                            {"alumno": alumno_id, "email_enviado": fecha_envio},
                            keys=["alumno"]
                        )
                    else:
                        upsert(
                            contactoAlumnoTabla,
                            {"email_alumno": email, "email_enviado": fecha_envio},
                            keys=["email_alumno"]
                        )
                st.success("Emails enviados correctamente! 🚀")
        except Exception as e:
            st.error(f"Falló el envío de mail: {e}")

