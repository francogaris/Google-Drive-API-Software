# Challenge Mercado Libre - Google Drive API

## Descripción

Este proyecto es una aplicación en Python que realizar un inventario de archivos de una unidad de Google Drive en una base de datos MySQL, modifica la visibilidad de los archivos de públicos a privados y notifica al propietario por correo electrónico.

## Ruta del Proyecto: Google-Drive-API-Software
  - .github:
      - workflows
          - main.yml
  - APP:
      - Scripts
          - .gitignore
          - requirements.txt
          - Dockerfile
          - main.py
          - drive_api.py
          - bd_conexion.py
          - servicio_mail.py
          - test_drive_api.py
          - test_bd.py
          - test_email.py
  - Consigna:
      - Challenge MeLi - ES.pdf

## Instalación por Docker

- Tener instalado docker y una cuenta correspondiente
- En un bash ejecutar: docker pull francogaris/challenge_meli:v1.0
- Luego para correrlo, ejecutar: docker run --name challenge_meli_container francogaris/challenge_meli:v1.0

## Instalación por GitHub

Tener en cuenta que para funcione el código se tiene que generar un archivo .env con las credenciales correspondientes para ejecutar el código de manera local

- Ejecutar en un bash: git clone https://github.com/francogaris/Google-Drive-API-Software.git
- Buscar la ruta del proyecto: cd "repositorio"
- Ejecutar el siguiente código para crear un entorno virtual: python -m venv env
- Activamos el entorno virtual
    - Windows: env\Scripts\activate
    - macOS/Linux: source env/bin/activate
- Instalamos las dependencias: pip install -r requirements.txt
- Crear un archivo .env, con las credenciales correspondientes, tiene que contar con los siguientes datos:
  - GOOGLE_TOKEN=tu_token
  - GOOGLE_CLIENT_ID=tu_client_id
  - GOOGLE_CLIENT_SECRET=tu_client_secret
  - GOOGLE_REFRESH_TOKEN=tu_refresh_token
  - GMAIL_CREDENTIALS_JSON=tu_gmail_credentials
  - GMAIL_TOKEN_JSON=tu_gmail_token
- Para correr el proyecto, ejecutar: python main.py (o bien, correrlo desde un IDE)

De esta forma el proyecto va a correr de forma personalizada para cada usuario, los registros se van a guardar en la base de datos cloud de MySQL
