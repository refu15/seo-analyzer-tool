# ローカル開発環境での起動方法

Docker Desktopを使わずにローカルで起動する手順です。

## 前提条件

- Python 3.11+ インストール済み
- Node.js 20+ インストール済み

## 起動手順

### 1. バックエンドのセットアップと起動

```bash
# バックエンドディレクトリに移動
cd C:\Users\nnkre\projects\seo-analyzer-tool\backend

# 仮想環境作成
python -m venv venv

# 仮想環境を有効化
venv\Scripts\activate

# 依存関係インストール
pip install -r requirements.txt

# 環境変数ファイルを作成
copy .env.example .env

# サーバー起動
python run.py
```

バックエンドが起動したら: `http://localhost:8000`

### 2. フロントエンドのセットアップと起動（別のターミナルで）

```bash
# フロントエンドディレクトリに移動
cd C:\Users\nnkre\projects\seo-analyzer-tool\frontend

# 依存関係インストール
npm install

# 開発サーバー起動
npm run dev
```

フロントエンドが起動したら: `http://localhost:5173`

## アクセス

- **フロントエンド**: http://localhost:5173
- **バックエンドAPI**: http://localhost:8000
- **APIドキュメント**: http://localhost:8000/docs

## トラブルシューティング

### Python仮想環境が作成できない
```bash
# pipを最新化
python -m pip install --upgrade pip
```

### npm installでエラー
```bash
# キャッシュクリア
npm cache clean --force
npm install
```

### ポートが使用中
- バックエンド: `run.py`の8000を8001に変更
- フロントエンド: `vite.config.js`の5173を別のポートに変更

## Docker Desktopを起動する場合

Docker Desktopを起動してから：

```bash
cd C:\Users\nnkre\projects\seo-analyzer-tool
docker-compose up -d
```

アクセス:
- **フロントエンド**: http://localhost
- **バックエンド**: http://localhost:8000
