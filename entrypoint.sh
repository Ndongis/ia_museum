#!/bin/bash
set -e

echo "[entrypoint] Démarrage de PostgreSQL..."
service postgresql start

echo "[entrypoint] Attente que PostgreSQL soit prêt..."
until su postgres -c "pg_isready -h localhost -p 5432" > /dev/null 2>&1; do
    sleep 1
done

echo "[entrypoint] Configuration de l'utilisateur et de la base vectordb..."
su postgres -c "psql -c \"ALTER USER postgres WITH PASSWORD '123';\""

DB_EXISTS=$(su postgres -c "psql -tAc \"SELECT 1 FROM pg_database WHERE datname='vectordb'\"")
if [ "$DB_EXISTS" != "1" ]; then
    su postgres -c "createdb vectordb"
    echo "[entrypoint] Base vectordb créée."
else
    echo "[entrypoint] Base vectordb déjà présente."
fi

echo "[entrypoint] Activation de l'extension pgvector..."
su postgres -c "psql -d vectordb -c \"CREATE EXTENSION IF NOT EXISTS vector;\""



echo "[entrypoint] PostgreSQL prêt. Lancement de l'application..."
exec uvicorn runpod.app.main:api --host 0.0.0.0 --port 8000