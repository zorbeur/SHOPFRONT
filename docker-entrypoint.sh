#!/bin/sh
set -e

echo "=== Exécution des migrations Django ==="
python manage.py makemigrations --noinput
python manage.py migrate --noinput

echo "=== Collecte des fichiers statiques ==="
python manage.py collectstatic --noinput

echo "=== Démarrage de l'application ==="
exec "$@"
