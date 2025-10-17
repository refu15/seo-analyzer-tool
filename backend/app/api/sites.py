from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from pydantic import BaseModel, HttpUrl
from datetime import datetime

from ..core.database import get_db
from ..models.site import Site

router = APIRouter()


# Pydantic schemas
class SiteCreate(BaseModel):
    domain: str
    url: HttpUrl
    name: Optional[str] = None


class SiteResponse(BaseModel):
    id: int
    domain: str
    url: str
    name: Optional[str] = None
    latest_score: Optional[float] = None
    created_at: datetime
    last_analyzed_at: Optional[datetime] = None

    class Config:
        from_attributes = True


@router.post("/", response_model=SiteResponse)
async def create_site(site: SiteCreate, db: Session = Depends(get_db)):
    """Register a new site for SEO analysis"""

    # Check if site already exists
    existing_site = db.query(Site).filter(Site.domain == site.domain).first()
    if existing_site:
        raise HTTPException(status_code=400, detail="Site already registered")

    # Create new site
    new_site = Site(
        domain=site.domain,
        url=str(site.url),
        name=site.name or site.domain
    )

    db.add(new_site)
    db.commit()
    db.refresh(new_site)

    return new_site


@router.get("/", response_model=List[SiteResponse])
async def get_sites(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get all registered sites"""
    sites = db.query(Site).offset(skip).limit(limit).all()
    return sites


@router.get("/{site_id}", response_model=SiteResponse)
async def get_site(site_id: int, db: Session = Depends(get_db)):
    """Get a specific site by ID"""
    site = db.query(Site).filter(Site.id == site_id).first()
    if not site:
        raise HTTPException(status_code=404, detail="Site not found")
    return site


@router.delete("/{site_id}")
async def delete_site(site_id: int, db: Session = Depends(get_db)):
    """Delete a site"""
    site = db.query(Site).filter(Site.id == site_id).first()
    if not site:
        raise HTTPException(status_code=404, detail="Site not found")

    db.delete(site)
    db.commit()

    return {"message": "Site deleted successfully"}
