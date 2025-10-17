"""
Google Search Console API Integration
Fetches keyword performance data and search analytics
"""

from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import json


class GoogleSearchConsoleService:
    """Service for interacting with Google Search Console API"""

    def __init__(self, credentials_json: Optional[str] = None):
        """
        Initialize GSC service

        Args:
            credentials_json: JSON string of OAuth credentials
        """
        self.credentials = None
        if credentials_json:
            creds_dict = json.loads(credentials_json)
            self.credentials = Credentials.from_authorized_user_info(creds_dict)

    def get_search_analytics(
        self,
        site_url: str,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        dimensions: List[str] = None
    ) -> Dict:
        """
        Fetch search analytics data from GSC

        Args:
            site_url: Site URL registered in GSC
            start_date: Start date (YYYY-MM-DD)
            end_date: End date (YYYY-MM-DD)
            dimensions: List of dimensions (query, page, country, device, etc.)

        Returns:
            Dict containing search analytics data
        """
        if not self.credentials:
            return {
                "error": "No credentials provided",
                "rows": []
            }

        # Default date range: last 30 days
        if not end_date:
            end_date = datetime.now().strftime("%Y-%m-%d")
        if not start_date:
            start_date = (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d")

        if not dimensions:
            dimensions = ["query"]

        try:
            service = build('searchconsole', 'v1', credentials=self.credentials)

            request = {
                'startDate': start_date,
                'endDate': end_date,
                'dimensions': dimensions,
                'rowLimit': 1000
            }

            response = service.searchanalytics().query(
                siteUrl=site_url,
                body=request
            ).execute()

            return self._parse_analytics_data(response)

        except Exception as e:
            return {
                "error": f"GSC API request failed: {str(e)}",
                "rows": []
            }

    def _parse_analytics_data(self, response: Dict) -> Dict:
        """Parse GSC analytics response"""
        rows = response.get("rows", [])

        keywords = []
        total_clicks = 0
        total_impressions = 0

        for row in rows:
            keys = row.get("keys", [])
            clicks = row.get("clicks", 0)
            impressions = row.get("impressions", 0)
            ctr = row.get("ctr", 0)
            position = row.get("position", 0)

            keyword = keys[0] if keys else "Unknown"

            keywords.append({
                "keyword": keyword,
                "clicks": clicks,
                "impressions": impressions,
                "ctr": round(ctr * 100, 2),
                "position": round(position, 1)
            })

            total_clicks += clicks
            total_impressions += impressions

        return {
            "keywords": keywords,
            "total_clicks": total_clicks,
            "total_impressions": total_impressions,
            "average_ctr": round((total_clicks / total_impressions * 100), 2) if total_impressions > 0 else 0,
            "keyword_count": len(keywords)
        }

    def get_top_keywords(self, site_url: str, limit: int = 10) -> List[Dict]:
        """Get top performing keywords"""
        data = self.get_search_analytics(site_url)

        if "error" in data:
            return []

        keywords = data.get("keywords", [])
        # Sort by clicks
        sorted_keywords = sorted(keywords, key=lambda x: x["clicks"], reverse=True)

        return sorted_keywords[:limit]

    def get_site_info(self, site_url: str) -> Dict:
        """Get site information from GSC"""
        if not self.credentials:
            return {"error": "No credentials provided"}

        try:
            service = build('searchconsole', 'v1', credentials=self.credentials)
            site = service.sites().get(siteUrl=site_url).execute()

            return {
                "site_url": site.get("siteUrl"),
                "permission_level": site.get("permissionLevel"),
            }

        except Exception as e:
            return {
                "error": f"Failed to get site info: {str(e)}"
            }
