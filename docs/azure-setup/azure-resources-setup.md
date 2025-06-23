# Azure リソース作成手順書

## 概要

この手順書では、工場設備管理アプリに必要なAzureリソースを作成する手順を詳細に説明します。Azure初心者の方でも安心して設定できるよう、ステップバイステップで解説します。

## 前提条件

- Azureアカウントが作成済みであること
- Azure CLIがインストールされていること
- 必要な権限（リソース作成権限）があること

## 必要なAzureリソース

1. **リソースグループ** - 全リソースを管理するコンテナ
2. **Azure Functions** - バックエンドAPI処理
3. **Azure SQL Database** - 設備マスタ・履歴データ保存
4. **Azure Cosmos DB** - IoTデータのリアルタイム処理
5. **Azure Storage Account** - ファイル・画像保存
6. **Application Insights** - アプリケーション監視
7. **Power BI ワークスペース** - データ可視化

## 作成手順

### 1. Azure CLIへのログイン

```bash
# Azureにログイン
az login

# サブスクリプション一覧確認
az account list --output table

# 使用するサブスクリプションを設定（必要に応じて）
az account set --subscription "your-subscription-id"
```

### 2. リソースグループの作成

```bash
# 変数定義
RESOURCE_GROUP="factory-management-rg"
LOCATION="japaneast"
PROJECT_NAME="factory-equipment"

# リソースグループ作成
az group create \
  --name $RESOURCE_GROUP \
  --location $LOCATION \
  --tags project=$PROJECT_NAME environment=development
```

### 3. Azure Storage Accountの作成

```bash
# ストレージアカウント名（ユニークである必要があります）
STORAGE_ACCOUNT="${PROJECT_NAME}storage$(date +%s)"

# ストレージアカウント作成
az storage account create \
  --name $STORAGE_ACCOUNT \
  --resource-group $RESOURCE_GROUP \
  --location $LOCATION \
  --sku Standard_LRS \
  --kind StorageV2 \
  --tags project=$PROJECT_NAME
```

### 4. Azure SQL Databaseの作成

```bash
# SQL Server名とデータベース名
SQL_SERVER="${PROJECT_NAME}-sql-server"
SQL_DATABASE="${PROJECT_NAME}-db"
SQL_ADMIN="sqladmin"
SQL_PASSWORD="YourSecurePassword123!"

# SQL Server作成
az sql server create \
  --name $SQL_SERVER \
  --resource-group $RESOURCE_GROUP \
  --location $LOCATION \
  --admin-user $SQL_ADMIN \
  --admin-password $SQL_PASSWORD

# ファイアウォール規則の設定（Azure サービスからのアクセス許可）
az sql server firewall-rule create \
  --resource-group $RESOURCE_GROUP \
  --server $SQL_SERVER \
  --name AllowAzureServices \
  --start-ip-address 0.0.0.0 \
  --end-ip-address 0.0.0.0

# SQL Database作成
az sql db create \
  --resource-group $RESOURCE_GROUP \
  --server $SQL_SERVER \
  --name $SQL_DATABASE \
  --service-objective Basic \
  --tags project=$PROJECT_NAME
```

### 5. Azure Cosmos DBの作成

```bash
# Cosmos DB アカウント名
COSMOS_ACCOUNT="${PROJECT_NAME}-cosmos"
COSMOS_DATABASE="iot-data"
COSMOS_CONTAINER="sensor-readings"

# Cosmos DB アカウント作成
az cosmosdb create \
  --name $COSMOS_ACCOUNT \
  --resource-group $RESOURCE_GROUP \
  --default-consistency-level Session \
  --locations regionName=$LOCATION \
  --tags project=$PROJECT_NAME

# データベース作成
az cosmosdb sql database create \
  --account-name $COSMOS_ACCOUNT \
  --resource-group $RESOURCE_GROUP \
  --name $COSMOS_DATABASE

# コンテナ作成
az cosmosdb sql container create \
  --account-name $COSMOS_ACCOUNT \
  --database-name $COSMOS_DATABASE \
  --resource-group $RESOURCE_GROUP \
  --name $COSMOS_CONTAINER \
  --partition-key-path "/equipment_id" \
  --throughput 400
```

### 6. Application Insightsの作成

```bash
# Application Insights名
APPINSIGHTS_NAME="${PROJECT_NAME}-insights"

# Application Insights作成
az monitor app-insights component create \
  --app $APPINSIGHTS_NAME \
  --location $LOCATION \
  --resource-group $RESOURCE_GROUP \
  --tags project=$PROJECT_NAME
```

### 7. Azure Functionsの作成

```bash
# Function App名（ユニークである必要があります）
FUNCTION_APP="${PROJECT_NAME}-functions-$(date +%s)"

# Function App作成
az functionapp create \
  --resource-group $RESOURCE_GROUP \
  --consumption-plan-location $LOCATION \
  --runtime python \
  --runtime-version 3.9 \
  --functions-version 4 \
  --name $FUNCTION_APP \
  --storage-account $STORAGE_ACCOUNT \
  --app-insights $APPINSIGHTS_NAME \
  --tags project=$PROJECT_NAME
```

### 8. 接続文字列とキーの取得

```bash
# SQL Database接続文字列取得
echo "SQL Database Connection String:"
az sql db show-connection-string \
  --server $SQL_SERVER \
  --name $SQL_DATABASE \
  --client ado.net

# Cosmos DB接続文字列取得
echo "Cosmos DB Connection String:"
az cosmosdb keys list \
  --name $COSMOS_ACCOUNT \
  --resource-group $RESOURCE_GROUP \
  --type connection-strings \
  --query "connectionStrings[0].connectionString" \
  --output tsv

# Storage Account接続文字列取得
echo "Storage Account Connection String:"
az storage account show-connection-string \
  --name $STORAGE_ACCOUNT \
  --resource-group $RESOURCE_GROUP \
  --query connectionString \
  --output tsv

# Application Insights Instrumentation Key取得
echo "Application Insights Instrumentation Key:"
az monitor app-insights component show \
  --app $APPINSIGHTS_NAME \
  --resource-group $RESOURCE_GROUP \
  --query instrumentationKey \
  --output tsv
```

### 9. Function Appの環境変数設定

```bash
# SQL Database接続文字列を環境変数に設定
SQL_CONNECTION_STRING="Server=tcp:${SQL_SERVER}.database.windows.net,1433;Initial Catalog=${SQL_DATABASE};Persist Security Info=False;User ID=${SQL_ADMIN};Password=${SQL_PASSWORD};MultipleActiveResultSets=False;Encrypt=True;TrustServerCertificate=False;Connection Timeout=30;"

az functionapp config appsettings set \
  --name $FUNCTION_APP \
  --resource-group $RESOURCE_GROUP \
  --settings "SQL_CONNECTION_STRING=$SQL_CONNECTION_STRING"

# Cosmos DB接続文字列を環境変数に設定
COSMOS_CONNECTION_STRING=$(az cosmosdb keys list \
  --name $COSMOS_ACCOUNT \
  --resource-group $RESOURCE_GROUP \
  --type connection-strings \
  --query "connectionStrings[0].connectionString" \
  --output tsv)

az functionapp config appsettings set \
  --name $FUNCTION_APP \
  --resource-group $RESOURCE_GROUP \
  --settings "COSMOS_CONNECTION_STRING=$COSMOS_CONNECTION_STRING"
```

## 作成完了の確認

### リソース一覧確認

```bash
# 作成されたリソースの確認
az resource list \
  --resource-group $RESOURCE_GROUP \
  --output table
```

### Function Appの動作確認

```bash
# Function Appの情報確認
az functionapp show \
  --name $FUNCTION_APP \
  --resource-group $RESOURCE_GROUP \
  --query "{name:name, state:state, defaultHostName:defaultHostName}" \
  --output table
```

## セキュリティ設定

### 1. SQL Serverファイアウォール設定（本番用）

```bash
# 特定のIPアドレスからのアクセス許可（開発用PC等）
# YOUR_IP_ADDRESSを実際のIPアドレスに置き換えてください
YOUR_IP_ADDRESS="xxx.xxx.xxx.xxx"

az sql server firewall-rule create \
  --resource-group $RESOURCE_GROUP \
  --server $SQL_SERVER \
  --name AllowDevelopmentIP \
  --start-ip-address $YOUR_IP_ADDRESS \
  --end-ip-address $YOUR_IP_ADDRESS
```

### 2. Function App認証設定

```bash
# Function App の認証レベル確認（本番では function キーを使用）
echo "Function App URL:"
echo "https://${FUNCTION_APP}.azurewebsites.net"
```

## トラブルシューティング

### よくある問題と解決方法

1. **リソース名の重複エラー**
   - ストレージアカウント名やFunction App名は全Azure内でユニークである必要があります
   - 名前に日時を含めるか、別の名前を使用してください

2. **権限エラー**
   - Azure サブスクリプションの共同作成者権限が必要です
   - 管理者に権限付与を依頼してください

3. **リージョンでのサービス利用不可**
   - 指定したリージョンで一部サービスが利用できない場合があります
   - `japanwest` や `eastus` 等の別リージョンを試してください

### ログ確認方法

```bash
# デプロイメントログの確認
az deployment group list \
  --resource-group $RESOURCE_GROUP \
  --query "[].{name:name, state:properties.provisioningState}" \
  --output table
```

## 次のステップ

1. **アプリケーションのデプロイ**
   - Azure Functions のコードをデプロイ
   - Vue.js アプリケーションをAzure Static Web Apps にデプロイ

2. **Power BI ワークスペースの設定**
   - Power BI Service でワークスペース作成
   - データセットとレポートの作成

3. **監視とアラートの設定**
   - Application Insights でのパフォーマンス監視
   - Azure Monitor でのアラート設定

## 参考リンク

- [Azure Functions ドキュメント](https://docs.microsoft.com/ja-jp/azure/azure-functions/)
- [Azure SQL Database ドキュメント](https://docs.microsoft.com/ja-jp/azure/azure-sql/)
- [Azure Cosmos DB ドキュメント](https://docs.microsoft.com/ja-jp/azure/cosmos-db/)
- [Azure CLI リファレンス](https://docs.microsoft.com/ja-jp/cli/azure/)