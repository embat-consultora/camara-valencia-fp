import streamlit as st
from page_utils import apply_page_config
from navigation import make_sidebar
from modules.drive_helper import upload_to_drive,list_drive_files
from variables import nombres_roles,carpetaDocumentacion,max_file_size,carpetaManuales
from modules.forms_helper import  file_size_bytes
from pathlib import Path
import uuid
# Configuración inicial de página
apply_page_config()
make_sidebar()
st.set_page_config(page_title="Docuentacion y Manuales", page_icon="🚀")

# Estilos CSS personalizados
st.markdown(
    """
    <style>
    .role-card {
        background-color: #F8F9FA;
        border-left: 5px solid #4F46E5;
        padding: 1.25rem;
        border-radius: 8px;
        margin-bottom: 1.5rem;
    }
    .badge-access {
        background-color: #DEF7EC;
        color: #03543F;
        font-weight: 600;
        padding: 0.2rem 0.5rem;
        border-radius: 4px;
        font-size: 0.85rem;
    }
    </style>
""",
    unsafe_allow_html=True,
)

st.title("📚 Centro de Documentación & Permisos por Rol")
st.caption(
    "Consulta las responsabilidades, accesos del sitio web y documentación por tipo de usuario."
)

# ----------------------------------------------------
# ESTRUCTURA DE DATOS DE ROLES Y DOCUMENTACIÓN
# ----------------------------------------------------
datos_roles = {
    "Administrador": {
        "descripcion": "Tiene acceso general y control total sobre la plataforma, configuraciones globales y gestión centralizada de datos.",
        "paginas_acceso": [
            "Panel estratégico",
            "Gestión de FE",
            "Formación en Empresa",
            "Gestión de Empresas",
            "Gestión de Alumnos",
            "Configuración",
        ],
        "recursos": [
            {
                "titulo": "Manual de Administración Global y Configuración",
                "duracion": "15 min lectura",
                "descripcion": "Guía completa para la gestión de usuarios, alta de empresas, parametrización del sistema y paneles estratégicos.",
                "pdf_path": "manual_administrador.pdf",
                "video_url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
            }
        ],
    },
    "Gestor": {
        "descripcion": "Consulta y gestiona las formaciones que tiene asignadas, además de supervisar paneles de control estratégico.",
        "paginas_acceso": [
            "Panel estratégico",
            "Gestión de FE",
            "Formación en Empresa",
        ],
        "recursos": [
            {
                "titulo": "Guía de Gestión de Formaciones Asignadas",
                "duracion": "10 min lectura",
                "descripcion": "Procedimientos para el seguimiento estratégico, validación de asignaciones y gestión de FE.",
                "pdf_path": "manual_gestor.pdf",
                "video_url": None,
            }
        ],
    },
    "Tutor de centro": {
        "descripcion": "Supervisa el seguimiento del alumnado desde el centro educativo dentro de las formaciones en empresa.",
        "paginas_acceso": ["Formación en Empresa"],
        "recursos": [
            {
                "titulo": "Manual para Tutores de Centro Educativo",
                "duracion": "8 min lectura",
                "descripcion": "Cómo realizar la supervisión de alumnos, revisar progresos y comunicarse con los tutores de empresa.",
                "pdf_path": "manual_tutor_centro.pdf",
                "video_url": None,
            }
        ],
    },
    "Empresa": {
        "descripcion": "Consulta la información de su entidad, publica ofertas, administra formaciones vinculadas y gestiona a sus tutores asignados.",
        "paginas_acceso": ["Formación en Empresa", "Mi Empresa"],
        "recursos": [
            {
                "titulo": "Guía de Portal Empresa: Ofertas y Tutores",
                "duracion": "12 min lectura",
                "descripcion": "Instructivo para la gestión del perfil corporativo, publicación de ofertas y alta de tutores de empresa.",
                "pdf_path": "manual_empresa.pdf",
                "video_url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
            }
        ],
    },
    "Tutor en Empresa": {
        "descripcion": "Realiza el seguimiento diario y evaluación práctica de los alumnos que tiene a su cargo.",
        "paginas_acceso": ["Formación en Empresa"],
        "recursos": [
            {
                "titulo": "Manual del Tutor de Empresa: Evaluación y Seguimiento",
                "duracion": "7 min lectura",
                "descripcion": "Paso a paso para registrar actividades, validar asistencias y calificar el desempeño del alumno.",
                "pdf_path": "manual_tutor_empresa.pdf",
                "video_url": None,
            }
        ],
    },
    "Alumno": {
        "descripcion": "Consulta el estado de su formación en la empresa y adjunta la documentación requerida.",
        "paginas_acceso": ["Mi Formación"],
        "recursos": [
            {
                "titulo": "Manual del Alumno: Carga de Documentación y Seguimiento",
                "duracion": "5 min lectura",
                "descripcion": "Tutorial sobre cómo subir anexos, consultar la formación asignada y revisar observaciones.",
                "pdf_path": "manual_alumno.pdf",
                "video_url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
            }
        ],
    },
}

# ----------------------------------------------------
# BLOQUE 1: SELECTOR DE ROL Y DESCRIPCIÓN
# ----------------------------------------------------
rol = st.session_state.get("rol", "admin")

roles_disponibles = list(datos_roles.keys())
rol_usuario = nombres_roles.get(rol, "")
indice_rol = next(
    (
        indice
        for indice, nombre_rol in enumerate(roles_disponibles)
        if nombre_rol.casefold() == rol_usuario.casefold()
    ),
    0,
)
rol_seleccionado = st.selectbox(
    "🎯 Selecciona un Rol para consultar su documentación:",
    roles_disponibles,
    index=indice_rol,
)

info_rol = datos_roles[rol_seleccionado]

st.markdown(
    f"""
    <div class="role-card">
        <h3 style="margin-top:0; color:#1E1B4B;">👤 Rol: {rol_seleccionado}</h3>
        <p style="font-size: 1.05rem; color:#374151;">{info_rol['descripcion']}</p>
    </div>
""",
    unsafe_allow_html=True,
)

# Paginas a las que tiene acceso el rol seleccionado
st.write("**Páginas con acceso permitido para este rol:**")
cols = st.columns(len(info_rol["paginas_acceso"]))
for idx, pag in enumerate(info_rol["paginas_acceso"]):
    with cols[idx]:
        st.markdown(
            f'<span class="badge-access">✓ {pag}</span>', unsafe_allow_html=True
        )

st.divider()

# ----------------------------------------------------
# BLOQUE 2: DOCUMENTACIÓN Y VIDEOS
# ----------------------------------------------------
st.subheader(f"📖 Manuales y Videos para {rol_seleccionado}")

if rol == "admin":
    with st.expander("Configuración documentación"):
        col1, col2 = st.columns([3, 1])
        with col1:
            st.write("Como administrador, puedes entrar a canva y cambiar los documentos")
            st.info("Una vez actualices los documentos, descargalos y subelos en la sección de abajo con el mismo nombre")
        with col2:
            st.link_button('Ir a Canva', 'https://www.canva.com/design/DAHQCSbVGkk/D2kh6ss6dJavaLmAwpeyBw/edit')
        st.divider()
        st.write("📤 Actualizar Documentos Oficiales")

        col_subir1, col_subir2 = st.columns(2)
        with col_subir1:
            st.markdown("**Manual de Seguimiento**") 
            uploaded_files = st.file_uploader(
                "Subir archivos",
                type=["pdf", "doc", "docx"],
                accept_multiple_files=True,
                key=f"up_manual_seguimiento"
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

            if uploaded_files:
                too_big = [f.name for f in uploaded_files if file_size_bytes(f) > max_file_size]
                if too_big:
                    st.error("Archivos demasiado grandes: " + ", ".join(too_big))
                else:
                    if st.button("Subir Archivos", key=f"subir_manual_seguimiento"):
                        with st.spinner("Subiendo archivos..."):
                            for file in uploaded_files:
                                extension = Path(file.name).suffix
                                nuevo_nombre = f"Manual_Seguimiento{extension}"
                                temp = Path("/tmp") / f"{uuid.uuid4()}_{nuevo_nombre}"
                                with open(temp, "wb") as f:
                                    f.write(file.getbuffer())
                                upload_to_drive(str(temp), carpetaDocumentacion, None, nuevo_nombre)
                                st.success(f"Subido: {nuevo_nombre}")

        with col_subir2:
                st.markdown("**Manual de Onboarding**")
                uploaded_files = st.file_uploader(
                    "Subir archivos",
                    type=["pdf", "doc", "docx"],
                    accept_multiple_files=True,
                    key=f"up_manual_onboarding"
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
    
                if uploaded_files:
                    too_big = [f.name for f in uploaded_files if file_size_bytes(f) > max_file_size]
                    if too_big:
                        st.error("Archivos demasiado grandes: " + ", ".join(too_big))
                    else:
                        if st.button("Subir Archivos", key=f"subir_manual_onboarding"):
                            with st.spinner("Subiendo archivos..."):
                                for file in uploaded_files:
                                    extension = Path(file.name).suffix
                                    nuevo_nombre = f"Manual_Onboarding{extension}"
                                    temp = Path("/tmp") / f"{uuid.uuid4()}_{nuevo_nombre}"
                                    with open(temp, "wb") as f:
                                        f.write(file.getbuffer())
                                    upload_to_drive(str(temp), carpetaDocumentacion, None, nuevo_nombre)
                                    st.success(f"Subido: {nuevo_nombre}")
    
    # --- MOSTRAR NAVEGACIÓN A LAS ÚLTIMAS VERSIONES ---
st.subheader("🔗 Enlaces a documentación")              
files, folderId = list_drive_files(carpetaManuales)

if files:
    for f in files:
        fecha = f.get("modifiedTime", "")[:10]
        st.write(f"- [{f['name']}]({f['webViewLink']}) _(última modificación: {fecha})_")
else:
    st.warning("No hay archivos.")


st.write('')
for recurso in info_rol["recursos"]:
    with st.expander(f"📌 {recurso['titulo']}", expanded=True):
        col_desc, col_actions = st.columns([2, 1])

        with col_desc:
            st.write(f"**Descripción:** {recurso['descripcion']}")
            st.caption(f"⏱️ Tiempo estimado: {recurso['duracion']}")

            if recurso.get("video_url"):
                st.markdown("#### 🎬 Video Tutorial")
                st.video(recurso["video_url"])

        with col_actions:
            st.markdown("#### 📥 Documentación")
            st.download_button(
                label="Descargar Manual (PDF)",
                data=b"Contenido de ejemplo del PDF",
                file_name=recurso["pdf_path"],
                mime="application/pdf",
                use_container_width=True,
            )

st.divider()
