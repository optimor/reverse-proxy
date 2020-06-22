#!/bin/bash
set -e

# Create media directory
mkdir -p $BACKEND_DIR/data/media
chown -R django:django $BACKEND_DIR/data

# Run migrations if any
su django -pc "$BACKEND_DIR/manage.py migrate --noinput"

# Create superuser if not created before
su django -pc "$BACKEND_DIR/manage.py initadmin"

if [[ "$ENVIRONMENT" = "production" ]]; then
  # Setup and run Nginx
  [[ -e /etc/nginx/nginx.conf ]] && rm /etc/nginx/nginx.conf
  cp $BACKEND_DIR/nginx.conf /etc/nginx/nginx.conf

  [[ -e /etc/nginx/sites-enabled/default ]] && rm /etc/nginx/sites-enabled/default
  cp $BACKEND_DIR/nginx_reverse_proxy /etc/nginx/sites-available/
  ln -sf /etc/nginx/sites-available/nginx_reverse_proxy /etc/nginx/sites-enabled/nginx_reverse_proxy
  service nginx restart

  # Setup and run uwsgi
  mkdir -p /var/log/uwsgi
  chown -R django:django /var/log/uwsgi
  uwsgi --ini $BACKEND_DIR/uwsgi.ini

  # Collect static files
  su django -pc "$BACKEND_DIR/manage.py collectstatic --noinput"
fi

eval "$@"
