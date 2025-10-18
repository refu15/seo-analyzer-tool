from sqlalchemy import Column, Integer, String, DateTime, Float, Boolean, Text, JSON, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from ..core.database import Base


class Site(Base):
    """Site model - represents a website being analyzed"""
    __tablename__ = "sites"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True)  # Will be used when auth is implemented
    domain = Column(String, unique=True, index=True, nullable=False)
    url = Column(String, nullable=False)
    name = Column(String, nullable=True)

    # Google Search Console integration
    gsc_property_url = Column(String, nullable=True)
    gsc_connected = Column(Boolean, default=False)

    # Latest SEO score
    latest_score = Column(Float, nullable=True)

    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_analyzed_at = Column(DateTime, nullable=True)

    # Relationships
    analyses = relationship("Analysis", back_populates="site", cascade="all, delete-orphan")
    keywords = relationship("Keyword", back_populates="site", cascade="all, delete-orphan")


class Analysis(Base):
    """Analysis model - stores SEO analysis results"""
    __tablename__ = "analyses"

    id = Column(Integer, primary_key=True, index=True)
    site_id = Column(Integer, ForeignKey('sites.id'), index=True, nullable=False)

    # Overall score
    total_score = Column(Float, nullable=False)
    raw_total_score = Column(Float, nullable=True)
    is_capped = Column(Boolean, default=False)

    # Category scores
    technical_score = Column(Float, nullable=False)
    content_score = Column(Float, nullable=False)
    user_experience_score = Column(Float, nullable=False)
    authority_score = Column(Float, nullable=False)

    # Score breakdown (JSON)
    score_breakdown = Column(JSON, nullable=True)

    # PageSpeed metrics
    pagespeed_desktop_score = Column(Float, nullable=True)
    pagespeed_mobile_score = Column(Float, nullable=True)
    largest_contentful_paint = Column(Float, nullable=True)
    first_input_delay = Column(Float, nullable=True)
    cumulative_layout_shift = Column(Float, nullable=True)

    # Technical metrics
    has_ssl = Column(Boolean, default=False)
    has_robots_txt = Column(Boolean, default=False)
    has_sitemap = Column(Boolean, default=False)
    mobile_friendly = Column(Boolean, default=False)

    # Content metrics
    meta_title = Column(String, nullable=True)
    meta_description = Column(Text, nullable=True)
    h1_count = Column(Integer, default=0)
    word_count = Column(Integer, default=0)

    # Detailed results (JSON)
    detailed_results = Column(JSON, nullable=True)

    # LLM-powered deep analysis results (JSON)
    llm_technical_analysis = Column(JSON, nullable=True)
    llm_content_analysis = Column(JSON, nullable=True)
    llm_ux_analysis = Column(JSON, nullable=True)
    llm_authority_analysis = Column(JSON, nullable=True)
    llm_action_plan = Column(JSON, nullable=True)

    # Timestamp
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationship
    site = relationship("Site", back_populates="analyses")


class Keyword(Base):
    """Keyword model - tracks keyword performance"""
    __tablename__ = "keywords"

    id = Column(Integer, primary_key=True, index=True)
    site_id = Column(Integer, ForeignKey('sites.id'), index=True, nullable=False)

    keyword = Column(String, nullable=False, index=True)

    # Search Console metrics
    clicks = Column(Integer, default=0)
    impressions = Column(Integer, default=0)
    ctr = Column(Float, default=0.0)
    position = Column(Float, default=0.0)

    # Tracking
    previous_position = Column(Float, nullable=True)
    position_change = Column(Float, default=0.0)

    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationship
    site = relationship("Site", back_populates="keywords")


class AnalysisProgress(Base):
    """Analysis Progress model - tracks real-time analysis progress"""
    __tablename__ = "analysis_progress"

    id = Column(Integer, primary_key=True, index=True)
    site_id = Column(Integer, ForeignKey('sites.id'), index=True, nullable=False)

    # Progress tracking
    status = Column(String, default="pending")  # pending, running, completed, failed
    current_step = Column(String, nullable=True)
    progress_percentage = Column(Integer, default=0)

    # Steps completed
    steps_completed = Column(JSON, nullable=True)  # List of completed steps
    total_steps = Column(Integer, default=8)

    # Results (when completed)
    analysis_id = Column(Integer, ForeignKey('analyses.id'), nullable=True)

    # Error tracking
    error_message = Column(Text, nullable=True)

    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    completed_at = Column(DateTime, nullable=True)


class Recommendation(Base):
    """Recommendation model - AI-generated improvement suggestions"""
    __tablename__ = "recommendations"

    id = Column(Integer, primary_key=True, index=True)
    site_id = Column(Integer, ForeignKey('sites.id'), index=True, nullable=False)
    analysis_id = Column(Integer, ForeignKey('analyses.id'), index=True, nullable=False)

    title = Column(String, nullable=False)
    description = Column(Text, nullable=False)

    # Priority: high, medium, low
    priority = Column(String, default="medium")

    # Difficulty: easy, moderate, complex
    difficulty = Column(String, default="moderate")

    # Expected impact (score improvement)
    expected_impact = Column(Float, default=0.0)

    # Category
    category = Column(String, nullable=False)  # technical, content, ux, authority

    # Implementation guide
    implementation_guide = Column(Text, nullable=True)
    external_resources = Column(JSON, nullable=True)

    # Status
    is_completed = Column(Boolean, default=False)

    # Timestamp
    created_at = Column(DateTime, default=datetime.utcnow)
