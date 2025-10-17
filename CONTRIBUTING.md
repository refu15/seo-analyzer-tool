# 貢献ガイド

SEO Analyzer Toolへの貢献ありがとうございます！

## 開発フロー

1. **Fork & Clone**
   ```bash
   git clone https://github.com/yourusername/seo-analyzer-tool.git
   cd seo-analyzer-tool
   ```

2. **ブランチ作成**
   ```bash
   git checkout -b feature/your-feature-name
   ```

3. **開発**
   - バックエンド: `backend/` ディレクトリ
   - フロントエンド: `frontend/` ディレクトリ
   - コーディング規約に従う

4. **テスト**
   ```bash
   # バックエンド
   cd backend && pytest

   # フロントエンド（今後追加予定）
   cd frontend && npm test
   ```

5. **コミット**
   ```bash
   git add .
   git commit -m "feat: add amazing feature"
   ```

   コミットメッセージ形式:
   - `feat:` - 新機能
   - `fix:` - バグ修正
   - `docs:` - ドキュメント
   - `style:` - フォーマット
   - `refactor:` - リファクタリング
   - `test:` - テスト追加
   - `chore:` - その他

6. **プッシュ & PR**
   ```bash
   git push origin feature/your-feature-name
   ```
   GitHubでプルリクエストを作成

## コーディング規約

### Python (Backend)
- PEP 8 準拠
- Black でフォーマット
- Type hints 使用推奨
- Docstring 記述（Google形式）

### JavaScript/React (Frontend)
- ESLint 規約準拠
- 関数コンポーネント使用
- PropTypes または TypeScript（将来）
- わかりやすい変数名

## プルリクエスト要件

- [ ] 機能が正しく動作する
- [ ] テストが通る
- [ ] ドキュメント更新済み
- [ ] コード品質チェック通過
- [ ] 破壊的変更の場合は説明

## 質問・議論

- [Discussions](https://github.com/yourusername/seo-analyzer-tool/discussions) で質問
- [Issues](https://github.com/yourusername/seo-analyzer-tool/issues) でバグ報告

ありがとうございます！
