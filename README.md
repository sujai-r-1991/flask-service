# Flask Service with Gunicorn + Uvicorn

A production-ready Flask REST API service that runs on Gunicorn web server with Uvicorn workers for ASGI support.

## Features

- ✅ Flask REST API with multiple endpoints
- ✅ ASGI support via Uvicorn workers
- ✅ Production-ready Gunicorn configuration
- ✅ Docker containerization
- ✅ Environment-based configuration
- ✅ Comprehensive error handling
- ✅ Structured logging
- ✅ Health check endpoints

## Project Structure

```
flask-service/
├── app.py                 # Flask application with API endpoints
├── asgi.py               # ASGI wrapper for Flask
├── gunicorn_config.py    # Gunicorn configuration
├── requirements.txt      # Python dependencies
├── .env.example         # Example environment variables
├── Dockerfile           # Docker configuration
├── .gitignore          # Git ignore rules
└── README.md           # This file
```

## API Endpoints

### 1. Health Check / Welcome
```
GET /
```
Returns a welcome message and service status.

**Example:**
```bash
curl http://localhost:8000/
```

**Response:**
```json
{
  "status": "success",
  "message": "Welcome to Flask Service with Gunicorn + Uvicorn",
  "service": "flask-service",
  "version": "1.0.0"
}
```

### 2. Hello Endpoint
```
GET /api/hello?name=YourName
```
Returns a JSON greeting. The `name` parameter is optional (defaults to "World").

**Example:**
```bash
curl http://localhost:8000/api/hello
curl http://localhost:8000/api/hello?name=John
```

**Response:**
```json
{
  "status": "success",
  "message": "Hello, John!",
  "timestamp": "2026-01-14T12:00:00.000000"
}
```

### 3. Echo Endpoint
```
POST /api/echo
```
Echoes back the JSON payload sent in the request body.

**Example:**
```bash
curl -X POST http://localhost:8000/api/echo \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello", "value": 123}'
```

**Response:**
```json
{
  "status": "success",
  "message": "Echo response",
  "data": {
    "message": "Hello",
    "value": 123
  },
  "timestamp": "2026-01-14T12:00:00.000000"
}
```

### 4. Status Endpoint
```
GET /api/status
```
Returns service status information including uptime.

**Example:**
```bash
curl http://localhost:8000/api/status
```

**Response:**
```json
{
  "status": "success",
  "service": "flask-service",
  "version": "1.0.0",
  "environment": "production",
  "debug": false,
  "uptime_seconds": 3600,
  "timestamp": "2026-01-14T12:00:00.000000"
}
```

## Installation

### Prerequisites
- Python 3.11 or higher
- pip (Python package manager)

### Local Setup

1. **Clone the repository:**
```bash
git clone <your-repository-url>
cd flask-service
```

2. **Create a virtual environment:**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies:**
```bash
pip install -r requirements.txt
```

4. **Set up environment variables:**
```bash
cp .env.example .env
# Edit .env file as needed
```

## Running the Service

### Development Mode (Flask Development Server)

For development and testing:

```bash
python app.py
```

The service will be available at `http://localhost:8000`

### Production Mode (Gunicorn + Uvicorn)

For production deployment:

```bash
gunicorn -c gunicorn_config.py asgi:application
```

This will:
- Start Gunicorn with Uvicorn workers
- Bind to `0.0.0.0:8000`
- Use the configuration from `gunicorn_config.py`
- Run with multiple workers for better performance

### Running with Docker

1. **Build the Docker image:**
```bash
docker build -t flask-service .
```

2. **Run the container:**
```bash
docker run -p 8000:8000 flask-service
```

3. **Run with environment variables:**
```bash
docker run -p 8000:8000 \
  -e FLASK_ENV=production \
  -e WORKERS=4 \
  flask-service
```

## Configuration

### Environment Variables

Configure the service using environment variables (see `.env.example`):

| Variable | Description | Default |
|----------|-------------|---------|
| `FLASK_ENV` | Flask environment (development/production) | `production` |
| `FLASK_DEBUG` | Enable debug mode (True/False) | `False` |
| `PORT` | Server port | `8000` |
| `BIND_ADDRESS` | Server bind address | `0.0.0.0:8000` |
| `WORKERS` | Number of Gunicorn workers | CPU count * 2 + 1 |
| `LOG_LEVEL` | Logging level (debug/info/warning/error) | `info` |

### Gunicorn Configuration

The `gunicorn_config.py` file contains production-ready settings:

- **Worker Class:** `uvicorn.workers.UvicornWorker` (ASGI support)
- **Workers:** Auto-calculated based on CPU cores (or set via `WORKERS` env var)
- **Timeout:** 30 seconds
- **Logging:** Stdout/stderr with structured format
- **Keepalive:** 2 seconds

You can modify these settings in `gunicorn_config.py` or override them via command-line arguments.

## Testing the API

### Using curl

Test all endpoints:

```bash
# Health check
curl http://localhost:8000/

# Hello endpoint
curl http://localhost:8000/api/hello
curl http://localhost:8000/api/hello?name=Alice

# Echo endpoint
curl -X POST http://localhost:8000/api/echo \
  -H "Content-Type: application/json" \
  -d '{"test": "data", "number": 42}'

# Status endpoint
curl http://localhost:8000/api/status
```

### Using Python requests

```python
import requests

# Health check
response = requests.get('http://localhost:8000/')
print(response.json())

# Hello endpoint
response = requests.get('http://localhost:8000/api/hello?name=Bob')
print(response.json())

# Echo endpoint
response = requests.post(
    'http://localhost:8000/api/echo',
    json={'message': 'test', 'value': 123}
)
print(response.json())

# Status endpoint
response = requests.get('http://localhost:8000/api/status')
print(response.json())
```

## Production Deployment Considerations

### 1. Security
- ✅ Run as non-root user (configured in Dockerfile)
- ⚠️ Use HTTPS in production (configure reverse proxy)
- ⚠️ Set strong secret keys if using sessions
- ✅ Keep dependencies updated
- ⚠️ Implement rate limiting for public APIs
- ⚠️ Add authentication/authorization as needed

### 2. Performance
- ✅ Gunicorn with Uvicorn workers for ASGI support
- ✅ Multiple workers for concurrent request handling
- ⚠️ Add caching layer (Redis) if needed
- ⚠️ Use CDN for static assets
- ✅ Configure appropriate timeouts

### 3. Monitoring & Logging
- ✅ Structured logging to stdout/stderr
- ⚠️ Integrate with logging aggregation (ELK, Datadog, etc.)
- ⚠️ Add health check endpoints (already included)
- ⚠️ Monitor application metrics
- ⚠️ Set up alerting for errors

### 4. Scalability
- ✅ Stateless application design
- ✅ Docker containerization
- ⚠️ Deploy behind load balancer
- ⚠️ Use container orchestration (Kubernetes, ECS, etc.)
- ⚠️ Implement horizontal auto-scaling

### 5. Reverse Proxy
Use Nginx or similar as a reverse proxy:

```nginx
server {
    listen 80;
    server_name example.com;

    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

## Development

### Adding New Endpoints

1. Add new route in `app.py`:
```python
@app.route('/api/new-endpoint', methods=['GET'])
def new_endpoint():
    return jsonify({'message': 'New endpoint'})
```

2. Test the endpoint
3. Update this README with endpoint documentation

### Code Style
- Follow PEP 8 guidelines
- Use meaningful variable names
- Add docstrings to functions
- Handle exceptions appropriately

## Troubleshooting

### Port Already in Use
```bash
# Find process using port 8000
lsof -i :8000
# Or on Linux
netstat -tulpn | grep 8000

# Kill the process or use a different port
PORT=8001 python app.py
```

### Import Errors
```bash
# Ensure virtual environment is activated
source venv/bin/activate

# Reinstall dependencies
pip install -r requirements.txt
```

### Docker Issues
```bash
# Remove old containers and images
docker rm -f $(docker ps -aq)
docker rmi flask-service

# Rebuild
docker build -t flask-service .
```

## License

This project is open source and available under the MIT License.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## Support

For issues and questions, please open an issue on GitHub.
