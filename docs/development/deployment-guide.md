# 開発・デプロイ手順書

## 概要

工場設備管理アプリケーションの開発環境構築からプロダクション環境へのデプロイまでの全手順を説明します。

## 開発環境構築

### 前提条件

以下のツールがインストールされていることを確認してください：

```bash
# Node.js バージョン確認
node --version  # v16.x 以上

# Python バージョン確認
python --version  # 3.9 以上

# Azure CLI バージョン確認
az --version

# Git バージョン確認
git --version
```

### 必要なツールのインストール

#### 1. Node.js および npm

```bash
# Windows (PowerShell)
winget install OpenJS.NodeJS

# macOS (Homebrew)
brew install node

# Linux (Ubuntu)
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt-get install -y nodejs
```

#### 2. Python

```bash
# Windows (PowerShell)
winget install Python.Python.3.9

# macOS (Homebrew)
brew install python@3.9

# Linux (Ubuntu)
sudo apt update
sudo apt install python3.9 python3.9-venv python3.9-pip
```

#### 3. Azure CLI

```bash
# Windows (PowerShell)
winget install Microsoft.AzureCLI

# macOS (Homebrew)
brew install azure-cli

# Linux (Ubuntu)
curl -sL https://aka.ms/InstallAzureCLIDeb | sudo bash
```

#### 4. Azure Functions Core Tools

```bash
# npm経由でインストール（全プラットフォーム共通）
npm install -g azure-functions-core-tools@4 --unsafe-perm true
```

#### 5. Vue CLI（オプション）

```bash
# Vue CLI のインストール
npm install -g @vue/cli
```

## プロジェクトセットアップ

### 1. リポジトリのクローン

```bash
# リポジトリをクローン
git clone https://github.com/gh-user-2025/agent-poc.git
cd agent-poc
```

### 2. フロントエンド開発環境

```bash
# 依存関係のインストール
npm install

# 開発サーバーの起動
npm run serve

# ビルド（プロダクション用）
npm run build

# コードのリント
npm run lint
```

**利用可能なスクリプト:**
- `npm run serve` - 開発サーバー起動（http://localhost:8080）
- `npm run build` - プロダクションビルド
- `npm run lint` - ESLint によるコード検査

### 3. バックエンド開発環境

```bash
# Azure Functions ディレクトリに移動
cd azure-functions

# Python仮想環境の作成
python -m venv venv

# 仮想環境の有効化
# Linux/macOS:
source venv/bin/activate
# Windows:
venv\Scripts\activate

# 依存関係のインストール
pip install -r requirements.txt

# ローカル設定ファイルの作成
cp local.settings.json.template local.settings.json
# エディタで接続文字列等を設定

# Functions の起動
func start
```

## 開発ワークフロー

### 1. 機能開発フロー

```bash
# 新機能ブランチの作成
git checkout -b feature/new-feature-name

# 開発作業
# ... コーディング ...

# 変更をステージング
git add .

# コミット
git commit -m "feat: 新機能の説明"

# リモートにプッシュ
git push origin feature/new-feature-name

# GitHubでプルリクエスト作成
```

### 2. コミットメッセージ規約

```
feat: 新機能
fix: バグ修正
docs: ドキュメント変更
style: コードスタイル変更
refactor: リファクタリング
test: テスト追加・修正
chore: その他の変更
```

### 3. ブランチ戦略

```
main          - 本番環境用ブランチ
develop       - 開発統合ブランチ
feature/*     - 機能開発ブランチ
bugfix/*      - バグ修正ブランチ
release/*     - リリース準備ブランチ
hotfix/*      - 緊急修正ブランチ
```

## テスト

### 1. フロントエンドテスト

```bash
# ユニットテスト実行（将来実装予定）
npm run test:unit

# E2Eテスト実行（将来実装予定）
npm run test:e2e
```

### 2. バックエンドテスト

```bash
cd azure-functions

# ユニットテスト実行
python -m pytest tests/

# カバレッジレポート生成
python -m pytest --cov=. tests/
```

### 3. API テスト

```bash
# 設備監視API テスト
curl -X POST http://localhost:7071/api/equipment/monitoring \
  -H "Content-Type: application/json" \
  -d '{
    "equipment_id": "A1",
    "timestamp": "2024-01-15T10:00:00Z",
    "status": "operational",
    "efficiency": 85,
    "temperature": 165
  }'

# メンテナンス管理API テスト
curl -X GET http://localhost:7071/api/maintenance

# データ分析API テスト
curl -X GET "http://localhost:7071/api/analytics?type=overview&period=week"
```

## デプロイメント

### 1. Azure リソースの準備

```bash
# Azure リソース作成スクリプトの実行
cd docs/azure-setup
bash create-azure-resources.sh
```

### 2. Azure Functions デプロイ

```bash
cd azure-functions

# Azure にログイン
az login
func azure login

# Function App にデプロイ
func azure functionapp publish your-function-app-name
```

### 3. フロントエンドデプロイ

#### Azure Static Web Apps を使用

```bash
# Azure Static Web Apps 作成
az staticwebapp create \
  --name factory-management-frontend \
  --resource-group factory-management-rg \
  --source https://github.com/gh-user-2025/agent-poc \
  --location "East Asia" \
  --branch main \
  --app-location "/" \
  --output-location "dist"
```

#### または Azure Blob Storage + CDN

```bash
# ビルド
npm run build

# Azure Storage にアップロード
az storage blob upload-batch \
  --source dist \
  --destination '$web' \
  --account-name your-storage-account
```

## CI/CD パイプライン設定

### 1. GitHub Actions ワークフロー

`.github/workflows/ci-cd.yml` を作成:

```yaml
name: CI/CD Pipeline

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  test-frontend:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    - name: Setup Node.js
      uses: actions/setup-node@v3
      with:
        node-version: '18'
    - name: Install dependencies
      run: npm install
    - name: Run tests
      run: npm run test:unit
    - name: Build
      run: npm run build

  test-backend:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    - name: Setup Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.9'
    - name: Install dependencies
      run: |
        cd azure-functions
        pip install -r requirements.txt
    - name: Run tests
      run: |
        cd azure-functions
        python -m pytest tests/

  deploy-staging:
    needs: [test-frontend, test-backend]
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/develop'
    steps:
    - uses: actions/checkout@v3
    - name: Deploy to staging
      run: echo "Deploy to staging environment"

  deploy-production:
    needs: [test-frontend, test-backend]
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    steps:
    - uses: actions/checkout@v3
    - name: Deploy to production
      run: echo "Deploy to production environment"
```

### 2. 環境別設定

#### 開発環境 (Development)
```bash
# 環境変数設定
export NODE_ENV=development
export VUE_APP_API_BASE_URL=http://localhost:7071/api
export VUE_APP_ENVIRONMENT=development
```

#### ステージング環境 (Staging)
```bash
# 環境変数設定
export NODE_ENV=staging
export VUE_APP_API_BASE_URL=https://your-staging-functions.azurewebsites.net/api
export VUE_APP_ENVIRONMENT=staging
```

#### 本番環境 (Production)
```bash
# 環境変数設定
export NODE_ENV=production
export VUE_APP_API_BASE_URL=https://your-production-functions.azurewebsites.net/api
export VUE_APP_ENVIRONMENT=production
```

## 運用・監視

### 1. ログ監視

```bash
# Azure Functions ログ確認
az webapp log tail \
  --name your-function-app-name \
  --resource-group factory-management-rg

# Application Insights クエリ
az monitor app-insights query \
  --app your-app-insights-name \
  --analytics-query "requests | top 10 by timestamp desc"
```

### 2. パフォーマンス監視

```bash
# Function App メトリクス確認
az monitor metrics list \
  --resource /subscriptions/{subscription-id}/resourceGroups/factory-management-rg/providers/Microsoft.Web/sites/your-function-app-name \
  --metric "FunctionExecutionCount"
```

### 3. アラート設定

```bash
# CPU 使用率アラート作成
az monitor metrics alert create \
  --name "High CPU Usage" \
  --resource-group factory-management-rg \
  --scopes /subscriptions/{subscription-id}/resourceGroups/factory-management-rg/providers/Microsoft.Web/sites/your-function-app-name \
  --condition "avg Percentage CPU > 80" \
  --description "Function App CPU usage is high"
```

## トラブルシューティング

### よくある問題と解決方法

#### 1. npm install エラー

```bash
# キャッシュクリア
npm cache clean --force

# node_modules削除して再インストール
rm -rf node_modules package-lock.json
npm install
```

#### 2. Azure Functions 起動エラー

```bash
# Python仮想環境の確認
which python
pip list

# 依存関係の再インストール
pip install -r requirements.txt --force-reinstall
```

#### 3. デプロイエラー

```bash
# Azure CLI 再ログイン
az login --use-device-code

# Function App 設定確認
az functionapp config show \
  --name your-function-app-name \
  --resource-group factory-management-rg
```

### 4. パフォーマンス問題

```bash
# フロントエンドバンドルサイズ確認
npm run build -- --report

# Azure Functions 実行時間確認
az monitor app-insights query \
  --app your-app-insights-name \
  --analytics-query "requests | summarize avg(duration) by name"
```

## コード品質管理

### 1. ESLint 設定

`.eslintrc.js`:
```javascript
module.exports = {
  root: true,
  env: {
    node: true
  },
  extends: [
    'plugin:vue/vue3-essential',
    'eslint:recommended'
  ],
  parserOptions: {
    parser: '@babel/eslint-parser'
  },
  rules: {
    'no-console': process.env.NODE_ENV === 'production' ? 'warn' : 'off',
    'no-debugger': process.env.NODE_ENV === 'production' ? 'warn' : 'off'
  }
}
```

### 2. Prettier 設定

`.prettierrc`:
```json
{
  "semi": false,
  "singleQuote": true,
  "tabWidth": 2,
  "trailingComma": "none",
  "printWidth": 80
}
```

### 3. pre-commit フック

```bash
# husky インストール
npm install --save-dev husky

# pre-commit フック設定
npx husky add .husky/pre-commit "npm run lint"
```

## セキュリティ

### 1. 依存関係の脆弱性チェック

```bash
# npm audit
npm audit

# 修正可能な脆弱性の自動修正
npm audit fix
```

### 2. 環境変数管理

```bash
# .env ファイル（git管理対象外）
VUE_APP_API_BASE_URL=https://your-api-domain.com/api
VUE_APP_APP_INSIGHTS_INSTRUMENTATION_KEY=your-key
```

### 3. Azure Key Vault 連携

```bash
# Key Vault から秘密情報取得
az keyvault secret show \
  --name api-key \
  --vault-name your-keyvault-name \
  --query value -o tsv
```

## 参考資料

- [Vue.js ドキュメント](https://v3.ja.vuejs.org/)
- [Azure Functions Python ガイド](https://docs.microsoft.com/ja-jp/azure/azure-functions/functions-reference-python)
- [Azure Static Web Apps ドキュメント](https://docs.microsoft.com/ja-jp/azure/static-web-apps/)
- [GitHub Actions ドキュメント](https://docs.github.com/ja/actions)

## 次のステップ

1. **テストカバレッジの向上**
   - ユニットテストの追加
   - 統合テストの実装

2. **セキュリティ強化**
   - 認証・認可の実装
   - API レート制限

3. **パフォーマンス最適化**
   - CDN の活用
   - 画像最適化

4. **監視・運用の強化**
   - より詳細なメトリクス収集
   - 自動復旧メカニズムの実装