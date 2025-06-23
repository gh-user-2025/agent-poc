#!/usr/bin/env python3
"""
工場設備管理システム バックエンドAPI
"""

from flask import Flask, jsonify, request
from flask_cors import CORS
from datetime import datetime, timedelta
import json
import os

app = Flask(__name__)
CORS(app)  # フロントエンドからのアクセスを許可

# サンプルデータ
SAMPLE_EQUIPMENT = [
    {
        "id": 1,
        "name": "射出成形機-1",
        "type": "射出成形機",
        "status": "running",
        "location": "ライン A",
        "operatingHours": 2450,
        "lastMaintenance": "2024-01-15",
        "temperature": 75,
        "pressure": 82,
        "vibration": 4.2,
        "history": [
            {"id": 1, "timestamp": "2024-01-20 10:30", "event": "稼働開始"},
            {"id": 2, "timestamp": "2024-01-15 15:00", "event": "定期メンテナンス完了"}
        ]
    },
    {
        "id": 2,
        "name": "射出成形機-2",
        "type": "射出成形機",
        "status": "running",
        "location": "ライン A",
        "operatingHours": 2380,
        "lastMaintenance": "2024-01-10",
        "temperature": 78,
        "pressure": 85,
        "vibration": 3.8,
        "history": [
            {"id": 1, "timestamp": "2024-01-20 09:15", "event": "稼働開始"},
            {"id": 2, "timestamp": "2024-01-10 14:30", "event": "定期メンテナンス完了"}
        ]
    },
    {
        "id": 3,
        "name": "組立ロボット-1",
        "type": "組立ロボット",
        "status": "idle",
        "location": "ライン B",
        "operatingHours": 1680,
        "lastMaintenance": "2024-01-05",
        "temperature": 45,
        "pressure": 65,
        "vibration": 2.1,
        "history": [
            {"id": 1, "timestamp": "2024-01-20 11:00", "event": "待機状態"},
            {"id": 2, "timestamp": "2024-01-05 16:45", "event": "定期メンテナンス完了"}
        ]
    },
    {
        "id": 4,
        "name": "組立ロボット-2",
        "type": "組立ロボット",
        "status": "running",
        "location": "ライン B",
        "operatingHours": 1720,
        "lastMaintenance": "2024-01-08",
        "temperature": 52,
        "pressure": 72,
        "vibration": 2.8,
        "history": [
            {"id": 1, "timestamp": "2024-01-20 08:30", "event": "稼働開始"},
            {"id": 2, "timestamp": "2024-01-08 13:20", "event": "定期メンテナンス完了"}
        ]
    },
    {
        "id": 5,
        "name": "検査装置-1",
        "type": "検査装置",
        "status": "maintenance",
        "location": "ライン C",
        "operatingHours": 3200,
        "lastMaintenance": "2024-01-20",
        "temperature": 35,
        "pressure": 0,
        "vibration": 0,
        "history": [
            {"id": 1, "timestamp": "2024-01-20 13:00", "event": "メンテナンス開始"},
            {"id": 2, "timestamp": "2024-01-18 17:30", "event": "稼働停止"}
        ]
    },
    {
        "id": 6,
        "name": "コンプレッサー-1",
        "type": "コンプレッサー",
        "status": "running",
        "location": "共通設備",
        "operatingHours": 5680,
        "lastMaintenance": "2023-12-20",
        "temperature": 68,
        "pressure": 88,
        "vibration": 5.2,
        "history": [
            {"id": 1, "timestamp": "2024-01-01 00:00", "event": "連続稼働中"},
            {"id": 2, "timestamp": "2023-12-20 10:00", "event": "定期メンテナンス完了"}
        ]
    },
    {
        "id": 7,
        "name": "コンプレッサー-2",
        "type": "コンプレッサー",
        "status": "error",
        "location": "共通設備",
        "operatingHours": 5420,
        "lastMaintenance": "2023-12-15",
        "temperature": 95,
        "pressure": 102,
        "vibration": 8.5,
        "history": [
            {"id": 1, "timestamp": "2024-01-20 14:25", "event": "温度異常検出"},
            {"id": 2, "timestamp": "2024-01-20 14:20", "event": "アラート発生"}
        ]
    }
]

SAMPLE_ALERTS = [
    {
        "id": 1,
        "timestamp": (datetime.now() - timedelta(minutes=5)).isoformat(),
        "message": "温度異常が検出されました",
        "equipmentName": "コンプレッサー-2",
        "equipmentId": 7,
        "severity": "error",
        "status": "active"
    },
    {
        "id": 2,
        "timestamp": (datetime.now() - timedelta(minutes=30)).isoformat(),
        "message": "メンテナンス時期に到達しました",
        "equipmentName": "検査装置-1",
        "equipmentId": 5,
        "severity": "warning",
        "status": "active"
    },
    {
        "id": 3,
        "timestamp": (datetime.now() - timedelta(hours=2)).isoformat(),
        "message": "センサー通信エラー",
        "equipmentName": "組立ロボット-1",
        "equipmentId": 3,
        "severity": "warning",
        "status": "resolved"
    }
]

@app.route('/api/health', methods=['GET'])
def health():
    """ヘルスチェック"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'version': '1.0.0'
    })

@app.route('/api/equipment', methods=['GET'])
def get_equipment():
    """設備一覧取得"""
    location = request.args.get('location')
    status = request.args.get('status')
    
    filtered_equipment = SAMPLE_EQUIPMENT
    
    if location:
        filtered_equipment = [eq for eq in filtered_equipment if eq['location'] == location]
    
    if status:
        filtered_equipment = [eq for eq in filtered_equipment if eq['status'] == status]
    
    return jsonify({
        'equipment': filtered_equipment,
        'total': len(filtered_equipment),
        'timestamp': datetime.now().isoformat()
    })

@app.route('/api/equipment/<int:equipment_id>', methods=['GET'])
def get_equipment_detail(equipment_id):
    """設備詳細取得"""
    equipment = next((eq for eq in SAMPLE_EQUIPMENT if eq['id'] == equipment_id), None)
    
    if not equipment:
        return jsonify({'error': '設備が見つかりません'}), 404
    
    return jsonify({
        'equipment': equipment,
        'timestamp': datetime.now().isoformat()
    })

@app.route('/api/equipment/summary', methods=['GET'])
def get_equipment_summary():
    """設備サマリー取得"""
    total = len(SAMPLE_EQUIPMENT)
    running = len([eq for eq in SAMPLE_EQUIPMENT if eq['status'] == 'running'])
    idle = len([eq for eq in SAMPLE_EQUIPMENT if eq['status'] == 'idle'])
    maintenance = len([eq for eq in SAMPLE_EQUIPMENT if eq['status'] == 'maintenance'])
    error = len([eq for eq in SAMPLE_EQUIPMENT if eq['status'] == 'error'])
    
    return jsonify({
        'summary': {
            'total': total,
            'running': running,
            'idle': idle,
            'maintenance': maintenance,
            'error': error
        },
        'timestamp': datetime.now().isoformat()
    })

@app.route('/api/alerts', methods=['GET'])
def get_alerts():
    """アラート一覧取得"""
    severity = request.args.get('severity')
    status = request.args.get('status', 'active')
    limit = int(request.args.get('limit', 10))
    
    filtered_alerts = SAMPLE_ALERTS
    
    if severity:
        filtered_alerts = [alert for alert in filtered_alerts if alert['severity'] == severity]
    
    if status:
        filtered_alerts = [alert for alert in filtered_alerts if alert['status'] == status]
    
    # 最新のアラートから指定件数を返す
    filtered_alerts = sorted(filtered_alerts, key=lambda x: x['timestamp'], reverse=True)[:limit]
    
    return jsonify({
        'alerts': filtered_alerts,
        'total': len(filtered_alerts),
        'timestamp': datetime.now().isoformat()
    })

@app.route('/api/sensor-data/<int:equipment_id>', methods=['GET'])
def get_sensor_data(equipment_id):
    """センサーデータ取得"""
    equipment = next((eq for eq in SAMPLE_EQUIPMENT if eq['id'] == equipment_id), None)
    
    if not equipment:
        return jsonify({'error': '設備が見つかりません'}), 404
    
    # 過去24時間のサンプルセンサーデータを生成
    import random
    sensor_data = []
    base_time = datetime.now() - timedelta(hours=24)
    
    for i in range(24):  # 1時間ごとのデータ
        timestamp = base_time + timedelta(hours=i)
        
        # 基準値からの変動を追加
        temp_variation = random.uniform(-5, 5)
        pressure_variation = random.uniform(-3, 3)
        vibration_variation = random.uniform(-0.5, 0.5)
        
        sensor_data.append({
            'timestamp': timestamp.isoformat(),
            'temperature': max(0, equipment['temperature'] + temp_variation),
            'pressure': max(0, equipment['pressure'] + pressure_variation),
            'vibration': max(0, equipment['vibration'] + vibration_variation)
        })
    
    return jsonify({
        'equipmentId': equipment_id,
        'sensorData': sensor_data,
        'timestamp': datetime.now().isoformat()
    })

@app.errorhandler(404)
def not_found_error(error):
    return jsonify({'error': 'エンドポイントが見つかりません'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'サーバー内部エラーが発生しました'}), 500

if __name__ == '__main__':
    # 本番環境では環境変数から設定を取得
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_ENV') == 'development'
    
    app.run(host='0.0.0.0', port=port, debug=debug)