#!/usr/bin/env python3
"""
工場設備管理システム バックエンドAPI (シンプルHTTPサーバー版)
"""

from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import urllib.parse
from datetime import datetime, timedelta
import random

class APIHandler(BaseHTTPRequestHandler):
    
    def do_OPTIONS(self):
        """CORS preflight request handling"""
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
    
    def do_GET(self):
        """GET request handling"""
        # URLパスを解析
        parsed_path = urllib.parse.urlparse(self.path)
        path = parsed_path.path
        query_params = urllib.parse.parse_qs(parsed_path.query)
        
        try:
            if path == '/api/health':
                self.handle_health()
            elif path == '/api/equipment':
                self.handle_equipment_list(query_params)
            elif path.startswith('/api/equipment/') and path.endswith('/'):
                # Remove trailing slash and try again
                path = path.rstrip('/')
                if path.startswith('/api/equipment/') and path != '/api/equipment':
                    equipment_id = path.split('/')[-1]
                    if equipment_id == 'summary':
                        self.handle_equipment_summary()
                    else:
                        self.handle_equipment_detail(equipment_id)
                else:
                    self.send_error(404)
            elif path.startswith('/api/equipment/') and path != '/api/equipment':
                equipment_id = path.split('/')[-1]
                if equipment_id == 'summary':
                    self.handle_equipment_summary()
                else:
                    self.handle_equipment_detail(equipment_id)
            elif path == '/api/alerts':
                self.handle_alerts(query_params)
            elif path.startswith('/api/sensor-data/'):
                equipment_id = path.split('/')[-1]
                self.handle_sensor_data(equipment_id)
            else:
                self.send_error(404)
        except Exception as e:
            print(f"Error handling request: {e}")
            self.send_error(500)
    
    def send_json_response(self, data, status_code=200):
        """JSONレスポンスを送信"""
        self.send_response(status_code)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        response_json = json.dumps(data, ensure_ascii=False)
        self.wfile.write(response_json.encode('utf-8'))
    
    def handle_health(self):
        """ヘルスチェック"""
        response = {
            'status': 'healthy',
            'timestamp': datetime.now().isoformat(),
            'version': '1.0.0'
        }
        self.send_json_response(response)
    
    def handle_equipment_list(self, query_params):
        """設備一覧取得"""
        # サンプルデータ
        equipment_data = [
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
        
        # フィルタリング
        filtered_equipment = equipment_data
        if 'location' in query_params and query_params['location'][0]:
            location = query_params['location'][0]
            filtered_equipment = [eq for eq in filtered_equipment if eq['location'] == location]
        
        if 'status' in query_params and query_params['status'][0]:
            status = query_params['status'][0]
            filtered_equipment = [eq for eq in filtered_equipment if eq['status'] == status]
        
        response = {
            'equipment': filtered_equipment,
            'total': len(filtered_equipment),
            'timestamp': datetime.now().isoformat()
        }
        self.send_json_response(response)
    
    def handle_equipment_detail(self, equipment_id):
        """設備詳細取得"""
        # サンプルデータから検索
        equipment_data = [
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
            }
        ]
        
        try:
            eq_id = int(equipment_id)
            equipment = next((eq for eq in equipment_data if eq['id'] == eq_id), None)
            
            if equipment:
                response = {
                    'equipment': equipment,
                    'timestamp': datetime.now().isoformat()
                }
                self.send_json_response(response)
            else:
                self.send_json_response({'error': '設備が見つかりません'}, 404)
        except ValueError:
            self.send_json_response({'error': '無効な設備IDです'}, 400)
    
    def handle_equipment_summary(self):
        """設備サマリー取得"""
        response = {
            'summary': {
                'total': 7,
                'running': 4,
                'idle': 1,
                'maintenance': 1,
                'error': 1
            },
            'timestamp': datetime.now().isoformat()
        }
        self.send_json_response(response)
    
    def handle_alerts(self, query_params):
        """アラート一覧取得"""
        alerts_data = [
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
            }
        ]
        
        # フィルタリング
        filtered_alerts = alerts_data
        if 'severity' in query_params and query_params['severity'][0]:
            severity = query_params['severity'][0]
            filtered_alerts = [alert for alert in filtered_alerts if alert['severity'] == severity]
        
        if 'status' in query_params and query_params['status'][0]:
            status = query_params['status'][0]
            filtered_alerts = [alert for alert in filtered_alerts if alert['status'] == status]
        
        # 件数制限
        limit = 10
        if 'limit' in query_params and query_params['limit'][0]:
            try:
                limit = int(query_params['limit'][0])
            except ValueError:
                pass
        
        filtered_alerts = filtered_alerts[:limit]
        
        response = {
            'alerts': filtered_alerts,
            'total': len(filtered_alerts),
            'timestamp': datetime.now().isoformat()
        }
        self.send_json_response(response)
    
    def handle_sensor_data(self, equipment_id):
        """センサーデータ取得"""
        try:
            eq_id = int(equipment_id)
            
            # サンプルセンサーデータを生成
            sensor_data = []
            base_time = datetime.now() - timedelta(hours=24)
            
            for i in range(24):  # 1時間ごとのデータ
                timestamp = base_time + timedelta(hours=i)
                
                # 基準値からの変動を追加
                temp_variation = random.uniform(-5, 5)
                pressure_variation = random.uniform(-3, 3)
                vibration_variation = random.uniform(-0.5, 0.5)
                
                base_temp = 75
                base_pressure = 82
                base_vibration = 4.2
                
                sensor_data.append({
                    'timestamp': timestamp.isoformat(),
                    'temperature': max(0, base_temp + temp_variation),
                    'pressure': max(0, base_pressure + pressure_variation),
                    'vibration': max(0, base_vibration + vibration_variation)
                })
            
            response = {
                'equipmentId': eq_id,
                'sensorData': sensor_data,
                'timestamp': datetime.now().isoformat()
            }
            self.send_json_response(response)
            
        except ValueError:
            self.send_json_response({'error': '無効な設備IDです'}, 400)

def run_server(port=5000):
    """HTTPサーバーを起動"""
    server_address = ('', port)
    httpd = HTTPServer(server_address, APIHandler)
    print(f"バックエンドAPIサーバーが起動しました: http://localhost:{port}")
    print("利用可能なエンドポイント:")
    print("  GET /api/health")
    print("  GET /api/equipment")
    print("  GET /api/equipment/{id}")
    print("  GET /api/equipment/summary")
    print("  GET /api/alerts")
    print("  GET /api/sensor-data/{id}")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nサーバーを停止します...")
        httpd.shutdown()

if __name__ == '__main__':
    run_server()