"""
メンテナンス管理用 Azure Function
メンテナンススケジュールの管理と最適化を行う
"""

import logging
import json
import azure.functions as func
from datetime import datetime, timedelta
import os

def main(req: func.HttpRequest) -> func.HttpResponse:
    """
    メンテナンス管理機能
    
    Args:
        req: HTTPリクエスト
    
    Returns:
        func.HttpResponse: 処理結果
    """
    logging.info('メンテナンス管理関数が実行されました')

    try:
        # HTTPメソッドに応じた処理分岐
        method = req.method
        
        if method == "GET":
            return get_maintenance_schedule(req)
        elif method == "POST":
            return create_maintenance_schedule(req)
        elif method == "PUT":
            return update_maintenance_schedule(req)
        elif method == "DELETE":
            return delete_maintenance_schedule(req)
        else:
            return func.HttpResponse(
                json.dumps({"error": "サポートされていないHTTPメソッドです"}, ensure_ascii=False),
                status_code=405,
                mimetype="application/json"
            )
            
    except Exception as e:
        logging.error(f'メンテナンス管理処理中にエラーが発生しました: {str(e)}')
        return func.HttpResponse(
            json.dumps({"error": "内部サーバーエラー"}, ensure_ascii=False),
            status_code=500,
            mimetype="application/json"
        )


def get_maintenance_schedule(req):
    """
    メンテナンススケジュールの取得
    
    Args:
        req: HTTPリクエスト
    
    Returns:
        func.HttpResponse: スケジュール情報
    """
    # クエリパラメータの取得
    equipment_id = req.params.get('equipment_id')
    start_date = req.params.get('start_date')
    end_date = req.params.get('end_date')
    
    # サンプルデータ（実際の実装ではデータベースから取得）
    schedule_data = generate_sample_schedule(equipment_id, start_date, end_date)
    
    response_data = {
        "status": "success",
        "schedule": schedule_data,
        "count": len(schedule_data),
        "timestamp": datetime.now().isoformat()
    }
    
    return func.HttpResponse(
        json.dumps(response_data, ensure_ascii=False),
        status_code=200,
        mimetype="application/json"
    )


def create_maintenance_schedule(req):
    """
    新規メンテナンススケジュールの作成
    
    Args:
        req: HTTPリクエスト
    
    Returns:
        func.HttpResponse: 作成結果
    """
    req_body = req.get_json()
    
    if not req_body:
        return func.HttpResponse(
            json.dumps({"error": "リクエストボディが空です"}, ensure_ascii=False),
            status_code=400,
            mimetype="application/json"
        )
    
    # 必須フィールドの検証
    required_fields = ['equipment_id', 'maintenance_type', 'scheduled_date', 'priority']
    for field in required_fields:
        if field not in req_body:
            return func.HttpResponse(
                json.dumps({"error": f"必須フィールド '{field}' が不足しています"}, ensure_ascii=False),
                status_code=400,
                mimetype="application/json"
            )
    
    # メンテナンススケジュールの作成
    new_schedule = create_new_schedule(req_body)
    
    # 最適化の実行
    optimized_schedule = optimize_schedule(new_schedule)
    
    response_data = {
        "status": "success",
        "message": "メンテナンススケジュールが作成されました",
        "schedule_id": new_schedule["id"],
        "optimized": optimized_schedule,
        "timestamp": datetime.now().isoformat()
    }
    
    return func.HttpResponse(
        json.dumps(response_data, ensure_ascii=False),
        status_code=201,
        mimetype="application/json"
    )


def update_maintenance_schedule(req):
    """
    メンテナンススケジュールの更新
    
    Args:
        req: HTTPリクエスト
    
    Returns:
        func.HttpResponse: 更新結果
    """
    schedule_id = req.params.get('id')
    req_body = req.get_json()
    
    if not schedule_id:
        return func.HttpResponse(
            json.dumps({"error": "スケジュールIDが指定されていません"}, ensure_ascii=False),
            status_code=400,
            mimetype="application/json"
        )
    
    # スケジュールの更新処理
    updated_schedule = update_schedule_data(schedule_id, req_body)
    
    response_data = {
        "status": "success",
        "message": "メンテナンススケジュールが更新されました",
        "schedule": updated_schedule,
        "timestamp": datetime.now().isoformat()
    }
    
    return func.HttpResponse(
        json.dumps(response_data, ensure_ascii=False),
        status_code=200,
        mimetype="application/json"
    )


def delete_maintenance_schedule(req):
    """
    メンテナンススケジュールの削除
    
    Args:
        req: HTTPリクエスト
    
    Returns:
        func.HttpResponse: 削除結果
    """
    schedule_id = req.params.get('id')
    
    if not schedule_id:
        return func.HttpResponse(
            json.dumps({"error": "スケジュールIDが指定されていません"}, ensure_ascii=False),
            status_code=400,
            mimetype="application/json"
        )
    
    # スケジュールの削除処理
    delete_result = delete_schedule_data(schedule_id)
    
    response_data = {
        "status": "success",
        "message": "メンテナンススケジュールが削除されました",
        "deleted_id": schedule_id,
        "timestamp": datetime.now().isoformat()
    }
    
    return func.HttpResponse(
        json.dumps(response_data, ensure_ascii=False),
        status_code=200,
        mimetype="application/json"
    )


def generate_sample_schedule(equipment_id=None, start_date=None, end_date=None):
    """
    サンプルスケジュールデータの生成
    
    Args:
        equipment_id: 設備ID
        start_date: 開始日
        end_date: 終了日
    
    Returns:
        list: スケジュールデータ
    """
    # サンプルデータ
    sample_schedules = [
        {
            "id": 1,
            "equipment_id": "A1",
            "equipment_name": "射出成形機 A1",
            "maintenance_type": "定期点検",
            "scheduled_date": (datetime.now() + timedelta(days=1)).isoformat(),
            "priority": "high",
            "status": "pending",
            "estimated_duration": 3
        },
        {
            "id": 2,
            "equipment_id": "B2",
            "equipment_name": "組立ロボット B2",
            "scheduled_date": (datetime.now() + timedelta(days=3)).isoformat(),
            "maintenance_type": "予防保全",
            "priority": "medium",
            "status": "pending",
            "estimated_duration": 2
        }
    ]
    
    # フィルタリング処理
    if equipment_id:
        sample_schedules = [s for s in sample_schedules if s["equipment_id"] == equipment_id]
    
    return sample_schedules


def create_new_schedule(schedule_data):
    """
    新しいスケジュールの作成
    
    Args:
        schedule_data: スケジュールデータ
    
    Returns:
        dict: 作成されたスケジュール
    """
    new_schedule = {
        "id": len(range(100)) + 1,  # 実際の実装ではUUIDを使用
        "equipment_id": schedule_data["equipment_id"],
        "maintenance_type": schedule_data["maintenance_type"],
        "scheduled_date": schedule_data["scheduled_date"],
        "priority": schedule_data["priority"],
        "status": "pending",
        "created_at": datetime.now().isoformat(),
        "estimated_duration": schedule_data.get("estimated_duration", 2)
    }
    
    return new_schedule


def optimize_schedule(schedule):
    """
    スケジュールの最適化
    
    Args:
        schedule: スケジュールデータ
    
    Returns:
        dict: 最適化結果
    """
    # 簡単な最適化ロジック
    optimization_result = {
        "original_date": schedule["scheduled_date"],
        "optimized": False,
        "recommendations": []
    }
    
    # 優先度に基づく最適化
    if schedule["priority"] == "high":
        optimization_result["recommendations"].append("高優先度タスクとして即座に実行することをお勧めします")
    
    # 効率的なスケジューリング
    optimization_result["recommendations"].append("他のメンテナンス作業との統合を検討してください")
    
    return optimization_result


def update_schedule_data(schedule_id, update_data):
    """
    スケジュールデータの更新
    
    Args:
        schedule_id: スケジュールID
        update_data: 更新データ
    
    Returns:
        dict: 更新されたスケジュール
    """
    # 実際の実装ではデータベースを更新
    updated_schedule = {
        "id": schedule_id,
        "updated_at": datetime.now().isoformat(),
        **update_data
    }
    
    return updated_schedule


def delete_schedule_data(schedule_id):
    """
    スケジュールデータの削除
    
    Args:
        schedule_id: スケジュールID
    
    Returns:
        bool: 削除成功フラグ
    """
    # 実際の実装ではデータベースから削除
    logging.info(f'スケジュール {schedule_id} を削除しました')
    return True