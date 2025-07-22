#!/usr/bin/env bash

echo "Start migration"
alembic upgrade head
exec "$@"
