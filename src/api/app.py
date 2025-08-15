"""
FastAPI Application Factory

This module creates and configures the FastAPI application.
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.responses import JSONResponse
import logging
import time
from contextlib import asynccontextmanager

from .routes import youtube, academic, health
from .dependencies import get_config
from config.settings import AppConfig

logger = logging.getLogger(__name__)

# Global variables for dependency injection
app_config: AppConfig = None
ai_service = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan management."""
    global app_config, ai_service
    
    # Startup
    logger.info("Starting FastAPI application...")
    app_config = get_config()
    
    # Initialize AI service would go here
    # ai_service = AIService(app_config)
    
    logger.info("FastAPI application started successfully")
    
    yield
    
    # Shutdown
    logger.info("Shutting down FastAPI application...")

def create_app() -> FastAPI:
    """
    Create and configure FastAPI application.
    
    Returns:
        Configured FastAPI application
    """
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
    
    # Trusted host middleware
    app.add_middleware(
        TrustedHostMiddleware,
        allowed_hosts=["*"]  # Configure appropriately for production
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
    app.include_router(youtube.router, prefix="/api/v1", tags=["YouTube"])
    app.include_router(academic.router, prefix="/api/v1", tags=["Academic"])
    
    # Root endpoint
    @app.get("/")
    async def root():
        return {
            "message": "CrewAI AI Assistant API",
            "version": "1.0.0",
            "docs": "/docs",
            "health": "/api/v1/health"
        }
    
    return app
