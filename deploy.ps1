# SEO Analyzer Tool - 自動デプロイスクリプト (PowerShell)

Write-Host ""
Write-Host "🚀 SEO Analyzer Tool - 自動デプロイスクリプト (PowerShell)" -ForegroundColor Cyan
Write-Host "================================================" -ForegroundColor Cyan
Write-Host ""

# 1. 依存関係のチェック
Write-Host "📦 依存関係のチェック..." -ForegroundColor Blue

# Git のチェック
try {
    git --version | Out-Null
    Write-Host "✅ Git存在" -ForegroundColor Green
} catch {
    Write-Host "❌ Gitがインストールされていません" -ForegroundColor Red
    Write-Host "   https://git-scm.com/download/win からインストールしてください" -ForegroundColor Yellow
    pause
    exit 1
}

# Node.js のチェック
try {
    node --version | Out-Null
    Write-Host "✅ Node.js存在" -ForegroundColor Green
} catch {
    Write-Host "❌ Node.jsがインストールされていません" -ForegroundColor Red
    Write-Host "   https://nodejs.org/ からインストールしてください" -ForegroundColor Yellow
    pause
    exit 1
}

Write-Host ""

# 2. Gitリポジトリの確認
Write-Host "🔍 Gitリポジトリの確認..." -ForegroundColor Blue

if (-not (Test-Path ".git")) {
    Write-Host "Gitリポジトリを初期化します..." -ForegroundColor Yellow
    git init
    Write-Host "✅ Git初期化完了" -ForegroundColor Green
} else {
    Write-Host "✅ Gitリポジトリ存在" -ForegroundColor Green
}

Write-Host ""

# 3. リモートリポジトリの確認
Write-Host "🌐 GitHubリモートの確認..." -ForegroundColor Blue

$remotes = git remote
if ($remotes -notcontains "origin") {
    Write-Host ""
    $repoUrl = Read-Host "GitHubリポジトリのURLを入力してください"
    git remote add origin $repoUrl
    Write-Host "✅ リモートリポジトリ追加完了" -ForegroundColor Green
} else {
    Write-Host "✅ リモートリポジトリ設定済み" -ForegroundColor Green
}

Write-Host ""

# 4. Vercel CLIのインストール確認
Write-Host "⚡ Vercel CLIのチェック..." -ForegroundColor Blue

try {
    vercel --version | Out-Null
    Write-Host "✅ Vercel CLI存在" -ForegroundColor Green
} catch {
    Write-Host "Vercel CLIをインストールします..." -ForegroundColor Yellow
    npm install -g vercel
    Write-Host "✅ Vercel CLIインストール完了" -ForegroundColor Green
}

Write-Host ""

# 5. 環境変数ファイルのチェック
Write-Host "🔐 環境変数の確認..." -ForegroundColor Blue

if (-not (Test-Path "backend\.env.production")) {
    Write-Host "backend\.env.production ファイルが見つかりません" -ForegroundColor Yellow
    $copyEnv = Read-Host "backend\.env.production.example からコピーしますか？ (y/n)"
    
    if ($copyEnv -eq "y") {
        Copy-Item "backend\.env.production.example" "backend\.env.production"
        Write-Host ""
        Write-Host "📝 backend\.env.production を編集してください:" -ForegroundColor Yellow
        Write-Host "  - GEMINI_API_KEY" -ForegroundColor Cyan
        Write-Host "  - SECRET_KEY" -ForegroundColor Cyan
        Write-Host "  - DATABASE_URL (Supabase)" -ForegroundColor Cyan
        Write-Host ""
        Read-Host "編集が完了したら Enter を押してください"
    }
}

Write-Host "✅ 環境変数OK" -ForegroundColor Green
Write-Host ""

# 6. Frontend ビルドテスト
Write-Host "🏗️  Frontend ビルドテスト..." -ForegroundColor Blue

Push-Location frontend
npm install
npm run build

if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Frontendビルド成功" -ForegroundColor Green
} else {
    Write-Host "❌ Frontendビルド失敗" -ForegroundColor Red
    Pop-Location
    pause
    exit 1
}

Pop-Location
Write-Host ""

# 7. Git コミット
Write-Host "📝 変更をコミット..." -ForegroundColor Blue

git add .

$commitMsg = Read-Host "コミットメッセージを入力してください"

if ([string]::IsNullOrWhiteSpace($commitMsg)) {
    $commitMsg = "Deploy: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')"
}

git commit -m $commitMsg 2>&1 | Out-Null
Write-Host "✅ コミット完了" -ForegroundColor Green
Write-Host ""

# 8. GitHubへプッシュ
Write-Host "🚀 GitHubへプッシュ..." -ForegroundColor Blue

git branch -M main 2>&1 | Out-Null
git push -u origin main

Write-Host "✅ プッシュ完了" -ForegroundColor Green
Write-Host ""

# 9. Vercelデプロイ
Write-Host "⚡ Vercelへデプロイ..." -ForegroundColor Blue
Write-Host ""
Write-Host "デプロイ方法を選択してください:" -ForegroundColor Yellow
Write-Host "1) 本番環境 (Production)" -ForegroundColor Cyan
Write-Host "2) プレビュー環境 (Preview)" -ForegroundColor Cyan
$deployType = Read-Host "選択 (1 or 2)"

if ($deployType -eq "1") {
    vercel --prod
} else {
    vercel
}

Write-Host ""
Write-Host "✅ デプロイ完了！" -ForegroundColor Green
Write-Host ""

# 10. 完了メッセージ
Write-Host "================================================" -ForegroundColor Cyan
Write-Host "🎉 デプロイが完了しました！" -ForegroundColor Green
Write-Host ""
Write-Host "次のステップ:" -ForegroundColor Yellow
Write-Host "1. Vercel Dashboardで環境変数を確認"
Write-Host "2. カスタムドメイン (alno-ai.net) を設定"
Write-Host "3. デプロイされたURLにアクセスして動作確認"
Write-Host ""
Write-Host "VercelダッシュボードURL: https://vercel.com/dashboard" -ForegroundColor Cyan
Write-Host "================================================" -ForegroundColor Cyan
Write-Host ""
pause
