import azure.functions as func
import logging
import json
from datetime import datetime
import os

def main(req: func.HttpRequest) -> func.HttpResponse:
    """
    IoTデバイスからのセンサーデータを処理する Azure Function
    """
    logging.info('IoT データ処理 Function が開始されました')

    try:
        # リクエストからIoTデータを取得
        req_body = req.get_json()
        
        if not req_body:
            return func.HttpResponse(
                json.dumps({"error": "リクエストボディが空です"}, ensure_ascii=False),
                status_code=400,
                mimetype="application/json"
            )

        # IoTデータの検証
        required_fields = ['deviceId', 'timestamp', 'sensorData']
        if not all(field in req_body for field in required_fields):
            return func.HttpResponse(
                json.dumps({"error": "必須フィールドが不足しています"}, ensure_ascii=False),
                status_code=400,
                mimetype="application/json"
            )

        device_id = req_body['deviceId']
        timestamp = req_body['timestamp']
        sensor_data = req_body['sensorData']

        # センサーデータの処理
        processed_data = process_sensor_data(device_id, timestamp, sensor_data)
        
        # 異常検知
        alerts = detect_anomalies(device_id, sensor_data)
        
        # Cosmos DBに保存（実際の実装では接続文字列を使用）
        # save_to_cosmosdb(processed_data)
        
        logging.info(f'デバイス {device_id} のデータ処理が完了しました')
        
        response_data = {
            "status": "success",
            "processedData": processed_data,
            "alerts": alerts,
            "timestamp": datetime.now().isoformat()
        }

        return func.HttpResponse(
            json.dumps(response_data, ensure_ascii=False),
            status_code=200,
            mimetype="application/json"
        )

    except Exception as e:
        logging.error(f'IoTデータ処理中にエラーが発生しました: {str(e)}')
        return func.HttpResponse(
            json.dumps({"error": "内部サーバーエラー"}, ensure_ascii=False),
            status_code=500,
            mimetype="application/json"
        )

def process_sensor_data(device_id, timestamp, sensor_data):
    """センサーデータの処理とフォーマット"""
    processed = {
        "deviceId": device_id,
        "timestamp": timestamp,
        "processedAt": datetime.now().isoformat(),
        "sensorData": {}
    }
    
    # 各センサーデータの正規化と検証
    for sensor_type, value in sensor_data.items():
        if sensor_type == 'temperature':
            # 温度データの処理
            processed["sensorData"][sensor_type] = {
                "value": float(value),
                "unit": "°C",
                "status": "normal" if 20 <= float(value) <= 85 else "warning"
            }
        elif sensor_type == 'pressure':
            # 圧力データの処理
            processed["sensorData"][sensor_type] = {
                "value": float(value),
                "unit": "%",
                "status": "normal" if 0 <= float(value) <= 95 else "warning"
            }
        elif sensor_type == 'vibration':
            # 振動データの処理
            processed["sensorData"][sensor_type] = {
                "value": float(value),
                "unit": "mm/s",
                "status": "normal" if 0 <= float(value) <= 8 else "warning"
            }
    
    return processed

def detect_anomalies(device_id, sensor_data):
    """異常検知処理"""
    alerts = []
    
    # 温度異常チェック
    if 'temperature' in sensor_data:
        temp = float(sensor_data['temperature'])
        if temp > 85:
            alerts.append({
                "type": "temperature_high",
                "deviceId": device_id,
                "message": f"高温異常: {temp}°C",
                "severity": "error" if temp > 90 else "warning",
                "timestamp": datetime.now().isoformat()
            })
        elif temp < 10:
            alerts.append({
                "type": "temperature_low",
                "deviceId": device_id,
                "message": f"低温異常: {temp}°C",
                "severity": "warning",
                "timestamp": datetime.now().isoformat()
            })
    
    # 圧力異常チェック
    if 'pressure' in sensor_data:
        pressure = float(sensor_data['pressure'])
        if pressure > 95:
            alerts.append({
                "type": "pressure_high",
                "deviceId": device_id,
                "message": f"高圧異常: {pressure}%",
                "severity": "error",
                "timestamp": datetime.now().isoformat()
            })
    
    # 振動異常チェック
    if 'vibration' in sensor_data:
        vibration = float(sensor_data['vibration'])
        if vibration > 8:
            alerts.append({
                "type": "vibration_high",
                "deviceId": device_id,
                "message": f"振動異常: {vibration}mm/s",
                "severity": "error" if vibration > 10 else "warning",
                "timestamp": datetime.now().isoformat()
            })
    
    return alerts

def save_to_cosmosdb(data):
    """Cosmos DBへの保存（実装例）"""
    # 本番環境では実際のCosmos DB接続を実装
    logging.info(f"Cosmos DBに保存: {data['deviceId']}")
    pass