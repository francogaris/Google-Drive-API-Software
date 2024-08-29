import os
import base64
import logging
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from email.mime.text import MIMEText

SCOPES_GMAIL = ['https://www.googleapis.com/auth/gmail.send']

def autenticacion_gmail():
        
    try:
        creds = None
        token_path = 'token_email.json'

        if os.path.exists(token_path):
            creds = Credentials.from_authorized_user_file(token_path, SCOPES_GMAIL)
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file('credentials_email.json', SCOPES_GMAIL)
                creds = flow.run_local_server(port=0)
            with open(token_path, 'w') as token:
                token.write(creds.to_json())
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