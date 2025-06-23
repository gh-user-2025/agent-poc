# 工場設備管理アプリ プロトタイプ開発手順書

## 概要

本プロトタイプは、工場設備の稼働状況やメンテナンス情報を一元管理するWebアプリケーションです。フロントエンドにVue.js、バックエンドにPython HTTPサーバー、サーバーレス処理にAzure Functionsを使用しています。

## システム構成

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   フロントエンド  │    │   バックエンド    │    │ Azure Functions │
│   (Vue.js)      │◄──►│   (Python API)  │◄──►│  (データ処理)   │
│   Port: 8080    │    │   Port: 5000    │    │   Port: 7071    │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## 必要な環境

### 基本要件
- Node.js 16以上
- Python 3.8以上
- Visual Studio Code (推奨)

### 開発ツール
- Azure Functions Core Tools (Azure Functions開発用)
- curl または Postman (API テスト用)

## セットアップ手順

### 1. プロジェクトクローン

```bash
git clone <repository-url>
cd agent-poc
```

### 2. フロントエンド環境構築

```bash
cd frontend
npm install
```

### 3. バックエンド環境構築

```bash
cd ../backend
# 依存関係は標準ライブラリのみのため、追加インストールは不要
```

### 4. Azure Functions 環境構築（オプション）

```bash
cd functions
# Azure Functions Core Tools をインストール済みの場合
func start
```

## 開発サーバー起動手順

### ターミナル1: バックエンドAPI起動

```bash
cd backend
python3 simple_api.py
```

サーバーが起動すると以下が表示されます：
```
バックエンドAPIサーバーが起動しました: http://localhost:5000
利用可能なエンドポイント:
  GET /api/health
  GET /api/equipment
  GET /api/equipment/{id}
  GET /api/equipment/summary
  GET /api/alerts
  GET /api/sensor-data/{id}
```

### ターミナル2: フロントエンド起動

```bash
cd frontend
npm run dev
```

ブラウザで http://localhost:8080 にアクセスしてアプリケーションを確認できます。

### ターミナル3: Azure Functions起動（オプション）

```bash
cd backend/functions
func start
```

## API エンドポイント

### ヘルスチェック
```bash
curl http://localhost:5000/api/health
```

### 設備一覧取得
```bash
# 全設備
curl http://localhost:5000/api/equipment

# 場所でフィルタ
curl "http://localhost:5000/api/equipment?location=ライン A"

# 状態でフィルタ
curl "http://localhost:5000/api/equipment?status=running"
```

### 設備詳細取得
```bash
curl http://localhost:5000/api/equipment/1
```

### 設備サマリー取得
```bash
curl http://localhost:5000/api/equipment/summary
```

### アラート一覧取得
```bash
# 全アラート
curl http://localhost:5000/api/alerts

# アクティブなアラートのみ
curl "http://localhost:5000/api/alerts?status=active"

# エラーレベルのみ
curl "http://localhost:5000/api/alerts?severity=error"
```

### センサーデータ取得
```bash
curl http://localhost:5000/api/sensor-data/1
```

## 機能確認手順

### 1. ホーム画面確認

1. ブラウザで http://localhost:8080 にアクセス
2. 設備サマリーが表示されることを確認
3. 「データを更新」ボタンでAPI連携が動作することを確認
4. 最近のアラートが表示されることを確認

### 2. 設備稼働状況画面確認

1. ナビゲーションから「設備稼働状況」をクリック
2. 設備一覧が表示されることを確認
3. フィルター機能（場所・状態）が動作することを確認
4. 設備カードをクリックして詳細モーダルが表示されることを確認
5. 「更新」ボタンでAPI連携が動作することを確認

### 3. API連携確認

フロントエンドの開発者ツール（F12）のConsoleで以下を確認：
- 「APIからデータを取得しました」というログが表示される
- APIエラーが発生していないことを確認

## トラブルシューティング

### ポート競合エラー

**エラー:** `Address already in use`

**解決策:**
```bash
# ポート5000を使用しているプロセスを確認
lsof -i :5000

# プロセスを停止
kill -9 <PID>
```

### CORS エラー

**エラー:** `Access to fetch at 'http://localhost:5000/api/...' from origin 'http://localhost:8080' has been blocked by CORS policy`

**解決策:** バックエンドAPIサーバーにCORS対応が含まれているため、通常は発生しません。発生した場合はブラウザのキャッシュをクリアしてください。

### API接続エラー

**エラー:** フロントエンドで「APIからのデータ取得に失敗しました」

**対処:**
1. バックエンドAPIサーバーが起動していることを確認
2. `curl http://localhost:5000/api/health` でAPIが応答することを確認
3. ファイアウォール設定を確認

## 本番環境デプロイ時の注意事項

### 1. 環境変数設定

フロントエンドの環境変数（`.env`ファイル）:
```
VUE_APP_API_URL=https://your-api-domain.com/api
VUE_APP_FUNCTIONS_URL=https://your-functions-app.azurewebsites.net
```

### 2. セキュリティ設定

- CORS設定を本番環境のドメインに限定
- APIキーまたは認証機能の追加
- HTTPS通信の強制

### 3. パフォーマンス最適化

- フロントエンドのプロダクションビルド: `npm run build`
- APIレスポンスのキャッシュ設定
- データベース接続プールの設定

## 次のステップ

1. **Azure リソースとの連携**
   - Azure SQL Database 接続
   - Azure Cosmos DB 接続
   - Azure IoT Hub 連携

2. **機能拡張**
   - リアルタイムデータ更新（WebSocket）
   - メンテナンス管理機能
   - ユーザー認証・認可

3. **監視・ログ**
   - Application Insights 連携
   - ログ収集・分析機能
   - アラート通知機能

## サポート

開発中に問題が発生した場合は、以下の情報を収集してください：

1. エラーメッセージ
2. ブラウザのConsoleログ
3. APIサーバーのログ
4. 実行環境情報（OS、Node.js・Pythonバージョン）