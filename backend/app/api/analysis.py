from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from typing import List, Dict, Optional
from pydantic import BaseModel
from datetime import datetime

from ..core.database import get_db
from ..models.site import Site, Analysis, Keyword
from ..services.seo_analyzer import SEOAnalyzer
from ..services.pagespeed_service import PageSpeedService

router = APIRouter()

# Initialize services
seo_analyzer = SEOAnalyzer()
pagespeed_service = PageSpeedService()


# Pydantic schemas
class AnalysisResponse(BaseModel):
    id: int
    site_id: int
    total_score: float
    raw_total_score: Optional[float] = None
    is_capped: Optional[bool] = None
    technical_score: float
    content_score: float
    user_experience_score: float
    authority_score: float
    score_breakdown: Optional[Dict] = None
    pagespeed_mobile_score: Optional[float] = None
    pagespeed_desktop_score: Optional[float] = None
    created_at: datetime

    class Config:
        from_attributes = True


class DetailedAnalysisResponse(BaseModel):
    analysis: AnalysisResponse
    technical_details: Optional[Dict] = None
    content_details: Optional[Dict] = None
    core_web_vitals: Optional[Dict] = None
    recommendations: List[Dict] = []
    # LLM-powered deep insights
    llm_technical_analysis: Optional[Dict] = None
    llm_content_analysis: Optional[Dict] = None
    llm_ux_analysis: Optional[Dict] = None
    llm_authority_analysis: Optional[Dict] = None
    llm_action_plan: Optional[Dict] = None


@router.post("/{site_id}")
async def run_analysis(
    site_id: int,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    """Run SEO analysis on a site"""

    # Get site
    site = db.query(Site).filter(Site.id == site_id).first()
    if not site:
        raise HTTPException(status_code=404, detail="Site not found")

    # Run SEO analysis
    analysis_result = seo_analyzer.analyze_site(site.url)

    if "error" in analysis_result:
        raise HTTPException(status_code=400, detail=analysis_result["error"])

    # Get PageSpeed scores (this can be slow, so could be backgrounded)
    pagespeed_data = pagespeed_service.get_mobile_and_desktop_scores(site.url)

    # Create analysis record
    new_analysis = Analysis(
        site_id=site.id,
        total_score=analysis_result["total_score"],
        raw_total_score=analysis_result.get("raw_total_score"),
        is_capped=analysis_result.get("is_capped", False),
        technical_score=analysis_result["technical_score"],
        content_score=analysis_result["content_score"],
        user_experience_score=analysis_result["user_experience_score"],
        authority_score=analysis_result["authority_score"],
        score_breakdown=analysis_result.get("score_breakdown"),
        pagespeed_mobile_score=pagespeed_data.get("mobile", {}).get("performance_score"),
        pagespeed_desktop_score=pagespeed_data.get("desktop", {}).get("performance_score"),
        largest_contentful_paint=pagespeed_data.get("mobile", {}).get("core_web_vitals", {}).get("largest_contentful_paint"),
        first_input_delay=pagespeed_data.get("mobile", {}).get("core_web_vitals", {}).get("first_input_delay"),
        cumulative_layout_shift=pagespeed_data.get("mobile", {}).get("core_web_vitals", {}).get("cumulative_layout_shift"),
        has_ssl=analysis_result.get("technical_details", {}).get("has_ssl", False),
        has_robots_txt=True,  # Would need to check
        has_sitemap=True,  # Would need to check
        mobile_friendly=analysis_result.get("ux_details", {}).get("mobile_friendly", False),
        meta_title=analysis_result.get("content_details", {}).get("meta_title"),
        meta_description=analysis_result.get("content_details", {}).get("meta_description"),
        h1_count=analysis_result.get("content_details", {}).get("h1_count", 0),
        word_count=analysis_result.get("content_details", {}).get("word_count", 0),
        detailed_results={
            "technical": analysis_result.get("technical_details"),
            "content": analysis_result.get("content_details"),
            "ux": analysis_result.get("ux_details"),
            "pagespeed": pagespeed_data
        },
        # Store LLM analysis results
        llm_technical_analysis=analysis_result.get("llm_technical_analysis"),
        llm_content_analysis=analysis_result.get("llm_content_analysis"),
        llm_ux_analysis=analysis_result.get("llm_ux_analysis"),
        llm_authority_analysis=analysis_result.get("llm_authority_analysis"),
        llm_action_plan=analysis_result.get("llm_action_plan")
    )

    db.add(new_analysis)

    # Update site's latest score and last analyzed time
    site.latest_score = analysis_result["total_score"]
    site.last_analyzed_at = datetime.utcnow()

    db.commit()
    db.refresh(new_analysis)

    return {
        "message": "Analysis completed successfully",
        "analysis_id": new_analysis.id,
        "total_score": new_analysis.total_score
    }


@router.get("/{site_id}/latest", response_model=DetailedAnalysisResponse)
async def get_latest_analysis(site_id: int, db: Session = Depends(get_db)):
    """Get the latest analysis for a site"""

    site = db.query(Site).filter(Site.id == site_id).first()
    if not site:
        raise HTTPException(status_code=404, detail="Site not found")

    # Get latest analysis
    latest_analysis = db.query(Analysis).filter(
        Analysis.site_id == site_id
    ).order_by(Analysis.created_at.desc()).first()

    if not latest_analysis:
        raise HTTPException(status_code=404, detail="No analysis found for this site")

    # Generate recommendations based on scores
    recommendations = generate_recommendations(latest_analysis)

    return DetailedAnalysisResponse(
        analysis=latest_analysis,
        technical_details=latest_analysis.detailed_results.get("technical") if latest_analysis.detailed_results else None,
        content_details=latest_analysis.detailed_results.get("content") if latest_analysis.detailed_results else None,
        core_web_vitals={
            "lcp": latest_analysis.largest_contentful_paint,
            "fid": latest_analysis.first_input_delay,
            "cls": latest_analysis.cumulative_layout_shift
        },
        recommendations=recommendations,
        # Include LLM analysis results
        llm_technical_analysis=latest_analysis.llm_technical_analysis,
        llm_content_analysis=latest_analysis.llm_content_analysis,
        llm_ux_analysis=latest_analysis.llm_ux_analysis,
        llm_authority_analysis=latest_analysis.llm_authority_analysis,
        llm_action_plan=latest_analysis.llm_action_plan
    )


@router.get("/{site_id}/history", response_model=List[AnalysisResponse])
async def get_analysis_history(
    site_id: int,
    limit: int = 10,
    db: Session = Depends(get_db)
):
    """Get analysis history for a site"""

    analyses = db.query(Analysis).filter(
        Analysis.site_id == site_id
    ).order_by(Analysis.created_at.desc()).limit(limit).all()

    return analyses


def generate_recommendations(analysis: Analysis) -> List[Dict]:
    """Generate recommendations based on analysis scores"""
    recommendations = []

    # Technical recommendations
    if analysis.technical_score < 70:
        if not analysis.has_ssl:
            recommendations.append({
                "title": "Enable HTTPS/SSL",
                "description": "Your site is not using HTTPS. This is critical for security and SEO.",
                "priority": "high",
                "difficulty": "moderate",
                "expected_impact": 15,
                "category": "technical"
            })

        if not analysis.has_sitemap:
            recommendations.append({
                "title": "Create XML Sitemap",
                "description": "Add an XML sitemap to help search engines discover and index your pages.",
                "priority": "high",
                "difficulty": "easy",
                "expected_impact": 10,
                "category": "technical"
            })

    # Content recommendations
    if analysis.content_score < 70:
        if not analysis.meta_title or len(analysis.meta_title) < 30:
            recommendations.append({
                "title": "Optimize Meta Title",
                "description": "Your meta title is missing or too short. Aim for 50-60 characters with target keywords.",
                "priority": "high",
                "difficulty": "easy",
                "expected_impact": 12,
                "category": "content"
            })

        if analysis.h1_count != 1:
            recommendations.append({
                "title": "Fix H1 Tag Structure",
                "description": f"Your page has {analysis.h1_count} H1 tags. There should be exactly one H1 per page.",
                "priority": "medium",
                "difficulty": "easy",
                "expected_impact": 8,
                "category": "content"
            })

    # UX recommendations
    if analysis.user_experience_score < 70:
        if not analysis.mobile_friendly:
            recommendations.append({
                "title": "Make Site Mobile-Friendly",
                "description": "Add a responsive viewport meta tag and ensure mobile optimization.",
                "priority": "high",
                "difficulty": "moderate",
                "expected_impact": 15,
                "category": "user_experience"
            })

    # PageSpeed recommendations
    if analysis.pagespeed_mobile_score and analysis.pagespeed_mobile_score < 50:
        if analysis.largest_contentful_paint and analysis.largest_contentful_paint > 2.5:
            recommendations.append({
                "title": "Improve Largest Contentful Paint (LCP)",
                "description": f"Your LCP is {analysis.largest_contentful_paint:.2f}s. Target is under 2.5s. Optimize images and server response time.",
                "priority": "high",
                "difficulty": "moderate",
                "expected_impact": 10,
                "category": "user_experience"
            })

    return recommendations
