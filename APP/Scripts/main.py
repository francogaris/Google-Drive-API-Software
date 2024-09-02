import logging
from drive_api import autenticacion_api, lista_archivos_drive, es_archivo_publico
from bd_conexion import conectar_db, crear_tablas, guardar_archivo, inventario_historico
from servicio_mail import autenticacion_gmail, cambiar_visibilidad_archivo, crear_mensaje, enviar_mail

# Configuración básica del logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("log.log"),
        logging.StreamHandler()
    ]
)

def main():
    logging.basicConfig(level=logging.INFO)

    try:
        logging.info("Inicio del proceso.")

        # Autenticación e inicialización de los servicios
        service_drive = autenticacion_api()
        service_gmail = autenticacion_gmail()
        connection = conectar_db()

        # Crear tablas si no existen
        crear_tablas(connection)

        # Listar archivos de Google Drive
        archivos = lista_archivos_drive(service_drive)

        for archivo in archivos:
            file_id = archivo['id']
            nombre = archivo['name']
            extension = archivo['mimeType'].split('/')[-1]  # Extraer la extensión del mimeType
            owner = archivo['owners'][0]['emailAddress']
            ultima_modificacion = archivo['modifiedTime']
            
            # Comprobar si el archivo es público
            if es_archivo_publico(service_drive, file_id):
                visibilidad = 'public'
                logging.info(f'Archivo público encontrado: {nombre}.{extension}')

                # Cambiar la visibilidad del archivo a privado
                cambiar_visibilidad_archivo(service_drive, file_id)

                # Enviar notificación por correo al owner
                enviar_mail(service_gmail, owner, nombre)
            else:
                visibilidad = 'private'

            # Guardar o actualizar el archivo en la base de datos
            guardar_archivo(connection, nombre, extension, owner, visibilidad, ultima_modificacion)

            # Mantener un inventario histórico de archivos que fueron públicos
            inventario_historico(connection, nombre, extension, owner, visibilidad, ultima_modificacion)

    except Exception as e:
        logging.error(f'Error en la ejecución principal: {e}')
    
    logging.info("Fin del proceso.")

if __name__ == '__main__':
    main()