"""
Flask Application
A sample Flask REST API service with multiple endpoints.
"""
import os
import logging
from datetime import datetime
from flask import Flask, jsonify, request
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)

# Configuration
app.config['ENV'] = os.getenv('FLASK_ENV', 'production')
app.config['DEBUG'] = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
app.config['JSON_SORT_KEYS'] = False

# Track startup time
STARTUP_TIME = datetime.utcnow()


@app.route('/', methods=['GET'])
def index():
    """
    Welcome/health check endpoint.
    Returns a welcome message and service status.
    """
    logger.info("Health check endpoint called")
    return jsonify({
        'status': 'success',
        'message': 'Welcome to Flask Service with Gunicorn + Uvicorn',
        'service': 'flask-service',
        'version': '1.0.0'
    })


@app.route('/api/hello', methods=['GET'])
def hello():
    """
    Returns a JSON greeting.
    Optionally accepts a 'name' query parameter.
    """
    name = request.args.get('name', 'World')
    logger.info(f"Hello endpoint called with name: {name}")
    
    return jsonify({
        'status': 'success',
        'message': f'Hello, {name}!',
        'timestamp': datetime.utcnow().isoformat()
    })


@app.route('/api/echo', methods=['POST'])
def echo():
    """
    Echoes back the JSON payload sent in the request.
    """
    try:
        data = request.get_json()
        
        if data is None:
            logger.warning("Echo endpoint called without JSON payload")
            return jsonify({
                'status': 'error',
                'message': 'No JSON payload provided'
            }), 400
        
        logger.info(f"Echo endpoint called with data: {data}")
        
        return jsonify({
            'status': 'success',
            'message': 'Echo response',
            'data': data,
            'timestamp': datetime.utcnow().isoformat()
        })
    except Exception as e:
        logger.error(f"Error in echo endpoint: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': 'Invalid JSON payload',
            'error': str(e)
        }), 400


@app.route('/api/status', methods=['GET'])
def status():
    """
    Returns service status information.
    """
    uptime = datetime.utcnow() - STARTUP_TIME
    
    logger.info("Status endpoint called")
    
    return jsonify({
        'status': 'success',
        'service': 'flask-service',
        'version': '1.0.0',
        'environment': app.config['ENV'],
        'debug': app.config['DEBUG'],
        'uptime_seconds': int(uptime.total_seconds()),
        'timestamp': datetime.utcnow().isoformat()
    })


@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors."""
    logger.warning(f"404 error: {request.url}")
    return jsonify({
        'status': 'error',
        'message': 'Resource not found',
        'path': request.path
    }), 404


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors."""
    logger.error(f"500 error: {str(error)}")
    return jsonify({
        'status': 'error',
        'message': 'Internal server error'
    }), 500


@app.errorhandler(Exception)
def handle_exception(error):
    """Handle all uncaught exceptions."""
    logger.error(f"Uncaught exception: {str(error)}", exc_info=True)
    return jsonify({
        'status': 'error',
        'message': 'An unexpected error occurred'
    }), 500


if __name__ == '__main__':
    # Run the Flask development server
    port = int(os.getenv('PORT', 8000))
    app.run(
        host='0.0.0.0',
        port=port,
        debug=app.config['DEBUG']
    )
