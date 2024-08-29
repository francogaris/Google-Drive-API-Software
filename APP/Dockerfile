# Usar una imagen base de Python
FROM python:3.9-slim

# Configurar el directorio de trabajo
WORKDIR /app

# Copiar los archivos de tu proyecto al contenedor
COPY . /app

# Instalar las dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Configurar el comando por defecto para ejecutar el main.py
CMD ["python", "APP/Scripts/main.py"]
