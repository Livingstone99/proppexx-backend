web: gunicorn propexx.wsgi  --log-file -
worker: celery -A propexx worker -l info --loglevel=INFO
beat: celery -A propexx beat -l info --pidfile= --loglevel=INFO