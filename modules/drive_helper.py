import streamlit as st
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.oauth2 import service_account
import mimetypes

def upload_to_drive(file_name, folder_id, folderName, nombre_archivo_drive=None):
    """
    Sube un archivo a Google Drive dentro de una subcarpeta (folderName).
    Si la subcarpeta no existe, la crea.
    
    Parámetros:
      file_name (str): ruta local del archivo a subir
      folder_id (str): ID de la carpeta padre en Drive
      folderName (str): nombre de la subcarpeta (por ejemplo, email del alumno)
      nombre_archivo_drive (str): nombre que tendrá el archivo en Drive (opcional)
    """
    # --- Autenticación ---
    credentials_info = st.secrets.connections.gcs
    credentials = service_account.Credentials.from_service_account_info(credentials_info)
    service = build("drive", "v3", credentials=credentials)

    # --- Verificar que folder_id sea una carpeta válida ---
    meta = service.files().get(
        fileId=folder_id,
        fields="id,name,mimeType",
        supportsAllDrives=True
    ).execute()
    if meta.get("mimeType") != "application/vnd.google-apps.folder":
        raise RuntimeError("El ID provisto no es una carpeta.")

    # --- Buscar si ya existe una carpeta con el nombre indicado ---
    query = (
        f"'{folder_id}' in parents and "
        f"name = '{folderName}' and "
        f"mimeType = 'application/vnd.google-apps.folder' and "
        f"trashed = false"
    )

    results = service.files().list(
        q=query,
        spaces="drive",
        fields="files(id, name)",
        supportsAllDrives=True,
        includeItemsFromAllDrives=True
    ).execute()

    if results.get("files"):
        # Ya existe la carpeta
        email_folder_id = results["files"][0]["id"]
    else:
        # Crear nueva carpeta
        folder_metadata = {
            "name": folderName,
            "mimeType": "application/vnd.google-apps.folder",
            "parents": [folder_id]
        }
        folder = service.files().create(
            body=folder_metadata,
            fields="id",
            supportsAllDrives=True
        ).execute()
        email_folder_id = folder["id"]

    # --- Subir el archivo dentro de la carpeta ---
    mime_type, _ = mimetypes.guess_type(file_name)
    media = MediaFileUpload(file_name, mimetype=mime_type, resumable=True)

    # Usar el nombre personalizado si se pasa, o el nombre del archivo local
    nombre_final = nombre_archivo_drive or file_name.split("/")[-1]

    file_metadata = {
        "name": nombre_final,
        "parents": [email_folder_id]
    }

    uploaded = service.files().create(
        body=file_metadata,
        media_body=media,
        fields="id, webViewLink, parents",
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