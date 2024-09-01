import os
import unittest
from unittest.mock import patch, MagicMock
import bd_conexion
from bd_conexion import inventario_historico, conectar_db, crear_tablas, guardar_archivo
from datetime import datetime

class TestBDConexion(unittest.TestCase):
    
    @patch('mysql.connector.connect')
    def test_conectar_db(self, mock_connect):
        """Test para la función conectar_db."""
        # Configurar el mock
        mock_connection = MagicMock()
        mock_connect.return_value = mock_connection
        
        # Llamar a la función
        connection = conectar_db()
        
        # Verificar que la función de conexión se ha llamado correctamente
        mock_connect.assert_called_once_with(
            host=os.getenv('DB_HOST'),
            database=os.getenv('DB_DATABASE'),
            user=os.getenv('DB_USERNAME'),
            password=os.getenv('DB_PASSWORD')
        )
        
        # Verificar que la conexión se ha establecido correctamente
        self.assertEqual(connection, mock_connection)
    
    @patch('bd_conexion.mysql.connector.connect')
    def test_crear_tablas(self, mock_connect):
        """Test para la función crear_tablas."""
        mock_connection = MagicMock()
        mock_connect.return_value = mock_connection
        
        # Llamar a la función
        crear_tablas(mock_connection)
        
        # Verificar que se han ejecutado los comandos SQL correctos
        cursor = mock_connection.cursor.return_value
        cursor.execute.assert_any_call('''
            CREATE TABLE IF NOT EXISTS files (
                id INT AUTO_INCREMENT PRIMARY KEY,
                nombre VARCHAR(255),
                extension VARCHAR(255),
                owner VARCHAR(255),
                visibilidad VARCHAR(50),
                ultima_modificacion DATETIME
            )
        ''')
        cursor.execute.assert_any_call('''
            CREATE TABLE IF NOT EXISTS historical_files (
                id INT AUTO_INCREMENT PRIMARY KEY,
                nombre VARCHAR(255),
                extension VARCHAR(255),
                owner VARCHAR(255),
                visibilidad VARCHAR(50),
                ultima_modificacion DATETIME
            )
        ''')
    
    @patch('bd_conexion.mysql.connector.connect')
    def test_guardar_archivo(self, mock_connect):
        """Test para la función guardar_archivo."""
        mock_connection = MagicMock()
        mock_connect.return_value = mock_connection
        
        cursor = mock_connection.cursor.return_value
        
        # Llamar a la función con parámetros de prueba
        guardar_archivo(mock_connection, 'file_name', 'txt', 'owner_name', 'private', '2024-09-01 00:00:00')
        
        # Verificar que se ha ejecutado la consulta correcta
        cursor.execute.assert_called()
        call_args_list = cursor.execute.call_args_list
        
        # Verificar si la consulta de actualización o inserción se ejecuta correctamente
        self.assertTrue(any('UPDATE files' in call[0][0] for call in call_args_list))
        self.assertTrue(any('INSERT INTO files' in call[0][0] for call in call_args_list))
    
    @patch('bd_conexion.mysql.connector.connect')
    def test_inventario_historico(self, mock_connect):
        """Test para la función inventario_historico."""
        mock_connection = MagicMock()
        mock_connect.return_value = mock_connection
        
        cursor = mock_connection.cursor.return_value
        
        # Llamar a la función con parámetros de prueba
        inventario_historico(mock_connection, 'file_name', 'txt', 'owner_name', 'public', '2024-09-01 00:00:00')
        
        # Verificar que se ha ejecutado la consulta de inserción correctamente
        cursor.execute.assert_called_once_with('''
            INSERT INTO historical_files (nombre, extension, owner, visibilidad, ultima_modificacion)
            VALUES (%s, %s, %s, %s, %s)
        ''', ('file_name', 'txt', 'owner_name', 'public', '2024-09-01 00:00:00'))
    
if __name__ == '__main__':
    unittest.main()