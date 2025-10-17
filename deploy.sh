#!/bin/bash

echo "🚀 SEO Analyzer Tool - 自動デプロイスクリプト"
echo "================================================"
echo ""

# 色の定義
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# エラーハンドリング
set -e

# 1. 依存関係のチェック
echo -e "${BLUE}📦 依存関係のチェック...${NC}"

if ! command -v git &> /dev/null; then
    echo -e "${RED}❌ Gitがインストールされていません${NC}"
    exit 1
fi

if ! command -v node &> /dev/null; then
    echo -e "${RED}❌ Node.jsがインストールされていません${NC}"
    exit 1
fi

echo -e "${GREEN}✅ 依存関係OK${NC}"
echo ""

# 2. GitHubリポジトリの確認
echo -e "${BLUE}🔍 Gitリポジトリの確認...${NC}"

if [ ! -d ".git" ]; then
    echo "Gitリポジトリを初期化します..."
    git init
    echo -e "${GREEN}✅ Git初期化完了${NC}"
else
    echo -e "${GREEN}✅ Gitリポジトリ存在${NC}"
fi

echo ""

# 3. リモートリポジトリの設定確認
echo -e "${BLUE}🌐 GitHubリモートの確認...${NC}"

if ! git remote | grep -q origin; then
    echo ""
    echo "GitHubリポジトリのURLを入力してください:"
    echo "（例: https://github.com/username/seo-analyzer-tool.git）"
    read -r REPO_URL
    git remote add origin "$REPO_URL"
    echo -e "${GREEN}✅ リモートリポジトリ追加完了${NC}"
else
    echo -e "${GREEN}✅ リモートリポジトリ設定済み${NC}"
fi

echo ""

# 4. Vercel CLIのインストール確認
echo -e "${BLUE}⚡ Vercel CLIのチェック...${NC}"

if ! command -v vercel &> /dev/null; then
    echo "Vercel CLIをインストールします..."
    npm install -g vercel
    echo -e "${GREEN}✅ Vercel CLIインストール完了${NC}"
else
    echo -e "${GREEN}✅ Vercel CLI存在${NC}"
fi

echo ""

# 5. 環境変数ファイルのチェック
echo -e "${BLUE}🔐 環境変数の確認...${NC}"

if [ ! -f "backend/.env.production" ]; then
    echo "backend/.env.production ファイルが見つかりません"
    echo "backend/.env.production.example からコピーしますか？ (y/n)"
    read -r COPY_ENV
    
    if [ "$COPY_ENV" = "y" ]; then
        cp backend/.env.production.example backend/.env.production
        echo -e "${BLUE}📝 backend/.env.production を編集してください:${NC}"
        echo "  - GEMINI_API_KEY"
        echo "  - SECRET_KEY"
        echo "  - DATABASE_URL (Supabase)"
        echo ""
        echo "編集が完了したら Enter を押してください..."
        read -r
    fi
fi

echo -e "${GREEN}✅ 環境変数OK${NC}"
echo ""

# 6. Frontend ビルドテスト
echo -e "${BLUE}🏗️  Frontend ビルドテスト...${NC}"

cd frontend
npm install
npm run build

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ Frontendビルド成功${NC}"
else
    echo -e "${RED}❌ Frontendビルド失敗${NC}"
    exit 1
fi

cd ..
echo ""

# 7. Git コミット
echo -e "${BLUE}📝 変更をコミット...${NC}"

git add .

echo "コミットメッセージを入力してください:"
read -r COMMIT_MSG

if [ -z "$COMMIT_MSG" ]; then
    COMMIT_MSG="Deploy: $(date +%Y-%m-%d\ %H:%M:%S)"
fi

git commit -m "$COMMIT_MSG" || echo "変更なし、またはすでにコミット済み"
echo -e "${GREEN}✅ コミット完了${NC}"
echo ""

# 8. GitHubへプッシュ
echo -e "${BLUE}🚀 GitHubへプッシュ...${NC}"

CURRENT_BRANCH=$(git branch --show-current)

if [ -z "$CURRENT_BRANCH" ]; then
    CURRENT_BRANCH="main"
    git branch -M main
fi

git push -u origin $CURRENT_BRANCH

echo -e "${GREEN}✅ プッシュ完了${NC}"
echo ""

# 9. Vercelデプロイ
echo -e "${BLUE}⚡ Vercelへデプロイ...${NC}"
echo ""
echo "デプロイ方法を選択してください:"
echo "1) 本番環境 (Production)"
echo "2) プレビュー環境 (Preview)"
read -r DEPLOY_TYPE

if [ "$DEPLOY_TYPE" = "1" ]; then
    vercel --prod
else
    vercel
fi

echo ""
echo -e "${GREEN}✅ デプロイ完了！${NC}"
echo ""

# 10. 完了メッセージ
echo "================================================"
echo -e "${GREEN}🎉 デプロイが完了しました！${NC}"
echo ""
echo "次のステップ:"
echo "1. Vercel Dashboardで環境変数を確認"
echo "2. カスタムドメイン (alno-ai.net) を設定"
echo "3. デプロイされたURLにアクセスして動作確認"
echo ""
echo "VercelダッシュボURL: https://vercel.com/dashboard"
echo "================================================"
