# 🏭 工場設備管理システム

Azure クラウドベースの工場設備管理アプリケーションのプロトタイプです。設備の稼働状況をリアルタイムで監視し、予防保全とデータ駆動型の運用改善を実現します。

## 📋 プロジェクト概要

### 目的
- **設備の稼働状況のリアルタイム監視**: センサーを活用して、設備の稼働状況をリアルタイムで監視
- **メンテナンス管理**: 設備のメンテナンススケジュールを管理し、予防保全を実現
- **データ分析**: 設備の稼働データを分析し、効率的な運用方法を提案

### 期待される成果
- 設備の稼働状況をリアルタイムで把握することで、ダウンタイムを削減
- メンテナンスの効率化により、設備の寿命を延長
- データに基づいた運用改善提案により、生産性を向上

## 🛠️ 技術スタック

### フロントエンド
- **Vue.js 3** - ユーザーインターフェース
- **Vue Router** - 画面遷移管理
- **Chart.js** - データ可視化（将来実装予定）

### バックエンド
- **Azure Functions** - サーバーレス API
- **Python 3.9+** - バックエンド言語

### データストレージ
- **Azure SQL Database** - 収集したデータを保存
- **Azure Cosmos DB** - IoT デバイスからのデータをリアルタイムで処理

### 可視化・分析
- **Power BI** - データの可視化と分析結果の共有
- **Application Insights** - アプリケーション監視

## 🏗️ アーキテクチャ

```
[IoTデバイス] → [Azure Cosmos DB] → [Azure Functions] → [Vue.js Frontend]
                      ↓
[Azure SQL Database] → [Power BI] → [ダッシュボード・レポート]
```

## 🚀 クイックスタート

### 前提条件

- Node.js 16.x 以上
- Python 3.9 以上
- Azure CLI
- Azure Functions Core Tools

### 1. リポジトリのクローン

```bash
git clone https://github.com/gh-user-2025/agent-poc.git
cd agent-poc
```

### 2. フロントエンドの起動

```bash
# 依存関係のインストール
npm install

# 開発サーバーの起動
npm run serve
```

アプリケーションは http://localhost:8080 でアクセスできます。

### 3. Azure Functions のローカル実行

```bash
# Azure Functions ディレクトリに移動
cd azure-functions

# Python仮想環境の作成
python -m venv venv
source venv/bin/activate  # Linux/macOS
# venv\Scripts\activate   # Windows

# 依存関係のインストール
pip install -r requirements.txt

# Functions の起動
func start
```

## 📱 機能概要

### 🏠 ダッシュボード
- 設備稼働状況の概要表示
- 主要KPI（稼働率、アラート数、メンテナンス予定）
- クイックアクションボタン

### 📺 設備監視
- リアルタイム設備ステータス監視
- 設備別の詳細情報表示
- アラート管理機能

### 🔧 メンテナンス管理
- メンテナンススケジュール管理
- メンテナンス履歴閲覧
- 統計情報とパフォーマンス分析

### 📈 データ分析
- AI による運用改善提案
- 予測分析（メンテナンス需要、生産予測）
- KPI ダッシュボード

## 🌐 API エンドポイント

### 設備監視 API
```
POST /api/equipment/monitoring
```
設備データの受信と処理

### メンテナンス管理 API
```
GET    /api/maintenance          # スケジュール一覧取得
POST   /api/maintenance          # 新規スケジュール作成
PUT    /api/maintenance/{id}     # スケジュール更新
DELETE /api/maintenance/{id}     # スケジュール削除
```

### データ分析 API
```
GET /api/analytics?type={type}&period={period}
```
- type: overview, efficiency, predictive, recommendations
- period: day, week, month, quarter

## 📚 ドキュメント

### Azure セットアップガイド
- [Azure リソース作成手順](docs/azure-setup/azure-resources-setup.md)
- [Azure Functions デプロイ手順](docs/azure-setup/azure-functions-deployment.md)
- [Power BI 連携設定](docs/azure-setup/power-bi-integration.md)

### 開発ガイド
- [フロントエンド開発ガイド](docs/development/frontend-guide.md)（作成予定）
- [バックエンド開発ガイド](docs/development/backend-guide.md)（作成予定）
- [データベース設計](docs/development/database-design.md)（作成予定）

## 🎯 開発状況

### 完了済み機能
- ✅ Vue.js フロントエンドアプリケーション
- ✅ Azure Functions バックエンド API
- ✅ 基本的な設備監視機能
- ✅ メンテナンス管理機能
- ✅ データ分析とAI提案機能

### 今後の開発予定
- 🔄 リアルタイムデータ連携
- 🔄 Power BI ダッシュボード統合
- 🔄 IoT デバイス連携
- 🔄 アラート通知機能
- 🔄 モバイルアプリ対応

## 🤝 コントリビューション

1. このリポジトリをフォーク
2. 機能ブランチを作成 (`git checkout -b feature/amazing-feature`)
3. 変更をコミット (`git commit -m 'Add amazing feature'`)
4. ブランチにプッシュ (`git push origin feature/amazing-feature`)
5. プルリクエストを作成

## 📄 ライセンス

このプロジェクトは MIT ライセンスの下で公開されています。詳細は [LICENSE](LICENSE) ファイルをご覧ください。

## 🆘 サポート

問題や質問がある場合は、[Issues](https://github.com/gh-user-2025/agent-poc/issues) ページで報告してください。

## 🔗 関連リンク

- [Azure Functions ドキュメント](https://docs.microsoft.com/ja-jp/azure/azure-functions/)
- [Vue.js ドキュメント](https://v3.ja.vuejs.org/)
- [Power BI ドキュメント](https://docs.microsoft.com/ja-jp/power-bi/)
- [Azure IoT ドキュメント](https://docs.microsoft.com/ja-jp/azure/iot/)

---

## AI-Driven Development Workshop 👉 [Link](https://dev-lab-io.github.io/aoai/scenario2/home)

このプロジェクトは AI-Driven Development の手法を活用して開発されました。
