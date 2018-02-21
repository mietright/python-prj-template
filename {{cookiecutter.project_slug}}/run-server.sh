#!/bin/bash
PORT=${PORT:-5000}
gunicorn {{ cookiecutter.project_slug }}.api.wsgi:app -b :$PORT --timeout 120 -w 4 --reload -c conf/gunicorn.py
