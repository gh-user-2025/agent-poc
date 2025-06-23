# データベース構成・サンプルデータ

本ディレクトリには、工場設備管理システムのデータベース構成ファイルとサンプルデータが格納されています。

## ディレクトリ構成

```
database/
├── schema/                           # Azure SQL Database スキーマ
│   ├── 01_create_tables.sql         # テーブル作成SQL
│   └── 02_insert_sample_data.sql    # サンプルデータ投入SQL
├── cosmosdb-data/                   # Azure Cosmos DB サンプルデータ
│   ├── sensor-data-sample.json     # センサーデータサンプル
│   ├── alerts-sample.json          # アラートデータサンプル
│   ├── bulk_insert_cosmosdb.py     # 一括投入スクリプト
│   └── requirements.txt            # Python依存関係
└── README.md                       # このファイル
```

## データベース構成

### Azure SQL Database v12
構造化データを格納するリレーショナルデータベース

**テーブル構成:**
- `Equipment` - 設備マスタ
- `MaintenanceHistory` - メンテナンス履歴
- `Parts` - 部品マスタ
- `EquipmentParts` - 設備-部品関連
- `Sensors` - センサーマスタ
- `Users` - ユーザーマスタ
- `MaintenanceSchedule` - メンテナンススケジュール

### Azure Cosmos DB NoSQL API
非構造化データ・時系列データを格納するNoSQLデータベース

**コンテナ構成:**
- `SensorData` - センサーデータ（時系列データ）
- `Alerts` - アラート・警告情報

## サンプルデータ概要

### 設備データ
- **射出成形機**: 5台（製造ライン A）
- **組立ロボット**: 3台（製造ライン B）
- **検査装置**: 2台（製造ライン C）
- **コンプレッサー**: 2台（共通設備）
- **その他**: 冷却装置、コンベア等

### センサーデータ
- **温度センサー**: 各設備に設置
- **圧力センサー**: 射出成形機・コンプレッサー
- **振動センサー**: 回転機械類
- **電流センサー**: 全設備
- **湿度センサー**: 検査装置

### ユーザーデータ
- **管理者**: システム管理者
- **技術者**: メンテナンス担当者（3名）
- **オペレーター**: 設備運転担当者（3名）
- **閲覧者**: 管理者・マネージャー

### メンテナンスデータ
- **定期点検**: 3ヶ月周期
- **定期メンテナンス**: 6ヶ月周期
- **年次点検**: 1年周期
- **緊急修理**: 故障時対応

## セットアップ手順

詳細な手順については以下のドキュメントを参照してください：

📖 **[データベース構築・サンプルデータ導入手順書](../docs/database/database-setup-guide.md)**

### クイックスタート

1. **Azure SQL Database の構築**
   ```bash
   # Azure CLIでリソース作成
   az sql server create --name YOUR_SERVER_NAME --resource-group YOUR_RG --admin-user YOUR_USER --admin-password YOUR_PASSWORD
   az sql db create --resource-group YOUR_RG --server YOUR_SERVER_NAME --name FactoryEquipmentDB
   
   # スキーマ作成
   sqlcmd -S YOUR_SERVER_NAME.database.windows.net -d FactoryEquipmentDB -U YOUR_USER -P YOUR_PASSWORD -i schema/01_create_tables.sql
   
   # サンプルデータ投入
   sqlcmd -S YOUR_SERVER_NAME.database.windows.net -d FactoryEquipmentDB -U YOUR_USER -P YOUR_PASSWORD -i schema/02_insert_sample_data.sql
   ```

2. **Azure Cosmos DB の構築**
   ```bash
   # Azure CLIでリソース作成
   az cosmosdb create --name YOUR_COSMOS_NAME --resource-group YOUR_RG
   az cosmosdb sql database create --account-name YOUR_COSMOS_NAME --resource-group YOUR_RG --name FactoryEquipmentDB
   az cosmosdb sql container create --account-name YOUR_COSMOS_NAME --resource-group YOUR_RG --database-name FactoryEquipmentDB --name SensorData --partition-key-path "/equipmentId"
   az cosmosdb sql container create --account-name YOUR_COSMOS_NAME --resource-group YOUR_RG --database-name FactoryEquipmentDB --name Alerts --partition-key-path "/equipmentId"
   
   # サンプルデータ投入
   cd cosmosdb-data
   pip install -r requirements.txt
   python bulk_insert_cosmosdb.py --endpoint YOUR_ENDPOINT --key YOUR_PRIMARY_KEY
   ```

## データ仕様

### SQL Database テーブル仕様

#### Equipment（設備マスタ）
| カラム名 | データ型 | 説明 | 制約 |
|----------|----------|------|------|
| EquipmentId | INT | 設備ID | PK, IDENTITY |
| EquipmentName | NVARCHAR(100) | 設備名 | NOT NULL |
| EquipmentType | NVARCHAR(50) | 設備タイプ | NOT NULL |
| Location | NVARCHAR(100) | 設置場所 | NOT NULL |
| InstallationDate | DATE | 導入日 | NOT NULL |
| Manufacturer | NVARCHAR(100) | メーカー | NULL |
| ModelNumber | NVARCHAR(50) | モデル番号 | NULL |
| MaxOperatingHours | INT | 最大稼働時間 | NULL |
| MaintenanceCycle | INT | メンテナンス周期（日） | NULL |
| Status | NVARCHAR(20) | ステータス | DEFAULT 'Active' |

#### Sensors（センサーマスタ）
| カラム名 | データ型 | 説明 | 制約 |
|----------|----------|------|------|
| SensorId | INT | センサーID | PK, IDENTITY |
| EquipmentId | INT | 設備ID | FK, NOT NULL |
| SensorType | NVARCHAR(50) | センサータイプ | NOT NULL |
| SensorName | NVARCHAR(100) | センサー名 | NOT NULL |
| MeasurementUnit | NVARCHAR(20) | 測定単位 | NOT NULL |
| MinThreshold | DECIMAL(10,3) | 最小閾値 | NULL |
| MaxThreshold | DECIMAL(10,3) | 最大閾値 | NULL |

### Cosmos DB ドキュメント仕様

#### SensorData（センサーデータ）
```json
{
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
}
```

#### Alerts（アラート情報）
```json
{
  "id": "alert-001",
  "equipmentId": "1",
  "alertType": "temperature_critical",
  "severity": "critical",
  "status": "active",
  "title": "温度異常発生",
  "message": "射出成形機-A001の温度が危険レベルに達しました。",
  "occurredAt": "2024-06-23T10:05:00Z",
  "assignedTo": "tech001",
  "metadata": {
    "recommendedAction": "直ちに設備停止し、冷却システムの点検を実施してください。"
  }
}
```

## 使用例・クエリサンプル

### SQL Database クエリ例

```sql
-- 設備一覧取得
SELECT EquipmentId, EquipmentName, EquipmentType, Location, Status
FROM Equipment
WHERE Status = 'Active'
ORDER BY Location, EquipmentName;

-- 今月のメンテナンス予定
SELECT e.EquipmentName, ms.ScheduledDate, ms.MaintenanceType, u.FullName as Technician
FROM MaintenanceSchedule ms
INNER JOIN Equipment e ON ms.EquipmentId = e.EquipmentId
INNER JOIN Users u ON ms.AssignedTechnician = u.UserId
WHERE ms.ScheduledDate BETWEEN '2024-06-01' AND '2024-06-30'
ORDER BY ms.ScheduledDate;

-- 部品在庫不足アラート
SELECT PartName, PartNumber, StockQuantity, MinimumStock
FROM Parts
WHERE StockQuantity <= MinimumStock
ORDER BY StockQuantity;
```

### Cosmos DB クエリ例

```sql
-- 最新センサーデータ取得
SELECT TOP 10 *
FROM SensorData s
WHERE s.equipmentId = "1"
ORDER BY s.timestamp DESC

-- アクティブアラート取得
SELECT *
FROM Alerts a
WHERE a.status = "active"
ORDER BY a.severity DESC, a.occurredAt DESC

-- 設備別センサーデータ集計
SELECT 
    s.equipmentId,
    s.sensorType,
    AVG(s.measurementValue) as avgValue,
    MAX(s.measurementValue) as maxValue,
    MIN(s.measurementValue) as minValue
FROM SensorData s
WHERE s.timestamp >= "2024-06-23T00:00:00Z"
GROUP BY s.equipmentId, s.sensorType
```

## トラブルシューティング

### よくある問題

1. **SQL Server接続エラー**
   - ファイアウォール設定を確認
   - 接続文字列の認証情報を確認

2. **Cosmos DB接続エラー**
   - エンドポイントURLの形式を確認
   - プライマリキーの値を確認

3. **データ投入エラー**
   - JSONの構文エラーを確認
   - 必須フィールドの不足を確認
   - パーティションキーの値を確認

### ログ確認
```bash
# Azure Activity Log確認
az monitor activity-log list --resource-group YOUR_RG --start-time 2024-06-23T00:00:00Z
```

## 更新履歴

- **2024-06-23**: 初版作成
  - Azure SQL Database v12用スキーマ作成
  - 日本語サンプルデータ作成
  - Cosmos DB NoSQL API用サンプルデータ作成
  - 一括投入スクリプト作成

## 参考資料

- [Azure SQL Database Documentation](https://docs.microsoft.com/azure/azure-sql/)
- [Azure Cosmos DB Documentation](https://docs.microsoft.com/azure/cosmos-db/)
- [T-SQL Reference](https://docs.microsoft.com/sql/t-sql/)
- [Cosmos DB SQL API Query Reference](https://docs.microsoft.com/azure/cosmos-db/sql/sql-query-getting-started)