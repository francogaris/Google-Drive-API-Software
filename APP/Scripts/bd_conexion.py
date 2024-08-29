import logging
import pyodbc
import os

def conectar_db():
    """Establece la conexión con SQL Server."""
    
    server = os.getenv('DB_SERVER')
    database = os.getenv('DB_DATABASE')
    username = os.getenv('DB_USERNAME')
    password = os.getenv('DB_PASSWORD')
    
    try:
        connection = pyodbc.connect(
            f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};UID={username};PWD={password}')
        logging.info('Conexión a la base de datos establecida exitosamente')
        return connection
    except pyodbc.Error as e:
        logging.error('Error al conectar a la base de datos: %s', e)
        raise e
    
def crear_tablas(connection):
    """Crea las tablas necesarias en la base de datos."""
    try:
        cursor = connection.cursor()
        
        # Crear tabla files
        cursor.execute('''
            IF NOT EXISTS (SELECT * FROM Challenge_MELI.dbo.sysobjects WHERE name='files' AND xtype='U')
            CREATE TABLE files (
                id INT PRIMARY KEY IDENTITY(1,1),
                nombre NVARCHAR(255),
                extension NVARCHAR(255),
                owner NVARCHAR(255),
                visibilidad NVARCHAR(50),
                ultima_modificacion DATETIME
            )
        ''')
        
        # Crear tabla historical_files
        cursor.execute('''
            IF NOT EXISTS (SELECT * FROM Challenge_MELI.dbo.sysobjects WHERE name='historical_files' AND xtype='U')
            CREATE TABLE historical_files (
                id INT PRIMARY KEY IDENTITY(1,1),
                nombre NVARCHAR(255),
                extension NVARCHAR(255),
                owner NVARCHAR(255),
                visibilidad NVARCHAR(50),
                ultima_modificacion DATETIME
            )
        ''')

        connection.commit()
        logging.info('Tablas creadas exitosamente')
    except pyodbc.Error as e:
        logging.error('Error al crear tablas: %s', e)
        raise e
    
def guardar_archivo(connection, nombre, extension, owner, visibilidad, ultima_modificacion):
    """Guarda o actualiza la información de un archivo en la base de datos."""
    try:
        cursor = connection.cursor()

        # Verifica si el archivo ya existe en la tabla files
        cursor.execute('''
            SELECT id FROM files WHERE nombre = ? AND extension = ?
        ''', (nombre, extension))
        
        row = cursor.fetchone()

        if row:
            # Si existe, actualiza su información
            cursor.execute('''
                UPDATE files
                SET owner = ?, visibilidad = ?, ultima_modificacion = ?
                WHERE id = ?
            ''', (owner, visibilidad, ultima_modificacion, row[0]))
            logging.info('Archivo actualizado: %s.%s', nombre, extension)
        else:
            # Si no existe, inserta un nuevo registro
            cursor.execute('''
                INSERT INTO files (nombre, extension, owner, visibilidad, ultima_modificacion)
                VALUES (?, ?, ?, ?, ?)
            ''', (nombre, extension, owner, visibilidad, ultima_modificacion))
            logging.info('Archivo guardado: %s.%s', nombre, extension)
        
        connection.commit()
    except pyodbc.Error as e:
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
                VALUES (?, ?, ?, ?, ?)
            ''', (nombre, extension, owner, visibilidad, ultima_modificacion))
            logging.info('Archivo público añadido al inventario histórico: %s.%s', nombre, extension)
        
        connection.commit()
    except pyodbc.Error as e:
        logging.error('Error al mantener el inventario histórico: %s', e)
        raise e
