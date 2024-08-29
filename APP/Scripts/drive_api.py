import os
import os.path
import logging
import json
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SCOPES = ['https://www.googleapis.com/auth/drive']
    
def autenticacion_api():
    """Autentica al usuario y devuelve un servicio de Google Drive."""
    creds = None
    token_path = 'token.json'

    try:
        # Cargar credenciales guardadas
        if os.path.exists(token_path):
            with open(token_path, 'r') as token:
                creds = Credentials.from_authorized_user_info(json.load(token), SCOPES)
            logging.info('Credenciales cargadas desde token.json')

        # Si no hay credenciales válidas, realiza la autenticación
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
                logging.info('Credenciales refrescadas exitosamente')
            else:
                flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
                creds = flow.run_local_server(port=0)
                logging.info('Autenticación completada exitosamente')

            # Guardar las credenciales para futuras ejecuciones
            with open(token_path, 'w') as token:
                token.write(creds.to_json())
                logging.info('Credenciales guardadas en token.json')

        service = build('drive', 'v3', credentials=creds)
        logging.info('Servicio de Google Drive creado exitosamente')
        return service

    except FileNotFoundError as e:
        logging.error('Archivo de credenciales no encontrado: %s', e)
        raise e
    except Exception as e:
        logging.error('Error durante la autenticación: %s', e)
        raise e
    
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