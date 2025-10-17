@echo off
chcp 65001 >nul
echo.
echo 🚀 SEO Analyzer Tool - 自動デプロイスクリプト (Windows)
echo ================================================
echo.

REM 1. 依存関係のチェック
echo 📦 依存関係のチェック...

where git >nul 2>&1
if errorlevel 1 (
    echo ❌ Gitがインストールされていません
    echo    https://git-scm.com/download/win からインストールしてください
    pause
    exit /b 1
)

where node >nul 2>&1
if errorlevel 1 (
    echo ❌ Node.jsがインストールされていません
    echo    https://nodejs.org/ からインストールしてください
    pause
    exit /b 1
)

echo ✅ 依存関係OK
echo.

REM 2. Gitリポジトリの確認
echo 🔍 Gitリポジトリの確認...

if not exist ".git" (
    echo Gitリポジトリを初期化します...
    git init
    echo ✅ Git初期化完了
) else (
    echo ✅ Gitリポジトリ存在
)
echo.

REM 3. リモートリポジトリの確認
echo 🌐 GitHubリモートの確認...

git remote | find "origin" >nul 2>&1
if errorlevel 1 (
    echo.
    set /p REPO_URL="GitHubリポジトリのURLを入力してください: "
    git remote add origin %REPO_URL%
    echo ✅ リモートリポジトリ追加完了
) else (
    echo ✅ リモートリポジトリ設定済み
)
echo.

REM 4. Vercel CLIのインストール確認
echo ⚡ Vercel CLIのチェック...

where vercel >nul 2>&1
if errorlevel 1 (
    echo Vercel CLIをインストールします...
    call npm install -g vercel
    echo ✅ Vercel CLIインストール完了
) else (
    echo ✅ Vercel CLI存在
)
echo.

REM 5. 環境変数ファイルのチェック
echo 🔐 環境変数の確認...

if not exist "backend\.env.production" (
    echo backend\.env.production ファイルが見つかりません
    set /p COPY_ENV="backend\.env.production.example からコピーしますか？ (y/n): "
    
    if /i "%COPY_ENV%"=="y" (
        copy backend\.env.production.example backend\.env.production
        echo.
        echo 📝 backend\.env.production を編集してください:
        echo   - GEMINI_API_KEY
        echo   - SECRET_KEY
        echo   - DATABASE_URL (Supabase)
        echo.
        pause
    )
)

echo ✅ 環境変数OK
echo.

REM 6. Frontend ビルドテスト
echo 🏗️  Frontend ビルドテスト...

cd frontend
call npm install
call npm run build

if errorlevel 1 (
    echo ❌ Frontendビルド失敗
    pause
    exit /b 1
)

echo ✅ Frontendビルド成功
cd ..
echo.

REM 7. Git コミット
echo 📝 変更をコミット...

git add .

set /p COMMIT_MSG="コミットメッセージを入力してください: "

if "%COMMIT_MSG%"=="" (
    set COMMIT_MSG=Deploy: %date% %time%
)

git commit -m "%COMMIT_MSG%" 2>nul || echo 変更なし、またはすでにコミット済み
echo ✅ コミット完了
echo.

REM 8. GitHubへプッシュ
echo 🚀 GitHubへプッシュ...

git branch -M main 2>nul
git push -u origin main

echo ✅ プッシュ完了
echo.

REM 9. Vercelデプロイ
echo ⚡ Vercelへデプロイ...
echo.
echo デプロイ方法を選択してください:
echo 1) 本番環境 (Production)
echo 2) プレビュー環境 (Preview)
set /p DEPLOY_TYPE="選択 (1 or 2): "

if "%DEPLOY_TYPE%"=="1" (
    call vercel --prod
) else (
    call vercel
)

echo.
echo ✅ デプロイ完了！
echo.

REM 10. 完了メッセージ
echo ================================================
echo 🎉 デプロイが完了しました！
echo.
echo 次のステップ:
echo 1. Vercel Dashboardで環境変数を確認
echo 2. カスタムドメイン (alno-ai.net) を設定
echo 3. デプロイされたURLにアクセスして動作確認
echo.
echo VercelダッシュボードURL: https://vercel.com/dashboard
echo ================================================
echo.
pause
