# 工場設備管理アプリ プロトタイプ

## 概要

この工場設備管理アプリは、工場内の設備の稼働状況やメンテナンス情報を一元管理し、効率的な運用をサポートすることを目的としたプロトタイプです。AI-Driven Development のアプローチを採用し、Azure クラウドサービスを活用してスケーラブルで高可用性なシステムを構築します。

## 主要機能

- **設備の稼働状況のリアルタイム監視**: センサーを活用した設備稼働状況のリアルタイム監視
- **メンテナンス管理**: 予防保全を実現するメンテナンススケジュール管理
- **データ分析**: 設備稼働データの分析による効率的な運用提案
- **アラート機能**: 異常検知時の自動通知システム

## 技術スタック

### Azure サービス
- **Azure Functions**: データ処理・分析
- **Azure SQL Database**: 構造化データの保存
- **Azure Cosmos DB**: IoTデバイスからのリアルタイムデータ処理
- **Azure IoT Hub**: IoTデバイスとの通信
- **Azure Event Hubs**: ストリーミングデータの取り込み
- **Power BI**: データ可視化と分析結果の共有

### 開発技術
- **バックエンド**: Python, Flask, Azure Functions
- **フロントエンド**: Vue.js, JavaScript
- **データベース**: Azure SQL Database, Azure Cosmos DB
- **CI/CD**: GitHub Actions
- **監視**: Application Insights

## ドキュメント

### 📋 設計・計画書
- **[工場設備管理アプリ設計書](docs/factory-equipment-management-design.md)**: システム全体の設計仕様書
- **[機能要件定義書](docs/functional-requirements.md)**: システムの機能要件詳細
- **[非機能要件定義書](docs/non-functional-requirements.md)**: システムの非機能要件詳細
- **[ユースケース仕様書](docs/factory-equipment-use-cases.md)**: 詳細なユースケース定義

### ⚙️ 構築・セットアップ
- **[Azureインフラ構築手順書](docs/azure-infrastructure-setup.md)**: Azure CLIを使用したリソース構築の詳細手順
- **[開発環境セットアップ手順書](docs/development-environment-setup.md)**: ローカル開発環境の構築手順

### 🚀 デプロイメント・運用
- **[デプロイメント手順書](docs/deployment-guide.md)**: Azureクラウドへのデプロイメント手順

## 始め方

### 1. 前提条件
- Azureサブスクリプション
- Visual Studio Code
- Azure CLI
- Python 3.9以上
- Node.js 16以上

### 2. セットアップ手順

1. **リポジトリのクローン**
   ```bash
   git clone <repository-url>
   cd factory-equipment-management
   ```

2. **Azureリソースの構築**
   - [Azureインフラ構築手順書](docs/azure-infrastructure-setup.md) に従ってAzureリソースを構築

3. **開発環境のセットアップ**
   - [開発環境セットアップ手順書](docs/development-environment-setup.md) に従って開発環境を構築

4. **アプリケーションのデプロイ**
   - [デプロイメント手順書](docs/deployment-guide.md) に従ってAzureにデプロイ

## プロジェクト構造

```
factory-equipment-management/
├── docs/                          # ドキュメント
│   ├── factory-equipment-management-design.md
│   ├── azure-infrastructure-setup.md
│   ├── development-environment-setup.md
│   └── deployment-guide.md
├── backend/                       # バックエンドコード
│   ├── functions/                 # Azure Functions
│   ├── api/                      # REST API
│   ├── models/                   # データモデル
│   └── utils/                    # ユーティリティ
├── frontend/                      # フロントエンドコード
│   ├── src/                      # Vue.js ソースコード
│   │   ├── components/           # Vue コンポーネント
│   │   ├── views/               # ページビュー
│   │   └── services/            # API サービス
│   └── public/                   # 静的ファイル
├── data/                         # テストデータ・スキーマ
│   ├── mock/                     # モックデータ
│   └── schemas/                  # データベーススキーマ
├── tests/                        # テストコード
│   ├── unit/                     # ユニットテスト
│   └── integration/              # 統合テスト
├── infrastructure/               # Infrastructure as Code
├── scripts/                      # 運用スクリプト
└── .github/                      # GitHub Actions
    └── workflows/                # CI/CDワークフロー
```

## 開発アプローチ

### AI-Driven Development
このプロジェクトでは、以下のAI-Driven Developmentアプローチを採用しています：

- **GitHub Copilot**: コード生成とドキュメント作成の支援
- **自動テスト生成**: AI支援によるテストケースの生成
- **コードレビュー**: AI による コード品質チェック
- **ドキュメント自動生成**: APIドキュメントの自動生成

### 開発フェーズ
1. **フェーズ1**: 基盤構築（Azureリソースの構築）
2. **フェーズ2**: データ取り込み機能の開発
3. **フェーズ3**: リアルタイム監視機能の開発
4. **フェーズ4**: メンテナンス管理機能の開発
5. **フェーズ5**: データ分析・レポート機能の開発

## 貢献

プロジェクトへの貢献を歓迎します。以下の手順に従ってください：

1. リポジトリをフォーク
2. フィーチャーブランチを作成 (`git checkout -b feature/amazing-feature`)
3. 変更をコミット (`git commit -m 'Add some amazing feature'`)
4. ブランチにプッシュ (`git push origin feature/amazing-feature`)
5. プルリクエストを作成

## ライセンス

このプロジェクトは MIT ライセンスの下で提供されています。詳細は [LICENSE](LICENSE) ファイルを参照してください。

## サポート

質問や問題がある場合は、以下の方法でサポートを受けることができます：

- **Issues**: GitHub Issues でバグ報告や機能要求を提出
- **Discussions**: GitHub Discussions で質問や提案を投稿
- **ドキュメント**: [docs/](docs/) フォルダ内の詳細なドキュメントを参照

## 関連リンク

- [Azure Portal](https://portal.azure.com/)
- [Azure CLI ドキュメント](https://docs.microsoft.com/ja-jp/cli/azure/)
- [Vue.js 公式ドキュメント](https://vuejs.org/)
- [Power BI](https://powerbi.microsoft.com/)

---

**工場設備管理アプリ プロトタイプ** - AI-Driven Development を活用したスマートファクトリーソリューション
