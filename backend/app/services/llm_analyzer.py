"""
LLM-Powered SEO Analysis Service
Uses Google Gemini AI to provide professional-grade, detailed SEO insights
"""

import google.generativeai as genai
from typing import Dict, List, Optional
import json
from ..core.config import settings


class LLMAnalyzer:
    """Advanced SEO analysis using Google Gemini AI"""

    def __init__(self):
        self.client = None
        if settings.GEMINI_API_KEY:
            genai.configure(api_key=settings.GEMINI_API_KEY)
            # Use the latest Gemini 2.5 Pro model
            self.client = genai.GenerativeModel('models/gemini-2.5-pro')
        self.generation_config = {
            'temperature': 0.3,
            'top_p': 0.95,
            'top_k': 40,
            'max_output_tokens': 8192,
        }

    def _call_gemini(self, prompt: str) -> Dict:
        """Call Gemini API and parse JSON response"""
        if not self.client:
            return {}

        try:
            response = self.client.generate_content(
                prompt,
                generation_config=self.generation_config
            )

            # Extract JSON from response
            text = response.text
            start_idx = text.find('{')
            end_idx = text.rfind('}') + 1

            if start_idx != -1 and end_idx > start_idx:
                json_str = text[start_idx:end_idx]
                return json.loads(json_str)

            return {}
        except Exception as e:
            print(f"Gemini API error: {str(e)}")
            return {}

    def analyze_technical_seo(
        self,
        technical_data: Dict,
        html_snippet: str,
        url: str
    ) -> Dict:
        """
        Deep technical SEO analysis

        Analyzes:
        - SSL/HTTPS configuration
        - Site speed and performance
        - Crawlability (robots.txt, sitemap)
        - Mobile responsiveness
        - Structured data implementation
        - URL structure
        - Canonical tags
        """

        if not self.client:
            return self._fallback_technical_analysis(technical_data)

        prompt = f"""あなたはプロフェッショナルなテクニカルSEOコンサルタントです。
以下のWebサイトの技術的SEO状況を詳細に分析してください。

URL: {url}

技術データ:
- SSL/HTTPS: {"有効" if technical_data.get('has_ssl') else "無効"}
- レスポンスタイム: {technical_data.get('response_time', 'N/A')}秒
- ステータスコード: {technical_data.get('status_code', 'N/A')}
- viewport設定: {"有" if technical_data.get('has_viewport') else "無"}
- canonical設定: {"有" if technical_data.get('has_canonical') else "無"}

HTML抜粋:
{html_snippet[:2000]}

以下の観点から分析し、JSON形式で回答してください:

{{
  "overall_assessment": "全体的な技術的SEOの状況を2-3文で要約",
  "critical_issues": [
    {{
      "issue": "問題点",
      "impact": "high/medium/low",
      "explanation": "なぜこれが問題なのか",
      "solution": "具体的な解決策"
    }}
  ],
  "strengths": ["良い点1", "良い点2"],
  "improvements": [
    {{
      "area": "改善領域",
      "current_state": "現状",
      "recommended_state": "推奨される状態",
      "implementation_steps": ["ステップ1", "ステップ2"],
      "expected_impact": "期待される効果",
      "difficulty": "easy/moderate/hard",
      "priority": "high/medium/low"
    }}
  ],
  "technical_score_breakdown": {{
    "https_security": {{"score": 0-100, "note": "評価コメント"}},
    "site_speed": {{"score": 0-100, "note": "評価コメント"}},
    "crawlability": {{"score": 0-100, "note": "評価コメント"}},
    "mobile_optimization": {{"score": 0-100, "note": "評価コメント"}},
    "structured_data": {{"score": 0-100, "note": "評価コメント"}}
  }},
  "professional_recommendations": [
    "プロとしての具体的推奨事項1",
    "プロとしての具体的推奨事項2"
  ]
}}

必ず有効なJSON形式で回答してください。"""

        result = self._call_gemini(prompt)
        return result if result else self._fallback_technical_analysis(technical_data)

    def analyze_content_seo(
        self,
        content_data: Dict,
        page_text: str,
        url: str,
        title: str,
        meta_description: Optional[str]
    ) -> Dict:
        """Deep content SEO analysis"""

        if not self.client:
            return self._fallback_content_analysis(content_data)

        page_text_sample = page_text[:3000]

        prompt = f"""あなたはプロフェッショナルなコンテンツSEOスペシャリストです。
以下のWebページのコンテンツSEOを詳細に分析してください。

URL: {url}
タイトル: {title or "未設定"}
メタディスクリプション: {meta_description or "未設定"}

コンテンツデータ:
- 単語数: {content_data.get('word_count', 0)}
- H1タグ数: {content_data.get('h1_count', 0)}
- H1テキスト: {content_data.get('h1_text', 'N/A')}

ページテキスト抜粋:
{page_text_sample}

以下の観点から分析し、JSON形式で回答してください:

{{
  "overall_assessment": "コンテンツSEOの全体的な評価を2-3文で",
  "title_analysis": {{
    "score": 0-100,
    "length_assessment": "文字数の評価",
    "keyword_placement": "キーワード配置の評価",
    "recommendations": ["改善提案1", "改善提案2"],
    "suggested_titles": ["代替タイトル案1", "代替タイトル案2"]
  }},
  "meta_description_analysis": {{
    "score": 0-100,
    "quality_assessment": "品質評価",
    "cta_presence": "行動喚起の有無と評価",
    "recommendations": ["改善提案"],
    "suggested_descriptions": ["代替ディスクリプション案1"]
  }},
  "heading_structure": {{
    "score": 0-100,
    "hierarchy_assessment": "見出し階層の評価",
    "h1_analysis": "H1タグの評価",
    "improvements": ["改善点"]
  }},
  "content_quality": {{
    "score": 0-100,
    "depth_assessment": "コンテンツの深さ評価",
    "readability": "読みやすさ評価",
    "engagement_potential": "エンゲージメント可能性",
    "expertise_signals": "専門性の表現度",
    "recommendations": ["コンテンツ改善案"]
  }},
  "keyword_analysis": {{
    "primary_keywords_detected": ["検出されたメインキーワード"],
    "keyword_density_assessment": "キーワード密度の評価",
    "semantic_relevance": "意味的関連性の評価",
    "recommendations": ["キーワード戦略の提案"]
  }},
  "content_gaps": [
    {{
      "gap": "不足しているコンテンツ要素",
      "why_important": "なぜ重要か",
      "how_to_add": "追加方法"
    }}
  ],
  "competitive_advantages": ["このコンテンツの強み"],
  "professional_recommendations": ["プロとしての具体的推奨事項"]
}}

必ず有効なJSON形式で回答してください。"""

        result = self._call_gemini(prompt)
        return result if result else self._fallback_content_analysis(content_data)

    def analyze_ux_seo(
        self,
        ux_data: Dict,
        html_snippet: str,
        url: str
    ) -> Dict:
        """Deep UX and Core Web Vitals analysis"""

        if not self.client:
            return self._fallback_ux_analysis(ux_data)

        prompt = f"""あなたはプロフェッショナルなUX/UIとSEOのスペシャリストです。
以下のWebサイトのユーザーエクスペリエンスとSEOへの影響を分析してください。

URL: {url}

UXデータ:
- 画像総数: {ux_data.get('total_images', 0)}
- alt属性付き画像: {ux_data.get('images_with_alt', 0)}
- モバイルフレンドリー: {"はい" if ux_data.get('mobile_friendly') else "いいえ"}

HTML抜粋:
{html_snippet[:2000]}

以下の観点から分析し、JSON形式で回答してください:

{{
  "overall_assessment": "UX観点からのSEO評価を2-3文で",
  "mobile_experience": {{
    "score": 0-100,
    "viewport_configuration": "viewport設定の評価",
    "responsive_design_assessment": "レスポンシブデザインの評価",
    "touch_target_sizing": "タッチターゲットサイズの評価",
    "recommendations": ["モバイルUX改善案"]
  }},
  "visual_hierarchy": {{
    "score": 0-100,
    "layout_assessment": "レイアウトの評価",
    "content_prioritization": "コンテンツ優先度の評価",
    "recommendations": ["視覚階層改善案"]
  }},
  "image_optimization": {{
    "score": 0-100,
    "alt_text_coverage": "alt属性カバレッジの評価",
    "alt_text_quality": "alt属性の質の評価",
    "image_loading_strategy": "画像読み込み戦略の評価",
    "recommendations": ["画像最適化案"]
  }},
  "navigation_and_links": {{
    "score": 0-100,
    "internal_linking_strategy": "内部リンク戦略の評価",
    "navigation_clarity": "ナビゲーション明確性の評価",
    "recommendations": ["ナビゲーション改善案"]
  }},
  "accessibility": {{
    "score": 0-100,
    "semantic_html_usage": "セマンティックHTML使用度",
    "aria_implementation": "ARIA実装評価",
    "color_contrast": "色のコントラスト評価",
    "recommendations": ["アクセシビリティ改善案"]
  }},
  "user_engagement_factors": {{
    "page_scannability": "ページスキャン性の評価",
    "cta_visibility": "CTA可視性の評価",
    "content_formatting": "コンテンツフォーマットの評価",
    "recommendations": ["エンゲージメント向上案"]
  }},
  "core_web_vitals_insights": {{
    "lcp_optimization_tips": ["LCP改善のヒント"],
    "fid_optimization_tips": ["FID改善のヒント"],
    "cls_optimization_tips": ["CLS改善のヒント"]
  }},
  "professional_recommendations": ["プロとしての具体的推奨事項"]
}}

必ず有効なJSON形式で回答してください。"""

        result = self._call_gemini(prompt)
        return result if result else self._fallback_ux_analysis(ux_data)

    def analyze_authority_seo(
        self,
        html_snippet: str,
        url: str,
        domain: str
    ) -> Dict:
        """Deep authority and trust signals analysis"""

        if not self.client:
            return self._fallback_authority_analysis()

        prompt = f"""あなたはプロフェッショナルなSEOコンサルタントで、E-E-A-T（経験、専門性、権威性、信頼性）の専門家です。
以下のWebサイトの権威性と信頼シグナルを分析してください。

URL: {url}
ドメイン: {domain}

HTML抜粋:
{html_snippet[:3000]}

以下の観点から分析し、JSON形式で回答してください:

{{
  "overall_assessment": "権威性・信頼性の全体評価を2-3文で",
  "eeat_analysis": {{
    "experience_signals": {{
      "score": 0-100,
      "detected_signals": ["検出された経験シグナル"],
      "missing_signals": ["欠けている経験シグナル"],
      "recommendations": ["経験を示す方法"]
    }},
    "expertise_signals": {{
      "score": 0-100,
      "detected_signals": ["検出された専門性シグナル"],
      "author_credentials": "著者の資格情報の評価",
      "recommendations": ["専門性を高める方法"]
    }},
    "authoritativeness_signals": {{
      "score": 0-100,
      "detected_signals": ["検出された権威性シグナル"],
      "brand_presence": "ブランドプレゼンスの評価",
      "recommendations": ["権威性を高める方法"]
    }},
    "trust_signals": {{
      "score": 0-100,
      "detected_signals": ["検出された信頼シグナル"],
      "transparency_elements": "透明性要素の評価",
      "recommendations": ["信頼性を高める方法"]
    }}
  }},
  "schema_markup": {{
    "score": 0-100,
    "implemented_schemas": ["実装されているSchema"],
    "missing_critical_schemas": ["欠けている重要なSchema"],
    "implementation_quality": "実装品質の評価",
    "recommendations": ["Schema実装の改善案"]
  }},
  "social_proof": {{
    "score": 0-100,
    "og_tags_quality": "OGタグの質の評価",
    "twitter_cards_quality": "Twitterカードの質の評価",
    "social_sharing_optimization": "ソーシャル共有最適化の評価",
    "recommendations": ["ソーシャルプルーフ改善案"]
  }},
  "content_credibility": {{
    "citation_presence": "引用の有無と質",
    "fact_checking_signals": "事実確認シグナル",
    "update_freshness": "更新頻度の評価",
    "recommendations": ["コンテンツ信頼性向上案"]
  }},
  "brand_signals": {{
    "brand_consistency": "ブランド一貫性の評価",
    "unique_value_proposition": "独自価値提案の明確性",
    "professional_presentation": "プロフェッショナルな表現の評価",
    "recommendations": ["ブランド強化案"]
  }},
  "trust_indicators": {{
    "contact_information": "連絡先情報の評価",
    "privacy_policy": "プライバシーポリシーの評価",
    "terms_of_service": "利用規約の評価",
    "security_indicators": "セキュリティ指標",
    "recommendations": ["信頼指標改善案"]
  }},
  "competitive_positioning": {{
    "strengths": ["競合に対する強み"],
    "weaknesses": ["競合に対する弱み"],
    "opportunities": ["改善機会"]
  }},
  "professional_recommendations": ["プロとしての具体的推奨事項"]
}}

必ず有効なJSON形式で回答してください。"""

        result = self._call_gemini(prompt)
        return result if result else self._fallback_authority_analysis()

    def generate_action_plan(
        self,
        all_analyses: Dict,
        site_url: str,
        current_score: float
    ) -> Dict:
        """Generate comprehensive, prioritized action plan"""

        if not self.client:
            return self._fallback_action_plan(current_score)

        prompt = f"""あなたはプロフェッショナルなSEOストラテジストです。
以下のWebサイトの包括的なSEO改善アクションプランを作成してください。

サイトURL: {site_url}
現在の総合スコア: {current_score}/100

各カテゴリーの分析結果に基づき、90日間のアクションプランを作成してください。

以下の形式でJSON回答してください:

{{
  "executive_summary": "3-4文でのエグゼクティブサマリー",
  "priority_actions": [
    {{
      "title": "アクション名",
      "category": "technical/content/ux/authority",
      "priority": "critical/high/medium/low",
      "effort": "1-5",
      "expected_impact": "1-10",
      "timeline": "完了までの推定日数",
      "steps": ["具体的ステップ1", "具体的ステップ2"],
      "required_resources": ["必要なリソース"],
      "kpis": ["測定すべきKPI"]
    }}
  ],
  "30_day_plan": {{
    "focus_areas": ["注力領域"],
    "expected_score_improvement": "予想されるスコア改善幅",
    "key_deliverables": ["主要な成果物"]
  }},
  "60_day_plan": {{
    "focus_areas": ["注力領域"],
    "expected_score_improvement": "予想されるスコア改善幅",
    "key_deliverables": ["主要な成果物"]
  }},
  "90_day_plan": {{
    "focus_areas": ["注力領域"],
    "expected_score_improvement": "予想されるスコア改善幅",
    "key_deliverables": ["主要な成果物"]
  }},
  "quick_wins": ["即座に実装できる改善案"],
  "long_term_strategy": "長期的なSEO戦略の提案",
  "monitoring_recommendations": ["継続的にモニタリングすべき指標"]
}}

必ず有効なJSON形式で回答してください。"""

        result = self._call_gemini(prompt)
        return result if result else self._fallback_action_plan(current_score)

    # Fallback methods when LLM is not available
    def _fallback_technical_analysis(self, technical_data: Dict) -> Dict:
        return {
            "overall_assessment": "LLM分析が利用できません。基本的な技術分析のみ実行されました。",
            "critical_issues": [],
            "strengths": [],
            "improvements": [],
            "technical_score_breakdown": {},
            "professional_recommendations": ["Gemini API keyを設定してください"]
        }

    def _fallback_content_analysis(self, content_data: Dict) -> Dict:
        return {
            "overall_assessment": "LLM分析が利用できません。基本的なコンテンツ分析のみ実行されました。",
            "title_analysis": {},
            "meta_description_analysis": {},
            "heading_structure": {},
            "content_quality": {},
            "keyword_analysis": {},
            "content_gaps": [],
            "competitive_advantages": [],
            "professional_recommendations": ["Gemini API keyを設定してください"]
        }

    def _fallback_ux_analysis(self, ux_data: Dict) -> Dict:
        return {
            "overall_assessment": "LLM分析が利用できません。基本的なUX分析のみ実行されました。",
            "mobile_experience": {},
            "visual_hierarchy": {},
            "image_optimization": {},
            "navigation_and_links": {},
            "accessibility": {},
            "user_engagement_factors": {},
            "core_web_vitals_insights": {},
            "professional_recommendations": ["Gemini API keyを設定してください"]
        }

    def _fallback_authority_analysis(self) -> Dict:
        return {
            "overall_assessment": "LLM分析が利用できません。基本的な権威性分析のみ実行されました。",
            "eeat_analysis": {},
            "schema_markup": {},
            "social_proof": {},
            "content_credibility": {},
            "brand_signals": {},
            "trust_indicators": {},
            "competitive_positioning": {},
            "professional_recommendations": ["Gemini API keyを設定してください"]
        }

    def _fallback_action_plan(self, current_score: float) -> Dict:
        return {
            "executive_summary": "LLM分析が利用できません。詳細なアクションプランを生成するにはGemini API keyを設定してください。",
            "priority_actions": [],
            "30_day_plan": {},
            "60_day_plan": {},
            "90_day_plan": {},
            "quick_wins": [],
            "long_term_strategy": "",
            "monitoring_recommendations": []
        }
