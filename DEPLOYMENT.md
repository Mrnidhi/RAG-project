# 🚀 RAG Production System - Deployment Guide

## 📋 Table of Contents

1. [Prerequisites](#prerequisites)
2. [Environment Setup](#environment-setup)
3. [Docker Deployment](#docker-deployment)
4. [Production Deployment](#production-deployment)
5. [Monitoring & Maintenance](#monitoring--maintenance)
6. [Troubleshooting](#troubleshooting)
7. [Security Considerations](#security-considerations)

## 🔧 Prerequisites

### System Requirements
- **Operating System**: Linux (Ubuntu 20.04+), macOS 10.15+, or Windows 10+
- **Docker**: Version 20.10+ with Docker Compose
- **Memory**: Minimum 4GB RAM (8GB+ recommended)
- **Storage**: Minimum 10GB free space
- **Network**: Internet access for API calls and package downloads

### Required Accounts & API Keys
- **Groq Account**: [Sign up at groq.com](https://groq.com) for LLM API access
- **Qdrant Cloud** (Optional): [Sign up at qdrant.tech](https://qdrant.tech) for managed vector database

## 🌍 Environment Setup

### 1. Clone the Repository
```bash
git clone <your-repository-url>
cd QA-Prod-Project-main/rag-prod
```

### 2. Create Environment File
Create a `.env` file in the project root:
```bash
# =============================================================================
# RAG Production System - Environment Configuration
# =============================================================================

# =============================================================================
# REQUIRED: AI SERVICE API KEYS
# =============================================================================
GROQ_API_KEY=gsk_your_actual_groq_api_key_here
QDRANT_API_KEY=your_qdrant_api_key_here

# =============================================================================
# REQUIRED: SERVICE CONFIGURATION
# =============================================================================
QDRANT_URL=http://qdrant:6333
DJANGO_SETTINGS_MODULE=rag.settings

# =============================================================================
# REQUIRED: DJANGO SECURITY SETTINGS
# =============================================================================
SECRET_KEY=your_very_long_random_secret_key_here
DEBUG=False
ALLOWED_HOSTS=your-domain.com,localhost,127.0.0.1

# =============================================================================
# OPTIONAL: PERFORMANCE TUNING
# =============================================================================
GUNICORN_WORKERS=4
GUNICORN_TIMEOUT=120
PYTHONUNBUFFERED=1
PYTHONDONTWRITEBYTECODE=1

# =============================================================================
# OPTIONAL: DATABASE CONFIGURATION
# =============================================================================
DATABASE_URL=sqlite:///db.sqlite3

# =============================================================================
# OPTIONAL: LOGGING CONFIGURATION
# =============================================================================
LOG_LEVEL=INFO
LOG_FILE=/app/logs/rag_app.log
```

### 3. Generate Secure Secret Key
```bash
# Generate a secure Django secret key
python3 -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

## 🐳 Docker Deployment

### Quick Start (Development)
```bash
# 1. Start all services
docker-compose up -d

# 2. Check service status
docker-compose ps

# 3. View logs
docker-compose logs -f rag-app

# 4. Access the application
# Web App: http://localhost:8000
# Qdrant: http://localhost:6333
```

### Manual Docker Deployment
```bash
# 1. Create Docker network
docker network create rag-network

# 2. Start Qdrant vector database
docker run -d \
  --name qdrant-container \
  --network rag-network \
  -p 6333:6333 \
  -v qdrant_data:/qdrant/storage \
  qdrant/qdrant:latest

# 3. Build RAG application
docker build -t rag-app .

# 4. Run RAG application
docker run -d \
  --name rag-container \
  --network rag-network \
  -p 8000:8000 \
  -e GROQ_API_KEY="your_groq_api_key" \
  -e QDRANT_API_KEY="your_qdrant_api_key" \
  -e QDRANT_URL="http://qdrant-container:6333" \
  rag-app

# 5. Apply database migrations
docker exec rag-container python manage.py migrate
```

## 🚀 Production Deployment

### 1. Production Environment Variables
```bash
# Production .env file
GROQ_API_KEY=gsk_your_production_groq_key
QDRANT_API_KEY=your_production_qdrant_key
QDRANT_URL=https://your-qdrant-instance.com
SECRET_KEY=your_production_secret_key
DEBUG=False
ALLOWED_HOSTS=your-domain.com,www.your-domain.com
```

### 2. Production Docker Compose
```yaml
# docker-compose.prod.yml
version: '3.8'

services:
  qdrant:
    image: qdrant/qdrant:latest
    restart: unless-stopped
    ports:
      - "6333:6333"
    volumes:
      - qdrant_data:/qdrant/storage
    environment:
      - QDRANT__SERVICE__HTTP_PORT=6333
    networks:
      - rag-network

  rag-app:
    build: .
    restart: unless-stopped
    ports:
      - "8000:8000"
    volumes:
      - ./uploads:/app/uploads
      - ./logs:/app/logs
    environment:
      - GROQ_API_KEY=${GROQ_API_KEY}
      - QDRANT_API_KEY=${QDRANT_API_KEY}
      - QDRANT_URL=${QDRANT_URL}
      - SECRET_KEY=${SECRET_KEY}
      - DEBUG=False
      - ALLOWED_HOSTS=${ALLOWED_HOSTS}
    depends_on:
      - qdrant
    networks:
      - rag-network
    command: >
      sh -c "
        python manage.py migrate &&
        python manage.py collectstatic --noinput &&
        gunicorn rag.wsgi:application --config gunicorn.conf.py
      "

volumes:
  qdrant_data:

networks:
  rag-network:
    driver: bridge
```

### 3. Production Deployment Commands
```bash
# Deploy production stack
docker-compose -f docker-compose.prod.yml up -d

# Check deployment status
docker-compose -f docker-compose.prod.yml ps

# View production logs
docker-compose -f docker-compose.prod.yml logs -f rag-app

# Update production deployment
docker-compose -f docker-compose.prod.yml pull
docker-compose -f docker-compose.prod.yml up -d --build
```

## 📊 Monitoring & Maintenance

### 1. Health Checks
```bash
# Check application health
curl -f http://localhost:8000/upload/

# Check Qdrant health
curl -f http://localhost:6333/health

# Check container status
docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"
```

### 2. Log Monitoring
```bash
# View real-time logs
docker-compose logs -f rag-app

# View specific service logs
docker logs -f rag-container

# Check for errors
docker-compose logs rag-app | grep -i error
```

### 3. Performance Monitoring
```bash
# Check resource usage
docker stats

# Monitor disk usage
docker system df

# Check network connectivity
docker network inspect rag-network
```

### 4. Database Maintenance
```bash
# Create database backup
docker exec rag-container python manage.py dumpdata > backup.json

# Restore database
docker exec -i rag-container python manage.py loaddata < backup.json

# Check database status
docker exec rag-container python manage.py dbshell
```

## 🔧 Troubleshooting

### Common Issues & Solutions

#### 1. Application Won't Start
```bash
# Check container logs
docker logs rag-container

# Verify environment variables
docker exec rag-container env | grep GROQ

# Check network connectivity
docker exec rag-container ping qdrant-container
```

#### 2. Qdrant Connection Issues
```bash
# Test Qdrant connectivity
curl -v http://localhost:6333/health

# Check Qdrant logs
docker logs qdrant-container

# Restart Qdrant service
docker restart qdrant-container
```

#### 3. PDF Upload Failures
```bash
# Check file permissions
docker exec rag-container ls -la /app/uploads/

# Verify storage space
docker exec rag-container df -h

# Check Django logs
docker exec rag-container tail -f /app/logs/rag_app.log
```

#### 4. Memory Issues
```bash
# Monitor memory usage
docker stats --no-stream

# Restart containers to free memory
docker-compose restart

# Check for memory leaks
docker exec rag-container ps aux
```

### Debug Mode
```bash
# Enable debug mode temporarily
docker exec rag-container bash -c "echo 'DEBUG=True' >> /app/rag/settings.py"

# Restart application
docker restart rag-container

# Check debug output
docker logs rag-container
```

## 🔒 Security Considerations

### 1. API Key Security
- **Never commit API keys** to version control
- Use environment variables for sensitive data
- Rotate API keys regularly
- Monitor API usage for anomalies

### 2. Network Security
```bash
# Restrict network access
docker network create --internal rag-internal

# Use custom bridge network
docker network create --driver bridge --subnet=172.20.0.0/16 rag-network
```

### 3. File Upload Security
- Validate file types and sizes
- Scan uploaded files for malware
- Implement rate limiting
- Use secure file storage

### 4. Django Security
```python
# settings.py security settings
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
```

## 📈 Scaling & Performance

### 1. Horizontal Scaling
```yaml
# docker-compose.scale.yml
services:
  rag-app:
    deploy:
      replicas: 3
    environment:
      - GUNICORN_WORKERS=2
```

### 2. Load Balancing
```yaml
# Add Nginx load balancer
nginx:
  image: nginx:alpine
  ports:
    - "80:80"
  volumes:
    - ./nginx/nginx.conf:/etc/nginx/nginx.conf:ro
  depends_on:
    - rag-app
```

### 3. Caching
```python
# Add Redis caching
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://redis:6379/1',
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        }
    }
}
```

## 📚 Additional Resources

### Documentation
- [Django Documentation](https://docs.djangoproject.com/)
- [Docker Documentation](https://docs.docker.com/)
- [Qdrant Documentation](https://qdrant.tech/documentation/)
- [Groq API Documentation](https://console.groq.com/docs)

### Support
- **GitHub Issues**: Report bugs and request features
- **Email Support**: [your-email@example.com](mailto:your-email@example.com)
- **Community Forum**: Join our community discussions

---

**Last Updated**: December 2024  
**Version**: 1.0.0  
**Author**: [Your Name]
