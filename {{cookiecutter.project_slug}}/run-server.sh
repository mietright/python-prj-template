#!/bin/bash
PORT=${PORT:-8000}
gunicorn ibanchecker.main:app -b :$PORT --timeout 120 -w 4 --reload -c conf/gunicorn.py
# uvicorn ibanchecker.main:app  --reload
