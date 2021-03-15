#!/bin/bash

set -eo pipefail
shopt -s nullglob

# logging functions
docker_log() {
	local type="$1"; shift
	printf '%s [%s] [Entrypoint]: %s\n' "$(date --rfc-3339=seconds)" "$type" "$*"
}

docker_note() {
	docker_log Note "$@"
}

docker_error() {
	docker_log ERROR "$@" >&2
	exit 1
}

# Verify that the minimally required password settings are set for new databases.
docker_verify_minimum_env() {
	if [ ! "$DATABASE_ENGINE" == "sqlite" ]; then
		if [ -z "$DATABASE" -a -z "$DATABASE_USERNAME" -a -z "$DATABASE_PASSWORD" ]; then
			docker_error $'You need to specify DATABASE DATABASE_USERNAME and DATABASE_PASSWORD for non sqlite type connections'
		else
			if [ -z "$DATABASE" ]; then
				docker_error $'You need to specify DATABASE sqlite type connections'
			fi
		fi
	fi
}

## DATABASE
# database engine
export DATABASE_ENGINE="${DATABASE_ENGINE:-sqlite}"
# database
export DATABASE_HOST="${DATABASE_HOST:-127.0.0.1}"
# database name for database connection
export DATABASE="${DATABASE}" # will be used by sqlite as database path
# username for database connection
export DATABASE_USERNAME="${DATABASE_USERNAME}"
# password for database connection
export DATABASE_PASSWORD="${DATABASE_PASSWORD}"

docker_note "Database engine: ${DATABASE_ENGINE}"
docker_note "Database host: ${DATABASE_HOST}"
docker_note "Database: ${DATABASE}"
docker_note "Database username: ${DATABASE_USERNAME}"
docker_note "Database password: ${DATABASE_PASSWORD}"

## GUNICORN
# gunicorn number of worker
export GUNICORN_WORKERS="${GUNICORN_WORKERS:-2}"
# gunicorn timeout
export GUNICORN_TIMEOUT="${GUNICORN_TIMEOUT:-30}"
# gunicorn bind port
export GUNICORN_BIND_PORT="${GUNICORN_BIND_PORT:-8080}"


docker_note "Gunicorn bind port: ${GUNICORN_BIND_PORT}"
docker_note "Gunicorn workers: ${GUNICORN_WORKERS}"
docker_note "Gunicorn timeout: ${GUNICORN_TIMEOUT}"

## APP
# path prefex
export APP_PATH_PREFIX="${APP_PATH_PREFIX:-/}"
# path environment
export APP_ENVIRONMENT="${APP_ENVIRONMENT:-Test}" # Possible options: Test, Staging, Prod

docker_note "API prefix: ${API_PATH_PREFIX}"

## AUTH
# secret key
export AUTH_SECRET_KEY="${AUTH_SECRET_KEY:-my-secret-key}"
# json web token expire limit in minutes
export AUTH_JWT_EXPIRE_LIMIT="${AUTH_JWT_EXPIRE_LIMIT:-30}"

docker_note "Auth secret key: ${AUTH_SECRET_KEY}"
docker_note "Auth jwt expire limit: ${AUTH_JWT_EXPIRE_LIMIT}"

docker_verify_minimum_env

echo "hello world"

exec "$@"
