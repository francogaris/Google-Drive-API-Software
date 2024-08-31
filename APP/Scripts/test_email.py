import unittest
from unittest.mock import patch, MagicMock
from servicio_mail import autenticacion_gmail, cambiar_visibilidad_archivo, crear_mensaje, enviar_mail

class TestServicioMail(unittest.TestCase):

    @patch('servicio_mail.build')
    @patch('servicio_mail.Credentials.from_authorized_user_file')
    def test_autenticacion_gmail(self, mock_from_authorized_user_file, mock_build):
        # Simula la función de las credenciales y contrucción
        mock_creds = MagicMock()
        mock_service = MagicMock()
        mock_from_authorized_user_file.return_value = mock_creds
        mock_build.return_value = mock_service

        service = autenticacion_gmail()

        self.assertIsNotNone(service)
        mock_build.assert_called_once_with('gmail', 'v1', credentials=mock_creds)

    @patch('servicio_mail.cambiar_visibilidad_archivo')
    def test_cambiar_visibilidad_archivo(self, mock_cambiar_visibilidad_archivo):
        # Simula los objetos del servicio y permisos
        mock_service = MagicMock()
        mock_permissions = mock_service.permissions.return_value
        mock_permissions.delete.return_value.execute.return_value = None

        cambiar_visibilidad_archivo(mock_service, 'file_id')

        mock_permissions.delete.assert_called_once_with(fileId='file_id', permissionId='anyoneWithLink')
        mock_permissions.delete().execute.assert_called_once()

    def test_crear_mensaje(self):
        destinatario = 'test@example.com'
        asunto = 'Test Subject'
        cuerpo = 'This is a test message.'

        mensaje = crear_mensaje(destinatario, asunto, cuerpo)

        self.assertIn('raw', mensaje)
        self.assertTrue(mensaje['raw'])

    @patch('servicio_mail.enviar_mail')
    def test_enviar_mail(self, mock_enviar_mail):
        # Simula el servicio y la función users.messages().send()
        mock_service = MagicMock()
        mock_send = mock_service.users().messages().send.return_value.execute.return_value = {}

        enviar_mail(mock_service, 'test@example.com', 'test_file')

        mock_service.users().messages().send.assert_called_once()
        mock_service.users().messages().send().execute.assert_called_once()

if __name__ == '__main__':
    unittest.main()
