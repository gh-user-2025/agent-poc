# Azure Functions デプロイ手順

## 概要

Azure Functions プロジェクトをAzureにデプロイする手順を説明します。

## 前提条件

- Azure リソースが作成済みであること（azure-resources-setup.md を参照）
- Azure Functions Core Tools がインストールされていること
- Python 3.9 以上がインストールされていること

## Azure Functions Core Tools のインストール

### Windows (PowerShell)

```powershell
# npm経由でインストール
npm install -g azure-functions-core-tools@4 --unsafe-perm true
```

### macOS

```bash
# Homebrew経由でインストール
brew tap azure/functions
brew install azure-functions-core-tools@4
```

### Linux (Ubuntu)

```bash
# Microsoft パッケージリポジトリを追加
curl https://packages.microsoft.com/keys/microsoft.asc | gpg --dearmor > microsoft.gpg
sudo mv microsoft.gpg /etc/apt/trusted.gpg.d/microsoft.gpg
sudo sh -c 'echo "deb [arch=amd64] https://packages.microsoft.com/repos/microsoft-ubuntu-$(lsb_release -cs)-prod $(lsb_release -cs) main" > /etc/apt/sources.list.d/dotnetdev.list'

# Azure Functions Core Tools をインストール
sudo apt-get update
sudo apt-get install azure-functions-core-tools-4
```

## プロジェクトの準備

### 1. Functions プロジェクトディレクトリに移動

```bash
cd azure-functions
```

### 2. Python仮想環境の作成と有効化

```bash
# 仮想環境作成
python -m venv venv

# 仮想環境有効化 (Linux/macOS)
source venv/bin/activate

# 仮想環境有効化 (Windows)
venv\Scripts\activate
```

### 3. 依存関係のインストール

```bash
# 必要なPythonパッケージをインストール
pip install -r requirements.txt
```

### 4. ローカル設定ファイルの作成

```bash
# local.settings.json ファイルを作成
cat > local.settings.json << EOF
{
  "IsEncrypted": false,
  "Values": {
    "AzureWebJobsStorage": "UseDevelopmentStorage=true",
    "FUNCTIONS_WORKER_RUNTIME": "python",
    "SQL_CONNECTION_STRING": "your-sql-connection-string",
    "COSMOS_CONNECTION_STRING": "your-cosmos-connection-string"
  }
}
EOF
```

**注意:** 本番の接続文字列は Azure Portal から取得してください。

## ローカルでの動作確認

### 1. Functions ホストの起動

```bash
# Azure Functions をローカルで起動
func start
```

### 2. API動作確認

```bash
# 設備監視API のテスト
curl -X POST http://localhost:7071/api/equipment/monitoring \
  -H "Content-Type: application/json" \
  -d '{
    "equipment_id": "A1",
    "timestamp": "2024-01-15T10:00:00Z",
    "status": "operational",
    "efficiency": 85,
    "temperature": 165
  }'

# メンテナンス管理API のテスト
curl -X GET http://localhost:7071/api/maintenance

# データ分析API のテスト
curl -X GET "http://localhost:7071/api/analytics?type=overview&period=week"
```

## Azure へのデプロイ

### 1. Azure にログイン

```bash
# Azure CLI でログイン
az login

# Functions Core Tools でログイン
func azure login
```

### 2. Function App にデプロイ

```bash
# Function App名を設定（azure-resources-setup.md で作成した名前）
FUNCTION_APP_NAME="your-function-app-name"

# デプロイ実行
func azure functionapp publish $FUNCTION_APP_NAME
```

### 3. デプロイ確認

```bash
# デプロイされたFunction一覧確認
func azure functionapp list-functions $FUNCTION_APP_NAME

# Function Appの情報確認
az functionapp show \
  --name $FUNCTION_APP_NAME \
  --resource-group factory-management-rg \
  --query "{name:name, state:state, defaultHostName:defaultHostName}"
```

## 環境変数の設定

### 1. 接続文字列の設定

```bash
# リソースグループとFunction App名
RESOURCE_GROUP="factory-management-rg"
FUNCTION_APP_NAME="your-function-app-name"

# SQL Database接続文字列の設定
SQL_CONNECTION_STRING="your-actual-sql-connection-string"
az functionapp config appsettings set \
  --name $FUNCTION_APP_NAME \
  --resource-group $RESOURCE_GROUP \
  --settings "SQL_CONNECTION_STRING=$SQL_CONNECTION_STRING"

# Cosmos DB接続文字列の設定
COSMOS_CONNECTION_STRING="your-actual-cosmos-connection-string"
az functionapp config appsettings set \
  --name $FUNCTION_APP_NAME \
  --resource-group $RESOURCE_GROUP \
  --settings "COSMOS_CONNECTION_STRING=$COSMOS_CONNECTION_STRING"
```

### 2. その他の設定

```bash
# タイムゾーン設定
az functionapp config appsettings set \
  --name $FUNCTION_APP_NAME \
  --resource-group $RESOURCE_GROUP \
  --settings "WEBSITE_TIME_ZONE=Tokyo Standard Time"

# Python バージョン確認
az functionapp config appsettings set \
  --name $FUNCTION_APP_NAME \
  --resource-group $RESOURCE_GROUP \
  --settings "FUNCTIONS_EXTENSION_VERSION=~4"
```

## デプロイ後の動作確認

### 1. Function URL の取得

```bash
# Function App のベースURL取得
FUNCTION_BASE_URL="https://${FUNCTION_APP_NAME}.azurewebsites.net"
echo "Function App URL: $FUNCTION_BASE_URL"

# Function キーの取得
FUNCTION_KEY=$(az functionapp keys list \
  --name $FUNCTION_APP_NAME \
  --resource-group $RESOURCE_GROUP \
  --query "functionKeys.default" \
  --output tsv)

echo "Function Key: $FUNCTION_KEY"
```

### 2. 本番環境でのAPI テスト

```bash
# 設備監視API のテスト
curl -X POST "${FUNCTION_BASE_URL}/api/equipment/monitoring?code=${FUNCTION_KEY}" \
  -H "Content-Type: application/json" \
  -d '{
    "equipment_id": "A1",
    "timestamp": "2024-01-15T10:00:00Z",
    "status": "operational",
    "efficiency": 85,
    "temperature": 165
  }'

# データ分析API のテスト
curl -X GET "${FUNCTION_BASE_URL}/api/analytics?type=overview&period=week&code=${FUNCTION_KEY}"
```

## 監視とログ

### 1. Application Insights でのログ確認

```bash
# Application Insights の設定確認
az functionapp config appsettings list \
  --name $FUNCTION_APP_NAME \
  --resource-group $RESOURCE_GROUP \
  --query "[?name=='APPINSIGHTS_INSTRUMENTATIONKEY']"
```

### 2. ログストリーミング

```bash
# リアルタイムログ確認
az webapp log tail \
  --name $FUNCTION_APP_NAME \
  --resource-group $RESOURCE_GROUP
```

### 3. ログダウンロード

```bash
# ログファイルのダウンロード
az webapp log download \
  --name $FUNCTION_APP_NAME \
  --resource-group $RESOURCE_GROUP \
  --log-file logs.zip
```

## トラブルシューティング

### よくある問題と解決方法

#### 1. デプロイエラー

```bash
# デプロイメント履歴確認
az functionapp deployment list \
  --name $FUNCTION_APP_NAME \
  --resource-group $RESOURCE_GROUP

# 詳細なデプロイログ確認
func azure functionapp logstream $FUNCTION_APP_NAME
```

#### 2. パッケージ依存関係エラー

```bash
# requirements.txt の内容確認
cat requirements.txt

# ローカルでの依存関係チェック
pip check

# 特定パッケージの再インストール
pip install --force-reinstall azure-functions
```

#### 3. 接続エラー

```bash
# 環境変数の確認
az functionapp config appsettings list \
  --name $FUNCTION_APP_NAME \
  --resource-group $RESOURCE_GROUP \
  --output table
```

#### 4. タイムアウトエラー

```bash
# Function App のタイムアウト設定確認・変更
az functionapp config set \
  --name $FUNCTION_APP_NAME \
  --resource-group $RESOURCE_GROUP \
  --timeout 300
```

## 継続的デプロイメント（CI/CD）

### GitHub Actions を使用した自動デプロイ

1. GitHub リポジトリで以下のシークレットを設定:
   - `AZURE_FUNCTIONAPP_NAME`: Function App名
   - `AZURE_FUNCTIONAPP_PUBLISH_PROFILE`: Publish Profile

2. `.github/workflows/azure-functions.yml` ファイルを作成:

```yaml
name: Deploy Azure Functions

on:
  push:
    branches: [ main ]
    paths: [ 'azure-functions/**' ]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v2
    
    - name: Setup Python
      uses: actions/setup-python@v2
      with:
        python-version: '3.9'
    
    - name: Install dependencies
      run: |
        cd azure-functions
        pip install -r requirements.txt
    
    - name: Deploy to Azure Functions
      uses: Azure/functions-action@v1
      with:
        app-name: ${{ secrets.AZURE_FUNCTIONAPP_NAME }}
        package: azure-functions
        publish-profile: ${{ secrets.AZURE_FUNCTIONAPP_PUBLISH_PROFILE }}
```

## パフォーマンス最適化

### 1. Application Insights の設定

```bash
# サンプリング設定
az functionapp config appsettings set \
  --name $FUNCTION_APP_NAME \
  --resource-group $RESOURCE_GROUP \
  --settings "APPINSIGHTS_SAMPLING_PERCENTAGE=10"
```

### 2. 関数の最適化

- **コールドスタート対策**: Premium プランまたは Dedicated プランの使用を検討
- **メモリ最適化**: 不要なライブラリのインポートを避ける
- **接続プール**: データベース接続の再利用

## 次のステップ

1. **セキュリティ強化**
   - API キー管理の強化
   - Azure Key Vault の活用

2. **スケーリング**
   - 負荷に応じた自動スケーリング設定
   - Premium プランへの移行検討

3. **監視の強化**
   - カスタムメトリクスの設定
   - アラート設定の最適化