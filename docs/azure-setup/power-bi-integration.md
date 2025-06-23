# Power BI 連携設定手順

## 概要

工場設備管理アプリとPower BIを連携させ、設備データの可視化とレポート作成を行う手順を説明します。

## 前提条件

- Power BI ライセンス（Power BI Pro または Premium）
- Azure SQL Database と Cosmos DB が設定済み
- 適切なデータアクセス権限

## Power BI ワークスペースの作成

### 1. Power BI Service にアクセス

```
https://app.powerbi.com/
```

1. Microsoft アカウントでサインイン
2. 左側メニューから「ワークスペース」を選択
3. 「ワークスペースの作成」をクリック

### 2. ワークスペース設定

```
ワークスペース名: 工場設備管理システム
説明: 工場設備の稼働状況、メンテナンス管理、データ分析用ダッシュボード
アクセス権: 組織内の関係者に応じて設定
```

## データソース接続設定

### 1. Azure SQL Database への接続

Power BI Desktop を使用してデータソースに接続:

#### データベース接続設定

```
サーバー: your-sql-server.database.windows.net
データベース: factory-equipment-db
認証方法: Azure Active Directory または SQL Server 認証
ユーザー名: sqladmin
パスワード: [設定したパスワード]
```

#### SQL クエリ例（設備マスタテーブル）

```sql
-- 設備マスタテーブル作成
CREATE TABLE Equipment (
    EquipmentID NVARCHAR(50) PRIMARY KEY,
    EquipmentName NVARCHAR(100) NOT NULL,
    LineID NVARCHAR(50),
    EquipmentType NVARCHAR(50),
    InstallationDate DATE,
    Manufacturer NVARCHAR(100),
    Model NVARCHAR(100),
    Status NVARCHAR(20) DEFAULT 'Active'
);

-- メンテナンス履歴テーブル作成
CREATE TABLE MaintenanceHistory (
    MaintenanceID INT IDENTITY(1,1) PRIMARY KEY,
    EquipmentID NVARCHAR(50) FOREIGN KEY REFERENCES Equipment(EquipmentID),
    MaintenanceDate DATETIME NOT NULL,
    MaintenanceType NVARCHAR(50),
    Technician NVARCHAR(100),
    Duration INT, -- 時間
    Description NVARCHAR(500),
    Cost DECIMAL(10,2)
);

-- 設備稼働履歴テーブル作成
CREATE TABLE OperationHistory (
    RecordID INT IDENTITY(1,1) PRIMARY KEY,
    EquipmentID NVARCHAR(50) FOREIGN KEY REFERENCES Equipment(EquipmentID),
    Timestamp DATETIME NOT NULL,
    Efficiency DECIMAL(5,2),
    Temperature DECIMAL(5,2),
    Status NVARCHAR(20),
    ProductionCount INT,
    AlertLevel NVARCHAR(20)
);
```

#### サンプルデータ投入

```sql
-- 設備マスタデータ
INSERT INTO Equipment VALUES
('A1', '射出成形機 A1', '製造ライン1', '射出成形機', '2020-01-15', 'Manufacturer A', 'Model X1', 'Active'),
('B2', '組立ロボット B2', '製造ライン1', 'ロボット', '2021-03-20', 'Manufacturer B', 'Model Y2', 'Active'),
('C3', '品質検査装置 C3', '製造ライン2', '検査装置', '2019-11-10', 'Manufacturer C', 'Model Z3', 'Active'),
('D4', 'パッケージング装置 D4', '製造ライン2', 'パッケージング', '2020-08-05', 'Manufacturer D', 'Model W4', 'Active'),
('E5', '搬送コンベア E5', '製造ライン3', 'コンベア', '2021-01-12', 'Manufacturer E', 'Model V5', 'Active');

-- メンテナンス履歴データ
INSERT INTO MaintenanceHistory VALUES
('A1', '2024-01-10 09:00:00', '定期点検', '田中技術者', 3, '月次定期点検実施', 50000),
('B2', '2024-01-08 14:00:00', '部品交換', '佐藤技術者', 2, 'センサー交換', 25000),
('C3', '2024-01-12 10:30:00', '校正', '鈴木技術者', 1, '測定器校正', 15000);

-- 稼働履歴データ（過去7日間のサンプル）
DECLARE @Date DATETIME = DATEADD(day, -7, GETDATE());
DECLARE @Counter INT = 0;

WHILE @Counter < 168 -- 7日間 × 24時間
BEGIN
    INSERT INTO OperationHistory VALUES
    ('A1', @Date, 85 + (ABS(CHECKSUM(NEWID())) % 20), 160 + (ABS(CHECKSUM(NEWID())) % 40), 'operational', 100 + (ABS(CHECKSUM(NEWID())) % 50), 'normal'),
    ('B2', @Date, 80 + (ABS(CHECKSUM(NEWID())) % 25), 45 + (ABS(CHECKSUM(NEWID())) % 20), 'operational', 80 + (ABS(CHECKSUM(NEWID())) % 40), 'normal'),
    ('C3', @Date, 75 + (ABS(CHECKSUM(NEWID())) % 30), 35 + (ABS(CHECKSUM(NEWID())) % 15), 'operational', 120 + (ABS(CHECKSUM(NEWID())) % 30), 'normal'),
    ('D4', @Date, 90 + (ABS(CHECKSUM(NEWID())) % 15), 25 + (ABS(CHECKSUM(NEWID())) % 10), 'operational', 200 + (ABS(CHECKSUM(NEWID())) % 50), 'normal'),
    ('E5', @Date, 95 + (ABS(CHECKSUM(NEWID())) % 10), 30 + (ABS(CHECKSUM(NEWID())) % 10), 'operational', 500 + (ABS(CHECKSUM(NEWID())) % 100), 'normal');
    
    SET @Date = DATEADD(hour, 1, @Date);
    SET @Counter = @Counter + 1;
END;
```

### 2. Azure Cosmos DB への接続

#### Power BI での Cosmos DB 接続

1. Power BI Desktop で「データを取得」を選択
2. 「Azure」→「Azure Cosmos DB」を選択
3. 接続情報を入力:

```
Account endpoint: https://your-cosmos-account.documents.azure.com:443/
Database: iot-data
Container: sensor-readings
Authentication: Account key
Account key: [Cosmos DB の主キー]
```

## Power BI レポート作成

### 1. 工場概要ダッシュボード

#### KPI カード作成

```dax
// 総設備数
Total Equipment = DISTINCTCOUNT(Equipment[EquipmentID])

// 稼働中設備数
Operational Equipment = 
CALCULATE(
    DISTINCTCOUNT(OperationHistory[EquipmentID]),
    OperationHistory[Status] = "operational",
    OperationHistory[Timestamp] >= TODAY()
)

// 平均稼働率
Average Efficiency = 
CALCULATE(
    AVERAGE(OperationHistory[Efficiency]),
    OperationHistory[Status] = "operational",
    OperationHistory[Timestamp] >= DATEADD(TODAY(), -7, DAY)
)

// 今月のメンテナンス件数
Monthly Maintenance = 
CALCULATE(
    COUNTROWS(MaintenanceHistory),
    MaintenanceHistory[MaintenanceDate] >= EOMONTH(TODAY(), -1) + 1,
    MaintenanceHistory[MaintenanceDate] <= EOMONTH(TODAY(), 0)
)
```

#### 時系列グラフ用メジャー

```dax
// 日別平均稼働率
Daily Avg Efficiency = 
CALCULATE(
    AVERAGE(OperationHistory[Efficiency]),
    OperationHistory[Status] = "operational"
)

// 時間別生産量
Hourly Production = 
SUMX(
    SUMMARIZE(
        OperationHistory,
        OperationHistory[Timestamp],
        OperationHistory[EquipmentID]
    ),
    OperationHistory[ProductionCount]
)
```

### 2. 設備監視ダッシュボード

#### リアルタイム監視用ビジュアル

```dax
// 最新ステータス
Latest Status = 
CALCULATE(
    FIRSTNONBLANK(OperationHistory[Status], 1),
    TOPN(1, OperationHistory, OperationHistory[Timestamp], DESC)
)

// 効率トレンド
Efficiency Trend = 
VAR CurrentEfficiency = [Average Efficiency]
VAR PreviousEfficiency = 
CALCULATE(
    AVERAGE(OperationHistory[Efficiency]),
    DATEADD(OperationHistory[Timestamp], -1, DAY)
)
RETURN
IF(CurrentEfficiency > PreviousEfficiency, "↗️ 上昇", 
   IF(CurrentEfficiency < PreviousEfficiency, "↘️ 下降", "→ 安定"))

// アラート件数
Alert Count = 
CALCULATE(
    COUNTROWS(OperationHistory),
    OperationHistory[AlertLevel] <> "normal",
    OperationHistory[Timestamp] >= TODAY()
)
```

### 3. メンテナンス分析ダッシュボード

#### メンテナンス分析用メジャー

```dax
// 平均メンテナンス間隔
Avg Maintenance Interval = 
AVERAGEX(
    SUMMARIZE(
        MaintenanceHistory,
        MaintenanceHistory[EquipmentID],
        "LastMaintenance", MAX(MaintenanceHistory[MaintenanceDate])
    ),
    TODAY() - [LastMaintenance]
)

// メンテナンスコスト推移
Monthly Maintenance Cost = 
CALCULATE(
    SUM(MaintenanceHistory[Cost]),
    MONTH(MaintenanceHistory[MaintenanceDate]) = MONTH(TODAY()),
    YEAR(MaintenanceHistory[MaintenanceDate]) = YEAR(TODAY())
)

// 予防保全率
Preventive Maintenance Rate = 
DIVIDE(
    CALCULATE(COUNTROWS(MaintenanceHistory), MaintenanceHistory[MaintenanceType] = "定期点検"),
    COUNTROWS(MaintenanceHistory)
) * 100
```

## ダッシュボード設計

### 1. レイアウト構成

```
+-------------------+-------------------+-------------------+
|   KPI カード       |   KPI カード       |   KPI カード       |
|   総設備数         |   稼働率           |   アラート数        |
+-------------------+-------------------+-------------------+
|                                                           |
|              設備稼働率推移（時系列グラフ）                  |
|                                                           |
+-------------------+-------------------+-------------------+
|                   |                   |                   |
|   設備別効率       |   温度分布         |   生産量推移       |
|   （棒グラフ）      |   （散布図）       |   （折れ線）       |
|                   |                   |                   |
+-------------------+-------------------+-------------------+
```

### 2. フィルター設定

```
// 日付フィルター
Date Range = 
FILTER(
    ALL(OperationHistory[Timestamp]),
    OperationHistory[Timestamp] >= [Start Date] &&
    OperationHistory[Timestamp] <= [End Date]
)

// 設備フィルター
Equipment Filter = 
FILTER(
    ALL(Equipment),
    Equipment[Status] = "Active"
)

// ライン別フィルター
Line Filter = 
VALUES(Equipment[LineID])
```

### 3. 自動更新設定

Power BI Service でのデータ更新設定:

1. ワークスペースでデータセットを選択
2. 「設定」→「スケジュールされた更新」
3. 更新頻度を設定:
   - 毎日: 1時間ごと
   - 週末: 4時間ごと

## リアルタイム データストリーミング

### 1. Azure Stream Analytics 設定

```sql
-- Stream Analytics クエリ例
WITH AggregatedData AS (
    SELECT
        equipment_id,
        System.Timestamp() AS window_end,
        AVG(efficiency) AS avg_efficiency,
        AVG(temperature) AS avg_temperature,
        COUNT(*) AS data_points
    FROM
        [input-stream]
    GROUP BY
        equipment_id,
        TumblingWindow(minute, 5)
)

SELECT
    equipment_id,
    window_end,
    avg_efficiency,
    avg_temperature,
    data_points
INTO
    [powerbi-output]
FROM
    AggregatedData
```

### 2. Power BI ストリーミング データセット

1. Power BI Service で「新しいデータセット」を作成
2. 「ストリーミング データセット」を選択
3. スキーマを定義:

```json
{
  "equipment_id": "string",
  "timestamp": "datetime",
  "avg_efficiency": "number",
  "avg_temperature": "number",
  "data_points": "number"
}
```

## セキュリティ設定

### 1. 行レベルセキュリティ（RLS）

```dax
// 部門別アクセス制御
Department Security = 
FILTER(
    Equipment,
    Equipment[Department] = USERNAME()
)

// ライン別アクセス制御
Line Security = 
FILTER(
    Equipment,
    Equipment[LineID] IN VALUES(UserAccess[LineID])
)
```

### 2. データ暗号化

- Power BI Premium での保存時暗号化
- Azure SQL Database の Transparent Data Encryption (TDE)
- Cosmos DB の保存時暗号化

## モニタリングとアラート

### 1. Power BI アラート設定

データ駆動アラートの設定:

```
アラート条件:
- 設備効率 < 70%
- 温度 > 200°C
- アラート件数 > 5件

通知方法:
- メール通知
- Microsoft Teams 通知
- モバイルアプリ通知
```

### 2. Usage Analytics

```
監視項目:
- ダッシュボード閲覧数
- レポート使用状況
- データ更新頻度
- エラー発生状況
```

## パフォーマンス最適化

### 1. データ モデル最適化

```dax
// 計算テーブル（集約済みデータ）
Hourly Summary = 
SUMMARIZE(
    OperationHistory,
    OperationHistory[EquipmentID],
    "Hour", FORMAT(OperationHistory[Timestamp], "yyyy-mm-dd hh"),
    "AvgEfficiency", AVERAGE(OperationHistory[Efficiency]),
    "AvgTemperature", AVERAGE(OperationHistory[Temperature]),
    "TotalProduction", SUM(OperationHistory[ProductionCount])
)
```

### 2. 増分更新設定

```
設定項目:
- 履歴データ保持期間: 2年
- 増分更新期間: 過去7日
- 検出列: Timestamp
```

## トラブルシューティング

### よくある問題と解決方法

#### 1. データ接続エラー

```
問題: Azure SQL Database への接続失敗
解決: ファイアウォール設定でPower BI IPアドレスを許可

問題: Cosmos DB データが表示されない
解決: パーティションキーの設定確認
```

#### 2. パフォーマンス問題

```
問題: レポート読み込みが遅い
解決: 
- DirectQuery から Import モードに変更
- 不要な列の削除
- 集約テーブルの作成

問題: データ更新エラー
解決:
- 接続文字列の確認
- 権限設定の見直し
- タイムアウト設定の調整
```

## 運用手順

### 1. 日次運用タスク

```
チェック項目:
□ データ更新状況確認
□ アラート確認・対応
□ ダッシュボード表示確認
□ ユーザーからの問い合わせ対応
```

### 2. 週次運用タスク

```
チェック項目:
□ パフォーマンス分析
□ 利用状況レビュー
□ データ品質チェック
□ バックアップ確認
```

### 3. 月次運用タスク

```
チェック項目:
□ 容量使用状況確認
□ コスト分析
□ ユーザーフィードバック収集
□ 機能改善計画
```

## 参考リンク

- [Power BI ドキュメント](https://docs.microsoft.com/ja-jp/power-bi/)
- [Azure Stream Analytics ドキュメント](https://docs.microsoft.com/ja-jp/azure/stream-analytics/)
- [Power BI REST API](https://docs.microsoft.com/ja-jp/rest/api/power-bi/)
- [DAX 関数リファレンス](https://docs.microsoft.com/ja-jp/dax/)