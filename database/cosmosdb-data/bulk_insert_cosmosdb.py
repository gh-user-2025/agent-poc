#!/usr/bin/env python3
"""
Azure Cosmos DB サンプルデータ一括投入スクリプト
工場設備管理システム用

使用方法:
    python bulk_insert_cosmosdb.py --endpoint <ENDPOINT> --key <PRIMARY_KEY>

必要な環境:
    pip install azure-cosmos
"""

import json
import os
import argparse
import sys
from typing import List, Dict, Any
from azure.cosmos import CosmosClient, exceptions

class CosmosDBDataLoader:
    def __init__(self, endpoint: str, key: str, database_name: str = "FactoryEquipmentDB"):
        """
        Cosmos DB データローダーの初期化
        
        Args:
            endpoint: Cosmos DB エンドポイントURL
            key: Cosmos DB プライマリキー
            database_name: データベース名
        """
        self.client = CosmosClient(endpoint, key)
        self.database_name = database_name
        self.database = self.client.get_database_client(database_name)
    
    def load_json_file(self, file_path: str) -> List[Dict[str, Any]]:
        """
        JSONファイルからデータを読み込む
        
        Args:
            file_path: JSONファイルのパス
            
        Returns:
            データのリスト
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            print(f"✓ {file_path} を読み込みました（{len(data)}件）")
            return data
        except FileNotFoundError:
            print(f"✗ エラー: ファイル {file_path} が見つかりません")
            return []
        except json.JSONDecodeError as e:
            print(f"✗ エラー: {file_path} のJSONフォーマットが無効です - {e}")
            return []
    
    def insert_data_to_container(self, container_name: str, data: List[Dict[str, Any]]) -> bool:
        """
        指定されたコンテナにデータを一括投入
        
        Args:
            container_name: コンテナ名
            data: 投入するデータのリスト
            
        Returns:
            成功した場合True、失敗した場合False
        """
        try:
            container = self.database.get_container_client(container_name)
            success_count = 0
            error_count = 0
            
            print(f"🔄 {container_name} コンテナにデータを投入中...")
            
            for i, item in enumerate(data, 1):
                try:
                    container.upsert_item(item)
                    success_count += 1
                    print(f"  📝 {i}/{len(data)}: {item.get('id', 'N/A')} を投入")
                except exceptions.CosmosHttpResponseError as e:
                    error_count += 1
                    print(f"  ✗ {i}/{len(data)}: {item.get('id', 'N/A')} の投入に失敗 - {e}")
            
            print(f"✓ {container_name} への投入完了: 成功 {success_count}件, 失敗 {error_count}件")
            return error_count == 0
            
        except exceptions.CosmosResourceNotFoundError:
            print(f"✗ エラー: コンテナ '{container_name}' が見つかりません")
            return False
        except Exception as e:
            print(f"✗ エラー: {container_name} への投入中に予期しないエラーが発生しました - {e}")
            return False
    
    def verify_data(self, container_name: str, expected_count: int) -> bool:
        """
        データ投入の確認
        
        Args:
            container_name: コンテナ名
            expected_count: 期待するデータ件数
            
        Returns:
            期待する件数と一致した場合True
        """
        try:
            container = self.database.get_container_client(container_name)
            query = "SELECT VALUE COUNT(1) FROM c"
            items = list(container.query_items(query=query, enable_cross_partition_query=True))
            actual_count = items[0] if items else 0
            
            print(f"📊 {container_name} データ件数確認: {actual_count}件（期待値: {expected_count}件）")
            
            if actual_count == expected_count:
                print(f"✓ {container_name} のデータ確認完了")
                return True
            else:
                print(f"⚠️  {container_name} のデータ件数が期待値と異なります")
                return False
                
        except Exception as e:
            print(f"✗ エラー: {container_name} のデータ確認に失敗しました - {e}")
            return False
    
    def load_all_sample_data(self, data_dir: str = "database/cosmosdb-data") -> bool:
        """
        すべてのサンプルデータを読み込んで投入
        
        Args:
            data_dir: データファイルが格納されているディレクトリ
            
        Returns:
            すべて成功した場合True
        """
        success = True
        
        # センサーデータの投入
        sensor_data_file = os.path.join(data_dir, "sensor-data-sample.json")
        sensor_data = self.load_json_file(sensor_data_file)
        if sensor_data:
            success &= self.insert_data_to_container("SensorData", sensor_data)
            success &= self.verify_data("SensorData", len(sensor_data))
        
        # アラートデータの投入
        alerts_data_file = os.path.join(data_dir, "alerts-sample.json")
        alerts_data = self.load_json_file(alerts_data_file)
        if alerts_data:
            success &= self.insert_data_to_container("Alerts", alerts_data)
            success &= self.verify_data("Alerts", len(alerts_data))
        
        return success

def main():
    parser = argparse.ArgumentParser(description="Azure Cosmos DB サンプルデータ投入")
    parser.add_argument("--endpoint", required=True, help="Cosmos DB エンドポイントURL")
    parser.add_argument("--key", required=True, help="Cosmos DB プライマリキー")
    parser.add_argument("--database", default="FactoryEquipmentDB", help="データベース名")
    parser.add_argument("--data-dir", default="database/cosmosdb-data", help="データファイルディレクトリ")
    
    args = parser.parse_args()
    
    print("🚀 Azure Cosmos DB サンプルデータ投入開始")
    print(f"📍 エンドポイント: {args.endpoint}")
    print(f"💾 データベース: {args.database}")
    print(f"📁 データディレクトリ: {args.data_dir}")
    print("=" * 50)
    
    try:
        loader = CosmosDBDataLoader(args.endpoint, args.key, args.database)
        success = loader.load_all_sample_data(args.data_dir)
        
        print("=" * 50)
        if success:
            print("🎉 すべてのサンプルデータの投入が正常に完了しました！")
            sys.exit(0)
        else:
            print("❌ データ投入中にエラーが発生しました")
            sys.exit(1)
            
    except exceptions.CosmosResourceNotFoundError:
        print(f"✗ エラー: データベース '{args.database}' が見つかりません")
        print("   データベースが作成されているか確認してください")
        sys.exit(1)
    except exceptions.CosmosAuthenticationError:
        print("✗ エラー: 認証に失敗しました")
        print("   エンドポイントURLとプライマリキーを確認してください")
        sys.exit(1)
    except Exception as e:
        print(f"✗ 予期しないエラーが発生しました: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()