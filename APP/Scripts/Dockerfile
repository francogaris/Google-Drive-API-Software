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
ENV GOOGLE_TOKEN="ya29.a0AcM612w5-W02e5mZ2QyAdp6FIAYNJ5-tV2k08j8yxndIgPRb8ODx8Ns6GmhM0y7ilgnmWYM_3oT8Yi8zmM5XXbhIjmwx411SOQozH1pCAZGTu_3hICjpdhVDiZMq4N4EskfJiP6kEtgyW26vGvzjPOCOMuEXVNUfJa34Y73glQaCgYKAd4SARISFQHGX2MialVhs59BQ81bi723Hsif5w0177"
ENV GOOGLE_CLIENT_ID="369412219539-io7brod70p6o8jes08472l40ua3tmk3p.apps.googleusercontent.com"
ENV GOOGLE_CLIENT_SECRET="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"
ENV GOOGLE_REFRESH_TOKEN="1//0hq_-O7NvnEWxCgYIARAAGBESNwF-L9IrMU_NP_HfO4B7gFRjRNP1GW3MgIGq65xw_lEabwA-vYl9OVNksa5U5l26Txte1Yg2gPg"
ENV DB_SERVER="172.17.0.2"
ENV DB_DATABASE="Challenge_MELI"
ENV DB_USERNAME="sa"
ENV DB_PASSWORD="Meli#1234"
ENV GMAIL_CREDENTIALS_JSON='{"installed":{"client_id":"369412219539-f1sbb8v522kkufb09fm5aav0r070nnn3.apps.googleusercontent.com","project_id":"meli-proyecto","auth_uri":"https://accounts.google.com/o/oauth2/auth","token_uri":"https://oauth2.googleapis.com/token","auth_provider_x509_cert_url":"https://www.googleapis.com/oauth2/v1/certs","client_secret":"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","redirect_uris":["http://localhost"]}}'
ENV GMAIL_TOKEN_JSON='{"token": "ya29.a0AcM612zi1mSJjoxbiMIGmDyjLJKfTj4Ob1gcqoZOnTirRLoYa3EHAsZXZjC36Dq748VJ97ihglCbI-ffCzvscOzKTUvFDVZBgltddqx30U9V6o0VIMy9XgYxOg2sejcEhFH3qGSMkqH_lBAq2fXcDb0YeGv7WMaTVtimcxmGaQaCgYKAYYSARISFQHGX2MiiM5t-NZiB_pkgrOzCr0PWQ0177", "refresh_token": "1//0hMph4u6OTR8ICgYIARAAGBESNwF-L9IrK06WxLcnGFDM7MbSb86HDiH-s0anVkgR0fQIN4OgfBwUUhbcoLkhiMIhpga12gl55rs", "token_uri": "https://oauth2.googleapis.com/token", "client_id": "369412219539-f1sbb8v522kkufb09fm5aav0r070nnn3.apps.googleusercontent.com", "client_secret": "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", "scopes": ["https://www.googleapis.com/auth/gmail.send"], "universe_domain": "googleapis.com", "account": "", "expiry": "2024-08-28T01:49:19.693877Z"}'

# Comando para ejecutar el script principal
CMD ["python", "main.py"]