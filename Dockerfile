FROM python:3.10-slim

# Empêcher Python d'écrire des fichiers .pyc et forcer l'unbuffered output
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Installation des dépendances système nécessaires (matplotlib, pillow, build tools, dos2unix)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libjpeg-dev \
    zlib1g-dev \
    libfreetype6-dev \
    libpng-dev \
    dos2unix \
    && rm -rf /var/lib/apt/lists/*

# Copie des dépendances et installation
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copie du projet
COPY . /app/

# Nettoyage des fin de lignes Windows (CRLF -> LF) et attribution des droits d'exécution
RUN dos2unix /app/docker-entrypoint.sh && chmod +x /app/docker-entrypoint.sh

EXPOSE 8000

ENTRYPOINT ["/app/docker-entrypoint.sh"]
CMD ["gunicorn", "shopfront.wsgi:application", "--bind", "0.0.0.0:8000"]
