#!/bin/bash
# Pterodactyl startup script for PostgreSQL
set -e

# Start PostgreSQL
exec docker-entrypoint.sh postgres
