#!/bin/bash
PORT=${PORT:-5000}
CELERY_BROKER_URL=${CELERY_BROKER_URL:-redis://}
CELERY_BACKEND_URL=${CELERY_BACKEND_URL:-redis://}

CELERY_BROKER_URL=$CELERY_BROKER \
                 celery -A {{ cookiecutter.project_slug }}.jobs.runner worker -l debug
