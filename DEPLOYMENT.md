# SEO Analyzer Tool - デプロイメントガイド

本番環境へのデプロイ手順を説明します。

## 前提条件

- Docker & Docker Compose がインストールされていること
- ドメイン名を取得していること（オプション：SSL証明書用）
- 必要なAPIキーを取得していること
  - Google Gemini API Key
  - Google PageSpeed API Key（オプション）

## 1. 本番環境用設定ファイルの準備

### Backend環境変数

```bash
cd backend
cp .env.production.example .env.production
```

`.env.production` を編集して、以下の値を設定：

```bash
# 必須項目
GEMINI_API_KEY=あなたのGemini APIキー

# セキュリティ - 必ず変更してください
SECRET_KEY=ランダムな長い文字列を生成

# CORS - 本番ドメインに変更
ALLOWED_ORIGINS=https://yourdomain.com

# デバッグモードをオフに
DEBUG=False
```

**セキュアなSECRET_KEYの生成方法:**

```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

### Frontend環境変数（オプション）

```bash
cd frontend
cp .env.example .env.production
```

`.env.production` を編集：

```bash
VITE_API_URL=https://yourdomain.com/api
```

## 2. Dockerでのデプロイ

### 開発環境でテスト

```bash
# プロジェクトルートで実行
docker-compose up --build
```

- Frontend: http://localhost
- Backend API: http://localhost:8000

### 本番環境でデプロイ

```bash
# 本番用docker-composeを使用
docker-compose -f docker-compose.prod.yml up -d --build
```

### デプロイの確認

```bash
# コンテナの状態確認
docker-compose -f docker-compose.prod.yml ps

# ログの確認
docker-compose -f docker-compose.prod.yml logs -f
```

## 3. SSL証明書の設定（HTTPS化）

### Let's Encryptを使用した無料SSL証明書

1. Certbotのインストール:

```bash
sudo apt-get update
sudo apt-get install certbot python3-certbot-nginx
```

2. SSL証明書の取得:

```bash
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com
```

3. 自動更新の設定:

```bash
sudo certbot renew --dry-run
```

### nginxのSSL設定

`frontend/nginx.conf` を編集してHTTPSリダイレクトを追加：

```nginx
server {
    listen 80;
    server_name yourdomain.com;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name yourdomain.com;

    ssl_certificate /etc/nginx/ssl/cert.pem;
    ssl_certificate_key /etc/nginx/ssl/key.pem;

    # ... 残りの設定
}
```

## 4. データベースのバックアップ

### 自動バックアップスクリプト

```bash
#!/bin/bash
# backup.sh

BACKUP_DIR="/path/to/backups"
DATE=$(date +%Y%m%d_%H%M%S)

docker cp seo-analyzer-backend-prod:/app/data/seo_analyzer.db \
  $BACKUP_DIR/seo_analyzer_$DATE.db

# 7日以上古いバックアップを削除
find $BACKUP_DIR -name "seo_analyzer_*.db" -mtime +7 -delete
```

### Cronで定期実行

```bash
# 毎日午前3時にバックアップ
0 3 * * * /path/to/backup.sh
```

## 5. モニタリングとログ

### ログの確認

```bash
# Backend ログ
docker logs seo-analyzer-backend-prod -f

# Frontend ログ
docker logs seo-analyzer-frontend-prod -f
```

### ヘルスチェック

```bash
# Backend ヘルスチェック
curl http://localhost:8000/health

# Frontend ヘルスチェック
curl http://localhost/health
```

## 6. アップデートとメンテナンス

### アプリケーションの更新

```bash
# 最新のコードを取得
git pull origin main

# コンテナの再ビルドと再起動
docker-compose -f docker-compose.prod.yml down
docker-compose -f docker-compose.prod.yml up -d --build
```

### データベースのマイグレーション

```bash
# Backendコンテナに入る
docker exec -it seo-analyzer-backend-prod bash

# マイグレーション実行（必要に応じて）
alembic upgrade head
```

## 7. トラブルシューティング

### コンテナが起動しない

```bash
# ログを確認
docker-compose -f docker-compose.prod.yml logs

# コンテナの状態を確認
docker ps -a
```

### データベースエラー

```bash
# データベースファイルのパーミッション確認
docker exec seo-analyzer-backend-prod ls -la /app/data
```

### API接続エラー

1. CORS設定を確認
2. Backend URLが正しいか確認
3. ファイアウォール設定を確認

## 8. セキュリティチェックリスト

- [ ] SECRET_KEYを本番用のランダムな値に変更
- [ ] DEBUG=Falseに設定
- [ ] HTTPS（SSL/TLS）を有効化
- [ ] CORS設定を本番ドメインに限定
- [ ] 定期的なバックアップを設定
- [ ] ファイアウォールで不要なポートを閉鎖
- [ ] 定期的なセキュリティアップデート

## 9. パフォーマンス最適化

### nginxキャッシング

```nginx
# 静的ファイルのキャッシュ
location ~* \.(jpg|jpeg|png|gif|ico|css|js)$ {
    expires 1y;
    add_header Cache-Control "public, immutable";
}
```

### Gzip圧縮

```nginx
gzip on;
gzip_vary on;
gzip_min_length 1024;
gzip_types text/plain text/css text/xml text/javascript application/javascript application/json;
```

## サポート

問題が発生した場合は、GitHubのIssuesでお知らせください。
