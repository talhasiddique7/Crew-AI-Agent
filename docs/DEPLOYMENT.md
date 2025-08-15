# Deployment Guide

## Local Development

### Quick Start
```bash
# Clone and setup
git clone <repository-url>
cd crew-ai
./scripts/setup.sh

# Run application
./scripts/run_app.sh simple
```

### Manual Setup
```bash
# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
echo "GROQ_API_KEY=your_key_here" > .env

# Run application
streamlit run app_working.py
```

## Production Deployment

### Docker Deployment

#### 1. Create Dockerfile
```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    software-properties-common \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy application code
COPY . .

# Expose port
EXPOSE 8501

# Health check
HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

# Run application
ENTRYPOINT ["streamlit", "run", "app_working.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

#### 2. Build and Run
```bash
# Build image
docker build -t crewai-app .

# Run container
docker run -p 8501:8501 \
  -e GROQ_API_KEY=your_key_here \
  crewai-app
```

### Cloud Deployment

#### Streamlit Cloud
1. Push code to GitHub
2. Connect to [share.streamlit.io](https://share.streamlit.io)
3. Add secrets in Streamlit Cloud dashboard:
   ```
   GROQ_API_KEY = "your_key_here"
   ```

#### Heroku
1. Create `Procfile`:
   ```
   web: streamlit run app_working.py --server.port=$PORT --server.address=0.0.0.0
   ```

2. Deploy:
   ```bash
   heroku create your-app-name
   heroku config:set GROQ_API_KEY=your_key_here
   git push heroku main
   ```

#### Google Cloud Run
1. Create `cloudbuild.yaml`:
   ```yaml
   steps:
   - name: 'gcr.io/cloud-builders/docker'
     args: ['build', '-t', 'gcr.io/$PROJECT_ID/crewai-app', '.']
   - name: 'gcr.io/cloud-builders/docker'
     args: ['push', 'gcr.io/$PROJECT_ID/crewai-app']
   - name: 'gcr.io/cloud-builders/gcloud'
     args: ['run', 'deploy', 'crewai-app', '--image', 'gcr.io/$PROJECT_ID/crewai-app', '--platform', 'managed', '--region', 'us-central1']
   ```

2. Deploy:
   ```bash
   gcloud builds submit --config cloudbuild.yaml
   ```

#### AWS EC2
1. Launch EC2 instance (Ubuntu 20.04+)
2. Install dependencies:
   ```bash
   sudo apt update
   sudo apt install python3-pip nginx
   pip3 install -r requirements.txt
   ```

3. Setup Nginx reverse proxy:
   ```nginx
   server {
       listen 80;
       server_name your-domain.com;

       location / {
           proxy_pass http://localhost:8501;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
       }
   }
   ```

4. Setup systemd service:
   ```ini
   [Unit]
   Description=CrewAI App
   After=network.target

   [Service]
   User=ubuntu
   WorkingDirectory=/home/ubuntu/crew-ai
   Environment=GROQ_API_KEY=your_key_here
   ExecStart=/usr/bin/python3 -m streamlit run app_working.py --server.port=8501
   Restart=always

   [Install]
   WantedBy=multi-user.target
   ```

## Environment Variables

### Required
- `GROQ_API_KEY`: Your Groq API key

### Optional
- `STREAMLIT_SERVER_PORT`: Custom port (default: 8501)
- `STREAMLIT_SERVER_ADDRESS`: Custom address (default: localhost)

## Security Considerations

### API Key Management
- Never commit API keys to version control
- Use environment variables or secret management systems
- Rotate keys regularly

### Network Security
- Use HTTPS in production
- Implement proper firewall rules
- Consider VPN for internal access

### Application Security
- Keep dependencies updated
- Implement rate limiting
- Monitor for unusual usage patterns

## Monitoring and Logging

### Application Logs
```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log'),
        logging.StreamHandler()
    ]
)
```

### Health Checks
- Implement `/health` endpoint
- Monitor API response times
- Track error rates

### Metrics
- User engagement metrics
- API usage statistics
- Performance monitoring

## Scaling Considerations

### Horizontal Scaling
- Use load balancers
- Implement session stickiness if needed
- Consider microservices architecture

### Performance Optimization
- Cache frequent requests
- Implement request queuing
- Use CDN for static assets

### Database Integration
- Add persistent storage for user data
- Implement caching layer (Redis)
- Consider database replicas for read scaling
