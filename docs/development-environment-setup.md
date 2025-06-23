# 開発環境セットアップ手順書

## 概要
この手順書では、工場設備管理アプリの開発環境をセットアップする手順を説明します。AI-Driven Development のアプローチを採用し、効率的な開発環境を構築します。

## 1. 前提条件

### 1.1 必要なソフトウェア
- **Visual Studio Code**: コードエディタ
- **Python 3.9以上**: メインの開発言語
- **Node.js 16以上**: フロントエンド開発ツール
- **Git**: バージョン管理
- **Azure CLI**: Azureリソース管理
- **Docker**: コンテナ開発（オプション）

### 1.2 アカウント要件
- **Azureサブスクリプション**: 開発・テスト環境用
- **GitHub アカウント**: ソースコード管理用
- **Power BI アカウント**: データ可視化用

## 2. 基本ツールのインストール

### 2.1 Visual Studio Code のインストール
```bash
# Ubuntu/Debian の場合
wget -qO- https://packages.microsoft.com/keys/microsoft.asc | gpg --dearmor > packages.microsoft.gpg
sudo install -o root -g root -m 644 packages.microsoft.gpg /etc/apt/trusted.gpg.d/
sudo sh -c 'echo "deb [arch=amd64,arm64,armhf signed-by=/etc/apt/trusted.gpg.d/packages.microsoft.gpg] https://packages.microsoft.com/repos/code stable main" > /etc/apt/sources.list.d/vscode.list'
sudo apt update
sudo apt install code

# macOS の場合
brew install --cask visual-studio-code

# Windows の場合
# https://code.visualstudio.com/ からダウンロードしてインストール
```

### 2.2 Python のインストールと設定
```bash
# Ubuntu/Debian の場合
sudo apt update
sudo apt install python3 python3-pip python3-venv

# macOS の場合
brew install python3

# Python バージョンの確認
python3 --version

# pip のアップグレード
python3 -m pip install --upgrade pip
```

### 2.3 Node.js のインストール
```bash
# Ubuntu/Debian の場合
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt-get install -y nodejs

# macOS の場合
brew install node

# Windows の場合
# https://nodejs.org/ からダウンロードしてインストール

# バージョン確認
node --version
npm --version
```

### 2.4 Azure CLI のインストール
```bash
# Ubuntu/Debian の場合
curl -sL https://aka.ms/InstallAzureCLIDeb | sudo bash

# macOS の場合
brew install azure-cli

# Windows の場合
# https://docs.microsoft.com/ja-jp/cli/azure/install-azure-cli-windows からインストール

# インストール確認
az --version
```

## 3. 開発環境の構築

### 3.1 プロジェクト構造の作成
```bash
# プロジェクトディレクトリの作成
mkdir factory-equipment-management
cd factory-equipment-management

# 基本的なディレクトリ構造を作成
mkdir -p {backend/{functions,api,models,utils},frontend/{src/{components,views,services},public},data/{mock,schemas},tests/{unit,integration},docs,infrastructure,scripts}

# 基本ファイルの作成
touch README.md
touch .gitignore
touch requirements.txt
touch package.json

# ディレクトリ構造の確認
tree . -L 3
```

### 3.2 Python 仮想環境の設定
```bash
# 仮想環境の作成
python3 -m venv venv

# 仮想環境の有効化
# Linux/macOS の場合
source venv/bin/activate

# Windows の場合
# venv\Scripts\activate

# 有効化の確認
which python
python --version
```

### 3.3 Python パッケージのインストール
```bash
# requirements.txt ファイルの作成
cat > requirements.txt << 'EOF'
# Azure SDK
azure-functions==1.15.0
azure-cosmos==4.5.1
azure-storage-blob==12.19.0
azure-sql-database==12.0.0
azure-eventhub==5.11.4
azure-iot-hub==2.6.1
azure-keyvault-secrets==4.7.0

# データ処理
pandas==2.1.4
numpy==1.24.3
scikit-learn==1.3.2

# Web フレームワーク
flask==3.0.0
flask-cors==4.0.0

# データベース
pyodbc==5.0.1
sqlalchemy==2.0.23

# ユーティリティ
python-dotenv==1.0.0
requests==2.31.0
pydantic==2.5.0

# 開発・テスト
pytest==7.4.3
pytest-cov==4.1.0
black==23.11.0
flake8==6.1.0

# 機械学習
tensorflow==2.14.0
joblib==1.3.2
EOF

# パッケージのインストール
pip install -r requirements.txt
```

### 3.4 Node.js プロジェクトの初期化
```bash
# package.json の作成
cat > package.json << 'EOF'
{
  "name": "factory-equipment-management-frontend",
  "version": "1.0.0",
  "description": "Factory Equipment Management Frontend",
  "main": "index.js",
  "scripts": {
    "dev": "vue-cli-service serve",
    "build": "vue-cli-service build",
    "lint": "vue-cli-service lint",
    "test": "jest"
  },
  "dependencies": {
    "vue": "^3.3.8",
    "vue-router": "^4.2.5",
    "vuex": "^4.1.0",
    "axios": "^1.6.2",
    "chart.js": "^4.4.0",
    "vue-chartjs": "^5.2.0",
    "element-plus": "^2.4.3"
  },
  "devDependencies": {
    "@vue/cli-service": "^5.0.8",
    "@vue/compiler-sfc": "^3.3.8",
    "jest": "^29.7.0",
    "eslint": "^8.54.0",
    "prettier": "^3.1.0"
  }
}
EOF

# Node.js パッケージのインストール
npm install
```

## 4. VS Code 拡張機能の設定

### 4.1 必須拡張機能のインストール
```bash
# Azure 関連
code --install-extension ms-azure-devops.azure-pipelines
code --install-extension ms-azuretools.azure-account
code --install-extension ms-azuretools.vscode-azurefunctions
code --install-extension ms-azuretools.vscode-cosmosdb

# Python 開発
code --install-extension ms-python.python
code --install-extension ms-python.black-formatter
code --install-extension ms-python.flake8

# JavaScript/Vue 開発
code --install-extension octref.vetur
code --install-extension esbenp.prettier-vscode
code --install-extension dbaeumer.vscode-eslint

# AI-Driven Development
code --install-extension github.copilot
code --install-extension github.copilot-chat

# その他のユーティリティ
code --install-extension ms-vscode.vscode-json
code --install-extension redhat.vscode-yaml
code --install-extension ms-vscode.azure-account
```

### 4.2 VS Code ワークスペース設定
```bash
# .vscode ディレクトリの作成
mkdir .vscode

# settings.json の作成
cat > .vscode/settings.json << 'EOF'
{
    "python.defaultInterpreterPath": "./venv/bin/python",
    "python.formatting.provider": "black",
    "python.linting.enabled": true,
    "python.linting.flake8Enabled": true,
    "python.testing.pytestEnabled": true,
    "python.testing.unittestEnabled": false,
    "python.testing.pytestArgs": ["tests"],
    
    "eslint.workingDirectories": ["frontend"],
    "prettier.configPath": "frontend/.prettierrc",
    
    "azure.subscription": "",
    "azure.resourceGroups": "",
    
    "git.autofetch": true,
    "git.enableSmartCommit": true,
    
    "files.exclude": {
        "**/__pycache__": true,
        "**/node_modules": true,
        "**/.pytest_cache": true
    }
}
EOF

# launch.json の作成（デバッグ設定）
cat > .vscode/launch.json << 'EOF'
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Python: Azure Functions",
            "type": "python",
            "request": "launch",
            "program": "${workspaceFolder}/backend/functions",
            "console": "integratedTerminal",
            "cwd": "${workspaceFolder}/backend/functions",
            "env": {
                "PYTHONPATH": "${workspaceFolder}/backend"
            }
        },
        {
            "name": "Python: Flask API",
            "type": "python",
            "request": "launch",
            "program": "${workspaceFolder}/backend/api/app.py",
            "console": "integratedTerminal",
            "cwd": "${workspaceFolder}/backend/api",
            "env": {
                "FLASK_ENV": "development",
                "PYTHONPATH": "${workspaceFolder}/backend"
            }
        }
    ]
}
EOF

# tasks.json の作成（ビルドタスク）
cat > .vscode/tasks.json << 'EOF'
{
    "version": "2.0.0",
    "tasks": [
        {
            "label": "Install Python Requirements",
            "type": "shell",
            "command": "${workspaceFolder}/venv/bin/pip",
            "args": ["install", "-r", "requirements.txt"],
            "group": "build",
            "presentation": {
                "echo": true,
                "reveal": "always",
                "panel": "new"
            }
        },
        {
            "label": "Run Python Tests",
            "type": "shell",
            "command": "${workspaceFolder}/venv/bin/pytest",
            "args": ["tests/", "-v", "--cov=backend"],
            "group": "test",
            "presentation": {
                "echo": true,
                "reveal": "always",
                "panel": "new"
            }
        },
        {
            "label": "Format Python Code",
            "type": "shell",
            "command": "${workspaceFolder}/venv/bin/black",
            "args": ["backend/", "tests/"],
            "group": "build",
            "presentation": {
                "echo": true,
                "reveal": "always",
                "panel": "new"
            }
        },
        {
            "label": "Install Node Dependencies",
            "type": "shell",
            "command": "npm",
            "args": ["install"],
            "options": {
                "cwd": "${workspaceFolder}/frontend"
            },
            "group": "build",
            "presentation": {
                "echo": true,
                "reveal": "always",
                "panel": "new"
            }
        },
        {
            "label": "Start Vue Development Server",
            "type": "shell",
            "command": "npm",
            "args": ["run", "dev"],
            "options": {
                "cwd": "${workspaceFolder}/frontend"
            },
            "group": "build",
            "presentation": {
                "echo": true,
                "reveal": "always",
                "panel": "new"
            }
        }
    ]
}
EOF
```

## 5. 環境変数の設定

### 5.1 .env ファイルの作成
```bash
# .env ファイルの作成
cat > .env << 'EOF'
# Azure リソース設定
AZURE_SUBSCRIPTION_ID=your-subscription-id
AZURE_RESOURCE_GROUP=your-resource-group
AZURE_LOCATION=japaneast

# Azure SQL Database
SQL_SERVER_NAME=your-sql-server-name
SQL_DATABASE_NAME=your-database-name
SQL_USERNAME=your-username
SQL_PASSWORD=your-password
SQL_CONNECTION_STRING=your-connection-string

# Azure Cosmos DB
COSMOS_ACCOUNT_NAME=your-cosmos-account-name
COSMOS_DATABASE_NAME=FactoryEquipmentDB
COSMOS_CONNECTION_STRING=your-cosmos-connection-string

# Azure Storage
STORAGE_ACCOUNT_NAME=your-storage-account-name
STORAGE_ACCOUNT_KEY=your-storage-key
STORAGE_CONNECTION_STRING=your-storage-connection-string

# Azure IoT Hub
IOT_HUB_NAME=your-iothub-name
IOT_HUB_CONNECTION_STRING=your-iothub-connection-string

# Azure Event Hubs
EVENT_HUB_NAMESPACE=your-eventhub-namespace
EVENT_HUB_NAME=sensor-data-stream
EVENT_HUB_CONNECTION_STRING=your-eventhub-connection-string

# Azure Key Vault
KEY_VAULT_NAME=your-keyvault-name
KEY_VAULT_URL=https://your-keyvault-name.vault.azure.net/

# API 設定
API_HOST=localhost
API_PORT=5000
API_DEBUG=True

# フロントエンド設定
VUE_APP_API_BASE_URL=http://localhost:5000/api
VUE_APP_ENVIRONMENT=development
EOF

echo ".env ファイルが作成されました。実際の値に置き換えてください。"
```

### 5.2 .gitignore ファイルの設定
```bash
# .gitignore ファイルの作成
cat > .gitignore << 'EOF'
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg
MANIFEST

# Virtual Environment
venv/
env/
ENV/

# IDEs
.vscode/settings.json
.idea/
*.swp
*.swo
*~

# Environment variables
.env
.env.local
.env.development.local
.env.test.local
.env.production.local

# Node.js
node_modules/
npm-debug.log*
yarn-debug.log*
yarn-error.log*

# Vue.js
dist/
.nuxt/

# Testing
.coverage
.pytest_cache/
coverage/

# Logs
logs/
*.log

# Azure
.azure/
local.settings.json

# Temporary files
*.tmp
*.temp
.DS_Store
Thumbs.db

# Database
*.db
*.sqlite

# Backup files
*.bak
*.backup

# OS generated files
.DS_Store
.DS_Store?
._*
.Spotlight-V100
.Trashes
ehthumbs.db
Thumbs.db
EOF
```

## 6. 開発ツールの設定

### 6.1 Python コードフォーマッターの設定
```bash
# pyproject.toml の作成（Black 設定）
cat > pyproject.toml << 'EOF'
[tool.black]
line-length = 88
target-version = ['py39']
include = '\.pyi?$'
extend-exclude = '''
/(
  # directories
  \.eggs
  | \.git
  | \.hg
  | \.mypy_cache
  | \.tox
  | \.venv
  | _build
  | buck-out
  | build
  | dist
)/
'''

[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = ["test_*.py", "*_test.py"]
python_classes = ["Test*"]
python_functions = ["test_*"]
addopts = "-v --cov=backend --cov-report=html --cov-report=term"
EOF

# .flake8 設定ファイルの作成
cat > .flake8 << 'EOF'
[flake8]
max-line-length = 88
extend-ignore = E203, W503
exclude = 
    .git,
    __pycache__,
    build,
    dist,
    venv,
    .venv
EOF
```

### 6.2 フロントエンド開発ツールの設定
```bash
# frontend ディレクトリに移動
cd frontend

# .eslintrc.js の作成
cat > .eslintrc.js << 'EOF'
module.exports = {
  env: {
    node: true,
  },
  extends: [
    'eslint:recommended',
    '@vue/eslint-config-prettier',
  ],
  parserOptions: {
    ecmaVersion: 2020,
  },
  rules: {
    'no-console': process.env.NODE_ENV === 'production' ? 'warn' : 'off',
    'no-debugger': process.env.NODE_ENV === 'production' ? 'warn' : 'off',
  },
}
EOF

# .prettierrc の作成
cat > .prettierrc << 'EOF'
{
  "semi": true,
  "singleQuote": true,
  "tabWidth": 2,
  "trailingComma": "es5",
  "printWidth": 80
}
EOF

# プロジェクトルートに戻る
cd ..
```

## 7. Azure Functions 開発環境の設定

### 7.1 Azure Functions Core Tools のインストール
```bash
# Ubuntu/Debian の場合
curl https://packages.microsoft.com/keys/microsoft.asc | gpg --dearmor > microsoft.gpg
sudo mv microsoft.gpg /etc/apt/trusted.gpg.d/microsoft.gpg
sudo sh -c 'echo "deb [arch=amd64] https://packages.microsoft.com/repos/microsoft-ubuntu-$(lsb_release -cs)-prod $(lsb_release -cs) main" > /etc/apt/sources.list.d/dotnetdev.list'
sudo apt-get update
sudo apt-get install azure-functions-core-tools-4

# macOS の場合
brew tap azure/functions
brew install azure-functions-core-tools@4

# インストール確認
func --version
```

### 7.2 Functions プロジェクトの初期化
```bash
# backend/functions ディレクトリに移動
cd backend/functions

# Functions プロジェクトの初期化
func init . --python

# local.settings.json の作成
cat > local.settings.json << 'EOF'
{
  "IsEncrypted": false,
  "Values": {
    "AzureWebJobsStorage": "UseDevelopmentStorage=true",
    "FUNCTIONS_WORKER_RUNTIME": "python",
    "CosmosDbConnectionString": "",
    "SqlConnectionString": "",
    "StorageConnectionString": "",
    "EventHubConnectionString": "",
    "IoTHubConnectionString": ""
  }
}
EOF

# プロジェクトルートに戻る
cd ../..

echo "Azure Functions 開発環境がセットアップされました"
```

## 8. 開発環境の検証

### 8.1 Python 環境の確認
```bash
# 仮想環境の有効化
source venv/bin/activate

# インストールされたパッケージの確認
pip list

# Python コードの動作確認
python -c "import azure.cosmos; print('Azure Cosmos DB SDK インストール済み')"
python -c "import pandas; print('Pandas インストール済み')"
python -c "import flask; print('Flask インストール済み')"
```

### 8.2 Node.js 環境の確認
```bash
# Node.js パッケージの確認
cd frontend
npm list --depth=0

# Vue CLI のインストール確認
npx vue --version

# プロジェクトルートに戻る
cd ..
```

### 8.3 Azure CLI の接続確認
```bash
# Azure へのログイン確認
az account show

# 必要に応じてログイン
# az login

# リソース グループの確認
az group list --output table
```

## 9. サンプルコードの作成

### 9.1 基本的な API サーバーの作成
```bash
# backend/api ディレクトリに移動
cd backend/api

# app.py の基本構造を作成
cat > app.py << 'EOF'
# Flask API の基本構造
from flask import Flask, jsonify
from flask_cors import CORS
import os
from dotenv import load_dotenv

# 環境変数の読み込み
load_dotenv()

app = Flask(__name__)
CORS(app)

@app.route('/api/health')
def health_check():
    """ヘルスチェック API"""
    return jsonify({
        'status': 'ok',
        'message': 'Factory Equipment Management API is running'
    })

@app.route('/api/equipment')
def get_equipment():
    """設備一覧の取得 API（サンプル）"""
    sample_equipment = [
        {
            'id': 1,
            'name': '射出成形機-1',
            'type': 'injection_molding',
            'status': 'running',
            'location': 'ライン A'
        },
        {
            'id': 2,
            'name': '組立ロボット-1',
            'type': 'assembly_robot',
            'status': 'idle',
            'location': 'ライン B'
        }
    ]
    return jsonify(sample_equipment)

if __name__ == '__main__':
    app.run(
        host=os.getenv('API_HOST', '0.0.0.0'),
        port=int(os.getenv('API_PORT', 5000)),
        debug=os.getenv('API_DEBUG', 'True').lower() == 'true'
    )
EOF

# プロジェクトルートに戻る
cd ../..
```

### 9.2 基本的な Vue.js アプリケーションの作成
```bash
# frontend/src ディレクトリに移動
cd frontend/src

# main.js の作成
cat > main.js << 'EOF'
import { createApp } from 'vue'
import App from './App.vue'

const app = createApp(App)
app.mount('#app')
EOF

# App.vue の基本構造を作成
cat > App.vue << 'EOF'
<template>
  <div id="app">
    <header>
      <h1>工場設備管理システム</h1>
    </header>
    
    <main>
      <div class="dashboard">
        <h2>設備監視ダッシュボード</h2>
        <div class="equipment-grid">
          <div 
            v-for="equipment in equipmentList" 
            :key="equipment.id"
            class="equipment-card"
            :class="equipment.status"
          >
            <h3>{{ equipment.name }}</h3>
            <p>場所: {{ equipment.location }}</p>
            <p>状態: {{ getStatusText(equipment.status) }}</p>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<script>
export default {
  name: 'App',
  data() {
    return {
      equipmentList: []
    }
  },
  methods: {
    async fetchEquipment() {
      try {
        const response = await fetch('http://localhost:5000/api/equipment')
        this.equipmentList = await response.json()
      } catch (error) {
        console.error('設備データの取得に失敗しました:', error)
      }
    },
    getStatusText(status) {
      const statusMap = {
        'running': '稼働中',
        'idle': '待機中',
        'maintenance': 'メンテナンス中',
        'error': 'エラー'
      }
      return statusMap[status] || '不明'
    }
  },
  mounted() {
    this.fetchEquipment()
  }
}
</script>

<style>
#app {
  font-family: Arial, sans-serif;
  margin: 0;
  padding: 20px;
}

header {
  background-color: #2c3e50;
  color: white;
  padding: 1rem;
  margin-bottom: 2rem;
  border-radius: 8px;
}

.equipment-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 1rem;
  margin-top: 1rem;
}

.equipment-card {
  border: 1px solid #ddd;
  border-radius: 8px;
  padding: 1rem;
  background-color: #f9f9f9;
}

.equipment-card.running {
  border-left: 4px solid #27ae60;
}

.equipment-card.idle {
  border-left: 4px solid #f39c12;
}

.equipment-card.maintenance {
  border-left: 4px solid #3498db;
}

.equipment-card.error {
  border-left: 4px solid #e74c3c;
}

.equipment-card h3 {
  margin: 0 0 0.5rem 0;
  color: #2c3e50;
}

.equipment-card p {
  margin: 0.25rem 0;
  color: #7f8c8d;
}
EOF

# プロジェクトルートに戻る
cd ../..
```

## 10. 開発環境の起動テスト

### 10.1 バックエンド API の起動
```bash
# Python 仮想環境の有効化
source venv/bin/activate

# バックエンド API の起動
cd backend/api
python app.py &
API_PID=$!

# API の動作確認
sleep 3
curl http://localhost:5000/api/health
curl http://localhost:5000/api/equipment

# プロセスの停止
kill $API_PID
cd ../..
```

### 10.2 フロントエンド の起動確認
```bash
# フロントエンド ディレクトリに移動
cd frontend

# 開発サーバーの起動（バックグラウンド）
npm run dev &
FRONTEND_PID=$!

echo "フロントエンド開発サーバーが起動しました"
echo "ブラウザで http://localhost:8080 にアクセスしてください"

# 5秒後にプロセスを停止
sleep 5
kill $FRONTEND_PID

# プロジェクトルートに戻る
cd ..
```

## 11. 開発環境の完了確認

### 11.1 環境構築の最終確認
```bash
echo "=== 開発環境セットアップ完了確認 ==="
echo ""

echo "✓ プロジェクト構造:"
tree . -L 2 -I 'node_modules|venv'

echo ""
echo "✓ Python 環境:"
source venv/bin/activate
python --version
pip --version

echo ""
echo "✓ Node.js 環境:"
node --version
npm --version

echo ""
echo "✓ Azure CLI:"
az --version | head -1

echo ""
echo "✓ VS Code 拡張機能:"
code --list-extensions | grep -E "(azure|python|copilot|vetur)"

echo ""
echo "=== セットアップ完了 ==="
echo "次のステップ:"
echo "1. .env ファイルの値を実際のAzureリソース情報に更新"
echo "2. Azure リソースの構築（azure-infrastructure-setup.md を参照）"
echo "3. アプリケーション開発の開始"
echo "4. VS Code でプロジェクトを開く: code ."
```

## まとめ

この手順書に従って、以下の開発環境が構築されました：

### 構築済み環境
1. **Visual Studio Code**: メインの開発エディタ
2. **Python 3.9**: バックエンド開発環境
3. **Node.js & Vue.js**: フロントエンド開発環境
4. **Azure CLI**: Azureリソース管理
5. **Azure Functions Core Tools**: サーバーレス開発
6. **GitHub Copilot**: AI-Driven Development

### プロジェクト構造
```
factory-equipment-management/
├── backend/
│   ├── functions/      # Azure Functions
│   ├── api/           # REST API
│   ├── models/        # データモデル
│   └── utils/         # ユーティリティ
├── frontend/
│   ├── src/           # Vue.js ソースコード
│   └── public/        # 静的ファイル
├── data/              # テストデータ・スキーマ
├── tests/             # テストコード
├── docs/              # ドキュメント
└── infrastructure/    # Azureリソース定義
```

### 次のステップ
1. Azureリソースの構築を実行
2. 環境変数の設定を完了
3. アプリケーション開発の開始
4. AI-Driven Development の活用開始

開発環境の準備が完了しました。効率的な開発のためにGitHub Copilotやその他のAIツールを積極的に活用してください。