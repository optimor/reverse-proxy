#!/bin/bash
set -e

if [[ "$ENVIRONMENT" = "production" ]]; then
  tail -f /var/log/nginx/access.log
else
  su django -c "$BACKEND_DIR/manage.py runserver 0:8000"
fi
