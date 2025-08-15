# 🚀 FastAPI Integration Guide

## Overview
The CrewAI AI Assistant now includes a robust FastAPI backend alongside the Streamlit frontend, providing REST API endpoints for programmatic access.

## 🏗️ Architecture

```
├── 📁 src/api/                      # FastAPI application
│   ├── app.py                       # FastAPI app factory
│   ├── dependencies/                # Dependency injection
│   └── routes/                      # API route handlers
│       ├── health.py               # Health check endpoints
│       ├── youtube.py              # YouTube analysis endpoints
│       └── academic.py             # Academic Q&A endpoints
├── api_server.py                   # FastAPI server entry point
├── launcher.py                     # Unified launcher (UI + API)
└── main.py                         # Default Streamlit launcher
```

## 🚀 Quick Start

### Launch Options

1. **Streamlit UI only** (default):
   ```bash
   python main.py
   # or
   python launcher.py streamlit
   ```

2. **FastAPI server only**:
   ```bash
   python launcher.py fastapi
   # or
   python api_server.py
   ```

3. **Both UI and API**:
   ```bash
   python launcher.py both
   ```

### Default URLs
- **Streamlit UI**: http://localhost:8501
- **FastAPI Server**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs
- **Alternative Docs**: http://localhost:8000/redoc

## 📡 API Endpoints

### Health & Status
```http
GET /api/v1/health                  # Basic health check
GET /api/v1/health/detailed         # Detailed health with service status
GET /api/v1/status                  # Current service status
```

### YouTube Analysis
```http
POST /api/v1/youtube/analyze        # Analyze YouTube video
POST /api/v1/youtube/analyze-text   # Analyze custom text content
GET  /api/v1/youtube/video-info/{id} # Get video metadata
```

### Academic Questions
```http
POST /api/v1/academic/ask           # Ask academic question
GET  /api/v1/academic/subjects      # Get supported subjects
GET  /api/v1/academic/subjects/details # Get subject details
POST /api/v1/academic/batch-questions  # Batch question processing
```

## 📝 Usage Examples

### YouTube Analysis
```python
import requests

# Analyze YouTube video
response = requests.post("http://localhost:8000/api/v1/youtube/analyze", 
    json={
        "video_url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
    }
)
result = response.json()
print(result["summary"])
```

### Academic Question
```python
import requests

# Ask academic question
response = requests.post("http://localhost:8000/api/v1/academic/ask",
    json={
        "question": "Explain photosynthesis",
        "subject_area": "Biology"
    }
)
answer = response.json()
print(answer["answer"])
```

### Text Analysis
```python
import requests

# Analyze custom text
response = requests.post("http://localhost:8000/api/v1/youtube/analyze-text",
    json={
        "content": "Your text content here...",
        "title": "My Custom Content"
    }
)
summary = response.json()
print(summary["summary"])
```

## 🔧 Configuration

### Environment Variables
```bash
# Server configuration
HOST=0.0.0.0
PORT=8000
RELOAD=true

# Application settings
GROQ_API_KEY=your_api_key_here
```

### Custom Ports
```bash
# Launch with custom ports
python launcher.py both --port-streamlit 8502 --port-fastapi 8001
```

## 🐳 Docker Support

### Build and Run
```bash
# Build Docker image
docker build -f docker/Dockerfile -t crewai-app .

# Run with Docker Compose
cd docker
docker-compose up
```

### Multi-service Setup
The Docker Compose configuration runs both Streamlit and FastAPI services:
- Streamlit UI: http://localhost:8501
- FastAPI Server: http://localhost:8000

## 📊 Response Models

### YouTube Analysis Response
```json
{
  "success": true,
  "video_id": "dQw4w9WgXcQ",
  "video_url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
  "summary": "Comprehensive video analysis...",
  "transcript_length": 1250,
  "error": null
}
```

### Academic Question Response
```json
{
  "success": true,
  "question": "Explain photosynthesis",
  "subject_area": "Biology",
  "answer": "Photosynthesis is the process...",
  "question_length": 21,
  "answer_length": 500,
  "error": null
}
```

## 🔒 Security Features

- **CORS Protection**: Configurable CORS middleware
- **Request Validation**: Pydantic model validation
- **Error Handling**: Comprehensive exception handling
- **Health Checks**: Built-in health monitoring
- **Rate Limiting**: Ready for rate limiting implementation

## 📈 Performance Features

- **Async Support**: Fully asynchronous FastAPI endpoints
- **Request Timing**: Automatic request duration tracking
- **Dependency Injection**: Efficient service initialization
- **Connection Pooling**: Optimized AI service connections

## 🧪 Testing

### API Testing with curl
```bash
# Health check
curl http://localhost:8000/api/v1/health

# YouTube analysis
curl -X POST http://localhost:8000/api/v1/youtube/analyze \
  -H "Content-Type: application/json" \
  -d '{"video_url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ"}'

# Academic question
curl -X POST http://localhost:8000/api/v1/academic/ask \
  -H "Content-Type: application/json" \
  -d '{"question": "What is machine learning?", "subject_area": "Computer Science"}'
```

## 🔮 Future Enhancements

- **Authentication**: JWT-based authentication system
- **Rate Limiting**: Request rate limiting per user/API key
- **Caching**: Redis-based response caching
- **Websockets**: Real-time streaming responses
- **Database**: Persistent storage for analytics
- **Monitoring**: Prometheus metrics and logging

## 🤝 Integration

The FastAPI backend seamlessly integrates with:
- **Streamlit Frontend**: Shared business logic
- **CrewAI Framework**: Same agent and task system
- **Groq AI**: Unified LLM integration
- **Configuration**: Shared settings and environment

This dual-interface approach provides maximum flexibility for both interactive users (Streamlit) and programmatic access (FastAPI).
