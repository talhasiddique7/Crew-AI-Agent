"""
Main entry point for CrewAI AI Assistant FastAPI Application
"""

import sys
import os
import uvicorn
from pathlib import Path
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from contextlib import asynccontextmanager
import logging
import time

# Add project root to Python path (current directory since we're in backend)
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from src.routes import academic, health
# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan management."""
    logger.info("Starting FastAPI application...")
    logger.info("FastAPI application started successfully")
    yield
    logger.info("Shutting down FastAPI application...")

# Create FastAPI app
app = FastAPI(
    title="CrewAI AI Assistant API",
    description="REST API for YouTube summarization and academic question answering",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request timing middleware
@app.middleware("http")
async def add_process_time_header(request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response

# Exception handlers
@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "error": exc.detail,
            "status_code": exc.status_code
        }
    )

@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    logger.error(f"Unhandled exception: {str(exc)}")
    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "error": "Internal server error",
            "status_code": 500
        }
    )

# Include routers
app.include_router(health.router, prefix="/api/v1", tags=["Health"])
# app.include_router(youtube.router, prefix="/api/v1", tags=["YouTube"])  # Not available in backend
app.include_router(academic.router, prefix="/api/v1/academic", tags=["Academic"])

# Mount static files for frontend
app.mount("/static", StaticFiles(directory="../frontend"), name="static")

# Root endpoint - serve the homepage dashboard
@app.get("/")
async def root():
    return FileResponse("../frontend/home.html")

# Academic agent endpoint
@app.get("/academic")
async def academic_app():
    return FileResponse("../frontend/academic.html")

# Legacy styles and scripts from frontend
@app.get("/styles.css")
async def styles():
    return FileResponse("../frontend/styles.css")

@app.get("/script.js")
async def script():
    return FileResponse("../frontend/script.js")

# API info endpoint
@app.get("/api")
async def api_info():
    return {
        "message": "CrewAI AI Assistant API",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/api/v1/health"
    }

def main():
    """Main entry point for FastAPI server."""
    # Get configuration from environment
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", "8000"))
    reload = os.getenv("RELOAD", "true").lower() == "true"
    
    print(f"🚀 Starting CrewAI FastAPI server...")
    print(f"📍 Server will be available at: http://{host}:{port}")
    print(f"📚 API Documentation: http://{host}:{port}/docs")
    print(f"🔍 ReDoc Documentation: http://{host}:{port}/redoc")
    print("-" * 50)
    
    uvicorn.run(
        "main:app",
        host=host,
        port=port,
        reload=reload,
        log_level="info"
    )

if __name__ == "__main__":
    main()
