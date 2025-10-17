# SEO Analyzer Frontend

React + Vite + Tailwind CSS ダッシュボード

## 技術スタック

- **React 18** - UIライブラリ
- **Vite** - 高速ビルドツール
- **Tailwind CSS** - スタイリング
- **React Router** - ルーティング
- **Axios** - HTTP通信
- **Lucide React** - アイコン

## ディレクトリ構造

```
frontend/
├── src/
│   ├── components/       # 共通コンポーネント
│   │   ├── Layout.jsx    # レイアウト
│   │   └── ScoreCard.jsx # スコア表示カード
│   ├── pages/            # ページコンポーネント
│   │   ├── Dashboard.jsx # ダッシュボード
│   │   ├── SiteList.jsx  # サイト一覧
│   │   ├── AddSite.jsx   # サイト追加
│   │   └── SiteDetail.jsx # サイト詳細
│   ├── services/         # API通信
│   │   └── api.js        # Axios設定
│   ├── App.jsx           # ルートコンポーネント
│   ├── main.jsx          # エントリーポイント
│   └── index.css         # グローバルスタイル
├── package.json
├── vite.config.js
├── tailwind.config.js
└── Dockerfile
```

## セットアップ

```bash
# 依存関係インストール
npm install

# 開発サーバー起動
npm run dev

# プロダクションビルド
npm run build

# プレビュー
npm run preview
```

## ページ構成

### Dashboard (`/`)
- 登録サイト一覧
- 最新スコア表示
- クイックアクセス

### SiteList (`/sites`)
- サイト管理
- 削除機能

### AddSite (`/sites/add`)
- 新規サイト登録フォーム

### SiteDetail (`/sites/:id`)
- SEO分析実行
- スコア詳細表示
- カテゴリー別分析
- Core Web Vitals
- 改善提案リスト

## 環境変数

`.env` ファイル（オプション）:

```env
VITE_API_URL=http://localhost:8000
```

## スタイリング

Tailwind CSSを使用:
- ユーティリティファーストCSS
- レスポンシブデザイン
- カスタムカラーテーマ（primary-*）

## ビルド

```bash
# プロダクションビルド
npm run build

# dist/ディレクトリに出力
```
