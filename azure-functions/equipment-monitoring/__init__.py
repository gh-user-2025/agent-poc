"""
設備監視データ処理用 Azure Function
IoTデバイスからのデータを受信し、リアルタイム処理を行う
"""

import logging
import json
import azure.functions as func
from datetime import datetime
import os

def main(req: func.HttpRequest) -> func.HttpResponse:
    """
    設備監視データの処理
    
    Args:
        req: HTTPリクエスト（設備データを含む）
    
    Returns:
        func.HttpResponse: 処理結果
    """
    logging.info('設備監視データ処理関数が実行されました')

    try:
        # リクエストボディからデータを取得
        req_body = req.get_json()
        
        if not req_body:
            return func.HttpResponse(
                json.dumps({"error": "リクエストボディが空です"}, ensure_ascii=False),
                status_code=400,
                mimetype="application/json"
            )
        
        # 設備データの検証
        required_fields = ['equipment_id', 'timestamp', 'status', 'efficiency', 'temperature']
        for field in required_fields:
            if field not in req_body:
                return func.HttpResponse(
                    json.dumps({"error": f"必須フィールド '{field}' が不足しています"}, ensure_ascii=False),
                    status_code=400,
                    mimetype="application/json"
                )
        
        # データ処理
        processed_data = process_equipment_data(req_body)
        
        # アラート判定
        alerts = check_alerts(processed_data)
        
        # 結果の返却
        response_data = {
            "status": "success",
            "processed_data": processed_data,
            "alerts": alerts,
            "timestamp": datetime.now().isoformat()
        }
        
        logging.info(f'設備 {req_body["equipment_id"]} のデータ処理が完了しました')
        
        return func.HttpResponse(
            json.dumps(response_data, ensure_ascii=False),
            status_code=200,
            mimetype="application/json"
        )
        
    except Exception as e:
        logging.error(f'設備監視データ処理中にエラーが発生しました: {str(e)}')
        return func.HttpResponse(
            json.dumps({"error": "内部サーバーエラー"}, ensure_ascii=False),
            status_code=500,
            mimetype="application/json"
        )


def process_equipment_data(data):
    """
    設備データの処理・分析
    
    Args:
        data: 受信した設備データ
    
    Returns:
        dict: 処理済みデータ
    """
    processed = {
        "equipment_id": data["equipment_id"],
        "timestamp": data["timestamp"],
        "status": data["status"],
        "efficiency": data["efficiency"],
        "temperature": data["temperature"],
        "health_score": calculate_health_score(data),
        "performance_trend": analyze_performance_trend(data)
    }
    
    return processed


def calculate_health_score(data):
    """
    設備の健康スコアを計算
    
    Args:
        data: 設備データ
    
    Returns:
        float: 健康スコア (0-100)
    """
    # 簡単な健康スコア計算ロジック
    efficiency_score = min(data["efficiency"], 100)
    
    # 温度による減点
    temp_penalty = 0
    if data["temperature"] > 200:  # 高温閾値
        temp_penalty = (data["temperature"] - 200) * 0.5
    elif data["temperature"] < 10:  # 低温閾値
        temp_penalty = (10 - data["temperature"]) * 0.3
    
    health_score = max(0, efficiency_score - temp_penalty)
    return round(health_score, 2)


def analyze_performance_trend(data):
    """
    パフォーマンストレンドの分析
    
    Args:
        data: 設備データ
    
    Returns:
        str: トレンド（'improving', 'stable', 'declining'）
    """
    # 実際の実装では過去データとの比較を行う
    # ここではサンプル実装
    efficiency = data["efficiency"]
    
    if efficiency > 90:
        return "improving"
    elif efficiency > 75:
        return "stable"
    else:
        return "declining"


def check_alerts(data):
    """
    アラート条件のチェック
    
    Args:
        data: 処理済み設備データ
    
    Returns:
        list: アラート情報のリスト
    """
    alerts = []
    
    # 稼働率が低い場合
    if data["efficiency"] < 70:
        alerts.append({
            "type": "efficiency",
            "level": "warning",
            "message": f"設備 {data['equipment_id']} の稼働率が低下しています ({data['efficiency']}%)",
            "timestamp": datetime.now().isoformat()
        })
    
    # 温度異常
    if data["temperature"] > 200:
        alerts.append({
            "type": "temperature",
            "level": "critical",
            "message": f"設備 {data['equipment_id']} の温度が異常に高いです ({data['temperature']}°C)",
            "timestamp": datetime.now().isoformat()
        })
    
    # 健康スコアが低い場合
    if data["health_score"] < 60:
        alerts.append({
            "type": "health",
            "level": "warning",
            "message": f"設備 {data['equipment_id']} の健康スコアが低下しています ({data['health_score']})",
            "timestamp": datetime.now().isoformat()
        })
    
    return alerts