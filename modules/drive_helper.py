import streamlit as st
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.oauth2 import service_account
import mimetypes

def upload_to_drive(file_name, folder_id, folderName, nombre_archivo_drive=None):
    # --- Autenticación ---
    credentials_info = st.secrets.connections.gcs
    credentials = service_account.Credentials.from_service_account_info(credentials_info)
    service = build("drive", "v3", credentials=credentials)

    # --- Verificar carpeta padre ---
    meta = service.files().get(fileId=folder_id, fields="id,mimeType", supportsAllDrives=True).execute()
    if meta.get("mimeType") != "application/vnd.google-apps.folder":
        raise RuntimeError("El ID provisto no es una carpeta.")

    # --- Buscar/Crear subcarpeta (folderName) ---
    query_folder = f"'{folder_id}' in parents and name = '{folderName}' and mimeType = 'application/vnd.google-apps.folder' and trashed = false"
    results_folder = service.files().list(q=query_folder, supportsAllDrives=True, includeItemsFromAllDrives=True).execute()

    if results_folder.get("files"):
        email_folder_id = results_folder["files"][0]["id"]
    else:
        folder_metadata = {"name": folderName, "mimeType": "application/vnd.google-apps.folder", "parents": [folder_id]}
        folder = service.files().create(body=folder_metadata, fields="id", supportsAllDrives=True).execute()
        email_folder_id = folder["id"]

    # --- Lógica de Sobrescritura ---
    nombre_final = nombre_archivo_drive or file_name.split("/")[-1]
    
    # 1. Buscar si el archivo ya existe EN ESA carpeta específica
    query_file = f"'{email_folder_id}' in parents and name = '{nombre_final}' and trashed = false"
    results_file = service.files().list(q=query_file, supportsAllDrives=True, includeItemsFromAllDrives=True).execute()
    
    mime_type, _ = mimetypes.guess_type(file_name)
    media = MediaFileUpload(file_name, mimetype=mime_type, resumable=True)

    if results_file.get("files"):
        # 2. SI EXISTE: Actualizar (Pisamos el archivo)
        file_id = results_file["files"][0]["id"]
        uploaded = service.files().update(
            fileId=file_id,
            media_body=media,
            fields="id, webViewLink",
            supportsAllDrives=True
        ).execute()
    else:
        # 3. NO EXISTE: Crear nuevo
        file_metadata = {"name": nombre_final, "parents": [email_folder_id]}
        uploaded = service.files().create(
            body=file_metadata,
            media_body=media,
            fields="id, webViewLink",
            supportsAllDrives=True
        ).execute()

    return uploaded["id"]


def list_drive_files(folder_name):
    files = []
    folder_id = None
    try:
        credentials_info = st.secrets.connections.gcs
        credentials = service_account.Credentials.from_service_account_info(credentials_info)
        service = build("drive", "v3", credentials=credentials)
        query_folder = (
            f"name = '{folder_name}' and "
            f"mimeType = 'application/vnd.google-apps.folder' and trashed = false"
        )

        folders = service.files().list(
            q=query_folder,
            spaces="drive",
            fields="files(id, name)",
            supportsAllDrives=True,
            includeItemsFromAllDrives=True
        ).execute().get("files", [])

        if not folders:
             return files, folder_id

        folder_id = folders[0]["id"]

        files = service.files().list(
            q=f"'{folder_id}' in parents and trashed = false",
            fields="files(id, name, webViewLink, modifiedTime)",
            orderBy="modifiedTime desc",
            supportsAllDrives=True,
            includeItemsFromAllDrives=True
        ).execute().get("files", [])

    except Exception as e:
        st.error(f"Error al listar los archivos: {e}")
        return []
    return files,folder_id


def create_drive_folder_practica(dni, nombre, apellido, empresa, folder_id):
    credentials_info = st.secrets.connections.gcs
    credentials = service_account.Credentials.from_service_account_info(credentials_info)
    service = build("drive", "v3", credentials=credentials)

    # --- 1. Definir nombres de carpetas ---
    # Carpeta Destino: Practica
    nombre_folder_practica = f"{apellido}_{nombre}_{dni}_practica_{empresa['nombre']}".strip()
    # Carpeta Origen: Legajo Alumno (Asegúrate que coincida con cómo guardaste el CV antes)
    nombre_folder_alumno = f"Alumno - {nombre}_{apellido}_{dni}".strip()
    st.write(nombre_folder_practica)
    try:
        # --- 2. Obtener o Crear Carpeta de la Práctica ---
        q_dest = f"name = '{nombre_folder_practica}' and mimeType = 'application/vnd.google-apps.folder' and trashed = false"
        res_dest = service.files().list(q=q_dest, supportsAllDrives=True, includeItemsFromAllDrives=True).execute().get("files", [])
        
        if res_dest:
            dest_id = res_dest[0]["id"]
        else:
            meta_dest = {
                "name": nombre_folder_practica,
                "mimeType": "application/vnd.google-apps.folder",
                "parents": [folder_id]
            }
            dest_id = service.files().create(body=meta_dest, fields="id", supportsAllDrives=True).execute()["id"]

        # --- 3. Buscar el CV en la carpeta del Alumno ---
        q_orig = f"name = '{nombre_folder_alumno}' and mimeType = 'application/vnd.google-apps.folder' and trashed = false"
        res_orig = service.files().list(q=q_orig, supportsAllDrives=True, includeItemsFromAllDrives=True).execute().get("files", [])

        if res_orig:
            orig_id = res_orig[0]["id"]
            # Buscamos archivos que contengan "CV" en el nombre dentro de esa carpeta
            q_cv = f"'{orig_id}' in parents and name contains 'CV' and trashed = false"
            cv_files = service.files().list(q=q_cv, supportsAllDrives=True, includeItemsFromAllDrives=True).execute().get("files", [])

            if cv_files:
                cv_id = cv_files[0]["id"]
                cv_nombre = cv_files[0]["name"]
                
                # --- 4. Copiar el archivo (Server-side copy) ---
                # Verificamos si ya existe para no duplicar cada vez que corra el script
                q_existe = f"'{dest_id}' in parents and name = 'CV_IMPORTADO_{cv_nombre}' and trashed = false"
                existe = service.files().list(q=q_existe, supportsAllDrives=True).execute().get("files", [])
                
                if not existe:
                    body_copy = {
                        "name": cv_nombre,
                        "parents": [dest_id]
                    }
                    service.files().copy(fileId=cv_id, body=body_copy, supportsAllDrives=True).execute()
        
        return dest_id

    except Exception as e:
        st.error(f"Error en setup_practica_con_cv: {e}")
        return None
    
def delete_drive_file(file_id: str, file_name: str):
    """
    Elimina un archivo de Google Drive por su ID.

    Args:
        file_id (str): ID del archivo en Drive.
        file_name (str): Nombre del archivo (solo para mensajes).
    """
    try:
        credentials_info = st.secrets.connections.gcs
        credentials = service_account.Credentials.from_service_account_info(credentials_info)
        service = build("drive", "v3", credentials=credentials)

        service.files().delete(
            fileId=file_id,
            supportsAllDrives=True
        ).execute()

        st.success(f"✅ Archivo '{file_name}' eliminado correctamente.")
        st.rerun()

    except Exception as e:
        st.error(f"❌ No se pudo eliminar el archivo '{file_name}': {e}")