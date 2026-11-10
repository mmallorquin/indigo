# Imagen de la app web de Indigo.
FROM python:3.12-slim

# Sin archivos .pyc y con logs al instante (se ven en Azure enseguida)
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1

WORKDIR /app

# Primero las dependencias: Docker reutiliza esta capa si no cambian, y el build es más rápido
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Después el código
COPY . .

# No correr como root dentro del contenedor
RUN useradd --create-home indigo
USER indigo

EXPOSE 8080
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080", "--proxy-headers", "--forwarded-allow-ips", "*"]
