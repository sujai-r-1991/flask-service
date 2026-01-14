"""
Gunicorn Configuration File
Configure Gunicorn to use Uvicorn workers for ASGI support.
"""
import multiprocessing
import os

# Server socket
bind = os.getenv('BIND_ADDRESS', '0.0.0.0:8000')
backlog = 2048

# Worker processes
workers = int(os.getenv('WORKERS', multiprocessing.cpu_count() * 2 + 1))
worker_class = 'uvicorn.workers.UvicornWorker'
worker_connections = 1000
timeout = 30
keepalive = 2

# Logging
accesslog = '-'  # Log to stdout
errorlog = '-'   # Log to stderr
loglevel = os.getenv('LOG_LEVEL', 'info')
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s"'

# Process naming
proc_name = 'flask-service'

# Server mechanics
daemon = False
pidfile = None
umask = 0o022
user = None
group = None
tmp_upload_dir = None

# SSL (if needed)
# keyfile = None
# certfile = None
