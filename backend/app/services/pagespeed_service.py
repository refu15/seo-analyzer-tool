"""
PageSpeed Insights API Integration
Fetches and analyzes Core Web Vitals and performance metrics
"""

import requests
from typing import Dict, Optional
from ..core.config import settings


class PageSpeedService:
    """Service for interacting with Google PageSpeed Insights API"""

    def __init__(self):
        self.api_url = "https://www.googleapis.com/pagespeedonline/v5/runPagespeed"
        self.api_key = settings.PAGESPEED_API_KEY

    def analyze_url(self, url: str, strategy: str = "mobile") -> Dict:
        """
        Analyze URL using PageSpeed Insights API

        Args:
            url: URL to analyze
            strategy: 'mobile' or 'desktop'

        Returns:
            Dict containing performance metrics
        """
        params = {
            "url": url,
            "strategy": strategy,
            "category": ["performance", "accessibility", "best-practices", "seo"]
        }

        if self.api_key:
            params["key"] = self.api_key

        try:
            response = requests.get(self.api_url, params=params, timeout=30)
            response.raise_for_status()
            data = response.json()

            return self._parse_pagespeed_data(data)

        except requests.exceptions.RequestException as e:
            return {
                "error": f"PageSpeed API request failed: {str(e)}",
                "score": 0
            }

    def _parse_pagespeed_data(self, data: Dict) -> Dict:
        """Parse PageSpeed Insights API response"""
        lighthouse = data.get("lighthouseResult", {})
        categories = lighthouse.get("categories", {})
        audits = lighthouse.get("audits", {})

        # Extract scores
        performance_score = categories.get("performance", {}).get("score", 0) * 100
        accessibility_score = categories.get("accessibility", {}).get("score", 0) * 100
        best_practices_score = categories.get("best-practices", {}).get("score", 0) * 100
        seo_score = categories.get("seo", {}).get("score", 0) * 100

        # Extract Core Web Vitals
        lcp_audit = audits.get("largest-contentful-paint", {})
        fid_audit = audits.get("max-potential-fid", {})
        cls_audit = audits.get("cumulative-layout-shift", {})

        lcp_value = lcp_audit.get("numericValue", 0) / 1000 if lcp_audit.get("numericValue") else None
        fid_value = fid_audit.get("numericValue", 0) if fid_audit.get("numericValue") else None
        cls_value = cls_audit.get("numericValue", 0) if cls_audit.get("numericValue") else None

        # Extract other metrics
        fcp_audit = audits.get("first-contentful-paint", {})
        si_audit = audits.get("speed-index", {})
        tbt_audit = audits.get("total-blocking-time", {})
        tti_audit = audits.get("interactive", {})

        return {
            "performance_score": round(performance_score, 1),
            "accessibility_score": round(accessibility_score, 1),
            "best_practices_score": round(best_practices_score, 1),
            "seo_score": round(seo_score, 1),
            "core_web_vitals": {
                "largest_contentful_paint": round(lcp_value, 2) if lcp_value else None,
                "first_input_delay": round(fid_value, 2) if fid_value else None,
                "cumulative_layout_shift": round(cls_value, 3) if cls_value else None,
            },
            "other_metrics": {
                "first_contentful_paint": fcp_audit.get("displayValue"),
                "speed_index": si_audit.get("displayValue"),
                "total_blocking_time": tbt_audit.get("displayValue"),
                "time_to_interactive": tti_audit.get("displayValue"),
            }
        }

    def get_mobile_and_desktop_scores(self, url: str) -> Dict:
        """Get both mobile and desktop PageSpeed scores"""
        mobile_data = self.analyze_url(url, strategy="mobile")
        desktop_data = self.analyze_url(url, strategy="desktop")

        return {
            "mobile": mobile_data,
            "desktop": desktop_data
        }
