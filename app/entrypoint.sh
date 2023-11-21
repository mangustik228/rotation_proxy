#!/bin/sh

echo "Waiting for postgres..."
while ! nc -z db_postgres 5432; do
  sleep 1
done
echo "PostgreSQL started"

echo "Waiting for redis..."
while ! nc -z db_redis 6379; do
  sleep 1
done
echo "Redis started"

alembic upgrade head

exec "$@"