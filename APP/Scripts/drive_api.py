import os
import logging
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SCOPES = ['https://www.googleapis.com/auth/drive']

def autenticacion_api():
    """Autentica al usuario y devuelve un servicio de Google Drive."""
    creds = None

    try:
        # Cargar credenciales desde variables de entorno
        token = os.getenv("GOOGLE_TOKEN")
        client_id = os.getenv("GOOGLE_CLIENT_ID")
        client_secret = os.getenv("GOOGLE_CLIENT_SECRET")
        refresh_token = os.getenv("GOOGLE_REFRESH_TOKEN")

        logging.info(f"Token: {token}")
        logging.info(f"Client ID: {client_id}")
        logging.info(f"Client Secret: {client_secret}")
        logging.info(f"Refresh Token: {refresh_token}")
        

        if token and client_id and client_secret:
            creds_data = {
                "token": token,
                "client_id": client_id,
                "client_secret": client_secret,
                "refresh_token": refresh_token,
                "scopes": SCOPES,
                "token_uri": "https://oauth2.googleapis.com/token",
            }
            creds = Credentials.from_authorized_user_info(creds_data)

        # Si no hay credenciales válidas, realiza la autenticación con el flujo de autorización
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
                logging.info('Credenciales refrescadas exitosamente')
            else:
                # Usa un método de autenticación adecuado para entornos sin navegador
                logging.error('No se puede autenticar. Revisa las credenciales proporcionadas.')
                raise Exception('No se puede autenticar.')

        service = build('drive', 'v3', credentials=creds)
        logging.info('Servicio de Google Drive creado exitosamente')
        return service

    except Exception as e:
        logging.error('Error durante la autenticación: %s', e)
        raise e

autenticacion_api()

def lista_archivos_drive(service):
    """Lista todos los archivos en la unidad de Google Drive."""
    files = []
    page_token = None

    try:
        while True:
            response = service.files().list(
                q="trashed=false and 'me' in owners",  # Excluir archivos en la papelera y solo listar los que tengo.
                spaces='drive',
                fields="nextPageToken, files(id, name, mimeType, owners, modifiedTime)",
                pageToken=page_token
            ).execute()

            files.extend(response.get('files', []))
            logging.info('Se listaron %d archivos en la página actual', len(response.get('files', [])))

            page_token = response.get('nextPageToken', None)
            if page_token is None:
                logging.info('Todos los archivos han sido listados')
                break

    except HttpError as e:
        logging.error('Error HTTP al listar archivos: %s', e)
        raise e
    except Exception as e:
        logging.error('Error inesperado al listar archivos: %s', e)
        raise e

    return files

def es_archivo_publico(service, file_id):
    """Determina si un archivo es público."""
    try:
        permissions = service.permissions().list(fileId=file_id).execute()
        for permission in permissions.get('permissions', []):
            if permission.get('type') == 'anyone':
                return True
        return False
    except HttpError as e:
        if e.resp.status == 403:
            logging.warning(f"Permisos insuficientes para el archivo {file_id}. Saltando...")
            return False 
        else:
            logging.error('Error al comprobar permisos del archivo: %s', e)
            raise e
