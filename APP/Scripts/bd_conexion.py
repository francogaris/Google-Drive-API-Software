import logging
import mysql.connector
import os

def conectar_db():
    """Establece la conexión con MySQL."""
    
    host = os.getenv('DB_HOST')
    database = os.getenv('DB_DATABASE')
    user = os.getenv('DB_USERNAME')
    password = os.getenv('DB_PASSWORD')
    
    try:
        connection = mysql.connector.connect(
            host=host,
            database=database,
            user=user,
            password=password
        )
        logging.info('Conexión a la base de datos establecida exitosamente')
        return connection
    except mysql.connector.Error as e:
        logging.error('Error al conectar a la base de datos: %s', e)
        raise e

def crear_tablas(connection):
    """Crea las tablas necesarias en la base de datos."""
    try:
        cursor = connection.cursor()
        
        # Crear tabla files
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS files (
                id INT AUTO_INCREMENT PRIMARY KEY,
                nombre VARCHAR(255),
                extension VARCHAR(255),
                owner VARCHAR(255),
                visibilidad VARCHAR(50),
                ultima_modificacion DATETIME
            )
        ''')
        
        # Crear tabla historical_files
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS historical_files (
                id INT AUTO_INCREMENT PRIMARY KEY,
                nombre VARCHAR(255),
                extension VARCHAR(255),
                owner VARCHAR(255),
                visibilidad VARCHAR(50),
                ultima_modificacion DATETIME
            )
        ''')

        connection.commit()
        logging.info('Tablas creadas exitosamente')
    except mysql.connector.Error as e:
        logging.error('Error al crear tablas: %s', e)
        raise e

def guardar_archivo(connection, nombre, extension, owner, visibilidad, ultima_modificacion):
    """Guarda o actualiza la información de un archivo en la base de datos."""
    try:
        cursor = connection.cursor()

        # Verifica si el archivo ya existe en la tabla files
        cursor.execute('''
            SELECT id FROM files WHERE nombre = %s AND extension = %s
        ''', (nombre, extension))
        
        row = cursor.fetchone()

        if row:
            # Si existe, actualiza su información
            cursor.execute('''
                UPDATE files
                SET owner = %s, visibilidad = %s, ultima_modificacion = %s
                WHERE id = %s
            ''', (owner, visibilidad, ultima_modificacion, row[0]))
            logging.info('Archivo actualizado: %s.%s', nombre, extension)
        else:
            # Si no existe, inserta un nuevo registro
            cursor.execute('''
                INSERT INTO files (nombre, extension, owner, visibilidad, ultima_modificacion)
                VALUES (%s, %s, %s, %s, %s)
            ''', (nombre, extension, owner, visibilidad, ultima_modificacion))
            logging.info('Archivo guardado: %s.%s', nombre, extension)
        
        connection.commit()
    except mysql.connector.Error as e:
        logging.error('Error al guardar o actualizar archivo: %s', e)
        raise e

def inventario_historico(connection, nombre, extension, owner, visibilidad, ultima_modificacion):
    """Mantiene un inventario histórico de archivos que fueron públicos."""
    try:
        cursor = connection.cursor()
        
        # Inserta el archivo en la tabla historical_files si es público
        if visibilidad == 'public':
            cursor.execute('''
                INSERT INTO historical_files (nombre, extension, owner, visibilidad, ultima_modificacion)
                VALUES (%s, %s, %s, %s, %s)
            ''', (nombre, extension, owner, visibilidad, ultima_modificacion))
            logging.info('Archivo público añadido al inventario histórico: %s.%s', nombre, extension)
        
        connection.commit()
    except mysql.connector.Error as e:
        logging.error('Error al mantener el inventario histórico: %s', e)
        raise e
