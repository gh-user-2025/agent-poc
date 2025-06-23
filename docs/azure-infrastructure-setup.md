# Azure リソース構築手順書

## 概要
この手順書では、工場設備管理アプリに必要なAzureリソースをAzure CLIを使用して構築する手順を詳細に説明します。Azure初心者の方でも安全に実行できるよう、各ステップを詳しく記載しています。

## 前提条件

### 必要なツール
- Azure CLI がインストールされていること
- Azureサブスクリプションが利用可能であること
- 適切な権限（Contributor以上）があること

### Azure CLIのインストール確認
```bash
# Azure CLI のバージョン確認
az --version

# インストールされていない場合は以下でインストール
curl -sL https://aka.ms/InstallAzureCLIDeb | sudo bash
```

## 1. 基本設定

### 1.1 Azureアカウントへのログイン
```bash
# Azure へログイン
az login

# ログイン後、利用可能なサブスクリプションを確認
az account list --output table

# 使用するサブスクリプションを設定（必要に応じて）
az account set --subscription "<サブスクリプションID>"
```

### 1.2 リソース グループの作成
```bash
# 変数設定（値は環境に合わせて変更してください）
RESOURCE_GROUP="rg-factory-equipment-mgmt"
LOCATION="japaneast"
APP_NAME="factory-equipment-mgmt"

# リソース グループの作成
az group create \
    --name $RESOURCE_GROUP \
    --location $LOCATION

# 作成確認
az group show --name $RESOURCE_GROUP --output table
```

## 2. ストレージアカウントの作成

### 2.1 汎用ストレージアカウントの作成
```bash
# 変数設定
STORAGE_ACCOUNT_NAME="${APP_NAME}storage$(date +%s)"

# ストレージアカウントの作成
az storage account create \
    --name $STORAGE_ACCOUNT_NAME \
    --resource-group $RESOURCE_GROUP \
    --location $LOCATION \
    --sku Standard_LRS \
    --kind StorageV2

# 作成確認
az storage account show \
    --name $STORAGE_ACCOUNT_NAME \
    --resource-group $RESOURCE_GROUP \
    --output table

# ストレージアカウントキーの取得
STORAGE_KEY=$(az storage account keys list \
    --account-name $STORAGE_ACCOUNT_NAME \
    --resource-group $RESOURCE_GROUP \
    --query '[0].value' \
    --output tsv)

echo "ストレージアカウント名: $STORAGE_ACCOUNT_NAME"
echo "ストレージキー: $STORAGE_KEY"
```

### 2.2 コンテナーの作成
```bash
# 必要なコンテナーを作成
az storage container create \
    --name "equipment-data" \
    --account-name $STORAGE_ACCOUNT_NAME \
    --account-key $STORAGE_KEY

az storage container create \
    --name "maintenance-files" \
    --account-name $STORAGE_ACCOUNT_NAME \
    --account-key $STORAGE_KEY

az storage container create \
    --name "backup-data" \
    --account-name $STORAGE_ACCOUNT_NAME \
    --account-key $STORAGE_KEY

# 作成確認
az storage container list \
    --account-name $STORAGE_ACCOUNT_NAME \
    --account-key $STORAGE_KEY \
    --output table
```

## 3. Azure SQL Database の作成

### 3.1 SQL Server の作成
```bash
# 変数設定
SQL_SERVER_NAME="${APP_NAME}-sqlserver-$(date +%s)"
SQL_ADMIN_USER="sqladmin"
SQL_ADMIN_PASSWORD="P@ssw0rd123!"  # 本番環境では強固なパスワードを使用

# SQL Server の作成
az sql server create \
    --name $SQL_SERVER_NAME \
    --resource-group $RESOURCE_GROUP \
    --location $LOCATION \
    --admin-user $SQL_ADMIN_USER \
    --admin-password $SQL_ADMIN_PASSWORD

# 作成確認
az sql server show \
    --name $SQL_SERVER_NAME \
    --resource-group $RESOURCE_GROUP \
    --output table

echo "SQL Server名: $SQL_SERVER_NAME"
echo "管理者ユーザー: $SQL_ADMIN_USER"
```

### 3.2 ファイアウォール規則の設定
```bash
# Azure サービスからのアクセスを許可
az sql server firewall-rule create \
    --server $SQL_SERVER_NAME \
    --resource-group $RESOURCE_GROUP \
    --name "AllowAzureServices" \
    --start-ip-address 0.0.0.0 \
    --end-ip-address 0.0.0.0

# 現在のクライアントIPからのアクセスを許可
CLIENT_IP=$(curl -s https://api.ipify.org)
az sql server firewall-rule create \
    --server $SQL_SERVER_NAME \
    --resource-group $RESOURCE_GROUP \
    --name "ClientAccess" \
    --start-ip-address $CLIENT_IP \
    --end-ip-address $CLIENT_IP

echo "クライアントIP $CLIENT_IP からのアクセスを許可しました"
```

### 3.3 SQL Database の作成
```bash
# データベース名の設定
SQL_DATABASE_NAME="${APP_NAME}-db"

# SQL Database の作成
az sql db create \
    --server $SQL_SERVER_NAME \
    --resource-group $RESOURCE_GROUP \
    --name $SQL_DATABASE_NAME \
    --edition Basic \
    --capacity 5

# 作成確認
az sql db show \
    --server $SQL_SERVER_NAME \
    --resource-group $RESOURCE_GROUP \
    --name $SQL_DATABASE_NAME \
    --output table

echo "データベース名: $SQL_DATABASE_NAME"
```

## 4. Azure Cosmos DB の作成

### 4.1 Cosmos DB アカウントの作成
```bash
# 変数設定
COSMOS_ACCOUNT_NAME="${APP_NAME}-cosmosdb-$(date +%s)"

# Cosmos DB アカウントの作成（SQL API）
az cosmosdb create \
    --name $COSMOS_ACCOUNT_NAME \
    --resource-group $RESOURCE_GROUP \
    --kind GlobalDocumentDB \
    --default-consistency-level Session \
    --locations regionName=$LOCATION failoverPriority=0 isZoneRedundant=False

# 作成確認
az cosmosdb show \
    --name $COSMOS_ACCOUNT_NAME \
    --resource-group $RESOURCE_GROUP \
    --output table

echo "Cosmos DB アカウント名: $COSMOS_ACCOUNT_NAME"
```

### 4.2 データベースとコンテナーの作成
```bash
# データベースの作成
az cosmosdb sql database create \
    --account-name $COSMOS_ACCOUNT_NAME \
    --resource-group $RESOURCE_GROUP \
    --name "FactoryEquipmentDB"

# センサーデータ用コンテナーの作成
az cosmosdb sql container create \
    --account-name $COSMOS_ACCOUNT_NAME \
    --resource-group $RESOURCE_GROUP \
    --database-name "FactoryEquipmentDB" \
    --name "SensorData" \
    --partition-key-path "/equipmentId" \
    --throughput 400

# アラート用コンテナーの作成
az cosmosdb sql container create \
    --account-name $COSMOS_ACCOUNT_NAME \
    --resource-group $RESOURCE_GROUP \
    --database-name "FactoryEquipmentDB" \
    --name "Alerts" \
    --partition-key-path "/equipmentId" \
    --throughput 400

# 作成確認
az cosmosdb sql container list \
    --account-name $COSMOS_ACCOUNT_NAME \
    --resource-group $RESOURCE_GROUP \
    --database-name "FactoryEquipmentDB" \
    --output table
```

## 5. Azure IoT Hub の作成

### 5.1 IoT Hub の作成
```bash
# 変数設定
IOT_HUB_NAME="${APP_NAME}-iothub-$(date +%s)"

# IoT Hub の作成
az iot hub create \
    --name $IOT_HUB_NAME \
    --resource-group $RESOURCE_GROUP \
    --location $LOCATION \
    --sku S1 \
    --unit 1

# 作成確認
az iot hub show \
    --name $IOT_HUB_NAME \
    --resource-group $RESOURCE_GROUP \
    --output table

echo "IoT Hub名: $IOT_HUB_NAME"
```

### 5.2 デバイス グループの作成
```bash
# 製造ライン A のデバイスを作成
for i in {1..5}; do
    az iot hub device-identity create \
        --hub-name $IOT_HUB_NAME \
        --device-id "injection-molding-$i"
done

# 製造ライン B のデバイスを作成
for i in {1..3}; do
    az iot hub device-identity create \
        --hub-name $IOT_HUB_NAME \
        --device-id "assembly-robot-$i"
done

# 製造ライン C のデバイスを作成
for i in {1..2}; do
    az iot hub device-identity create \
        --hub-name $IOT_HUB_NAME \
        --device-id "inspection-device-$i"
done

# 共通設備のデバイスを作成
az iot hub device-identity create \
    --hub-name $IOT_HUB_NAME \
    --device-id "compressor-1"

az iot hub device-identity create \
    --hub-name $IOT_HUB_NAME \
    --device-id "compressor-2"

az iot hub device-identity create \
    --hub-name $IOT_HUB_NAME \
    --device-id "cooling-system-1"

# デバイス一覧の確認
az iot hub device-identity list \
    --hub-name $IOT_HUB_NAME \
    --output table
```

## 6. Azure Event Hubs の作成

### 6.1 Event Hubs 名前空間の作成
```bash
# 変数設定
EVENT_HUB_NAMESPACE="${APP_NAME}-eventhub-$(date +%s)"

# Event Hubs 名前空間の作成
az eventhubs namespace create \
    --name $EVENT_HUB_NAMESPACE \
    --resource-group $RESOURCE_GROUP \
    --location $LOCATION \
    --sku Standard

# 作成確認
az eventhubs namespace show \
    --name $EVENT_HUB_NAMESPACE \
    --resource-group $RESOURCE_GROUP \
    --output table

echo "Event Hub 名前空間: $EVENT_HUB_NAMESPACE"
```

### 6.2 Event Hub の作成
```bash
# Event Hub の作成
az eventhubs eventhub create \
    --name "sensor-data-stream" \
    --namespace-name $EVENT_HUB_NAMESPACE \
    --resource-group $RESOURCE_GROUP \
    --partition-count 4 \
    --message-retention 7

# 作成確認
az eventhubs eventhub show \
    --name "sensor-data-stream" \
    --namespace-name $EVENT_HUB_NAMESPACE \
    --resource-group $RESOURCE_GROUP \
    --output table
```

## 7. Azure Functions の作成

### 7.1 Function App の作成
```bash
# 変数設定
FUNCTION_APP_NAME="${APP_NAME}-functions-$(date +%s)"

# Function App の作成
az functionapp create \
    --name $FUNCTION_APP_NAME \
    --resource-group $RESOURCE_GROUP \
    --storage-account $STORAGE_ACCOUNT_NAME \
    --consumption-plan-location $LOCATION \
    --runtime python \
    --runtime-version 3.9 \
    --functions-version 4

# 作成確認
az functionapp show \
    --name $FUNCTION_APP_NAME \
    --resource-group $RESOURCE_GROUP \
    --output table

echo "Function App名: $FUNCTION_APP_NAME"
```

### 7.2 アプリケーション設定の構成
```bash
# Cosmos DB の接続文字列を取得
COSMOS_CONNECTION_STRING=$(az cosmosdb keys list \
    --name $COSMOS_ACCOUNT_NAME \
    --resource-group $RESOURCE_GROUP \
    --type connection-strings \
    --query 'connectionStrings[0].connectionString' \
    --output tsv)

# SQL Database の接続文字列を構築
SQL_CONNECTION_STRING="Server=tcp:${SQL_SERVER_NAME}.database.windows.net,1433;Initial Catalog=${SQL_DATABASE_NAME};Persist Security Info=False;User ID=${SQL_ADMIN_USER};Password=${SQL_ADMIN_PASSWORD};MultipleActiveResultSets=False;Encrypt=True;TrustServerCertificate=False;Connection Timeout=30;"

# Function App にアプリケーション設定を追加
az functionapp config appsettings set \
    --name $FUNCTION_APP_NAME \
    --resource-group $RESOURCE_GROUP \
    --settings \
        "CosmosDbConnectionString=$COSMOS_CONNECTION_STRING" \
        "SqlConnectionString=$SQL_CONNECTION_STRING" \
        "StorageAccountConnectionString=DefaultEndpointsProtocol=https;AccountName=$STORAGE_ACCOUNT_NAME;AccountKey=$STORAGE_KEY;EndpointSuffix=core.windows.net"

echo "Function App の設定が完了しました"
```

## 8. Azure Key Vault の作成

### 8.1 Key Vault の作成
```bash
# 変数設定
KEY_VAULT_NAME="${APP_NAME}-kv-$(date +%s | cut -c 6-10)"

# Key Vault の作成
az keyvault create \
    --name $KEY_VAULT_NAME \
    --resource-group $RESOURCE_GROUP \
    --location $LOCATION \
    --sku standard

# 作成確認
az keyvault show \
    --name $KEY_VAULT_NAME \
    --resource-group $RESOURCE_GROUP \
    --output table

echo "Key Vault名: $KEY_VAULT_NAME"
```

### 8.2 シークレットの保存
```bash
# データベース接続文字列をシークレットとして保存
az keyvault secret set \
    --vault-name $KEY_VAULT_NAME \
    --name "sql-connection-string" \
    --value "$SQL_CONNECTION_STRING"

az keyvault secret set \
    --vault-name $KEY_VAULT_NAME \
    --name "cosmos-connection-string" \
    --value "$COSMOS_CONNECTION_STRING"

az keyvault secret set \
    --vault-name $KEY_VAULT_NAME \
    --name "storage-connection-string" \
    --value "DefaultEndpointsProtocol=https;AccountName=$STORAGE_ACCOUNT_NAME;AccountKey=$STORAGE_KEY;EndpointSuffix=core.windows.net"

# 保存されたシークレットの確認
az keyvault secret list \
    --vault-name $KEY_VAULT_NAME \
    --output table

echo "シークレットが正常に保存されました"
```

## 9. 作成されたリソースの確認

### 9.1 全リソースの一覧表示
```bash
# リソース グループ内の全リソースを表示
az resource list \
    --resource-group $RESOURCE_GROUP \
    --output table

echo "=== 作成されたリソース一覧 ==="
echo "リソース グループ: $RESOURCE_GROUP"
echo "ストレージアカウント: $STORAGE_ACCOUNT_NAME"
echo "SQL Server: $SQL_SERVER_NAME"
echo "SQL Database: $SQL_DATABASE_NAME"
echo "Cosmos DB アカウント: $COSMOS_ACCOUNT_NAME"
echo "IoT Hub: $IOT_HUB_NAME"
echo "Event Hub 名前空間: $EVENT_HUB_NAMESPACE"
echo "Function App: $FUNCTION_APP_NAME"
echo "Key Vault: $KEY_VAULT_NAME"
```

### 9.2 接続情報の保存
```bash
# 接続情報をファイルに保存
cat > /tmp/azure-resources-info.txt << EOF
=== Azure リソース接続情報 ===
作成日時: $(date)

リソース グループ: $RESOURCE_GROUP
場所: $LOCATION

ストレージアカウント: $STORAGE_ACCOUNT_NAME
ストレージキー: $STORAGE_KEY

SQL Server: $SQL_SERVER_NAME
SQL Database: $SQL_DATABASE_NAME
SQL 管理者ユーザー: $SQL_ADMIN_USER
SQL 管理者パスワード: $SQL_ADMIN_PASSWORD

Cosmos DB アカウント: $COSMOS_ACCOUNT_NAME
Cosmos DB データベース: FactoryEquipmentDB

IoT Hub: $IOT_HUB_NAME
Event Hub 名前空間: $EVENT_HUB_NAMESPACE
Event Hub: sensor-data-stream

Function App: $FUNCTION_APP_NAME
Key Vault: $KEY_VAULT_NAME

注意: この情報は安全な場所に保管してください。
EOF

echo "接続情報が /tmp/azure-resources-info.txt に保存されました"
echo "この情報は開発時に必要になりますので、安全に保管してください。"
```

## 10. セキュリティ設定

### 10.1 RBAC（Role-Based Access Control）の設定
```bash
# 現在のユーザーのオブジェクトIDを取得
CURRENT_USER_OBJECT_ID=$(az ad signed-in-user show --query id --output tsv)

# Key Vault への適切なアクセス権限を設定
az keyvault set-policy \
    --name $KEY_VAULT_NAME \
    --object-id $CURRENT_USER_OBJECT_ID \
    --secret-permissions get list set delete

echo "セキュリティ設定が完了しました"
```

## 11. 後片付け（必要な場合）

### 11.1 全リソースの削除
```bash
# 注意: 以下のコマンドは全てのリソースを削除します
# 実行前に十分確認してください

# リソース グループの削除（全てのリソースが削除されます）
# az group delete --name $RESOURCE_GROUP --yes --no-wait

echo "リソースを削除する場合は、上記のコメントアウトされたコマンドを実行してください"
```

## まとめ

この手順書に従って、工場設備管理アプリに必要な以下のAzureリソースが構築されました：

1. **Azure Storage Account**: ファイルやバックアップデータの保存
2. **Azure SQL Database**: 構造化データの保存
3. **Azure Cosmos DB**: リアルタイムIoTデータの保存
4. **Azure IoT Hub**: IoTデバイスとの通信
5. **Azure Event Hubs**: ストリーミングデータの処理
6. **Azure Functions**: サーバーレスコンピューティング
7. **Azure Key Vault**: 秘密情報の安全な管理

次のステップでは、これらのリソースを使用してアプリケーションの開発を開始できます。