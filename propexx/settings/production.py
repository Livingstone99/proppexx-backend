import os
import dj_database_url
from .base import *

DEBUG = os.getenv('DEBUG')

DATABASES = {
    'default': dj_database_url.config(
        engine='django.contrib.gis.db.backends.postgis',
        default=os.environ['DATABASE_URL']
    )
}

CELERY_BROKER_URL = os.environ['REDIS_URL'],
CELERY_RESULT_BACKEND = os.environ['REDIS_URL']
CELERY_ACCEPT_CONTENT = ['json', 'pickle']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = 'Africa/Lagos'
CELERY_TASK_TIME_LIMIT = 30 * 60