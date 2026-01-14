"""
ASGI Wrapper for Flask Application
Wraps the Flask WSGI app to make it compatible with ASGI servers like Uvicorn.
"""
from asgiref.wsgi import WsgiToAsgi
from app import app

# Wrap the Flask WSGI application as an ASGI application
asgi_app = WsgiToAsgi(app)

# Export for Gunicorn to use
application = asgi_app
