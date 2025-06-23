# データベース構築・サンプルデータ導入手順書

本ドキュメントでは、工場設備管理システムのデータベース環境構築とサンプルデータの導入手順について説明します。

## 概要

本システムは以下の2つのデータベースを使用します：

- **Azure SQL Database v12**: 構造化データ（設備マスタ、メンテナンス履歴、部品管理等）
- **Azure Cosmos DB NoSQL API**: 非構造化データ（センサーデータ、アラート情報等）

## 前提条件

- Azure サブスクリプションが利用可能であること
- Azure CLI がインストール・ログイン済みであること
- 必要な権限（Contributor以上）を持っていること

## 1. Azure SQL Database の構築とデータ投入

### 1.1 Azure SQL Database リソースの作成

```bash
# 変数設定
RESOURCE_GROUP="factory-equipment-rg"
LOCATION="japaneast"
SQL_SERVER_NAME="factory-sql-$(date +%s)"
SQL_DATABASE_NAME="FactoryEquipmentDB"
SQL_ADMIN_USER="sqladmin"
SQL_ADMIN_PASSWORD="P@ssw0rd123Factory!"  # 本番環境では強固なパスワードを使用

# リソースグループの作成（存在しない場合）
az group create --name $RESOURCE_GROUP --location $LOCATION

# SQL Server の作成
az sql server create \
    --name $SQL_SERVER_NAME \
    --resource-group $RESOURCE_GROUP \
    --location $LOCATION \
    --admin-user $SQL_ADMIN_USER \
    --admin-password $SQL_ADMIN_PASSWORD

# ファイアウォール規則の設定（開発環境用）
az sql server firewall-rule create \
    --resource-group $RESOURCE_GROUP \
    --server $SQL_SERVER_NAME \
    --name AllowAllIPs \
    --start-ip-address 0.0.0.0 \
    --end-ip-address 255.255.255.255

# SQL Database の作成
az sql db create \
    --resource-group $RESOURCE_GROUP \
    --server $SQL_SERVER_NAME \
    --name $SQL_DATABASE_NAME \
    --service-objective S1

# 作成確認
az sql db show \
    --resource-group $RESOURCE_GROUP \
    --server $SQL_SERVER_NAME \
    --name $SQL_DATABASE_NAME \
    --output table

echo "SQL Server名: $SQL_SERVER_NAME"
echo "データベース名: $SQL_DATABASE_NAME"
echo "管理者ユーザー: $SQL_ADMIN_USER"
```

### 1.2 SQL Server Management Studio または sqlcmd の準備

#### Windows環境の場合
1. SQL Server Management Studio (SSMS) をダウンロード・インストール
2. サーバー名：`$SQL_SERVER_NAME.database.windows.net`
3. 認証：SQL Server認証
4. ユーザー名：`$SQL_ADMIN_USER`
5. パスワード：`$SQL_ADMIN_PASSWORD`

#### Linux/macOS環境の場合
```bash
# sqlcmdツールのインストール（Ubuntu/Debian）
curl https://packages.microsoft.com/keys/microsoft.asc | sudo apt-key add -
curl https://packages.microsoft.com/config/ubuntu/20.04/prod.list | sudo tee /etc/apt/sources.list.d/msprod.list
sudo apt-get update
sudo apt-get install mssql-tools unixodbc-dev

# sqlcmdツールのインストール（CentOS/RHEL）
sudo curl -o /etc/yum.repos.d/msprod.repo https://packages.microsoft.com/config/rhel/8/prod.repo
sudo yum install mssql-tools unixODBC-devel

# sqlcmdツールのインストール（macOS）
brew tap microsoft/mssql-release https://github.com/Microsoft/homebrew-mssql-release
brew install mssql-tools
```

### 1.3 データベーススキーマの作成

```bash
# データベーススキーマのデプロイ
sqlcmd -S $SQL_SERVER_NAME.database.windows.net \
       -d $SQL_DATABASE_NAME \
       -U $SQL_ADMIN_USER \
       -P $SQL_ADMIN_PASSWORD \
       -i database/schema/01_create_tables.sql

echo "データベーススキーマの作成が完了しました"
```

### 1.4 サンプルデータの投入

```bash
# サンプルデータの投入
sqlcmd -S $SQL_SERVER_NAME.database.windows.net \
       -d $SQL_DATABASE_NAME \
       -U $SQL_ADMIN_USER \
       -P $SQL_ADMIN_PASSWORD \
       -i database/schema/02_insert_sample_data.sql

echo "サンプルデータの投入が完了しました"
```

### 1.5 データ投入の確認

```bash
# データ確認用SQLの実行
sqlcmd -S $SQL_SERVER_NAME.database.windows.net \
       -d $SQL_DATABASE_NAME \
       -U $SQL_ADMIN_USER \
       -P $SQL_ADMIN_PASSWORD \
       -Q "SELECT COUNT(*) as '設備数' FROM Equipment; SELECT COUNT(*) as '部品数' FROM Parts; SELECT COUNT(*) as 'センサー数' FROM Sensors; SELECT COUNT(*) as 'ユーザー数' FROM Users;"
```

## 2. Azure Cosmos DB の構築とデータ投入

### 2.1 Azure Cosmos DB リソースの作成

```bash
# 変数設定
COSMOS_ACCOUNT_NAME="factory-cosmosdb-$(date +%s)"

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

### 2.2 データベースとコンテナーの作成

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

### 2.3 接続文字列の取得

```bash
# Cosmos DB 接続文字列の取得
az cosmosdb keys list \
    --name $COSMOS_ACCOUNT_NAME \
    --resource-group $RESOURCE_GROUP \
    --type connection-strings \
    --output table

# 主キーの取得
PRIMARY_KEY=$(az cosmosdb keys list \
    --name $COSMOS_ACCOUNT_NAME \
    --resource-group $RESOURCE_GROUP \
    --type keys \
    --query primaryMasterKey \
    --output tsv)

echo "Primary Key: $PRIMARY_KEY"
echo "Endpoint: https://$COSMOS_ACCOUNT_NAME.documents.azure.com:443/"
```

### 2.4 サンプルデータの投入

#### 方法1: Azure Data Explorer を使用

1. Azure Portal で作成したCosmos DBアカウントを開く
2. 「Data Explorer」を選択
3. 「FactoryEquipmentDB」→「SensorData」→「Items」を選択
4. 「New Item」をクリック
5. `database/cosmosdb-data/sensor-data-sample.json` の内容を1件ずつコピー&ペースト
6. 同様に「Alerts」コンテナーに `database/cosmosdb-data/alerts-sample.json` のデータを投入

#### 方法2: Azure CLI を使用

```bash
# センサーデータの投入（個別実行）
az cosmosdb sql container create-item \
    --account-name $COSMOS_ACCOUNT_NAME \
    --resource-group $RESOURCE_GROUP \
    --database-name "FactoryEquipmentDB" \
    --container-name "SensorData" \
    --body '{
        "id": "sensor-data-001",
        "equipmentId": "1",
        "sensorId": "1",
        "sensorType": "temperature",
        "measurementValue": 85.5,
        "measurementUnit": "℃",
        "status": "normal",
        "timestamp": "2024-06-23T10:00:00Z",
        "metadata": {
            "equipmentName": "射出成形機-A001",
            "location": "製造ライン A-1",
            "sensorName": "射出成形機-A001-温度センサー1"
        }
    }'

# アラートデータの投入（個別実行）
az cosmosdb sql container create-item \
    --account-name $COSMOS_ACCOUNT_NAME \
    --resource-group $RESOURCE_GROUP \
    --database-name "FactoryEquipmentDB" \
    --container-name "Alerts" \
    --body '{
        "id": "alert-001",
        "equipmentId": "1",
        "alertType": "temperature_critical",
        "severity": "critical",
        "status": "active",
        "title": "温度異常発生",
        "message": "射出成形機-A001の温度が危険レベル（210.5℃）に達しました。直ちに点検が必要です。",
        "occurredAt": "2024-06-23T10:05:00Z",
        "metadata": {
            "equipmentName": "射出成形機-A001",
            "location": "製造ライン A-1",
            "recommendedAction": "直ちに設備停止し、冷却システムの点検を実施してください。"
        }
    }'
```

#### 方法3: Python スクリプトを使用（推奨）

```python
# bulk_insert_cosmosdb.py
import json
from azure.cosmos import CosmosClient

# 接続情報（実際の値に置き換えてください）
ENDPOINT = "https://YOUR_COSMOS_ACCOUNT_NAME.documents.azure.com:443/"
PRIMARY_KEY = "YOUR_PRIMARY_KEY"
DATABASE_NAME = "FactoryEquipmentDB"

# Cosmos DB クライアントの初期化
client = CosmosClient(ENDPOINT, PRIMARY_KEY)
database = client.get_database_client(DATABASE_NAME)

# センサーデータの一括投入
sensor_container = database.get_container_client("SensorData")
with open('database/cosmosdb-data/sensor-data-sample.json', 'r', encoding='utf-8') as f:
    sensor_data = json.load(f)
    for item in sensor_data:
        sensor_container.upsert_item(item)
print("センサーデータの投入完了")

# アラートデータの一括投入
alerts_container = database.get_container_client("Alerts")
with open('database/cosmosdb-data/alerts-sample.json', 'r', encoding='utf-8') as f:
    alerts_data = json.load(f)
    for item in alerts_data:
        alerts_container.upsert_item(item)
print("アラートデータの投入完了")
```

実行方法:
```bash
# 必要なライブラリのインストール
pip install azure-cosmos

# スクリプトの実行
python bulk_insert_cosmosdb.py
```

### 2.5 データ投入の確認

```bash
# データ件数の確認
az cosmosdb sql query \
    --account-name $COSMOS_ACCOUNT_NAME \
    --resource-group $RESOURCE_GROUP \
    --database-name "FactoryEquipmentDB" \
    --container-name "SensorData" \
    --query-text "SELECT VALUE COUNT(1) FROM c"

az cosmosdb sql query \
    --account-name $COSMOS_ACCOUNT_NAME \
    --resource-group $RESOURCE_GROUP \
    --database-name "FactoryEquipmentDB" \
    --container-name "Alerts" \
    --query-text "SELECT VALUE COUNT(1) FROM c"
```

## 3. 動作確認

### 3.1 SQL Database の動作確認

```sql
-- 設備一覧の確認
SELECT 
    EquipmentId,
    EquipmentName,
    EquipmentType,
    Location,
    Status
FROM Equipment
ORDER BY EquipmentId;

-- センサー情報の確認
SELECT 
    s.SensorId,
    s.SensorName,
    s.SensorType,
    e.EquipmentName,
    s.Status
FROM Sensors s
INNER JOIN Equipment e ON s.EquipmentId = e.EquipmentId
ORDER BY s.EquipmentId, s.SensorId;

-- メンテナンス履歴の確認
SELECT 
    m.MaintenanceId,
    e.EquipmentName,
    m.MaintenanceType,
    m.PerformedDate,
    m.Technician,
    m.Cost
FROM MaintenanceHistory m
INNER JOIN Equipment e ON m.EquipmentId = e.EquipmentId
ORDER BY m.PerformedDate DESC;
```

### 3.2 Cosmos DB の動作確認

```bash
# 最新のセンサーデータ確認
az cosmosdb sql query \
    --account-name $COSMOS_ACCOUNT_NAME \
    --resource-group $RESOURCE_GROUP \
    --database-name "FactoryEquipmentDB" \
    --container-name "SensorData" \
    --query-text "SELECT TOP 5 * FROM c ORDER BY c.timestamp DESC"

# アクティブなアラート確認
az cosmosdb sql query \
    --account-name $COSMOS_ACCOUNT_NAME \
    --resource-group $RESOURCE_GROUP \
    --database-name "FactoryEquipmentDB" \
    --container-name "Alerts" \
    --query-text "SELECT * FROM c WHERE c.status = 'active'"
```

## 4. トラブルシューティング

### 4.1 よくある問題と解決方法

#### SQL Database 接続エラー
- ファイアウォール設定を確認
- 接続文字列の確認
- 認証情報の確認

#### Cosmos DB 接続エラー
- エンドポイントURLの確認
- アクセスキーの確認
- ネットワーク設定の確認

#### データ投入エラー
- JSONフォーマットの確認
- 必須フィールドの確認
- パーティションキーの確認

### 4.2 ログの確認方法

```bash
# Azure Activity Log の確認
az monitor activity-log list \
    --resource-group $RESOURCE_GROUP \
    --start-time 2024-06-23T00:00:00Z \
    --output table
```

## 5. クリーンアップ

テスト完了後、リソースを削除する場合：

```bash
# リソースグループ全体の削除（注意：すべてのリソースが削除されます）
az group delete --name $RESOURCE_GROUP --yes --no-wait
```

## 6. 次のステップ

データベース構築完了後、以下の作業を進めてください：

1. アプリケーションからの接続設定
2. API の実装
3. 監視・アラート設定
4. バックアップ設定
5. セキュリティ設定の強化

## 参考資料

- [Azure SQL Database Documentation](https://docs.microsoft.com/azure/azure-sql/)
- [Azure Cosmos DB Documentation](https://docs.microsoft.com/azure/cosmos-db/)
- [Azure CLI Reference](https://docs.microsoft.com/cli/azure/)