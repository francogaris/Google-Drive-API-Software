# Usa una imagen base de Python
FROM python:3.11

# Establece el directorio de trabajo
WORKDIR /app

# Instala las dependencias del sistema necesarias para pyodbc y el controlador ODBC 17 para SQL Server
RUN apt-get update && \
    apt-get install -y unixodbc unixodbc-dev curl gnupg && \
    curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add - && \
    curl https://packages.microsoft.com/config/debian/10/prod.list > /etc/apt/sources.list.d/mssql-release.list && \
    apt-get update && \
    ACCEPT_EULA=Y apt-get install -y msodbcsql17 && \
    rm -rf /var/lib/apt/lists/*

# Copia los archivos del proyecto al contenedor
COPY . /app

# Copia el archivo requirements.txt y instala las dependencias
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Acepta argumentos de construcción y configúralos como variables de entorno
ARG DB_SERVER
ARG DB_DATABASE
ARG DB_USERNAME
ARG DB_PASSWORD
ARG GMAIL_CREDENTIALS_JSON
ARG GMAIL_TOKEN_JSON
ARG GOOGLE_CLIENT_ID
ARG GOOGLE_CLIENT_SECRET
ARG GOOGLE_REFRESH_TOKEN
ARG GOOGLE_TOKEN

ENV DB_SERVER=$DB_SERVER
ENV DB_DATABASE=$DB_DATABASE
ENV DB_USERNAME=$DB_USERNAME
ENV DB_PASSWORD=$DB_PASSWORD
ENV GMAIL_CREDENTIALS_JSON=$GMAIL_CREDENTIALS_JSON
ENV GMAIL_TOKEN_JSON=$GMAIL_TOKEN_JSON
ENV GOOGLE_CLIENT_ID=$GOOGLE_CLIENT_ID
ENV GOOGLE_CLIENT_SECRET=$GOOGLE_CLIENT_SECRET
ENV GOOGLE_REFRESH_TOKEN=$GOOGLE_REFRESH_TOKEN
ENV GOOGLE_TOKEN=$GOOGLE_TOKEN

# Comando para ejecutar el script principal
CMD ["python", "main.py"]
