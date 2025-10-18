from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from typing import List, Dict, Optional
from pydantic import BaseModel
from datetime import datetime
import threading

from ..core.database import get_db
from ..models.site import Site, Analysis, Keyword, AnalysisProgress
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


class ProgressResponse(BaseModel):
    id: int
    site_id: int
    status: str
    current_step: Optional[str] = None
    progress_percentage: int
    analysis_id: Optional[int] = None
    error_message: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


def run_analysis_in_thread(site_id: int, site_url: str, progress_id: int):
    """Run analysis in a separate thread with progress tracking"""
    from ..core.database import SessionLocal
    db = SessionLocal()

    try:
        print(f"Starting analysis thread for site {site_id}, progress {progress_id}", flush=True)

        # Get progress record
        progress = db.query(AnalysisProgress).filter(AnalysisProgress.id == progress_id).first()
        if not progress:
            print(f"ERROR: Progress record {progress_id} not found!", flush=True)
            return

        print(f"Progress record found, starting analysis...", flush=True)

        # Update status to running
        progress.status = "running"
        progress.current_step = "分析を開始しています..."
        progress.progress_percentage = 0
        db.commit()

        # Set up progress callback
        def update_progress(step: str, percentage: int):
            progress.current_step = step
            progress.progress_percentage = percentage
            db.commit()

        seo_analyzer.set_progress_callback(update_progress)

        # Run SEO analysis
        analysis_result = seo_analyzer.analyze_site(site_url)

        if "error" in analysis_result:
            progress.status = "failed"
            progress.error_message = analysis_result["error"]
            progress.progress_percentage = 0
            db.commit()
            return

        # Get PageSpeed scores
        progress.current_step = "PageSpeed分析を実行中..."
        progress.progress_percentage = 95
        db.commit()

        pagespeed_data = pagespeed_service.get_mobile_and_desktop_scores(site_url)

        # Create analysis record
        site = db.query(Site).filter(Site.id == site_id).first()
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
            has_robots_txt=True,
            has_sitemap=True,
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

        # Update progress to completed
        progress.status = "completed"
        progress.analysis_id = new_analysis.id
        progress.current_step = "分析が完了しました"
        progress.progress_percentage = 100
        progress.completed_at = datetime.utcnow()
        db.commit()

    except Exception as e:
        print(f"Analysis error: {str(e)}", flush=True)
        import traceback
        traceback.print_exc()

        progress = db.query(AnalysisProgress).filter(AnalysisProgress.id == progress_id).first()
        if progress:
            progress.status = "failed"
            progress.error_message = str(e)
            db.commit()
    finally:
        db.close()


@router.post("/{site_id}", response_model=ProgressResponse)
async def run_analysis(
    site_id: int,
    db: Session = Depends(get_db)
):
    """Start SEO analysis on a site (runs in background)"""
    print(f"Analysis requested for site {site_id}", flush=True)

    # Get site
    site = db.query(Site).filter(Site.id == site_id).first()
    if not site:
        print(f"Site {site_id} not found!", flush=True)
        raise HTTPException(status_code=404, detail="Site not found")

    print(f"Site found: {site.url}", flush=True)

    # Create progress record
    progress = AnalysisProgress(
        site_id=site.id,
        status="pending",
        progress_percentage=0,
        steps_completed=[]
    )
    db.add(progress)
    db.commit()
    db.refresh(progress)

    print(f"Progress record created with ID {progress.id}", flush=True)

    # Start analysis in background thread
    thread = threading.Thread(
        target=run_analysis_in_thread,
        args=(site.id, site.url, progress.id)
    )
    thread.daemon = True
    thread.start()

    print(f"Background thread started", flush=True)

    return progress


@router.get("/{site_id}/progress", response_model=ProgressResponse)
async def get_analysis_progress(site_id: int, db: Session = Depends(get_db)):
    """Get the progress of the latest analysis for a site"""

    progress = db.query(AnalysisProgress).filter(
        AnalysisProgress.site_id == site_id
    ).order_by(AnalysisProgress.created_at.desc()).first()

    if not progress:
        raise HTTPException(status_code=404, detail="No analysis in progress")

    return progress


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
