import unittest
from unittest.mock import patch, MagicMock
import bd_conexion
from bd_conexion import inventario_historico, conectar_db, crear_tablas, guardar_archivo

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

    @patch('bd_conexion.conectar_db')
    def test_guardar_archivo(self, mock_conectar_db):
        # Configuración del mock
        mock_connection = MagicMock()
        mock_conectar_db.return_value = mock_connection
        
        # Ejecutar la función
        bd_conexion.guardar_archivo(mock_connection, 'test_file', 'txt', 'test_owner', 'private', '2024-08-28')
        
        # Verificaciones
        mock_connection.cursor.assert_called_once()
        mock_cursor = mock_connection.cursor.return_value
        expected_query = '''
            SELECT id FROM files WHERE nombre = %s AND extension = %s
        '''
        # Verificar que la consulta esperada haya sido ejecutada
        mock_cursor.execute.assert_any_call(expected_query, ('test_file', 'txt'))

    @patch('bd_conexion.mysql.connector.connect')
    def test_inventario_historico(self, mock_connect):
        # Configura el mock de la conexión y el cursor
        mock_connection = MagicMock()
        mock_cursor = MagicMock()
        mock_connect.return_value = mock_connection
        mock_connection.cursor.return_value = mock_cursor

        # Llama a la función con visibilidad 'public'
        inventario_historico(mock_connection, 'archivo', 'txt', 'owner', 'public', '2024-08-28')

        # Verifica que se ejecutó el INSERT
        mock_cursor.execute.assert_called_once_with('''
                INSERT INTO historical_files (nombre, extension, owner, visibilidad, ultima_modificacion)
                VALUES (%s, %s, %s, %s, %s)
            ''', ('archivo', 'txt', 'owner', 'public', '2024-08-28'))

        # Verifica que se hizo commit
        mock_connection.commit.assert_called_once()

if __name__ == '__main__':
    unittest.main()
