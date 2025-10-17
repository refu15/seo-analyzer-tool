"""
SEO Score Calculation Engine
Analyzes websites and calculates SEO scores based on multiple factors
"""

import requests
from bs4 import BeautifulSoup
from typing import Dict, Tuple
from urllib.parse import urlparse
import ssl
import socket


class SEOAnalyzer:
    """Main SEO analysis engine"""

    def __init__(self, use_llm: bool = True):
        self.weights = {
            "technical": 0.30,
            "content": 0.25,
            "user_experience": 0.25,
            "authority": 0.20
        }
        self.use_llm = use_llm
        self.llm_analyzer = None

        if use_llm:
            try:
                from .llm_analyzer import LLMAnalyzer
                self.llm_analyzer = LLMAnalyzer()
            except Exception as e:
                print(f"LLM Analyzer initialization failed: {str(e)}")
                self.use_llm = False

    def analyze_site(self, url: str) -> Dict:
        """
        Perform complete SEO analysis on a URL
        Returns analysis results with scores and metrics
        """
        # Ensure URL has protocol
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url

        # Fetch page content
        try:
            response = requests.get(url, timeout=10, headers={
                'User-Agent': 'Mozilla/5.0 (SEO Analyzer Bot)'
            })
            html_content = response.text
            soup = BeautifulSoup(html_content, 'lxml')
        except Exception as e:
            return {
                "error": f"Failed to fetch URL: {str(e)}",
                "total_score": 0
            }

        # Calculate category scores
        technical_score = self._calculate_technical_score(url, response, soup)
        content_score = self._calculate_content_score(soup)
        ux_score = self._calculate_ux_score(soup)
        authority_score = self._calculate_authority_score(soup)

        # Calculate total score
        total_score = (
            technical_score * self.weights["technical"] +
            content_score * self.weights["content"] +
            ux_score * self.weights["user_experience"] +
            authority_score * self.weights["authority"]
        )

        # Get basic details
        technical_details = self._get_technical_details(url, response, soup)
        content_details = self._get_content_details(soup)
        ux_details = self._get_ux_details(soup)

        # Add score breakdown for transparency
        score_breakdown = {
            "technical": {
                "score": round(technical_score, 1),
                "weight": self.weights["technical"],
                "contribution": round(technical_score * self.weights["technical"], 1),
                "details": self._get_technical_score_details(url, response, soup)
            },
            "content": {
                "score": round(content_score, 1),
                "weight": self.weights["content"],
                "contribution": round(content_score * self.weights["content"], 1),
                "details": self._get_content_score_details(soup)
            },
            "user_experience": {
                "score": round(ux_score, 1),
                "weight": self.weights["user_experience"],
                "contribution": round(ux_score * self.weights["user_experience"], 1),
                "details": self._get_ux_score_details(soup)
            },
            "authority": {
                "score": round(authority_score, 1),
                "weight": self.weights["authority"],
                "contribution": round(authority_score * self.weights["authority"], 1),
                "details": self._get_authority_score_details(soup)
            }
        }

        result = {
            "total_score": round(total_score, 1),
            "technical_score": round(technical_score, 1),
            "content_score": round(content_score, 1),
            "user_experience_score": round(ux_score, 1),
            "authority_score": round(authority_score, 1),
            "score_breakdown": score_breakdown,
            "technical_details": technical_details,
            "content_details": content_details,
            "ux_details": ux_details,
        }

        # Add LLM-powered deep analysis if enabled
        if self.use_llm and self.llm_analyzer:
            try:
                html_snippet = str(soup)[:5000]  # Limit HTML size
                page_text = soup.get_text()
                domain = urlparse(url).netloc

                # Run parallel LLM analyses
                result["llm_technical_analysis"] = self.llm_analyzer.analyze_technical_seo(
                    technical_details, html_snippet, url
                )
                result["llm_content_analysis"] = self.llm_analyzer.analyze_content_seo(
                    content_details, page_text, url,
                    content_details.get("meta_title"),
                    content_details.get("meta_description")
                )
                result["llm_ux_analysis"] = self.llm_analyzer.analyze_ux_seo(
                    ux_details, html_snippet, url
                )
                result["llm_authority_analysis"] = self.llm_analyzer.analyze_authority_seo(
                    html_snippet, url, domain
                )
                result["llm_action_plan"] = self.llm_analyzer.generate_action_plan(
                    {
                        "technical": result.get("llm_technical_analysis"),
                        "content": result.get("llm_content_analysis"),
                        "ux": result.get("llm_ux_analysis"),
                        "authority": result.get("llm_authority_analysis")
                    },
                    url,
                    total_score
                )
            except Exception as e:
                print(f"LLM analysis error: {str(e)}")
                result["llm_analysis_error"] = str(e)

        return result

    def _calculate_technical_score(self, url: str, response, soup) -> float:
        """Calculate technical SEO score (0-100)"""
        score = 0
        max_score = 100

        # SSL Certificate (20 points)
        if url.startswith('https://'):
            score += 20

        # Response time (20 points)
        if response.elapsed.total_seconds() < 2:
            score += 20
        elif response.elapsed.total_seconds() < 4:
            score += 10

        # Robots.txt (15 points)
        domain = urlparse(url).netloc
        robots_url = f"{urlparse(url).scheme}://{domain}/robots.txt"
        try:
            robots_response = requests.get(robots_url, timeout=5)
            if robots_response.status_code == 200:
                score += 15
        except:
            pass

        # Sitemap (15 points)
        sitemap_url = f"{urlparse(url).scheme}://{domain}/sitemap.xml"
        try:
            sitemap_response = requests.get(sitemap_url, timeout=5)
            if sitemap_response.status_code == 200:
                score += 15
        except:
            pass

        # Meta viewport for mobile (15 points)
        viewport = soup.find('meta', attrs={'name': 'viewport'})
        if viewport:
            score += 15

        # Canonical tag (15 points)
        canonical = soup.find('link', attrs={'rel': 'canonical'})
        if canonical:
            score += 15

        return min(score, max_score)

    def _calculate_content_score(self, soup) -> float:
        """Calculate content quality score (0-100)"""
        score = 0

        # Title tag (25 points)
        title = soup.find('title')
        if title and title.string:
            title_text = title.string.strip()
            if 30 <= len(title_text) <= 60:
                score += 25
            elif len(title_text) > 0:
                score += 15

        # Meta description (25 points)
        meta_desc = soup.find('meta', attrs={'name': 'description'})
        if meta_desc and meta_desc.get('content'):
            desc_text = meta_desc.get('content').strip()
            if 120 <= len(desc_text) <= 160:
                score += 25
            elif len(desc_text) > 0:
                score += 15

        # H1 tag (20 points)
        h1_tags = soup.find_all('h1')
        if len(h1_tags) == 1:
            score += 20
        elif len(h1_tags) > 1:
            score += 10

        # Heading structure (15 points)
        h2_tags = soup.find_all('h2')
        h3_tags = soup.find_all('h3')
        if len(h2_tags) > 0 and len(h3_tags) > 0:
            score += 15
        elif len(h2_tags) > 0:
            score += 10

        # Word count (15 points)
        text_content = soup.get_text()
        word_count = len(text_content.split())
        if word_count >= 1000:
            score += 15
        elif word_count >= 300:
            score += 10
        elif word_count >= 100:
            score += 5

        return min(score, 100)

    def _calculate_ux_score(self, soup) -> float:
        """Calculate user experience score (0-100)"""
        score = 0

        # Images with alt tags (30 points)
        images = soup.find_all('img')
        if images:
            images_with_alt = [img for img in images if img.get('alt')]
            alt_ratio = len(images_with_alt) / len(images)
            score += alt_ratio * 30

        # Internal links (25 points)
        internal_links = soup.find_all('a', href=True)
        if len(internal_links) >= 5:
            score += 25
        elif len(internal_links) > 0:
            score += 15

        # Mobile-friendly viewport (25 points)
        viewport = soup.find('meta', attrs={'name': 'viewport'})
        if viewport:
            score += 25

        # No excessive external scripts (20 points)
        scripts = soup.find_all('script', src=True)
        if len(scripts) <= 10:
            score += 20
        elif len(scripts) <= 20:
            score += 10

        return min(score, 100)

    def _calculate_authority_score(self, soup) -> float:
        """Calculate authority score (0-100) - Basic implementation"""
        score = 50  # Base score

        # Schema markup (25 points)
        schema = soup.find_all('script', type='application/ld+json')
        if schema:
            score += 25

        # Social meta tags (25 points)
        og_tags = soup.find_all('meta', property=lambda x: x and x.startswith('og:'))
        twitter_tags = soup.find_all('meta', attrs={'name': lambda x: x and x.startswith('twitter:')})

        if len(og_tags) >= 3:
            score += 15
        if len(twitter_tags) >= 2:
            score += 10

        return min(score, 100)

    def _get_technical_details(self, url: str, response, soup) -> Dict:
        """Get detailed technical metrics"""
        viewport = soup.find('meta', attrs={'name': 'viewport'})
        canonical = soup.find('link', attrs={'rel': 'canonical'})

        return {
            "has_ssl": url.startswith('https://'),
            "response_time": response.elapsed.total_seconds(),
            "has_viewport": bool(viewport),
            "has_canonical": bool(canonical),
            "status_code": response.status_code
        }

    def _get_content_details(self, soup) -> Dict:
        """Get detailed content metrics"""
        title = soup.find('title')
        meta_desc = soup.find('meta', attrs={'name': 'description'})
        h1_tags = soup.find_all('h1')

        text_content = soup.get_text()
        word_count = len(text_content.split())

        return {
            "meta_title": title.string.strip() if title and title.string else None,
            "meta_description": meta_desc.get('content') if meta_desc else None,
            "h1_count": len(h1_tags),
            "h1_text": h1_tags[0].get_text().strip() if h1_tags else None,
            "word_count": word_count
        }

    def _get_ux_details(self, soup) -> Dict:
        """Get detailed UX metrics"""
        images = soup.find_all('img')
        images_with_alt = [img for img in images if img.get('alt')]

        return {
            "total_images": len(images),
            "images_with_alt": len(images_with_alt),
            "mobile_friendly": bool(soup.find('meta', attrs={'name': 'viewport'}))
        }

    def _get_technical_score_details(self, url: str, response, soup) -> Dict:
        """Get detailed breakdown of technical score calculation"""
        details = {}

        # SSL Certificate (20 points)
        has_ssl = url.startswith('https://')
        details["ssl"] = {
            "status": "Pass" if has_ssl else "Fail",
            "points_earned": 20 if has_ssl else 0,
            "max_points": 20,
            "description": "HTTPS/SSL証明書"
        }

        # Response time (20 points)
        response_time = response.elapsed.total_seconds()
        if response_time < 2:
            time_points = 20
            time_status = "Excellent"
        elif response_time < 4:
            time_points = 10
            time_status = "Good"
        else:
            time_points = 0
            time_status = "Slow"

        details["response_time"] = {
            "status": time_status,
            "value": f"{response_time:.2f}秒",
            "points_earned": time_points,
            "max_points": 20,
            "description": "ページ読み込み速度"
        }

        # Robots.txt (15 points)
        domain = urlparse(url).netloc
        robots_url = f"{urlparse(url).scheme}://{domain}/robots.txt"
        has_robots = False
        try:
            robots_response = requests.get(robots_url, timeout=5)
            has_robots = robots_response.status_code == 200
        except:
            pass

        details["robots_txt"] = {
            "status": "Pass" if has_robots else "Fail",
            "points_earned": 15 if has_robots else 0,
            "max_points": 15,
            "description": "robots.txtファイル"
        }

        # Sitemap (15 points)
        sitemap_url = f"{urlparse(url).scheme}://{domain}/sitemap.xml"
        has_sitemap = False
        try:
            sitemap_response = requests.get(sitemap_url, timeout=5)
            has_sitemap = sitemap_response.status_code == 200
        except:
            pass

        details["sitemap"] = {
            "status": "Pass" if has_sitemap else "Fail",
            "points_earned": 15 if has_sitemap else 0,
            "max_points": 15,
            "description": "XMLサイトマップ"
        }

        # Meta viewport for mobile (15 points)
        viewport = soup.find('meta', attrs={'name': 'viewport'})
        has_viewport = bool(viewport)
        details["viewport"] = {
            "status": "Pass" if has_viewport else "Fail",
            "points_earned": 15 if has_viewport else 0,
            "max_points": 15,
            "description": "モバイル対応(viewport)"
        }

        # Canonical tag (15 points)
        canonical = soup.find('link', attrs={'rel': 'canonical'})
        has_canonical = bool(canonical)
        details["canonical"] = {
            "status": "Pass" if has_canonical else "Fail",
            "points_earned": 15 if has_canonical else 0,
            "max_points": 15,
            "description": "正規URLタグ"
        }

        return details

    def _get_content_score_details(self, soup) -> Dict:
        """Get detailed breakdown of content score calculation"""
        details = {}

        # Title tag (25 points)
        title = soup.find('title')
        if title and title.string:
            title_text = title.string.strip()
            title_len = len(title_text)
            if 30 <= title_len <= 60:
                title_points = 25
                title_status = "Optimal"
            elif title_len > 0:
                title_points = 15
                title_status = "Present"
            else:
                title_points = 0
                title_status = "Missing"
        else:
            title_text = ""
            title_len = 0
            title_points = 0
            title_status = "Missing"

        details["title_tag"] = {
            "status": title_status,
            "value": f"{title_len}文字",
            "points_earned": title_points,
            "max_points": 25,
            "description": "タイトルタグ(30-60文字推奨)"
        }

        # Meta description (25 points)
        meta_desc = soup.find('meta', attrs={'name': 'description'})
        if meta_desc and meta_desc.get('content'):
            desc_text = meta_desc.get('content').strip()
            desc_len = len(desc_text)
            if 120 <= desc_len <= 160:
                desc_points = 25
                desc_status = "Optimal"
            elif desc_len > 0:
                desc_points = 15
                desc_status = "Present"
            else:
                desc_points = 0
                desc_status = "Missing"
        else:
            desc_len = 0
            desc_points = 0
            desc_status = "Missing"

        details["meta_description"] = {
            "status": desc_status,
            "value": f"{desc_len}文字",
            "points_earned": desc_points,
            "max_points": 25,
            "description": "メタディスクリプション(120-160文字推奨)"
        }

        # H1 tag (20 points)
        h1_tags = soup.find_all('h1')
        h1_count = len(h1_tags)
        if h1_count == 1:
            h1_points = 20
            h1_status = "Optimal"
        elif h1_count > 1:
            h1_points = 10
            h1_status = "Multiple"
        else:
            h1_points = 0
            h1_status = "Missing"

        details["h1_tag"] = {
            "status": h1_status,
            "value": f"{h1_count}個",
            "points_earned": h1_points,
            "max_points": 20,
            "description": "H1タグ(1個推奨)"
        }

        # Heading structure (15 points)
        h2_tags = soup.find_all('h2')
        h3_tags = soup.find_all('h3')
        h2_count = len(h2_tags)
        h3_count = len(h3_tags)

        if h2_count > 0 and h3_count > 0:
            heading_points = 15
            heading_status = "Good"
        elif h2_count > 0:
            heading_points = 10
            heading_status = "Fair"
        else:
            heading_points = 0
            heading_status = "Poor"

        details["heading_structure"] = {
            "status": heading_status,
            "value": f"H2: {h2_count}個, H3: {h3_count}個",
            "points_earned": heading_points,
            "max_points": 15,
            "description": "見出し構造"
        }

        # Word count (15 points)
        text_content = soup.get_text()
        word_count = len(text_content.split())

        if word_count >= 1000:
            wc_points = 15
            wc_status = "Excellent"
        elif word_count >= 300:
            wc_points = 10
            wc_status = "Good"
        elif word_count >= 100:
            wc_points = 5
            wc_status = "Fair"
        else:
            wc_points = 0
            wc_status = "Poor"

        details["word_count"] = {
            "status": wc_status,
            "value": f"{word_count}語",
            "points_earned": wc_points,
            "max_points": 15,
            "description": "コンテンツ量(1000語以上推奨)"
        }

        return details

    def _get_ux_score_details(self, soup) -> Dict:
        """Get detailed breakdown of UX score calculation"""
        details = {}

        # Images with alt tags (30 points)
        images = soup.find_all('img')
        total_images = len(images)
        if total_images > 0:
            images_with_alt = [img for img in images if img.get('alt')]
            alt_count = len(images_with_alt)
            alt_ratio = alt_count / total_images
            alt_points = alt_ratio * 30

            if alt_ratio >= 0.9:
                alt_status = "Excellent"
            elif alt_ratio >= 0.5:
                alt_status = "Good"
            else:
                alt_status = "Poor"
        else:
            alt_count = 0
            alt_ratio = 0
            alt_points = 0
            alt_status = "No Images"

        details["image_alt_tags"] = {
            "status": alt_status,
            "value": f"{alt_count}/{total_images}画像",
            "points_earned": round(alt_points, 1),
            "max_points": 30,
            "description": "画像のalt属性"
        }

        # Internal links (25 points)
        internal_links = soup.find_all('a', href=True)
        link_count = len(internal_links)

        if link_count >= 5:
            link_points = 25
            link_status = "Good"
        elif link_count > 0:
            link_points = 15
            link_status = "Fair"
        else:
            link_points = 0
            link_status = "Poor"

        details["internal_links"] = {
            "status": link_status,
            "value": f"{link_count}個",
            "points_earned": link_points,
            "max_points": 25,
            "description": "内部リンク数"
        }

        # Mobile-friendly viewport (25 points)
        viewport = soup.find('meta', attrs={'name': 'viewport'})
        has_viewport = bool(viewport)

        details["mobile_viewport"] = {
            "status": "Pass" if has_viewport else "Fail",
            "points_earned": 25 if has_viewport else 0,
            "max_points": 25,
            "description": "モバイル対応設定"
        }

        # External scripts (20 points)
        scripts = soup.find_all('script', src=True)
        script_count = len(scripts)

        if script_count <= 10:
            script_points = 20
            script_status = "Excellent"
        elif script_count <= 20:
            script_points = 10
            script_status = "Good"
        else:
            script_points = 0
            script_status = "Too Many"

        details["external_scripts"] = {
            "status": script_status,
            "value": f"{script_count}個",
            "points_earned": script_points,
            "max_points": 20,
            "description": "外部スクリプト数"
        }

        return details

    def _get_authority_score_details(self, soup) -> Dict:
        """Get detailed breakdown of authority score calculation"""
        details = {}

        # Base score (50 points)
        details["base_score"] = {
            "status": "Default",
            "value": "ベーススコア",
            "points_earned": 50,
            "max_points": 50,
            "description": "基本権威スコア"
        }

        # Schema markup (25 points)
        schema = soup.find_all('script', type='application/ld+json')
        schema_count = len(schema)
        has_schema = schema_count > 0

        details["schema_markup"] = {
            "status": "Pass" if has_schema else "Fail",
            "value": f"{schema_count}個",
            "points_earned": 25 if has_schema else 0,
            "max_points": 25,
            "description": "構造化データ(Schema.org)"
        }

        # Open Graph tags (15 points)
        og_tags = soup.find_all('meta', property=lambda x: x and x.startswith('og:'))
        og_count = len(og_tags)

        if og_count >= 3:
            og_points = 15
            og_status = "Good"
        else:
            og_points = 0
            og_status = "Insufficient"

        details["open_graph"] = {
            "status": og_status,
            "value": f"{og_count}個",
            "points_earned": og_points,
            "max_points": 15,
            "description": "Open Graphタグ"
        }

        # Twitter Card tags (10 points)
        twitter_tags = soup.find_all('meta', attrs={'name': lambda x: x and x.startswith('twitter:')})
        twitter_count = len(twitter_tags)

        if twitter_count >= 2:
            twitter_points = 10
            twitter_status = "Good"
        else:
            twitter_points = 0
            twitter_status = "Insufficient"

        details["twitter_card"] = {
            "status": twitter_status,
            "value": f"{twitter_count}個",
            "points_earned": twitter_points,
            "max_points": 10,
            "description": "Twitter Cardタグ"
        }

        return details
