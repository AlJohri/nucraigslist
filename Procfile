web: gunicorn freeandforsale.wsgi --log-file -
worker: celery beat -A freeandforsale -l info
worker: celery worker -A freeandforsale -l info