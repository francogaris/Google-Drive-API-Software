import os
import base64
import logging
import json
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from email.mime.text import MIMEText

SCOPES_GMAIL = ['https://www.googleapis.com/auth/gmail.send']

def autenticacion_gmail():
    """Autentica al usuario y devuelve un servicio de Gmail."""
    creds = None

    try:
        # Leer credenciales y token de las variables de entorno
        credentials_json = os.getenv('GMAIL_CREDENTIALS_JSON')
        token_json = os.getenv('GMAIL_TOKEN_JSON')

        if token_json:
            creds = Credentials.from_authorized_user_info(json.loads(token_json), SCOPES_GMAIL)

        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                if not credentials_json:
                    raise ValueError("No se proporcionaron credenciales de Gmail")
                creds = InstalledAppFlow.from_client_config(json.loads(credentials_json), SCOPES_GMAIL).run_local_server(port=0)
            # Guardar el token para futuras ejecuciones
            token_json = creds.to_json()
            os.environ['GMAIL_TOKEN_JSON'] = token_json
        logging.info('Servicio de Gmail creado exitosamente')
        return build('gmail', 'v1', credentials=creds)

    except Exception as e:
        logging.error('Error durante la autenticación: %s', e)
        raise e

def cambiar_visibilidad_archivo(service, file_id):
    """Cambia la visibilidad de un archivo a privado."""
    try:
        # Establece los permisos del archivo a privado
        service.permissions().delete(fileId=file_id, permissionId='anyoneWithLink').execute()
        logging.info(f'Visibilidad del archivo {file_id} cambiada a privada')
    except Exception as e:
        logging.error(f'Error al cambiar la visibilidad del archivo: {e}')
        raise e

def crear_mensaje(destinatario, asunto, cuerpo):
    message = MIMEText(cuerpo)
    message['To'] = destinatario
    message['From'] = 'francogaris@gmail.com'
    message['Subject'] = asunto
    # Convierte el mensaje a bytes y luego a una cadena codificada en base64
    raw = base64.urlsafe_b64encode(message.as_bytes()).decode('utf-8')
    raw = raw.replace("=", "")
    return {'raw': raw}

def enviar_mail(service, destinatario, nombre_archivo):
    try:
        mensaje = crear_mensaje(destinatario, "Cambio en la visibilidad de tu archivo", f'Hola. La visibilidad de tu archivo "{nombre_archivo}" ha sido cambiada a privada.')
        send_message = (service.users().messages().send(userId='me', body=mensaje).execute())
        logging.info(f'Correo enviado exitosamente a {destinatario} sobre el archivo {nombre_archivo}')
    except Exception as e:
        logging.error(f'Error al enviar el correo: {e}')
