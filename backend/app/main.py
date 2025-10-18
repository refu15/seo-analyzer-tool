from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .core.config import settings
from .core.database import engine, Base
from .api import sites, analysis

# Create database tables
Base.metadata.create_all(bind=engine)

# Initialize FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="SEO Analysis Tool - Comprehensive website SEO analyzer with scoring and recommendations"
)

# Configure CORS
# Get allowed origins from settings
import os
print(f"DEBUG: Environment variable ALLOWED_ORIGINS = {os.getenv('ALLOWED_ORIGINS')}")  # Debug log

allowed_origins = settings.get_allowed_origins()
print(f"DEBUG: Allowed origins: {allowed_origins}")  # Debug log

# If no specific origins are configured, allow all in development
# In production, you should set ALLOWED_ORIGINS environment variable
if not allowed_origins or allowed_origins == ['']:
    allowed_origins = ["*"]
    print("WARNING: Using wildcard CORS. Set ALLOWED_ORIGINS environment variable in production.")

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
