"""
データ分析用 Azure Function
設備データの分析とAI による運用改善提案を行う
"""

import logging
import json
import azure.functions as func
from datetime import datetime, timedelta
import statistics
import os

def main(req: func.HttpRequest) -> func.HttpResponse:
    """
    データ分析機能
    
    Args:
        req: HTTPリクエスト
    
    Returns:
        func.HttpResponse: 分析結果
    """
    logging.info('データ分析関数が実行されました')

    try:
        # 分析タイプの取得
        analysis_type = req.params.get('type', 'overview')
        period = req.params.get('period', 'week')
        
        # 分析タイプに応じた処理
        if analysis_type == 'overview':
            result = generate_overview_analysis(period)
        elif analysis_type == 'efficiency':
            result = analyze_efficiency_trends(period)
        elif analysis_type == 'predictive':
            result = perform_predictive_analysis(period)
        elif analysis_type == 'recommendations':
            result = generate_recommendations(period)
        else:
            return func.HttpResponse(
                json.dumps({"error": "無効な分析タイプです"}, ensure_ascii=False),
                status_code=400,
                mimetype="application/json"
            )
        
        response_data = {
            "status": "success",
            "analysis_type": analysis_type,
            "period": period,
            "result": result,
            "timestamp": datetime.now().isoformat()
        }
        
        logging.info(f'データ分析が完了しました: {analysis_type}')
        
        return func.HttpResponse(
            json.dumps(response_data, ensure_ascii=False),
            status_code=200,
            mimetype="application/json"
        )
        
    except Exception as e:
        logging.error(f'データ分析処理中にエラーが発生しました: {str(e)}')
        return func.HttpResponse(
            json.dumps({"error": "内部サーバーエラー"}, ensure_ascii=False),
            status_code=500,
            mimetype="application/json"
        )


def generate_overview_analysis(period):
    """
    概要分析の生成
    
    Args:
        period: 分析期間
    
    Returns:
        dict: 概要分析結果
    """
    # サンプルデータを使用した分析
    sample_data = get_sample_equipment_data(period)
    
    # KPI計算
    kpis = calculate_kpis(sample_data)
    
    # トレンド分析
    trends = analyze_trends(sample_data)
    
    overview = {
        "kpis": kpis,
        "trends": trends,
        "equipment_summary": generate_equipment_summary(sample_data),
        "alerts_summary": generate_alerts_summary(sample_data)
    }
    
    return overview


def analyze_efficiency_trends(period):
    """
    効率トレンド分析
    
    Args:
        period: 分析期間
    
    Returns:
        dict: 効率トレンド分析結果
    """
    sample_data = get_sample_equipment_data(period)
    
    efficiency_analysis = {
        "overall_efficiency": calculate_overall_efficiency(sample_data),
        "equipment_rankings": rank_equipment_by_efficiency(sample_data),
        "efficiency_patterns": identify_efficiency_patterns(sample_data),
        "improvement_opportunities": find_improvement_opportunities(sample_data)
    }
    
    return efficiency_analysis


def perform_predictive_analysis(period):
    """
    予測分析の実行
    
    Args:
        period: 分析期間
    
    Returns:
        dict: 予測分析結果
    """
    sample_data = get_sample_equipment_data(period)
    
    predictions = {
        "maintenance_predictions": predict_maintenance_needs(sample_data),
        "production_forecast": forecast_production(sample_data),
        "failure_risk_assessment": assess_failure_risks(sample_data),
        "optimal_scheduling": suggest_optimal_schedule(sample_data)
    }
    
    return predictions


def generate_recommendations(period):
    """
    改善提案の生成
    
    Args:
        period: 分析期間
    
    Returns:
        dict: 改善提案
    """
    sample_data = get_sample_equipment_data(period)
    
    recommendations = {
        "high_priority": generate_high_priority_recommendations(sample_data),
        "medium_priority": generate_medium_priority_recommendations(sample_data),
        "low_priority": generate_low_priority_recommendations(sample_data),
        "cost_benefit_analysis": calculate_cost_benefits(sample_data)
    }
    
    return recommendations


def get_sample_equipment_data(period):
    """
    サンプル設備データの取得
    
    Args:
        period: データ期間
    
    Returns:
        list: サンプルデータ
    """
    # 実際の実装では Azure SQL Database や Cosmos DB からデータを取得
    base_date = datetime.now()
    data_points = []
    
    # 期間に応じたデータポイント数の決定
    if period == 'day':
        days = 1
        points_per_day = 24
    elif period == 'week':
        days = 7
        points_per_day = 4
    elif period == 'month':
        days = 30
        points_per_day = 1
    else:
        days = 7
        points_per_day = 4
    
    equipment_list = ['A1', 'B2', 'C3', 'D4', 'E5']
    
    for day in range(days):
        for point in range(points_per_day):
            timestamp = base_date - timedelta(days=day, hours=point*6)
            
            for equipment in equipment_list:
                data_points.append({
                    'equipment_id': equipment,
                    'timestamp': timestamp.isoformat(),
                    'efficiency': 85 + (hash(f"{equipment}{day}{point}") % 20),
                    'temperature': 150 + (hash(f"{equipment}{day}{point}") % 50),
                    'status': 'operational' if (hash(f"{equipment}{day}{point}") % 10) > 1 else 'maintenance'
                })
    
    return data_points


def calculate_kpis(data):
    """
    KPI の計算
    
    Args:
        data: 設備データ
    
    Returns:
        dict: KPI値
    """
    operational_data = [d for d in data if d['status'] == 'operational']
    
    if not operational_data:
        return {"error": "稼働データが不足しています"}
    
    efficiencies = [d['efficiency'] for d in operational_data]
    
    kpis = {
        "overall_efficiency": round(statistics.mean(efficiencies), 1),
        "efficiency_std": round(statistics.stdev(efficiencies) if len(efficiencies) > 1 else 0, 1),
        "operational_ratio": round(len(operational_data) / len(data) * 100, 1),
        "equipment_count": len(set(d['equipment_id'] for d in data)),
        "data_points": len(data)
    }
    
    return kpis


def analyze_trends(data):
    """
    トレンド分析
    
    Args:
        data: 設備データ
    
    Returns:
        dict: トレンド情報
    """
    # 時系列データの分析
    equipment_trends = {}
    
    for equipment_id in set(d['equipment_id'] for d in data):
        equipment_data = [d for d in data if d['equipment_id'] == equipment_id]
        equipment_data.sort(key=lambda x: x['timestamp'])
        
        if len(equipment_data) >= 2:
            recent_efficiency = statistics.mean([d['efficiency'] for d in equipment_data[-3:]])
            older_efficiency = statistics.mean([d['efficiency'] for d in equipment_data[:3]])
            
            if recent_efficiency > older_efficiency + 2:
                trend = "improving"
            elif recent_efficiency < older_efficiency - 2:
                trend = "declining"
            else:
                trend = "stable"
        else:
            trend = "stable"
        
        equipment_trends[equipment_id] = {
            "trend": trend,
            "current_efficiency": round(equipment_data[-1]['efficiency'], 1) if equipment_data else 0
        }
    
    return equipment_trends


def generate_equipment_summary(data):
    """
    設備サマリーの生成
    
    Args:
        data: 設備データ
    
    Returns:
        dict: 設備サマリー
    """
    equipment_summary = {}
    
    for equipment_id in set(d['equipment_id'] for d in data):
        equipment_data = [d for d in data if d['equipment_id'] == equipment_id]
        operational_data = [d for d in equipment_data if d['status'] == 'operational']
        
        if operational_data:
            avg_efficiency = statistics.mean([d['efficiency'] for d in operational_data])
            avg_temperature = statistics.mean([d['temperature'] for d in operational_data])
        else:
            avg_efficiency = 0
            avg_temperature = 0
        
        equipment_summary[equipment_id] = {
            "avg_efficiency": round(avg_efficiency, 1),
            "avg_temperature": round(avg_temperature, 1),
            "uptime_ratio": round(len(operational_data) / len(equipment_data) * 100, 1) if equipment_data else 0,
            "data_points": len(equipment_data)
        }
    
    return equipment_summary


def generate_alerts_summary(data):
    """
    アラートサマリーの生成
    
    Args:
        data: 設備データ
    
    Returns:
        dict: アラートサマリー
    """
    alerts = {
        "critical": 0,
        "warning": 0,
        "info": 0
    }
    
    for d in data:
        if d['efficiency'] < 60:
            alerts["critical"] += 1
        elif d['efficiency'] < 80:
            alerts["warning"] += 1
        
        if d['temperature'] > 200:
            alerts["critical"] += 1
        elif d['temperature'] > 180:
            alerts["warning"] += 1
    
    return alerts


def calculate_overall_efficiency(data):
    """
    全体効率の計算
    
    Args:
        data: 設備データ
    
    Returns:
        float: 全体効率
    """
    operational_data = [d for d in data if d['status'] == 'operational']
    if not operational_data:
        return 0
    
    return round(statistics.mean([d['efficiency'] for d in operational_data]), 2)


def rank_equipment_by_efficiency(data):
    """
    効率による設備ランキング
    
    Args:
        data: 設備データ
    
    Returns:
        list: ランキングリスト
    """
    equipment_efficiency = {}
    
    for equipment_id in set(d['equipment_id'] for d in data):
        equipment_data = [d for d in data if d['equipment_id'] == equipment_id and d['status'] == 'operational']
        if equipment_data:
            avg_efficiency = statistics.mean([d['efficiency'] for d in equipment_data])
            equipment_efficiency[equipment_id] = round(avg_efficiency, 1)
    
    # 効率順でソート
    ranked = sorted(equipment_efficiency.items(), key=lambda x: x[1], reverse=True)
    
    return [{"equipment_id": eq, "efficiency": eff} for eq, eff in ranked]


def identify_efficiency_patterns(data):
    """
    効率パターンの特定
    
    Args:
        data: 設備データ
    
    Returns:
        dict: パターン情報
    """
    # 簡単なパターン分析
    patterns = {
        "peak_hours": "09:00-11:00, 14:00-16:00",
        "low_efficiency_periods": "12:00-13:00, 17:00-18:00",
        "optimal_temperature_range": "150-180°C",
        "efficiency_correlation": "温度と効率に正の相関関係"
    }
    
    return patterns


def find_improvement_opportunities(data):
    """
    改善機会の発見
    
    Args:
        data: 設備データ
    
    Returns:
        list: 改善機会リスト
    """
    opportunities = [
        {
            "area": "温度管理",
            "description": "最適温度範囲での運転により効率5%向上が期待される",
            "impact": "高"
        },
        {
            "area": "運転スケジュール",
            "description": "ピーク時間外の保全作業により稼働率向上",
            "impact": "中"
        },
        {
            "area": "予防保全",
            "description": "予測保全の導入により計画外停止を30%削減",
            "impact": "高"
        }
    ]
    
    return opportunities


def predict_maintenance_needs(data):
    """
    メンテナンス需要の予測
    
    Args:
        data: 設備データ
    
    Returns:
        dict: メンテナンス予測
    """
    predictions = {}
    
    for equipment_id in set(d['equipment_id'] for d in data):
        equipment_data = [d for d in data if d['equipment_id'] == equipment_id]
        
        # 簡単な予測ロジック
        recent_efficiency = [d['efficiency'] for d in equipment_data[-5:]]
        if recent_efficiency:
            avg_recent = statistics.mean(recent_efficiency)
            if avg_recent < 70:
                urgency = "即座に"
            elif avg_recent < 85:
                urgency = "7日以内に"
            else:
                urgency = "30日以内に"
        else:
            urgency = "データ不足"
        
        predictions[equipment_id] = {
            "next_maintenance": urgency,
            "confidence": "85%" if urgency != "データ不足" else "N/A"
        }
    
    return predictions


def forecast_production(data):
    """
    生産予測
    
    Args:
        data: 設備データ
    
    Returns:
        dict: 生産予測
    """
    current_efficiency = calculate_overall_efficiency(data)
    
    forecast = {
        "next_week": {
            "estimated_efficiency": round(current_efficiency * 0.98, 1),  # 若干の低下を想定
            "production_rate": "95%",
            "confidence": "78%"
        },
        "next_month": {
            "estimated_efficiency": round(current_efficiency * 0.95, 1),
            "production_rate": "92%",
            "confidence": "65%"
        }
    }
    
    return forecast


def assess_failure_risks(data):
    """
    故障リスクの評価
    
    Args:
        data: 設備データ
    
    Returns:
        dict: リスク評価
    """
    risk_assessment = {}
    
    for equipment_id in set(d['equipment_id'] for d in data):
        equipment_data = [d for d in data if d['equipment_id'] == equipment_id]
        
        # リスク要因の計算
        efficiency_risk = len([d for d in equipment_data if d['efficiency'] < 70]) / len(equipment_data)
        temperature_risk = len([d for d in equipment_data if d['temperature'] > 200]) / len(equipment_data)
        
        overall_risk = (efficiency_risk + temperature_risk) / 2
        
        if overall_risk > 0.3:
            risk_level = "高"
        elif overall_risk > 0.1:
            risk_level = "中"
        else:
            risk_level = "低"
        
        risk_assessment[equipment_id] = {
            "risk_level": risk_level,
            "risk_score": round(overall_risk * 100, 1),
            "primary_factors": ["効率低下", "温度上昇"] if overall_risk > 0.2 else ["正常範囲内"]
        }
    
    return risk_assessment


def suggest_optimal_schedule(data):
    """
    最適スケジュールの提案
    
    Args:
        data: 設備データ
    
    Returns:
        dict: スケジュール提案
    """
    schedule_suggestions = {
        "maintenance_windows": [
            "毎週土曜日 08:00-12:00",
            "月末最終日曜日 終日"
        ],
        "optimal_operation_hours": "平日 09:00-17:00",
        "recommended_breaks": "12:00-13:00 (全設備)",
        "load_balancing": "設備A1,B2の負荷分散を推奨"
    }
    
    return schedule_suggestions


def generate_high_priority_recommendations(data):
    """
    高優先度の改善提案生成
    
    Args:
        data: 設備データ
    
    Returns:
        list: 高優先度提案
    """
    recommendations = [
        {
            "title": "緊急メンテナンス実施",
            "description": "効率が60%を下回る設備の即座メンテナンス",
            "expected_impact": "ダウンタイム50%削減",
            "implementation_time": "即座",
            "cost_estimate": "50万円"
        }
    ]
    
    return recommendations


def generate_medium_priority_recommendations(data):
    """
    中優先度の改善提案生成
    
    Args:
        data: 設備データ
    
    Returns:
        list: 中優先度提案
    """
    recommendations = [
        {
            "title": "予防保全スケジュール最適化",
            "description": "データに基づく保全間隔の調整",
            "expected_impact": "保全コスト20%削減",
            "implementation_time": "2週間",
            "cost_estimate": "30万円"
        }
    ]
    
    return recommendations


def generate_low_priority_recommendations(data):
    """
    低優先度の改善提案生成
    
    Args:
        data: 設備データ
    
    Returns:
        list: 低優先度提案
    """
    recommendations = [
        {
            "title": "運転パラメーター微調整",
            "description": "温度・速度設定の最適化",
            "expected_impact": "効率3-5%向上",
            "implementation_time": "1ヶ月",
            "cost_estimate": "10万円"
        }
    ]
    
    return recommendations


def calculate_cost_benefits(data):
    """
    コストベネフィット分析
    
    Args:
        data: 設備データ
    
    Returns:
        dict: 分析結果
    """
    analysis = {
        "investment_required": "90万円",
        "annual_savings": "200万円",
        "payback_period": "5.4ヶ月",
        "roi_percentage": "122%",
        "risk_factors": ["実装時の一時的な生産性低下", "技術者教育コスト"]
    }
    
    return analysis