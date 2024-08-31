import unittest
from unittest.mock import patch, MagicMock
from APP.Scripts.drive_api import autenticacion_api, lista_archivos_drive, es_archivo_publico

class TestDriveAPI(unittest.TestCase):

    @patch('drive_api.build')
    def test_autenticacion_api(self, mock_build):
        mock_service = MagicMock()
        mock_build.return_value = mock_service

        service = autenticacion_api()

        self.assertIsNotNone(service)
        mock_build.assert_called_once_with('drive', 'v3', credentials=unittest.mock.ANY)

    @patch('drive_api.autenticacion_api')
    def test_lista_archivos_drive(self, mock_autenticacion_api):
        # Simula el servicio y la respuesta de la llamada API
        mock_service = MagicMock()
        mock_autenticacion_api.return_value = mock_service

        mock_service.files.return_value.list.return_value.execute.return_value = {
            'files': [
                {'id': '1', 'name': 'Test File', 'mimeType': 'application/vnd.google-apps.document'}
            ]
        }

        # Ahora llama a la función y prueba la salida.
        files = lista_archivos_drive(mock_service)

        self.assertEqual(len(files), 1)
        self.assertEqual(files[0]['name'], 'Test File')

    @patch('drive_api.autenticacion_api')
    def test_es_archivo_publico(self, mock_autenticacion_api):
        # Simula la llamada de permisos dentro de la función
        mock_service = MagicMock()
        mock_autenticacion_api.return_value = mock_service
        mock_permissions = mock_service.permissions.return_value
        mock_permissions.list.return_value.execute.return_value = {
            'permissions': [{'type': 'anyone'}]
        }

        is_public = es_archivo_publico(mock_service, '1')

        self.assertTrue(is_public)
        mock_permissions.list.assert_called_once_with(fileId='1')

if __name__ == '__main__':
    unittest.main()
