import azure.functions as func
import logging
import json
from datetime import datetime, timedelta
import os

def main(req: func.HttpRequest) -> func.HttpResponse:
    """
    データ変換・統計処理を行う Azure Function
    """
    logging.info('データ変換 Function が開始されました')

    try:
        # リクエストからデータを取得
        req_body = req.get_json()
        
        if not req_body:
            return func.HttpResponse(
                json.dumps({"error": "リクエストボディが空です"}, ensure_ascii=False),
                status_code=400,
                mimetype="application/json"
            )

        # データの種類に応じて変換処理を実行
        transform_type = req_body.get('transformType', 'default')
        raw_data = req_body.get('data', [])
        
        if transform_type == 'hourly_aggregation':
            result = hourly_aggregation(raw_data)
        elif transform_type == 'daily_summary':
            result = daily_summary(raw_data)
        elif transform_type == 'equipment_efficiency':
            result = calculate_equipment_efficiency(raw_data)
        else:
            result = default_transformation(raw_data)
        
        logging.info(f'データ変換が完了しました: {transform_type}')
        
        response_data = {
            "status": "success",
            "transformType": transform_type,
            "result": result,
            "processedAt": datetime.now().isoformat(),
            "recordCount": len(result) if isinstance(result, list) else 1
        }

        return func.HttpResponse(
            json.dumps(response_data, ensure_ascii=False),
            status_code=200,
            mimetype="application/json"
        )

    except Exception as e:
        logging.error(f'データ変換中にエラーが発生しました: {str(e)}')
        return func.HttpResponse(
            json.dumps({"error": "内部サーバーエラー"}, ensure_ascii=False),
            status_code=500,
            mimetype="application/json"
        )

def hourly_aggregation(data):
    """時間別集計処理"""
    if not data:
        return []
    
    # 時間別にデータをグループ化
    hourly_groups = {}
    
    for record in data:
        timestamp = record.get('timestamp', '')
        if timestamp:
            # 時間単位に丸める
            dt = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
            hour_key = dt.strftime('%Y-%m-%d %H:00:00')
            
            if hour_key not in hourly_groups:
                hourly_groups[hour_key] = {
                    'timestamp': hour_key,
                    'temperature_sum': 0,
                    'pressure_sum': 0,
                    'vibration_sum': 0,
                    'count': 0,
                    'equipment_ids': set()
                }
            
            group = hourly_groups[hour_key]
            sensor_data = record.get('sensorData', {})
            
            if 'temperature' in sensor_data:
                group['temperature_sum'] += sensor_data['temperature'].get('value', 0)
            if 'pressure' in sensor_data:
                group['pressure_sum'] += sensor_data['pressure'].get('value', 0)
            if 'vibration' in sensor_data:
                group['vibration_sum'] += sensor_data['vibration'].get('value', 0)
            
            group['count'] += 1
            if 'deviceId' in record:
                group['equipment_ids'].add(record['deviceId'])
    
    # 平均値を計算
    result = []
    for hour_key, group in hourly_groups.items():
        if group['count'] > 0:
            result.append({
                'timestamp': hour_key,
                'averageTemperature': round(group['temperature_sum'] / group['count'], 2),
                'averagePressure': round(group['pressure_sum'] / group['count'], 2),
                'averageVibration': round(group['vibration_sum'] / group['count'], 2),
                'equipmentCount': len(group['equipment_ids']),
                'dataPointCount': group['count']
            })
    
    return sorted(result, key=lambda x: x['timestamp'])

def daily_summary(data):
    """日別サマリー処理"""
    if not data:
        return {}
    
    # 日別統計を計算
    daily_stats = {
        'date': datetime.now().strftime('%Y-%m-%d'),
        'totalRecords': len(data),
        'equipmentCount': 0,
        'averageTemperature': 0,
        'averagePressure': 0,
        'averageVibration': 0,
        'maxTemperature': 0,
        'minTemperature': float('inf'),
        'alertCount': 0
    }
    
    equipment_ids = set()
    temp_sum = pressure_sum = vibration_sum = 0
    temp_count = pressure_count = vibration_count = 0
    
    for record in data:
        if 'deviceId' in record:
            equipment_ids.add(record['deviceId'])
        
        sensor_data = record.get('sensorData', {})
        
        if 'temperature' in sensor_data:
            temp = sensor_data['temperature'].get('value', 0)
            temp_sum += temp
            temp_count += 1
            daily_stats['maxTemperature'] = max(daily_stats['maxTemperature'], temp)
            daily_stats['minTemperature'] = min(daily_stats['minTemperature'], temp)
        
        if 'pressure' in sensor_data:
            pressure_sum += sensor_data['pressure'].get('value', 0)
            pressure_count += 1
        
        if 'vibration' in sensor_data:
            vibration_sum += sensor_data['vibration'].get('value', 0)
            vibration_count += 1
        
        # アラートカウント
        if record.get('alerts'):
            daily_stats['alertCount'] += len(record['alerts'])
    
    # 平均値を計算
    daily_stats['equipmentCount'] = len(equipment_ids)
    if temp_count > 0:
        daily_stats['averageTemperature'] = round(temp_sum / temp_count, 2)
    if pressure_count > 0:
        daily_stats['averagePressure'] = round(pressure_sum / pressure_count, 2)
    if vibration_count > 0:
        daily_stats['averageVibration'] = round(vibration_sum / vibration_count, 2)
    
    if daily_stats['minTemperature'] == float('inf'):
        daily_stats['minTemperature'] = 0
    
    return daily_stats

def calculate_equipment_efficiency(data):
    """設備効率計算"""
    if not data:
        return []
    
    equipment_stats = {}
    
    for record in data:
        device_id = record.get('deviceId')
        if not device_id:
            continue
        
        if device_id not in equipment_stats:
            equipment_stats[device_id] = {
                'deviceId': device_id,
                'totalDataPoints': 0,
                'normalOperationTime': 0,
                'warningTime': 0,
                'errorTime': 0,
                'averageTemperature': 0,
                'averagePressure': 0,
                'averageVibration': 0,
                'temp_sum': 0,
                'pressure_sum': 0,
                'vibration_sum': 0,
                'temp_count': 0,
                'pressure_count': 0,
                'vibration_count': 0
            }
        
        stats = equipment_stats[device_id]
        stats['totalDataPoints'] += 1
        
        # センサーデータの状態を確認
        sensor_data = record.get('sensorData', {})
        has_warning = False
        has_error = False
        
        for sensor_type, sensor_info in sensor_data.items():
            if isinstance(sensor_info, dict):
                status = sensor_info.get('status', 'normal')
                value = sensor_info.get('value', 0)
                
                if status == 'warning':
                    has_warning = True
                elif status == 'error':
                    has_error = True
                
                # 平均値計算用の累積
                if sensor_type == 'temperature':
                    stats['temp_sum'] += value
                    stats['temp_count'] += 1
                elif sensor_type == 'pressure':
                    stats['pressure_sum'] += value
                    stats['pressure_count'] += 1
                elif sensor_type == 'vibration':
                    stats['vibration_sum'] += value
                    stats['vibration_count'] += 1
        
        # 運転状態の分類
        if has_error:
            stats['errorTime'] += 1
        elif has_warning:
            stats['warningTime'] += 1
        else:
            stats['normalOperationTime'] += 1
    
    # 効率計算と平均値計算
    result = []
    for device_id, stats in equipment_stats.items():
        if stats['totalDataPoints'] > 0:
            efficiency = round((stats['normalOperationTime'] / stats['totalDataPoints']) * 100, 2)
            
            # 平均値計算
            avg_temp = round(stats['temp_sum'] / stats['temp_count'], 2) if stats['temp_count'] > 0 else 0
            avg_pressure = round(stats['pressure_sum'] / stats['pressure_count'], 2) if stats['pressure_count'] > 0 else 0
            avg_vibration = round(stats['vibration_sum'] / stats['vibration_count'], 2) if stats['vibration_count'] > 0 else 0
            
            result.append({
                'deviceId': device_id,
                'efficiency': efficiency,
                'totalDataPoints': stats['totalDataPoints'],
                'normalOperationTime': stats['normalOperationTime'],
                'warningTime': stats['warningTime'],
                'errorTime': stats['errorTime'],
                'averageTemperature': avg_temp,
                'averagePressure': avg_pressure,
                'averageVibration': avg_vibration
            })
    
    return sorted(result, key=lambda x: x['efficiency'], reverse=True)

def default_transformation(data):
    """デフォルトの変換処理"""
    return {
        'transformationType': 'default',
        'inputRecords': len(data),
        'processedAt': datetime.now().isoformat(),
        'summary': 'データの基本的な変換処理が完了しました'
    }