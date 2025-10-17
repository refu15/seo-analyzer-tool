# SEO Analyzer Tool

Google Gemini AIを活用したプロフェッショナル向けSEO分析ツール

## 機能

### 基本機能
- **包括的なSEO分析**: 技術的SEO、コンテンツ品質、UX、権威性の4カテゴリーで評価
- **透明性のあるスコアリング**: 各項目の配点と評価基準を詳細表示
- **PageSpeed Insights連携**: モバイル・デスクトップの Performance スコア測定
- **Core Web Vitals**: LCP、FID、CLSの測定

### AI機能（Google Gemini 2.5 Pro）
- **カテゴリー別詳細分析**: 各SEOカテゴリーの深掘り分析
- **問題点の自動検出**: 重大な問題、強み、改善点を特定
- **プロフェッショナルな推奨事項**: 具体的な改善アクションを提案
- **90日間アクションプラン**: 優先度付きの実装ロードマップ

### スコア内訳表示
- 各カテゴリーの重み付けと貢献度を可視化
- チェック項目ごとの合格/不合格状態
- 獲得ポイントとプログレスバー表示

## 技術スタック

### Backend
- FastAPI
- SQLAlchemy (SQLite)
- Google Generative AI (Gemini 2.5 Pro)
- BeautifulSoup4
- Pydantic

### Frontend
- React 18
- Vite
- TailwindCSS
- Lucide React Icons

### インフラ
- Docker & Docker Compose
- Nginx

## クイックスタート

### 開発環境

1. リポジトリのクローン:
```bash
git clone https://github.com/yourusername/seo-analyzer-tool.git
cd seo-analyzer-tool
```

2. Backend環境変数の設定:
```bash
cd backend
cp .env.example .env
```

`.env` を編集して、Gemini API Keyを設定:
```bash
GEMINI_API_KEY=your_gemini_api_key_here
```

3. Backend起動:
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
python run.py
```

4. Frontend起動（別ターミナル）:
```bash
cd frontend
npm install
npm run dev
```

5. ブラウザでアクセス:
- Frontend: http://localhost:5173
- Backend API: http://localhost:8000

### Dockerでの起動

```bash
docker-compose up --build
```

- Frontend: http://localhost
- Backend API: http://localhost:8000

## 本番環境へのデプロイ

詳細は [DEPLOYMENT.md](./DEPLOYMENT.md) を参照してください。

### 簡易手順

1. 本番環境用設定ファイルの作成:
```bash
cd backend
cp .env.production.example .env.production
# .env.production を編集
```

2. Docker Composeで起動:
```bash
docker-compose -f docker-compose.prod.yml up -d --build
```

## 使い方

1. **サイト登録**: ダッシュボードから分析したいサイトのURLを登録
2. **分析実行**: 「SEO分析を実行」ボタンをクリック
3. **結果確認**:
   - 総合スコア（100点満点）
   - カテゴリー別スコア
   - スコア詳細内訳（展開可能）
   - AI詳細分析（4カテゴリー）
   - 90日間アクションプラン

## スコアリング基準

### 重み付け
- 技術的SEO: 30%
- コンテンツ品質: 25%
- ユーザー体験: 25%
- 権威性: 20%

### 技術的SEO（100点）
- HTTPS/SSL: 20点
- ページ読み込み速度: 20点
- robots.txt: 15点
- XMLサイトマップ: 15点
- モバイル対応（viewport）: 15点
- 正規URLタグ: 15点

### コンテンツ品質（100点）
- タイトルタグ（30-60文字）: 25点
- メタディスクリプション（120-160文字）: 25点
- H1タグ（1個推奨）: 20点
- 見出し構造: 15点
- コンテンツ量（1000語以上）: 15点

### ユーザー体験（100点）
- 画像alt属性: 30点
- 内部リンク: 25点
- モバイル対応: 25点
- 外部スクリプト最適化: 20点

### 権威性（100点）
- ベーススコア: 50点
- Schema.org構造化データ: 25点
- Open Graphタグ: 15点
- Twitter Cardタグ: 10点

## 環境変数

### Backend（.env）

```bash
# 必須
GEMINI_API_KEY=your_gemini_api_key_here

# オプション
PAGESPEED_API_KEY=your_pagespeed_api_key_here
GOOGLE_API_KEY=your_google_api_key_here

# セキュリティ
SECRET_KEY=your_secret_key_here_change_in_production

# CORS
ALLOWED_ORIGINS=http://localhost:5173,http://localhost:3000
```

## API Keys取得方法

### Gemini API Key
1. [Google AI Studio](https://aistudio.google.com/app/apikey) にアクセス
2. 「Get API key」をクリック
3. 新しいAPIキーを作成

### PageSpeed API Key（オプション）
1. [Google Cloud Console](https://console.cloud.google.com/) にアクセス
2. APIとサービス > 認証情報
3. 「APIキーを作成」
4. PageSpeed Insights APIを有効化

## ライセンス

MIT License

## 貢献

プルリクエストを歓迎します。大きな変更の場合は、まずissueを開いて変更内容を議論してください。

## サポート

問題が発生した場合は、GitHubのIssuesでお知らせください。
