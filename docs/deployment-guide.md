# デプロイメント手順書

## 概要
この手順書では、工場設備管理アプリケーションをAzureクラウド環境にデプロイする手順を詳細に説明します。AI-Driven Development のアプローチを活用し、効率的でスケーラブルなデプロイメントを実現します。

## 1. デプロイメント戦略

### 1.1 デプロイメント環境
- **開発環境（Development）**: 開発者個人の検証用
- **ステージング環境（Staging）**: 統合テスト・受入テスト用
- **本番環境（Production）**: 実際の運用環境

### 1.2 デプロイメント方式
- **Azure Functions**: コンテナーベースのデプロイメント
- **Web API**: Azure App Service へのデプロイ
- **フロントエンド**: Azure Static Web Apps へのデプロイ
- **データベース**: Azure SQL Database のスキーマデプロイ

### 1.3 CI/CD パイプライン
- **GitHub Actions**: ソースコード管理とCI/CD
- **Azure DevOps**: 複雑なリリース管理（オプション）
- **自動テスト**: ユニット・統合・E2Eテスト
- **コード品質チェック**: SonarQube または CodeQL

## 2. 事前準備

### 2.1 必要なツールとアクセス権限
```bash
# 必要なツールの確認
echo "=== デプロイメント前チェック ==="

# Azure CLI の確認
echo "Azure CLI バージョン:"
az --version | head -1

# Azure へのログイン確認
echo "現在のAzureアカウント:"
az account show --query user.name --output tsv

# GitHub CLI のインストール（オプション）
# Ubuntu/Debian の場合
sudo apt update
sudo apt install gh

# macOS の場合
# brew install gh

# GitHub CLI のログイン
gh auth login
```

### 2.2 環境変数の準備
```bash
# デプロイメント用環境変数の設定
export AZURE_SUBSCRIPTION_ID="your-subscription-id"
export AZURE_RESOURCE_GROUP="rg-factory-equipment-mgmt"
export AZURE_LOCATION="japaneast"
export APP_NAME="factory-equipment-mgmt"
export ENVIRONMENT="production"  # development, staging, production

# GitHub リポジトリ情報
export GITHUB_REPO="your-username/factory-equipment-management"
export GITHUB_BRANCH="main"

echo "環境変数が設定されました"
echo "サブスクリプション ID: $AZURE_SUBSCRIPTION_ID"
echo "リソースグループ: $AZURE_RESOURCE_GROUP"
echo "アプリケーション名: $APP_NAME"
```

## 3. Azure Functions のデプロイ

### 3.1 Function App の設定確認
```bash
# Function App 名の設定
FUNCTION_APP_NAME="${APP_NAME}-functions-${ENVIRONMENT}"

# Function App の存在確認
az functionapp show \
    --name $FUNCTION_APP_NAME \
    --resource-group $AZURE_RESOURCE_GROUP \
    --output table

# Function App が存在しない場合は作成
if [ $? -ne 0 ]; then
    echo "Function App を作成しています..."
    az functionapp create \
        --name $FUNCTION_APP_NAME \
        --resource-group $AZURE_RESOURCE_GROUP \
        --storage-account "${APP_NAME}storage" \
        --consumption-plan-location $AZURE_LOCATION \
        --runtime python \
        --runtime-version 3.9 \
        --functions-version 4
fi
```

### 3.2 アプリケーション設定の構成
```bash
# Key Vault からシークレットを取得
KEY_VAULT_NAME="${APP_NAME}-kv"

# 接続文字列の取得
SQL_CONNECTION_STRING=$(az keyvault secret show \
    --vault-name $KEY_VAULT_NAME \
    --name "sql-connection-string" \
    --query value --output tsv)

COSMOS_CONNECTION_STRING=$(az keyvault secret show \
    --vault-name $KEY_VAULT_NAME \
    --name "cosmos-connection-string" \
    --query value --output tsv)

STORAGE_CONNECTION_STRING=$(az keyvault secret show \
    --vault-name $KEY_VAULT_NAME \
    --name "storage-connection-string" \
    --query value --output tsv)

# Function App の設定を更新
az functionapp config appsettings set \
    --name $FUNCTION_APP_NAME \
    --resource-group $AZURE_RESOURCE_GROUP \
    --settings \
        "SqlConnectionString=$SQL_CONNECTION_STRING" \
        "CosmosDbConnectionString=$COSMOS_CONNECTION_STRING" \
        "StorageConnectionString=$STORAGE_CONNECTION_STRING" \
        "ENVIRONMENT=$ENVIRONMENT"

echo "Function App の設定が完了しました"
```

### 3.3 Functions のデプロイ
```bash
# backend/functions ディレクトリに移動
cd backend/functions

# Python の依存関係をインストール
pip install -r requirements.txt

# Functions のビルドとデプロイ
func azure functionapp publish $FUNCTION_APP_NAME --python

# デプロイ確認
az functionapp function list \
    --name $FUNCTION_APP_NAME \
    --resource-group $AZURE_RESOURCE_GROUP \
    --output table

echo "Azure Functions のデプロイが完了しました"

# プロジェクトルートに戻る
cd ../..
```

## 4. Web API のデプロイ（Azure App Service）

### 4.1 App Service Plan の作成
```bash
# App Service Plan 名の設定
APP_SERVICE_PLAN="${APP_NAME}-plan-${ENVIRONMENT}"
WEB_APP_NAME="${APP_NAME}-api-${ENVIRONMENT}"

# App Service Plan の作成
az appservice plan create \
    --name $APP_SERVICE_PLAN \
    --resource-group $AZURE_RESOURCE_GROUP \
    --location $AZURE_LOCATION \
    --sku B1 \
    --is-linux

# 作成確認
az appservice plan show \
    --name $APP_SERVICE_PLAN \
    --resource-group $AZURE_RESOURCE_GROUP \
    --output table
```

### 4.2 Web App の作成
```bash
# Web App の作成
az webapp create \
    --name $WEB_APP_NAME \
    --resource-group $AZURE_RESOURCE_GROUP \
    --plan $APP_SERVICE_PLAN \
    --runtime "PYTHON|3.9"

# アプリケーション設定の構成
az webapp config appsettings set \
    --name $WEB_APP_NAME \
    --resource-group $AZURE_RESOURCE_GROUP \
    --settings \
        "SqlConnectionString=$SQL_CONNECTION_STRING" \
        "CosmosDbConnectionString=$COSMOS_CONNECTION_STRING" \
        "StorageConnectionString=$STORAGE_CONNECTION_STRING" \
        "ENVIRONMENT=$ENVIRONMENT" \
        "SCM_DO_BUILD_DURING_DEPLOYMENT=true"

echo "Web App が作成されました: https://${WEB_APP_NAME}.azurewebsites.net"
```

### 4.3 Web API のデプロイ
```bash
# backend/api ディレクトリに移動
cd backend/api

# デプロイ用の requirements.txt を作成（必要に応じて）
cat > requirements.txt << 'EOF'
flask==3.0.0
flask-cors==4.0.0
azure-cosmos==4.5.1
azure-storage-blob==12.19.0
pyodbc==5.0.1
sqlalchemy==2.0.23
python-dotenv==1.0.0
pydantic==2.5.0
EOF

# Startup Command の設定
az webapp config set \
    --name $WEB_APP_NAME \
    --resource-group $AZURE_RESOURCE_GROUP \
    --startup-file "gunicorn --bind=0.0.0.0 --workers=1 app:app"

# ZIP デプロイの実行
zip -r api-deploy.zip . -x "*.pyc" "__pycache__/*" ".git/*"

az webapp deployment source config-zip \
    --name $WEB_APP_NAME \
    --resource-group $AZURE_RESOURCE_GROUP \
    --src api-deploy.zip

# デプロイ確認
sleep 30
curl "https://${WEB_APP_NAME}.azurewebsites.net/api/health"

echo "Web API のデプロイが完了しました"

# プロジェクトルートに戻る
cd ../..
```

## 5. フロントエンドのデプロイ（Azure Static Web Apps）

### 5.1 Static Web App の作成
```bash
# Static Web App 名の設定
STATIC_WEB_APP_NAME="${APP_NAME}-frontend-${ENVIRONMENT}"

# Static Web App の作成
az staticwebapp create \
    --name $STATIC_WEB_APP_NAME \
    --resource-group $AZURE_RESOURCE_GROUP \
    --location $AZURE_LOCATION \
    --source "https://github.com/${GITHUB_REPO}" \
    --branch $GITHUB_BRANCH \
    --app-location "frontend" \
    --api-location "backend/api" \
    --output-location "dist"

# 作成確認
az staticwebapp show \
    --name $STATIC_WEB_APP_NAME \
    --resource-group $AZURE_RESOURCE_GROUP \
    --output table

echo "Static Web App が作成されました"
```

### 5.2 フロントエンドのビルドとデプロイ
```bash
# frontend ディレクトリに移動
cd frontend

# 本番用の環境変数を設定
cat > .env.production << EOF
VUE_APP_API_BASE_URL=https://${WEB_APP_NAME}.azurewebsites.net/api
VUE_APP_ENVIRONMENT=production
EOF

# 依存関係のインストール
npm install

# 本番ビルド
npm run build

# SWA CLI を使用したデプロイ（オプション）
# npm install -g @azure/static-web-apps-cli
# swa deploy ./dist --deployment-token $SWA_DEPLOYMENT_TOKEN

echo "フロントエンドのビルドが完了しました"

# プロジェクトルートに戻る
cd ..
```

## 6. データベースのデプロイ

### 6.1 SQL Database スキーマの作成
```bash
# データベーススキーマファイルの作成
mkdir -p database/schema

cat > database/schema/01_create_tables.sql << 'EOF'
-- 設備マスタテーブル
CREATE TABLE Equipment (
    EquipmentId INT IDENTITY(1,1) PRIMARY KEY,
    EquipmentName NVARCHAR(100) NOT NULL,
    EquipmentType NVARCHAR(50) NOT NULL,
    Location NVARCHAR(100) NOT NULL,
    InstallationDate DATE NOT NULL,
    Manufacturer NVARCHAR(100),
    ModelNumber NVARCHAR(50),
    MaxOperatingHours INT,
    MaintenanceCycle INT,
    Status NVARCHAR(20) DEFAULT 'Active',
    CreatedAt DATETIME2 DEFAULT GETDATE(),
    UpdatedAt DATETIME2 DEFAULT GETDATE()
);

-- メンテナンス履歴テーブル
CREATE TABLE MaintenanceHistory (
    MaintenanceId INT IDENTITY(1,1) PRIMARY KEY,
    EquipmentId INT NOT NULL,
    MaintenanceType NVARCHAR(50) NOT NULL,
    PerformedDate DATETIME2 NOT NULL,
    Technician NVARCHAR(100) NOT NULL,
    WorkDescription NVARCHAR(MAX),
    PartsReplaced NVARCHAR(MAX),
    Cost DECIMAL(10,2),
    NextScheduledDate DATE,
    CreatedAt DATETIME2 DEFAULT GETDATE(),
    FOREIGN KEY (EquipmentId) REFERENCES Equipment(EquipmentId)
);

-- 部品マスタテーブル
CREATE TABLE Parts (
    PartId INT IDENTITY(1,1) PRIMARY KEY,
    PartName NVARCHAR(100) NOT NULL,
    PartNumber NVARCHAR(50) NOT NULL UNIQUE,
    Supplier NVARCHAR(100),
    UnitPrice DECIMAL(10,2),
    StockQuantity INT DEFAULT 0,
    MinimumStock INT DEFAULT 0,
    CreatedAt DATETIME2 DEFAULT GETDATE(),
    UpdatedAt DATETIME2 DEFAULT GETDATE()
);

-- 設備-部品関連テーブル
CREATE TABLE EquipmentParts (
    EquipmentId INT NOT NULL,
    PartId INT NOT NULL,
    Quantity INT DEFAULT 1,
    PRIMARY KEY (EquipmentId, PartId),
    FOREIGN KEY (EquipmentId) REFERENCES Equipment(EquipmentId),
    FOREIGN KEY (PartId) REFERENCES Parts(PartId)
);
EOF

cat > database/schema/02_insert_sample_data.sql << 'EOF'
-- サンプル設備データの挿入
INSERT INTO Equipment (EquipmentName, EquipmentType, Location, InstallationDate, Manufacturer, ModelNumber, MaxOperatingHours, MaintenanceCycle)
VALUES 
    ('射出成形機-1', 'injection_molding', '製造ライン A', '2022-01-15', '株式会社A製作所', 'IM-2000A', 8760, 90),
    ('射出成形機-2', 'injection_molding', '製造ライン A', '2022-02-01', '株式会社A製作所', 'IM-2000A', 8760, 90),
    ('組立ロボット-1', 'assembly_robot', '製造ライン B', '2022-03-10', 'ロボティクス株式会社', 'AR-500X', 8760, 180),
    ('検査装置-1', 'inspection_device', '製造ライン C', '2022-04-20', '精密機器メーカー', 'ID-300Z', 8760, 120),
    ('コンプレッサー-1', 'compressor', '共通設備', '2021-12-01', 'エア機器株式会社', 'CP-1000', 8760, 365);

-- サンプル部品データの挿入
INSERT INTO Parts (PartName, PartNumber, Supplier, UnitPrice, StockQuantity, MinimumStock)
VALUES 
    ('オイルフィルター', 'OF-001', '部品サプライヤーA', 1500.00, 50, 10),
    ('ベアリング', 'BR-002', '部品サプライヤーB', 3000.00, 30, 5),
    ('シール材', 'SL-003', '部品サプライヤーC', 800.00, 100, 20),
    ('モーター', 'MT-004', '部品サプライヤーD', 50000.00, 5, 2),
    ('センサー', 'SN-005', '部品サプライヤーE', 8000.00, 20, 5);

-- 設備-部品関連データの挿入
INSERT INTO EquipmentParts (EquipmentId, PartId, Quantity)
VALUES 
    (1, 1, 2), (1, 2, 4), (1, 3, 1),
    (2, 1, 2), (2, 2, 4), (2, 3, 1),
    (3, 2, 8), (3, 4, 1), (3, 5, 3),
    (4, 5, 5), (4, 3, 2),
    (5, 1, 1), (5, 2, 2), (5, 4, 1);
EOF
```

### 6.2 データベーススキーマのデプロイ
```bash
# SQL Server 情報の取得
SQL_SERVER_NAME=$(echo $SQL_CONNECTION_STRING | grep -o 'Server=tcp:[^,]*' | cut -d':' -f2 | cut -d',' -f1)
SQL_DATABASE_NAME=$(echo $SQL_CONNECTION_STRING | grep -o 'Initial Catalog=[^;]*' | cut -d'=' -f2)
SQL_USERNAME=$(echo $SQL_CONNECTION_STRING | grep -o 'User ID=[^;]*' | cut -d'=' -f2)
SQL_PASSWORD=$(echo $SQL_CONNECTION_STRING | grep -o 'Password=[^;]*' | cut -d'=' -f2)

echo "データベース情報:"
echo "サーバー: $SQL_SERVER_NAME"
echo "データベース: $SQL_DATABASE_NAME"
echo "ユーザー: $SQL_USERNAME"

# sqlcmd の実行（SQL Server コマンドラインツールが必要）
# Ubuntu/Debian の場合
curl https://packages.microsoft.com/keys/microsoft.asc | sudo apt-key add -
curl https://packages.microsoft.com/config/ubuntu/20.04/prod.list | sudo tee /etc/apt/sources.list.d/msprod.list
sudo apt-get update
sudo apt-get install mssql-tools unixodbc-dev

# スキーマのデプロイ
echo "データベーススキーマをデプロイしています..."
/opt/mssql-tools/bin/sqlcmd -S $SQL_SERVER_NAME -d $SQL_DATABASE_NAME -U $SQL_USERNAME -P $SQL_PASSWORD -i database/schema/01_create_tables.sql

echo "サンプルデータを挿入しています..."
/opt/mssql-tools/bin/sqlcmd -S $SQL_SERVER_NAME -d $SQL_DATABASE_NAME -U $SQL_USERNAME -P $SQL_PASSWORD -i database/schema/02_insert_sample_data.sql

echo "データベースのデプロイが完了しました"
```

## 7. CI/CD パイプラインの設定

### 7.1 GitHub Actions ワークフローの作成
```bash
# .github/workflows ディレクトリの作成
mkdir -p .github/workflows

# CI/CD パイプラインの作成
cat > .github/workflows/deploy.yml << 'EOF'
name: Deploy Factory Equipment Management App

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

env:
  AZURE_RESOURCE_GROUP: ${{ secrets.AZURE_RESOURCE_GROUP }}
  AZURE_FUNCTIONAPP_NAME: ${{ secrets.AZURE_FUNCTIONAPP_NAME }}
  AZURE_WEBAPP_NAME: ${{ secrets.AZURE_WEBAPP_NAME }}
  AZURE_STATICWEBAPP_NAME: ${{ secrets.AZURE_STATICWEBAPP_NAME }}

jobs:
  test:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v4
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.9'
    
    - name: Install Python dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
        pip install pytest pytest-cov
    
    - name: Run Python tests
      run: |
        pytest tests/ --cov=backend --cov-report=xml
    
    - name: Set up Node.js
      uses: actions/setup-node@v4
      with:
        node-version: '18'
    
    - name: Install Node.js dependencies
      working-directory: ./frontend
      run: npm install
    
    - name: Run frontend tests
      working-directory: ./frontend
      run: npm run test:unit
    
    - name: Build frontend
      working-directory: ./frontend
      run: npm run build

  deploy-functions:
    needs: test
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    
    steps:
    - uses: actions/checkout@v4
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.9'
    
    - name: Install dependencies
      working-directory: ./backend/functions
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
    
    - name: Login to Azure
      uses: azure/login@v1
      with:
        creds: ${{ secrets.AZURE_CREDENTIALS }}
    
    - name: Deploy Azure Functions
      uses: Azure/functions-action@v1
      with:
        app-name: ${{ env.AZURE_FUNCTIONAPP_NAME }}
        package: './backend/functions'
        publish-profile: ${{ secrets.AZURE_FUNCTIONAPP_PUBLISH_PROFILE }}

  deploy-webapp:
    needs: test
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    
    steps:
    - uses: actions/checkout@v4
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.9'
    
    - name: Install dependencies
      working-directory: ./backend/api
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
    
    - name: Login to Azure
      uses: azure/login@v1
      with:
        creds: ${{ secrets.AZURE_CREDENTIALS }}
    
    - name: Deploy to Azure Web App
      uses: azure/webapps-deploy@v2
      with:
        app-name: ${{ env.AZURE_WEBAPP_NAME }}
        package: './backend/api'

  deploy-frontend:
    needs: test
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    
    steps:
    - uses: actions/checkout@v4
    
    - name: Set up Node.js
      uses: actions/setup-node@v4
      with:
        node-version: '18'
    
    - name: Install dependencies
      working-directory: ./frontend
      run: npm install
    
    - name: Build application
      working-directory: ./frontend
      run: npm run build
    
    - name: Deploy to Azure Static Web Apps
      uses: Azure/static-web-apps-deploy@v1
      with:
        azure_static_web_apps_api_token: ${{ secrets.AZURE_STATIC_WEB_APPS_API_TOKEN }}
        repo_token: ${{ secrets.GITHUB_TOKEN }}
        action: "upload"
        app_location: "/frontend"
        api_location: ""
        output_location: "dist"
EOF

echo "GitHub Actions ワークフローが作成されました"
```

### 7.2 GitHub Secrets の設定
```bash
# GitHub CLI を使用したシークレットの設定
echo "以下のシークレットをGitHubリポジトリに設定してください："

echo ""
echo "Azure認証情報："
az ad sp create-for-rbac --name "factory-equipment-mgmt-deploy" \
    --role contributor \
    --scopes /subscriptions/$AZURE_SUBSCRIPTION_ID/resourceGroups/$AZURE_RESOURCE_GROUP \
    --sdk-auth

echo ""
echo "GitHub Secrets として設定が必要な項目："
echo "AZURE_CREDENTIALS: 上記で出力されたJSON"
echo "AZURE_RESOURCE_GROUP: $AZURE_RESOURCE_GROUP"
echo "AZURE_FUNCTIONAPP_NAME: $FUNCTION_APP_NAME"
echo "AZURE_WEBAPP_NAME: $WEB_APP_NAME"
echo "AZURE_STATICWEBAPP_NAME: $STATIC_WEB_APP_NAME"

# 発行プロファイルの取得
echo ""
echo "発行プロファイルの取得："
az functionapp deployment list-publishing-profiles \
    --name $FUNCTION_APP_NAME \
    --resource-group $AZURE_RESOURCE_GROUP \
    --xml > function-app-publish-profile.xml

echo "function-app-publish-profile.xml をAZURE_FUNCTIONAPP_PUBLISH_PROFILE シークレットに設定してください"

# Static Web Apps のデプロイトークン取得
STATIC_WEB_APPS_TOKEN=$(az staticwebapp secrets list \
    --name $STATIC_WEB_APP_NAME \
    --resource-group $AZURE_RESOURCE_GROUP \
    --query properties.apiKey --output tsv)

echo "AZURE_STATIC_WEB_APPS_API_TOKEN: $STATIC_WEB_APPS_TOKEN"
```

## 8. 監視とアラートの設定

### 8.1 Application Insights の設定
```bash
# Application Insights の作成
APP_INSIGHTS_NAME="${APP_NAME}-insights-${ENVIRONMENT}"

az monitor app-insights component create \
    --app $APP_INSIGHTS_NAME \
    --location $AZURE_LOCATION \
    --resource-group $AZURE_RESOURCE_GROUP \
    --application-type web

# インストルメンテーションキーの取得
INSTRUMENTATION_KEY=$(az monitor app-insights component show \
    --app $APP_INSIGHTS_NAME \
    --resource-group $AZURE_RESOURCE_GROUP \
    --query instrumentationKey --output tsv)

# Function App に Application Insights を設定
az functionapp config appsettings set \
    --name $FUNCTION_APP_NAME \
    --resource-group $AZURE_RESOURCE_GROUP \
    --settings "APPINSIGHTS_INSTRUMENTATIONKEY=$INSTRUMENTATION_KEY"

# Web App に Application Insights を設定
az webapp config appsettings set \
    --name $WEB_APP_NAME \
    --resource-group $AZURE_RESOURCE_GROUP \
    --settings "APPINSIGHTS_INSTRUMENTATIONKEY=$INSTRUMENTATION_KEY"

echo "Application Insights が設定されました"
```

### 8.2 アラートルールの作成
```bash
# CPU使用率のアラート
az monitor metrics alert create \
    --name "High CPU Usage - ${WEB_APP_NAME}" \
    --resource-group $AZURE_RESOURCE_GROUP \
    --scopes "/subscriptions/$AZURE_SUBSCRIPTION_ID/resourceGroups/$AZURE_RESOURCE_GROUP/providers/Microsoft.Web/sites/$WEB_APP_NAME" \
    --condition "avg Percentage CPU > 80" \
    --description "CPU usage is above 80%" \
    --evaluation-frequency 5m \
    --window-size 15m \
    --severity 2

# エラー率のアラート
az monitor metrics alert create \
    --name "High Error Rate - ${WEB_APP_NAME}" \
    --resource-group $AZURE_RESOURCE_GROUP \
    --scopes "/subscriptions/$AZURE_SUBSCRIPTION_ID/resourceGroups/$AZURE_RESOURCE_GROUP/providers/Microsoft.Web/sites/$WEB_APP_NAME" \
    --condition "avg Http5xx > 5" \
    --description "Error rate is above 5 per minute" \
    --evaluation-frequency 5m \
    --window-size 15m \
    --severity 1

echo "アラートルールが作成されました"
```

## 9. デプロイメント後の確認

### 9.1 各サービスの動作確認
```bash
echo "=== デプロイメント後の動作確認 ==="

# Web API の確認
echo "Web API の確認:"
curl "https://${WEB_APP_NAME}.azurewebsites.net/api/health"
echo ""

# Function App の確認
echo "Function App の確認:"
az functionapp function list \
    --name $FUNCTION_APP_NAME \
    --resource-group $AZURE_RESOURCE_GROUP \
    --output table

# Static Web App の確認
echo "Static Web App の確認:"
STATIC_WEB_APP_URL=$(az staticwebapp show \
    --name $STATIC_WEB_APP_NAME \
    --resource-group $AZURE_RESOURCE_GROUP \
    --query defaultHostname --output tsv)

echo "Frontend URL: https://$STATIC_WEB_APP_URL"

# データベース接続の確認
echo "データベース接続の確認:"
/opt/mssql-tools/bin/sqlcmd -S $SQL_SERVER_NAME -d $SQL_DATABASE_NAME -U $SQL_USERNAME -P $SQL_PASSWORD -Q "SELECT COUNT(*) as EquipmentCount FROM Equipment"
```

### 9.2 エンドツーエンドテストの実行
```bash
# 簡単なエンドツーエンドテスト
echo "=== エンドツーエンドテスト ==="

# API エンドポイントのテスト
echo "1. API Health Check:"
response=$(curl -s -o /dev/null -w "%{http_code}" "https://${WEB_APP_NAME}.azurewebsites.net/api/health")
if [ $response -eq 200 ]; then
    echo "✓ API Health Check 成功"
else
    echo "✗ API Health Check 失敗 (HTTP $response)"
fi

echo "2. Equipment API Test:"
response=$(curl -s -o /dev/null -w "%{http_code}" "https://${WEB_APP_NAME}.azurewebsites.net/api/equipment")
if [ $response -eq 200 ]; then
    echo "✓ Equipment API 成功"
else
    echo "✗ Equipment API 失敗 (HTTP $response)"
fi

echo "3. Frontend アクセステスト:"
response=$(curl -s -o /dev/null -w "%{http_code}" "https://$STATIC_WEB_APP_URL")
if [ $response -eq 200 ]; then
    echo "✓ Frontend アクセス 成功"
else
    echo "✗ Frontend アクセス 失敗 (HTTP $response)"
fi

echo ""
echo "=== デプロイメント完了 ==="
echo "フロントエンド: https://$STATIC_WEB_APP_URL"
echo "API: https://${WEB_APP_NAME}.azurewebsites.net"
echo "Application Insights: https://portal.azure.com/#resource/subscriptions/$AZURE_SUBSCRIPTION_ID/resourceGroups/$AZURE_RESOURCE_GROUP/providers/Microsoft.Insights/components/$APP_INSIGHTS_NAME"
```

## 10. 運用・保守

### 10.1 ログ監視
```bash
# Application Insights でのログ確認
echo "Application Insights でのログ確認手順:"
echo "1. Azure Portal にアクセス"
echo "2. Application Insights リソース '$APP_INSIGHTS_NAME' を開く"
echo "3. 'ログ' メニューから以下のクエリを実行:"

cat << 'EOF'
-- リクエスト数の確認
requests
| summarize count() by bin(timestamp, 1h)
| order by timestamp desc

-- エラーログの確認
exceptions
| where timestamp > ago(24h)
| summarize count() by type
| order by count_ desc

-- パフォーマンス監視
requests
| where timestamp > ago(1h)
| summarize avg(duration) by bin(timestamp, 5m)
| order by timestamp desc
EOF
```

### 10.2 スケーリング設定
```bash
# Web App の自動スケーリング設定
az monitor autoscale create \
    --resource-group $AZURE_RESOURCE_GROUP \
    --resource "/subscriptions/$AZURE_SUBSCRIPTION_ID/resourceGroups/$AZURE_RESOURCE_GROUP/providers/Microsoft.Web/serverfarms/$APP_SERVICE_PLAN" \
    --name "autoscale-${WEB_APP_NAME}" \
    --min-count 1 \
    --max-count 5 \
    --count 1

# CPU使用率ベースのスケーリングルール
az monitor autoscale rule create \
    --resource-group $AZURE_RESOURCE_GROUP \
    --autoscale-name "autoscale-${WEB_APP_NAME}" \
    --condition "Percentage CPU > 70 avg 5m" \
    --scale out 1

az monitor autoscale rule create \
    --resource-group $AZURE_RESOURCE_GROUP \
    --autoscale-name "autoscale-${WEB_APP_NAME}" \
    --condition "Percentage CPU < 30 avg 5m" \
    --scale in 1

echo "自動スケーリングが設定されました"
```

### 10.3 バックアップとリストア
```bash
# SQL Database の自動バックアップ確認
az sql db show \
    --server $SQL_SERVER_NAME \
    --resource-group $AZURE_RESOURCE_GROUP \
    --name $SQL_DATABASE_NAME \
    --query '{BackupRetentionPeriod: currentBackupStorageRedundancy, EarliestRestoreDate: earliestRestoreDate}'

# Cosmos DB の継続的バックアップ確認
az cosmosdb show \
    --name $COSMOS_ACCOUNT_NAME \
    --resource-group $AZURE_RESOURCE_GROUP \
    --query '{BackupPolicy: backupPolicy}'

echo "バックアップ設定の確認が完了しました"
```

## まとめ

このデプロイメント手順書に従って、以下が完了しました：

### デプロイ済みコンポーネント
1. **Azure Functions**: サーバーレス処理機能
2. **Azure App Service**: Web API ホスティング
3. **Azure Static Web Apps**: フロントエンド ホスティング
4. **Azure SQL Database**: データベーススキーマとサンプルデータ
5. **Application Insights**: 監視とログ収集
6. **GitHub Actions**: CI/CDパイプライン

### 運用開始後のタスク
1. **監視ダッシュボードの確認**: Application Insights でのメトリクス監視
2. **アラート設定の調整**: 実際の使用パターンに基づく閾値調整
3. **スケーリング設定の最適化**: 負荷に応じたリソース調整
4. **セキュリティ設定の強化**: 本番運用に向けたセキュリティ強化
5. **災害復旧テスト**: バックアップとリストアの動作確認

### 次のステップ
1. Power BI ダッシュボードの作成と連携
2. IoT デバイスシミュレーターの構築
3. 機械学習モデルの実装と統合
4. 本格的な運用データの投入
5. ユーザートレーニングと運用開始

デプロイメントが完了し、工場設備管理アプリケーションが本番環境で稼働可能になりました。