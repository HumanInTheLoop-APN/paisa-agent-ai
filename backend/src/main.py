import logging
from contextlib import asynccontextmanager

from dotenv import load_dotenv
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.responses import JSONResponse

# Load environment variables from .env if present
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager"""
    # Startup: Initialize Firebase
    logger.info("Starting Talk to Your Money Backend...")
    try:
        from src.config.firebase_config import initialize_firebase

        initialize_firebase()
        logger.info("✅ Firebase initialized successfully")
    except Exception as e:
        logger.error(f"❌ Failed to initialize Firebase: {e}")
        logger.error("Application will start but Firebase features will not work")

    yield

    # Shutdown: Clean up Firebase
    logger.info("Shutting down Talk to Your Money Backend...")
    try:
        from src.config.firebase_config import cleanup_firebase

        cleanup_firebase()
    except Exception as e:
        logger.warning(f"Error during Firebase cleanup: {e}")


# Create FastAPI app instance
app = FastAPI(
    title="Talk to Your Money Backend",
    version="1.0.0",
    description="Backend API for Talk to Your Money application with agent orchestration",
    lifespan=lifespan,
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Frontend URLs
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add trusted host middleware for security
app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=["localhost", "127.0.0.1", "*.talktoyourmoney.com"],
)


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Global exception handler"""
    logger.error(f"Unhandled exception: {exc}")
    return JSONResponse(status_code=500, content={"detail": "Internal server error"})


@app.get("/")
def read_root():
    """Root endpoint"""
    return {
        "message": "Talk to Your Money Backend is up and running!",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/healthz",
    }


@app.get("/health")
def health_check():
    """Legacy health check endpoint"""
    from src.config.firebase_config import is_initialized

    return {
        "status": "healthy",
        "firebase_initialized": is_initialized(),
        "version": "1.0.0",
    }


from src.config.setup_app import setup_app

setup_app(app)
