# SEO Analyzer Backend

FastAPI-based REST API for SEO analysis

## ディレクトリ構造

```
backend/
├── app/
│   ├── api/              # APIエンドポイント
│   │   ├── sites.py      # サイト管理API
│   │   └── analysis.py   # 分析API
│   ├── core/             # コア設定
│   │   ├── config.py     # アプリ設定
│   │   └── database.py   # DB接続
│   ├── models/           # データモデル
│   │   └── site.py       # Site, Analysis, Keyword, Recommendation
│   ├── services/         # ビジネスロジック
│   │   ├── seo_analyzer.py      # SEOスコア計算エンジン
│   │   ├── pagespeed_service.py # PageSpeed API
│   │   └── gsc_service.py       # Google Search Console API
│   └── main.py           # FastAPIアプリ
├── requirements.txt
├── .env.example
└── Dockerfile
```

## セットアップ

```bash
# 仮想環境作成
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 依存関係インストール
pip install -r requirements.txt

# 環境変数設定
cp .env.example .env
# .envを編集

# サーバー起動
uvicorn app.main:app --reload
```

## APIエンドポイント

### サイト管理

- `POST /api/v1/sites/` - サイト登録
- `GET /api/v1/sites/` - サイト一覧
- `GET /api/v1/sites/{id}` - サイト詳細
- `DELETE /api/v1/sites/{id}` - サイト削除

### 分析

- `POST /api/v1/analysis/{id}` - SEO分析実行
- `GET /api/v1/analysis/{id}/latest` - 最新分析結果
- `GET /api/v1/analysis/{id}/history` - 分析履歴

## データベースモデル

### Site
- id, domain, url, name
- gsc_connected, latest_score
- created_at, updated_at, last_analyzed_at

### Analysis
- id, site_id
- total_score, technical_score, content_score, ux_score, authority_score
- pagespeed scores, Core Web Vitals
- detailed_results (JSON)

### Keyword
- id, site_id, keyword
- clicks, impressions, ctr, position
- position_change

### Recommendation
- id, site_id, analysis_id
- title, description, priority, difficulty
- expected_impact, category

## テスト

```bash
pytest
```
