#!/usr/bin/env bash

echo "wait db up"

while ! nc -z db_auth_service 3306; do
  sleep 1
done

echo "start migration"
alembic upgrade head
exec "$@"
