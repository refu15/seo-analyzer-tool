from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .core.config import settings
from .core.database import engine, Base
from .api import sites, analysis
import os

# Suppress gRPC ALTS warnings (harmless when not running on GCP)
os.environ.setdefault('GRPC_VERBOSITY', 'ERROR')
os.environ.setdefault('GLOG_minloglevel', '2')

# Create database tables
Base.metadata.create_all(bind=engine)

# Initialize FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="SEO Analysis Tool - Comprehensive website SEO analyzer with scoring and recommendations"
)

# Configure CORS
import os
import sys

# Force flush output for Railway logs
def log(msg):
    print(msg, flush=True)
    sys.stdout.flush()

log("=" * 80)
log("SEO Analyzer Tool - Starting up")
log("=" * 80)
log(f"Environment variable ALLOWED_ORIGINS = {os.getenv('ALLOWED_ORIGINS', 'NOT SET')}")
log(f"Environment variable GEMINI_API_KEY = {'SET' if os.getenv('GEMINI_API_KEY') else 'NOT SET'}")
log(f"Environment variable DEBUG = {os.getenv('DEBUG', 'NOT SET')}")

allowed_origins = settings.get_allowed_origins()
log(f"Parsed allowed origins: {allowed_origins}")

# If no specific origins are configured, allow all in development
# In production, you should set ALLOWED_ORIGINS environment variable
if not allowed_origins or allowed_origins == ['']:
    allowed_origins = ["*"]
    log("WARNING: Using wildcard CORS. Set ALLOWED_ORIGINS environment variable in production.")

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True if allowed_origins != ["*"] else False,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"],
    allow_headers=["*"],
    expose_headers=["*"],
    max_age=3600,  # Cache preflight requests for 1 hour
)

# Include routers
app.include_router(sites.router, prefix="/api/v1/sites", tags=["Sites"])
app.include_router(analysis.router, prefix="/api/v1/analysis", tags=["Analysis"])


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "SEO Analyzer Tool API",
        "version": settings.APP_VERSION,
        "docs": "/docs"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}


@app.get("/debug/env")
async def debug_env():
    """Debug endpoint to check environment variables (REMOVE IN PRODUCTION)"""
    import os
    return {
        "allowed_origins": settings.get_allowed_origins(),
        "allowed_origins_raw": os.getenv("ALLOWED_ORIGINS", "NOT SET"),
        "has_gemini_key": bool(os.getenv("GEMINI_API_KEY")),
        "has_pagespeed_key": bool(os.getenv("PAGESPEED_API_KEY")),
        "debug_mode": settings.DEBUG,
        "app_version": settings.APP_VERSION,
    }
