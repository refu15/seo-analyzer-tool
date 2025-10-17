# AI駆動SEO分析機能セットアップガイド

## 概要

このSEOAnalyzerツールは、Anthropic社のClaude AIを使用したプロフェッショナルレベルの詳細SEO分析機能を搭載しています。

## 機能

### 1. カテゴリー別AI分析

各SEOカテゴリーに対して、AIが詳細な分析を提供します：

#### 技術的SEO分析
- SSL/HTTPS設定の評価
- サイト速度とパフォーマンス分析
- クローラビリティ（robots.txt、sitemap）
- モバイルレスポンシブネス
- 構造化データ実装
- URL構造とCanonicalタグ

#### コンテンツSEO分析
- タイトルタグ最適化
- メタディスクリプション効果性
- 見出し構造と階層
- コンテンツ品質と深さ
- キーワード使用と密度
- 読みやすさとユーザーエンゲージメント

#### UX/UI SEO分析
- モバイルフレンドリー度
- ページレイアウトと視覚階層
- ナビゲーション構造
- 画像最適化
- 内部リンク戦略
- アクセシビリティ
- Core Web Vitals改善

#### 権威性・信頼性分析
- E-E-A-T シグナル（経験、専門性、権威性、信頼性）
- Schema markup実装
- ソーシャルプルーフ要素
- ブランドシグナル
- コンテンツの信憑性
- 外部信頼指標

### 2. 90日間アクションプラン

AIが包括的な改善ロードマップを自動生成：

- **優先アクション**: 影響度・難易度・期間を考慮した具体的な実装ステップ
- **30/60/90日タイムライン**: 段階的な改善計画
- **クイックウィン**: 即座に実装できる改善案
- **長期戦略**: 持続的なSEO成長のための戦略
- **KPIモニタリング**: 継続的に追跡すべき指標

## セットアップ手順

### 1. Anthropic API Keyの取得

1. [Anthropic Console](https://console.anthropic.com/)にアクセス
2. アカウントを作成またはログイン
3. API Keysセクションで新しいAPIキーを生成
4. 生成されたキーをコピー

### 2. 環境変数の設定

`backend/.env`ファイルにAPIキーを追加：

```bash
# Anthropic API for LLM-powered analysis
ANTHROPIC_API_KEY=sk-ant-api03-xxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

### 3. バックエンドの再起動

```bash
cd backend
# 仮想環境がアクティブな状態で
python run.py
```

## 使用方法

### 基本的な使い方

1. フロントエンド（http://localhost:5173）でサイトを登録
2. 「SEO分析を実行」ボタンをクリック
3. 分析が完了すると、以下が表示されます：
   - 基本的なSEOスコア（0-100点）
   - カテゴリー別スコア
   - **AI詳細分析**（Anthropic API key設定時のみ）
   - **90日間アクションプラン**（Anthropic API key設定時のみ）

### AI分析セクション

各カテゴリーの詳細分析セクションをクリックして展開すると：

- **全体評価**: AIによる2-3文の要約
- **重要な問題点**: 高・中・低の影響度で分類された問題
- **優れている点**: 現在うまくいっている要素
- **改善提案**:
  - 現状と推奨される状態
  - 具体的な実装手順
  - 期待される効果
  - 難易度と優先度
- **詳細スコア**: サブカテゴリー別の評価
- **プロからの推奨事項**: 専門家レベルのアドバイス

### アクションプランセクション

3つのタブで構成：

1. **優先アクション**:
   - 影響度と難易度でソートされたタスク
   - 実装ステップ、必要リソース、KPI付き

2. **タイムライン**:
   - 30日プラン（即効性の高い改善）
   - 60日プラン（中期的な最適化）
   - 90日プラン（戦略的な強化）

3. **クイックウィン**:
   - すぐに実装できる改善案
   - 継続的モニタリング推奨事項

## API使用量とコスト

### Claude 3.5 Sonnet

- **モデル**: claude-3-5-sonnet-20241022
- **使用量**: 1回の分析で約4つのLLM呼び出し（各カテゴリー + アクションプラン）
- **推定コスト**: 1サイト分析あたり約$0.10-0.30（入力トークン数による）

### 推奨事項

- 開発/テスト中は少量のテストを推奨
- 本番環境では、Anthropic Consoleで使用量制限を設定
- 頻繁な再分析を避け、適切な間隔（週1回など）で実行

## API Keyなしでの使用

Anthropic API Keyが設定されていない場合：

- 基本的なSEOスコア計算は動作
- PageSpeed Insightsスコアは動作（PAGESPEED_API_KEY設定時）
- AI詳細分析は「詳細分析が利用できません」と表示
- アクションプランは表示されません

## トラブルシューティング

### AI分析が表示されない

1. `.env`ファイルで`ANTHROPIC_API_KEY`が正しく設定されているか確認
2. バックエンドを再起動
3. ブラウザコンソールでエラーを確認

### APIエラー

- **401 Unauthorized**: API Keyが無効または期限切れ
- **429 Too Many Requests**: レート制限超過、しばらく待ってから再試行
- **500 Internal Server Error**: バックエンドログを確認（LLMレスポンスのパースエラーなど）

### 分析が遅い

- LLM呼び出しには時間がかかります（1サイトあたり30-60秒程度）
- これは正常です。分析中メッセージが表示されます

## 技術詳細

### アーキテクチャ

```
frontend (React)
    ↓
backend API (FastAPI)
    ↓
SEOAnalyzer Service
    ↓
LLMAnalyzer Service ← Anthropic Claude API
```

### 主要ファイル

- `backend/app/services/llm_analyzer.py`: LLM分析ロジック
- `backend/app/services/seo_analyzer.py`: SEOAnalyzer本体（LLM統合済み）
- `backend/app/models/site.py`: データベースモデル（LLM結果保存用フィールド追加）
- `frontend/src/components/LLMAnalysisSection.jsx`: AI分析表示コンポーネント
- `frontend/src/components/ActionPlan.jsx`: アクションプラン表示コンポーネント

### データベーススキーマ

Analysis テーブルに以下のJSON列が追加：

- `llm_technical_analysis`
- `llm_content_analysis`
- `llm_ux_analysis`
- `llm_authority_analysis`
- `llm_action_plan`

## カスタマイズ

### プロンプトのカスタマイズ

`backend/app/services/llm_analyzer.py`の各分析メソッドでプロンプトをカスタマイズ可能：

- `analyze_technical_seo()`: 技術SEOプロンプト
- `analyze_content_seo()`: コンテンツSEOプロンプト
- `analyze_ux_seo()`: UX/UIプロンプト
- `analyze_authority_seo()`: 権威性プロンプト
- `generate_action_plan()`: アクションプランプロンプト

### モデル変更

`llm_analyzer.py`の`self.model`を変更：

```python
self.model = "claude-3-5-sonnet-20241022"  # 現在
# or
self.model = "claude-3-opus-20240229"  # より高精度（高コスト）
# or
self.model = "claude-3-haiku-20240307"  # より高速（低コスト）
```

## ライセンスと利用規約

- このツールはAnthropicのClaude APIを使用しています
- [Anthropic利用規約](https://www.anthropic.com/legal/terms)に従ってください
- 生成されたコンテンツの著作権については、Anthropicのポリシーを確認してください

## サポート

問題が発生した場合：

1. バックエンドログを確認: コンソール出力をチェック
2. ブラウザ開発者ツールでネットワークタブを確認
3. GitHubでissueを作成

## まとめ

このAI駆動SEO分析機能により、プロフェッショナルレベルの詳細なSEOインサイトと実行可能なアクションプランを自動生成できます。Anthropic API Keyを設定するだけで、すぐに使用開始できます。
