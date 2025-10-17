# クイックスタートガイド - 5分で完全無料デプロイ

このガイドに従えば、5分でSEO Analyzer Toolを完全無料でデプロイできます。

## 🚀 超簡単！自動デプロイ

### Windows の場合

1. **このフォルダで右クリック → Git Bash Here**

2. **自動デプロイスクリプトを実行:**
```bash
./deploy.sh
```

または、コマンドプロンプトで:
```cmd
deploy.bat
```

3. **画面の指示に従って進めるだけ！**

---

## 📋 事前準備（初回のみ）

### 1. GitHubアカウント
- https://github.com でアカウント作成
- 新しいリポジトリを作成: `seo-analyzer-tool`

### 2. Supabase（無料データベース）

1. https://supabase.com にアクセス
2. 「Start your project」→ GitHubでサインアップ
3. 「New Project」をクリック
4. 設定:
   - Name: `seo-analyzer`
   - Password: 自動生成（コピーして保存）
   - Region: `Tokyo`
   - Plan: `Free`
5. 「Create project」クリック（2-3分待つ）

6. **テーブル作成:**
   - SQL Editor を開く
   - `VERCEL_SUPABASE_DEPLOYMENT.md` の Part 1-3 のSQLをコピー
   - 実行

7. **接続文字列をコピー:**
   - Settings → Database
   - Connection string の `URI` をコピー

### 3. Vercel（無料ホスティング）

1. https://vercel.com にアクセス
2. 「Sign Up」→ GitHubで連携
3. （デプロイスクリプトが自動で設定します）

### 4. Gemini API Key（無料）

1. https://aistudio.google.com/app/apikey にアクセス
2. 「Get API key」→ 「Create API key」
3. APIキーをコピー

---

## ⚡ 自動デプロイの流れ

スクリプトを実行すると、以下が自動的に行われます:

1. ✅ Git/Node.jsのチェック
2. ✅ Gitリポジトリの初期化
3. ✅ GitHubリモートの設定
4. ✅ Vercel CLIのインストール
5. ✅ 環境変数ファイルの作成
6. ✅ Frontendのビルドテスト
7. ✅ GitHubへのプッシュ
8. ✅ Vercelへのデプロイ

**あなたがやることは質問に答えるだけ！**

---

## 🔐 環境変数の設定

スクリプト実行中に `backend/.env.production` の編集を求められます。

以下を設定してください:

```bash
# Supabaseの接続文字列（Step 2-7でコピーしたもの）
DATABASE_URL=postgresql://postgres:[PASSWORD]@[HOST]:5432/postgres

# Gemini API Key（Step 4でコピーしたもの）
GEMINI_API_KEY=あなたのAPIキー

# ランダムな文字列を生成（PowerShellで）
# -Length 32 | ConvertTo-SecureString -AsPlainText -Force | ConvertFrom-SecureString
SECRET_KEY=ランダムな長い文字列

# ドメイン（後で変更可能）
ALLOWED_ORIGINS=https://alno-ai.net,https://seo-analyzer-tool.vercel.app
```

---

## 🌐 カスタムドメイン設定（alno-ai.net）

デプロイ完了後:

### 1. Vercelでドメイン追加

1. https://vercel.com/dashboard を開く
2. プロジェクトを選択
3. Settings → Domains
4. `alno-ai.net` を入力
5. DNS設定情報が表示される

### 2. XserverでDNS設定

1. Xserver サーバーパネルにログイン
2. DNSレコード設定 → `alno-ai.net`
3. Aレコードを追加:
   - ホスト名: `@`
   - 値: `76.76.21.21`
4. CNAMEレコードを追加:
   - ホスト名: `www`
   - 値: `cname.vercel-dns.com`

**数分〜24時間で反映！**

---

## ✅ 動作確認

1. https://your-project.vercel.app にアクセス
2. サイトを登録
3. SEO分析を実行
4. AI分析結果を確認

---

## 🔄 コードを更新したら

```bash
# 自動デプロイスクリプトを実行するだけ！
./deploy.sh   # または deploy.bat
```

→ GitHub Actions が自動的にVercelへデプロイ

---

## ❓ トラブルシューティング

### Git/Node.jsがない

**Git:**
- Windows: https://git-scm.com/download/win
- Mac: `brew install git`

**Node.js:**
- https://nodejs.org/ から LTS 版をインストール

### デプロイエラー

```bash
# ローカルでテスト
cd frontend
npm install
npm run build

cd ../backend
pip install -r requirements.txt
```

### データベース接続エラー

- Supabaseの接続文字列を再確認
- パスワードに特殊文字がある場合はURLエンコード

---

## 📞 サポート

問題があれば:
1. `VERCEL_SUPABASE_DEPLOYMENT.md` の詳細ガイドを確認
2. GitHub Issues で質問

---

## 🎉 完了！

**おめでとうございます！**

完全無料のプロダクション環境が完成しました🚀

- Frontend + Backend: Vercel
- Database: Supabase  
- AI分析: Google Gemini
- **合計: 0円/月**

楽しんでください！
