# 工場設備管理システム アプリケーションアーキテクチャ設計書

## 1. アプリケーションアーキテクチャ

以下のシステムアーキテクチャは、工場設備管理システムの全体構成を示しています。Azure クラウドサービスを活用したスケーラブルで信頼性の高いアーキテクチャです。

```mermaid
graph TB
    subgraph "工場現場"
        A[IoTセンサー] --> B[Azure IoT Hub]
        A1[温度センサー] --> B
        A2[圧力センサー] --> B
        A3[振動センサー] --> B
        A4[稼働状態センサー] --> B
    end

    subgraph "データ取り込み層"
        B --> C[Azure Event Hubs]
        C --> D[Azure Stream Analytics]
    end

    subgraph "処理・分析層"
        D --> E[Azure Functions]
        E --> F[Azure Machine Learning]
        F --> G[AI予測モデル]
    end

    subgraph "データ保存層"
        E --> H[Azure Cosmos DB<br/>リアルタイムデータ]
        E --> I[Azure SQL Database<br/>構造化データ]
        E --> J[Azure Storage Account<br/>ファイル・ログ]
    end

    subgraph "認証・セキュリティ"
        K[Azure Active Directory] --> L[多要素認証]
        M[Azure Key Vault] --> N[秘密情報管理]
    end

    subgraph "アプリケーション層"
        O[Azure App Service<br/>Web API] --> H
        O --> I
        P[Azure Static Web Apps<br/>フロントエンド] --> O
    end

    subgraph "可視化・分析"
        Q[Power BI] --> I
        Q --> H
        R[Azure Monitor] --> S[Application Insights]
    end

    subgraph "ユーザーインターフェース"
        T[Webブラウザ] --> P
        U[モバイルアプリ] --> P
        V[タブレット] --> P
    end

    subgraph "外部システム連携"
        W[ERPシステム] --> O
        X[MESシステム] --> O
        Y[在庫管理システム] --> O
    end

    K --> O
    K --> P
    M --> E
    R --> E
```

### アーキテクチャの主要コンポーネント

- **データ収集**: IoTセンサーからAzure IoT Hub経由でリアルタイムデータを収集
- **データ処理**: Azure Event HubsとStream Analyticsによるストリーミング処理
- **AI/ML**: Azure Machine Learningによる故障予測と異常検知
- **データ保存**: 用途別に最適化されたデータストア（Cosmos DB、SQL Database、Storage）
- **セキュリティ**: Azure AD統合とKey Vaultによる包括的なセキュリティ
- **可視化**: Power BIとカスタムダッシュボードによるデータ可視化

## 2. データモデル設計

以下のERDは、工場設備管理システムで扱う主要なデータエンティティとその関係を表しています。

```mermaid
erDiagram
    EQUIPMENT {
        varchar equipment_id PK "設備ID"
        varchar equipment_name "設備名"
        varchar equipment_type "設備タイプ"
        varchar location "設置場所"
        date installation_date "導入日"
        varchar manufacturer "メーカー"
        varchar model_number "モデル番号"
        int max_operating_hours "最大稼働時間"
        int maintenance_cycle "メンテナンス周期"
        varchar status "稼働状態"
        datetime created_at "作成日時"
        datetime updated_at "更新日時"
    }

    SENSOR {
        varchar sensor_id PK "センサーID"
        varchar equipment_id FK "設備ID"
        varchar sensor_type "センサータイプ"
        varchar measurement_unit "測定単位"
        float min_threshold "最小閾値"
        float max_threshold "最大閾値"
        varchar status "ステータス"
        datetime created_at "作成日時"
    }

    SENSOR_DATA {
        varchar data_id PK "データID"
        varchar sensor_id FK "センサーID"
        varchar equipment_id FK "設備ID"
        float measurement_value "測定値"
        varchar status "ステータス"
        datetime timestamp "タイムスタンプ"
        json metadata "メタデータ"
    }

    MAINTENANCE_HISTORY {
        varchar maintenance_id PK "メンテナンスID"
        varchar equipment_id FK "設備ID"
        varchar maintenance_type "メンテナンス種別"
        datetime performed_date "実施日時"
        varchar technician "担当者"
        text work_description "作業内容"
        text parts_replaced "部品交換情報"
        decimal cost "コスト"
        datetime next_scheduled_date "次回予定日"
        varchar status "ステータス"
        datetime created_at "作成日時"
    }

    ALERT {
        varchar alert_id PK "アラートID"
        varchar equipment_id FK "設備ID"
        varchar sensor_id FK "センサーID"
        varchar alert_type "アラートタイプ"
        varchar severity "重要度"
        datetime occurred_at "発生日時"
        text message "詳細メッセージ"
        varchar response_status "対応状況"
        varchar assigned_to "担当者"
        datetime resolved_at "解決日時"
        datetime created_at "作成日時"
    }

    USER {
        varchar user_id PK "ユーザーID"
        varchar username "ユーザー名"
        varchar email "メールアドレス"
        varchar role "役割"
        varchar department "部署"
        varchar phone "電話番号"
        boolean is_active "有効フラグ"
        datetime last_login "最終ログイン"
        datetime created_at "作成日時"
    }

    MAINTENANCE_SCHEDULE {
        varchar schedule_id PK "スケジュールID"
        varchar equipment_id FK "設備ID"
        varchar maintenance_type "メンテナンスタイプ"
        datetime scheduled_date "予定日時"
        varchar assigned_technician FK "担当技術者"
        varchar status "ステータス"
        text notes "備考"
        datetime created_at "作成日時"
    }

    PARTS_INVENTORY {
        varchar part_id PK "部品ID"
        varchar part_name "部品名"
        varchar part_number "部品番号"
        varchar equipment_type "対応設備タイプ"
        int stock_quantity "在庫数量"
        int min_stock_level "最小在庫レベル"
        decimal unit_cost "単価"
        varchar supplier "サプライヤー"
        datetime last_updated "最終更新日"
    }

    PREDICTION_RESULT {
        varchar prediction_id PK "予測ID"
        varchar equipment_id FK "設備ID"
        varchar model_version "モデルバージョン"
        float failure_probability "故障確率"
        datetime predicted_failure_date "予測故障日"
        text recommended_actions "推奨対応策"
        datetime prediction_date "予測実行日"
        varchar confidence_level "信頼度レベル"
    }

    %% リレーションシップ
    EQUIPMENT ||--o{ SENSOR : "設備は複数のセンサーを持つ"
    SENSOR ||--o{ SENSOR_DATA : "センサーは複数のデータを生成"
    EQUIPMENT ||--o{ SENSOR_DATA : "設備は複数のセンサーデータを持つ"
    EQUIPMENT ||--o{ MAINTENANCE_HISTORY : "設備は複数のメンテナンス履歴を持つ"
    EQUIPMENT ||--o{ ALERT : "設備は複数のアラートを生成"
    SENSOR ||--o{ ALERT : "センサーは複数のアラートを生成"
    USER ||--o{ MAINTENANCE_HISTORY : "ユーザーはメンテナンス作業を担当"
    EQUIPMENT ||--o{ MAINTENANCE_SCHEDULE : "設備は複数のメンテナンススケジュールを持つ"
    USER ||--o{ MAINTENANCE_SCHEDULE : "ユーザーはメンテナンススケジュールを担当"
    EQUIPMENT ||--o{ PREDICTION_RESULT : "設備は複数の予測結果を持つ"
    ALERT }|--|| USER : "アラートはユーザーに割り当てられる"
```

### データモデルの特徴

- **正規化**: 第3正規形に準拠したデータベース設計
- **スケーラビリティ**: 時系列データ（SENSOR_DATA）はAzure Cosmos DBで管理
- **構造化データ**: マスタデータと履歴データはAzure SQL Databaseで管理
- **監査追跡**: created_at、updated_atによる変更履歴の追跡
- **柔軟性**: JSONメタデータフィールドによる拡張性の確保

## 3. 画面遷移図

以下の画面遷移図は、各ユーザー役割に応じたシステムの操作フローを示しています。

```mermaid
graph TD
    A[ログイン画面] --> B{認証}
    B -->|成功| C[ホーム画面<br/>ダッシュボード]
    B -->|失敗| A

    C --> D[監視ダッシュボード]
    C --> E[メンテナンス管理]
    C --> F[データ分析]
    C --> G[システム管理]
    C --> H[アラート一覧]

    %% 監視ダッシュボード系統
    D --> D1[設備一覧画面]
    D1 --> D2[設備詳細画面]
    D2 --> D3[リアルタイムグラフ]
    D2 --> D4[履歴データ表示]
    
    %% アラート系統
    H --> H1[アラート詳細]
    H1 --> H2[対応記録入力]
    H2 --> H3[対応完了]
    H3 --> H

    %% メンテナンス管理系統
    E --> E1[スケジュール管理]
    E --> E2[作業記録]
    E --> E3[履歴検索]
    
    E1 --> E11[新規スケジュール登録]
    E11 --> E12[担当者選択]
    E12 --> E13[競合チェック]
    E13 -->|競合なし| E14[スケジュール保存]
    E13 -->|競合あり| E11
    E14 --> E1

    E2 --> E21[作業開始記録]
    E21 --> E22[作業内容入力]
    E22 --> E23[写真アップロード]
    E23 --> E24[部品使用記録]
    E24 --> E25[作業完了記録]
    E25 --> E2

    E3 --> E31[検索条件設定]
    E31 --> E32[履歴一覧表示]
    E32 --> E33[履歴詳細表示]

    %% データ分析系統
    F --> F1[傾向分析]
    F --> F2[故障予測]
    F --> F3[レポート生成]

    F1 --> F11[期間・設備選択]
    F11 --> F12[分析実行]
    F12 --> F13[結果表示]
    F13 --> F14[レポート出力]

    F2 --> F21[予測対象選択]
    F21 --> F22[AI分析実行]
    F22 --> F23[予測結果表示]
    F23 --> F24[推奨対応策表示]
    F24 --> F25[メンテナンス計画反映]

    F3 --> F31[レポート種別選択]
    F31 --> F32[パラメータ設定]
    F32 --> F33[レポート生成]
    F33 --> F34[ダウンロード/印刷]

    %% システム管理系統（管理者のみ）
    G --> G1[ユーザー管理]
    G --> G2[設備マスタ管理]
    G --> G3[システム設定]
    G --> G4[バックアップ管理]

    G1 --> G11[ユーザー一覧]
    G11 --> G12[ユーザー詳細/編集]
    G12 --> G13[権限設定]

    G2 --> G21[設備一覧管理]
    G21 --> G22[設備詳細編集]
    G22 --> G23[センサー設定]

    G3 --> G31[アラート設定]
    G31 --> G32[閾値設定]
    G32 --> G33[通知設定]

    %% 共通ナビゲーション
    D --> C
    E --> C
    F --> C
    G --> C
    H --> C

    subgraph "権限別アクセス制御"
        style G fill:#ffcccc
        style G1 fill:#ffcccc
        style G2 fill:#ffcccc
        style G3 fill:#ffcccc
        style G4 fill:#ffcccc
    end
```

### 画面遷移の特徴

- **役割ベースアクセス制御**: ユーザーの役割に応じた画面制限
- **直感的ナビゲーション**: ホーム画面からすべての主要機能にアクセス可能
- **効率的ワークフロー**: 作業の流れに沿った画面遷移設計
- **モバイル対応**: レスポンシブデザインによるマルチデバイス対応

## 4. プロジェクトマイルストーン

### 4.1 リソース計算

**プロジェクト期間**: 2023年12月28日 ～ 2024年3月28日（3ヶ月 = 約13週間）

**利用可能工数の計算**:
- 開発者数: 3名
- 平均稼働率: 90%
- 営業日: 土日祝日を除く（約65営業日）
- 1日の作業時間: 8時間
- 総工数: 3名 × 65日 × 8時間 × 0.9 = 1,404時間

**フェーズ別工数配分**:
1. **フェーズ1（基盤構築）**: 351時間（25%）
2. **フェーズ2（データ取り込み）**: 281時間（20%）
3. **フェーズ3（リアルタイム監視）**: 351時間（25%）
4. **フェーズ4（メンテナンス管理）**: 281時間（20%）
5. **フェーズ5（データ分析）**: 140時間（10%）

### 4.2 詳細マイルストーン

```mermaid
gantt
    title 工場設備管理システム 開発マイルストーン
    dateFormat YYYY-MM-DD
    axisFormat %m/%d

    section フェーズ1: 基盤構築
    Azureリソース構築           :p1-1, 2023-12-28, 5d
    開発環境セットアップ        :p1-2, after p1-1, 3d
    認証基盤実装               :p1-3, after p1-2, 5d
    基本データモデル構築        :p1-4, after p1-3, 4d
    APIフレームワーク構築       :p1-5, after p1-4, 5d
    フロントエンド基盤構築      :p1-6, after p1-5, 3d
    
    section フェーズ2: データ取り込み
    IoTシミュレーター開発       :p2-1, after p1-6, 4d
    Azure IoT Hub統合          :p2-2, after p2-1, 3d
    データパイプライン構築      :p2-3, after p2-2, 5d
    リアルタイムデータ処理      :p2-4, after p2-3, 4d
    データ保存機能実装         :p2-5, after p2-4, 4d
    
    section フェーズ3: リアルタイム監視
    監視ダッシュボードUI        :p3-1, after p2-5, 6d
    リアルタイム表示機能        :p3-2, after p3-1, 5d
    アラート機能実装           :p3-3, after p3-2, 4d
    設備詳細画面開発           :p3-4, after p3-3, 4d
    通知機能実装               :p3-5, after p3-4, 3d
    監視機能テスト             :p3-6, after p3-5, 3d
    
    section フェーズ4: メンテナンス管理
    スケジュール管理機能        :p4-1, after p3-6, 5d
    作業記録機能               :p4-2, after p4-1, 4d
    履歴管理機能               :p4-3, after p4-2, 4d
    ユーザー管理機能           :p4-4, after p4-3, 3d
    システム管理機能           :p4-5, after p4-4, 4d
    
    section フェーズ5: データ分析・最終調整
    傾向分析機能               :p5-1, after p4-5, 4d
    故障予測AI実装             :p5-2, after p5-1, 3d
    レポート機能               :p5-3, after p5-2, 2d
    総合テスト                 :p5-4, after p5-3, 3d
    デプロイ・リリース         :p5-5, after p5-4, 2d
    
    section マイルストーン
    基盤完成                   :milestone, m1, after p1-6, 0d
    データ取り込み完成         :milestone, m2, after p2-5, 0d
    監視機能完成               :milestone, m3, after p3-6, 0d
    メンテナンス機能完成       :milestone, m4, after p4-5, 0d
    初期リリース               :milestone, m5, after p5-5, 0d
```

### 4.3 優先順位と理由

**最優先（初期リリース必須機能）**:
1. **基盤構築**: すべての機能の土台となるため
2. **リアルタイム監視**: 工場運営に直接的な価値を提供
3. **アラート機能**: 安全性と効率性に直結

**高優先度**:
4. **メンテナンス管理**: 予防保全による長期的価値
5. **ユーザー管理**: セキュリティと運用管理

**中優先度**:
6. **データ分析**: 長期的な改善効果が期待される
7. **故障予測**: AI機能による付加価値

### 4.4 リスクと対策

**技術的リスク**:
- Azure サービス学習コスト: フェーズ1で集中的に技術習得
- IoT接続の複雑さ: シミュレーターで先行検証

**スケジュールリスク**:
- 外部システム連携の遅延: モックデータでの先行開発
- テスト期間の確保: 各フェーズでの継続的テスト実施

**品質リスク**:
- データ精度の確保: 検証機能の早期実装
- パフォーマンス要件: 負荷テストの計画実施

## 5. 次のステップ

この設計書に基づいて、以下の開発作業を順次実施していきます：

1. **Azure環境構築**: Infrastructure as Codeによる自動化
2. **開発チーム体制**: 役割分担と作業分担の明確化
3. **品質保証**: テスト戦略とCI/CDパイプラインの構築
4. **ユーザー受け入れ**: 段階的なユーザーフィードバックの収集

このアーキテクチャ設計により、スケーラブルで保守性の高い工場設備管理システムの実現を目指します。