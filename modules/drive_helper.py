import streamlit as st
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.oauth2 import service_account
import mimetypes
def upload_to_drive(file_name,folder_id,emailCandidato):
    credentials_info = st.secrets.connections.gcs
    credentials = service_account.Credentials.from_service_account_info(credentials_info)
    service = build("drive", "v3", credentials=credentials)
    meta = service.files().get(
            fileId=folder_id,
            fields="id,name,mimeType,driveId,parents",
            supportsAllDrives=True
        ).execute()
    if meta.get("mimeType") != "application/vnd.google-apps.folder":
        raise RuntimeError("El ID provisto no es una carpeta.")

    mime_type, _ = mimetypes.guess_type(file_name)
    media = MediaFileUpload(file_name, mimetype=mime_type, resumable=True)

    file_metadata = {
        "name": emailCandidato,
        "parents": [folder_id],
    }

    uploaded = service.files().create(
        body=file_metadata,
        media_body=media,
        fields="id,webViewLink,parents,driveId",
        supportsAllDrives=True
    ).execute()

    return uploaded["id"]