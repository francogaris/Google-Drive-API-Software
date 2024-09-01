import unittest
from unittest.mock import patch, MagicMock
import bd_conexion
from bd_conexion import inventario_historico, conectar_db, crear_tablas, guardar_archivo
from datetime import datetime

class TestBDConexion(unittest.TestCase):

    @patch('bd_conexion.mysql.connector.connect')
    def test_conectar_db(self, mock_connect):
        # Configura el mock para que devuelva una conexión ficticia
        mock_connect.return_value = 'mock_connection'
        
        # Llama a la función conectar_db
        conexion = bd_conexion.conectar_db()
        
        # Verifica que se haya llamado a connect
        mock_connect.assert_called_once()

        # Verifica que el objeto de conexión se haya devuelto
        self.assertEqual(conexion, 'mock_connection')

    @patch('bd_conexion.conectar_db')
    def test_crear_tablas(self, mock_conectar_db):
        # Configuración del mock
        mock_connection = MagicMock()
        mock_conectar_db.return_value = mock_connection
        
        # Ejecutar la función
        bd_conexion.crear_tablas(mock_connection)
        
        # Verificaciones
        mock_connection.cursor.assert_called_once()
        mock_cursor = mock_connection.cursor.return_value
        # Las consultas esperadas
        expected_query_files = '''
            CREATE TABLE IF NOT EXISTS files (
                id INT AUTO_INCREMENT PRIMARY KEY,
                nombre VARCHAR(255),
                extension VARCHAR(255),
                owner VARCHAR(255),
                visibilidad VARCHAR(50),
                ultima_modificacion DATETIME
            )
        '''
        expected_query_historical_files = '''
            CREATE TABLE IF NOT EXISTS historical_files (
                id INT AUTO_INCREMENT PRIMARY KEY,
                nombre VARCHAR(255),
                extension VARCHAR(255),
                owner VARCHAR(255),
                visibilidad VARCHAR(50),
                ultima_modificacion DATETIME
            )
        '''
        # Verificar que las consultas esperadas hayan sido ejecutadas
        mock_cursor.execute.assert_any_call(expected_query_files)
        mock_cursor.execute.assert_any_call(expected_query_historical_files)

    @patch('bd_conexion.pyodbc')
    def test_guardar_archivo(self, mock_pyodbc):
        # Mock de la conexión y el cursor
        mock_connection = MagicMock()
        mock_cursor = mock_connection.cursor.return_value
        
        ultima_modificacion = '2024-08-28T12:34:56.000Z'
        ultima_modificacion_dt = datetime.strptime(ultima_modificacion, '%Y-%m-%dT%H:%M:%S.%fZ')
        
        # Llamar a la función que estamos probando
        bd_conexion.guardar_archivo(mock_connection, 'test_file', 'txt', 'test_owner', 'private', ultima_modificacion)
        
        # Verificar que se haya hecho la consulta SELECT con los placeholders correctos
        mock_cursor.execute.assert_any_call('''
            SELECT id FROM files WHERE nombre = ? AND extension = ?
        ''', ('test_file', 'txt'))
        
        # Verificar que se haya hecho la consulta INSERT o UPDATE con los placeholders correctos
        mock_cursor.execute.assert_any_call('''
            INSERT INTO files (nombre, extension, owner, visibilidad, ultima_modificacion)
            VALUES (?, ?, ?, ?, ?)
        ''', ('test_file', 'txt', 'test_owner', 'private', ultima_modificacion_dt))
    
    @patch('bd_conexion.pyodbc')
    def test_inventario_historico(self, mock_pyodbc):
        # Mock de la conexión y el cursor
        mock_connection = MagicMock()
        mock_cursor = mock_connection.cursor.return_value
        
        ultima_modificacion = '2024-08-28T12:34:56.000Z'
        ultima_modificacion_dt = datetime.strptime(ultima_modificacion, '%Y-%m-%dT%H:%M:%S.%fZ')
        
        # Llamar a la función que estamos probando
        bd_conexion.inventario_historico(mock_connection, 'archivo', 'txt', 'owner', 'public', ultima_modificacion)
        
        # Verificar que el cursor se haya ejecutado con la fecha formateada y como objeto datetime
        mock_cursor.execute.assert_called_once_with('''
            INSERT INTO historical_files (nombre, extension, owner, visibilidad, ultima_modificacion)
            VALUES (?, ?, ?, ?, ?)
        ''', ('archivo', 'txt', 'owner', 'public', ultima_modificacion_dt))


if __name__ == '__main__':
    unittest.main()
