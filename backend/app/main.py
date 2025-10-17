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
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.get_allowed_origins(),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
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
