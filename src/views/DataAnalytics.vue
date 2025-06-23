<!-- データ分析画面 - 設備の稼働データを分析し運用改善提案を表示 -->
<template>
  <div class="data-analytics">
    <h2 class="page-title">📈 データ分析</h2>
    <p class="page-description">設備の稼働データを分析し、効率的な運用方法を提案します</p>

    <!-- 分析期間選択 -->
    <div class="analysis-controls">
      <div class="period-selector">
        <label for="analysis-period">分析期間:</label>
        <select v-model="selectedPeriod" id="analysis-period" class="control-select">
          <option value="day">本日</option>
          <option value="week">過去7日間</option>
          <option value="month">過去30日間</option>
          <option value="quarter">過去3ヶ月</option>
        </select>
      </div>
      
      <button @click="generateReport" class="generate-button">
        📊 レポート生成
      </button>
    </div>

    <!-- KPI概要 -->
    <div class="kpi-section">
      <h3 class="section-title">📊 主要指標 (KPI)</h3>
      <div class="kpi-grid">
        <div class="kpi-card">
          <div class="kpi-icon">⚡</div>
          <div class="kpi-content">
            <h4 class="kpi-title">総合稼働率</h4>
            <p class="kpi-value">{{ kpis.overallEfficiency }}%</p>
            <p class="kpi-trend" :class="kpis.efficiencyTrend">
              {{ getTrendLabel(kpis.efficiencyTrend) }}
            </p>
          </div>
        </div>
        
        <div class="kpi-card">
          <div class="kpi-icon">⏱️</div>
          <div class="kpi-content">
            <h4 class="kpi-title">ダウンタイム</h4>
            <p class="kpi-value">{{ kpis.downtime }}h</p>
            <p class="kpi-trend" :class="kpis.downtimeTrend">
              {{ getTrendLabel(kpis.downtimeTrend) }}
            </p>
          </div>
        </div>
        
        <div class="kpi-card">
          <div class="kpi-icon">🎯</div>
          <div class="kpi-content">
            <h4 class="kpi-title">生産目標達成率</h4>
            <p class="kpi-value">{{ kpis.targetAchievement }}%</p>
            <p class="kpi-trend" :class="kpis.achievementTrend">
              {{ getTrendLabel(kpis.achievementTrend) }}
            </p>
          </div>
        </div>
        
        <div class="kpi-card">
          <div class="kpi-icon">💰</div>
          <div class="kpi-content">
            <h4 class="kpi-title">コスト削減</h4>
            <p class="kpi-value">¥{{ kpis.costSaving.toLocaleString() }}</p>
            <p class="kpi-trend" :class="kpis.costTrend">
              {{ getTrendLabel(kpis.costTrend) }}
            </p>
          </div>
        </div>
      </div>
    </div>

    <!-- チャート表示エリア -->
    <div class="charts-section">
      <h3 class="section-title">📊 データ可視化</h3>
      <div class="charts-grid">
        <!-- 稼働率推移グラフ（プレースホルダー） -->
        <div class="chart-container">
          <h4 class="chart-title">設備稼働率推移</h4>
          <div class="chart-placeholder">
            <p>📈 Chart.js or Power BI埋め込みエリア</p>
            <p>実際の実装では外部データソースから取得したデータを表示</p>
          </div>
        </div>
        
        <!-- 生産量グラフ（プレースホルダー） -->
        <div class="chart-container">
          <h4 class="chart-title">日別生産量</h4>
          <div class="chart-placeholder">
            <p>📊 生産量データの可視化エリア</p>
            <p>Azure SQL Database からのデータを表示</p>
          </div>
        </div>
      </div>
    </div>

    <!-- AI分析結果と改善提案 -->
    <div class="insights-section">
      <h3 class="section-title">🤖 AI分析結果と改善提案</h3>
      <div class="insights-grid">
        <div 
          v-for="insight in analysisInsights"
          :key="insight.id"
          class="insight-card"
          :class="insight.priority"
        >
          <div class="insight-header">
            <span class="insight-icon">{{ insight.icon }}</span>
            <h4 class="insight-title">{{ insight.title }}</h4>
            <span class="insight-priority" :class="insight.priority">
              {{ getPriorityLabel(insight.priority) }}
            </span>
          </div>
          
          <div class="insight-content">
            <p class="insight-description">{{ insight.description }}</p>
            <div class="insight-impact">
              <strong>期待効果:</strong> {{ insight.expectedImpact }}
            </div>
            <div class="insight-action">
              <strong>推奨アクション:</strong> {{ insight.recommendedAction }}
            </div>
          </div>
          
          <div class="insight-footer">
            <button 
              @click="implementSuggestion(insight.id)"
              class="implement-button"
              :disabled="insight.implemented"
            >
              {{ insight.implemented ? '実装済み' : '提案を採用' }}
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- 予測分析 -->
    <div class="predictions-section">
      <h3 class="section-title">🔮 予測分析</h3>
      <div class="predictions-grid">
        <div class="prediction-card">
          <h4 class="prediction-title">メンテナンス予測</h4>
          <div class="prediction-content">
            <p><strong>射出成形機 A1:</strong> 7日以内にメンテナンスが必要</p>
            <p><strong>組立ロボット B2:</strong> 14日以内に部品交換推奨</p>
            <p><strong>品質検査装置 C3:</strong> 要注意 - センサー校正が必要</p>
          </div>
        </div>
        
        <div class="prediction-card">
          <h4 class="prediction-title">生産量予測</h4>
          <div class="prediction-content">
            <p><strong>来週予測:</strong> 目標の102%達成見込み</p>
            <p><strong>来月予測:</strong> 現状維持で95%程度</p>
            <p><strong>改善後予測:</strong> 提案実装で105%達成可能</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'DataAnalytics',
  data() {
    return {
      selectedPeriod: 'week',
      // KPI データ
      kpis: {
        overallEfficiency: 87.5,
        efficiencyTrend: 'up',
        downtime: 12.3,
        downtimeTrend: 'down',
        targetAchievement: 95.2,
        achievementTrend: 'up',
        costSaving: 450000,
        costTrend: 'up'
      },
      // AI分析結果
      analysisInsights: [
        {
          id: 1,
          icon: '⚡',
          title: '設備稼働率の最適化',
          priority: 'high',
          description: '射出成形機A1の稼働パターンを分析した結果、午後2-4時の稼働率が低下しています。',
          expectedImpact: '稼働率5%向上、月間30万円のコスト削減',
          recommendedAction: '作業シフトの調整とオペレーター配置の見直し',
          implemented: false
        },
        {
          id: 2,
          icon: '🔧',
          title: '予防保全スケジュールの改善',
          priority: 'medium',
          description: '過去のメンテナンスデータから、現在の保全間隔は最適ではありません。',
          expectedImpact: 'ダウンタイム20%削減、保全コスト15%削減',
          recommendedAction: '保全間隔を3週間から4週間に延長',
          implemented: false
        },
        {
          id: 3,
          icon: '📊',
          title: '品質管理プロセスの効率化',
          priority: 'low',
          description: '品質検査装置の検査時間にばらつきがあり、効率化の余地があります。',
          expectedImpact: '検査時間10%短縮、スループット向上',
          recommendedAction: '検査パラメーターの標準化と自動化拡張',
          implemented: true
        }
      ]
    }
  },
  mounted() {
    // コンポーネントマウント時にデータを読み込み
    this.loadAnalyticsData()
  },
  methods: {
    // トレンド表示ラベル
    getTrendLabel(trend) {
      const labels = {
        up: '↗️ 上昇',
        down: '↘️ 下降',
        stable: '→ 安定'
      }
      return labels[trend] || '→ 安定'
    },
    
    // 優先度ラベル
    getPriorityLabel(priority) {
      const labels = {
        high: '高優先度',
        medium: '中優先度',
        low: '低優先度'
      }
      return labels[priority] || '標準'
    },
    
    // レポート生成
    generateReport() {
      console.log(`${this.selectedPeriod}期間のレポートを生成中...`)
      // 実際の実装では Azure Functions を呼び出してレポート生成
      alert('レポートを生成しました。実際の実装では Power BI レポートを表示します。')
    },
    
    // 改善提案の採用
    implementSuggestion(insightId) {
      const insight = this.analysisInsights.find(item => item.id === insightId)
      if (insight && !insight.implemented) {
        insight.implemented = true
        console.log(`改善提案「${insight.title}」を採用しました`)
        
        // 実際の実装では Azure Functions でワークフローをトリガー
        alert(`改善提案「${insight.title}」の実装を開始しました。`)
      }
    },
    
    // 分析データの読み込み
    loadAnalyticsData() {
      console.log('分析データを読み込み中...')
      // 実際の実装では以下のデータソースから取得:
      // - Azure SQL Database (履歴データ)
      // - Azure Cosmos DB (リアルタイムデータ)
      // - Azure Functions (AI分析結果)
    }
  },
  watch: {
    // 分析期間が変更された時の処理
    selectedPeriod(newPeriod) {
      console.log(`分析期間を${newPeriod}に変更しました`)
      this.loadAnalyticsData()
    }
  }
}
</script>

<style scoped>
.data-analytics {
  max-width: 1200px;
  margin: 0 auto;
}

.page-title {
  font-size: 2.5rem;
  color: #2c3e50;
  margin-bottom: 0.5rem;
}

.page-description {
  color: #7f8c8d;
  margin-bottom: 2rem;
  font-size: 1.1rem;
}

.section-title {
  font-size: 1.5rem;
  color: #2c3e50;
  margin-bottom: 1rem;
}

/* 分析コントロール */
.analysis-controls {
  display: flex;
  gap: 2rem;
  margin-bottom: 3rem;
  align-items: center;
  flex-wrap: wrap;
}

.period-selector {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.control-select {
  padding: 0.5rem 1rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 1rem;
}

.generate-button {
  background: #3498db;
  color: white;
  border: none;
  padding: 0.5rem 1rem;
  border-radius: 4px;
  cursor: pointer;
  font-size: 1rem;
  transition: background-color 0.3s;
}

.generate-button:hover {
  background: #2980b9;
}

/* KPI セクション */
.kpi-section {
  margin-bottom: 3rem;
}

.kpi-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1.5rem;
}

.kpi-card {
  background: white;
  padding: 1.5rem;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
  display: flex;
  align-items: center;
  gap: 1rem;
}

.kpi-icon {
  font-size: 2.5rem;
}

.kpi-title {
  font-size: 0.9rem;
  color: #7f8c8d;
  margin: 0 0 0.5rem 0;
}

.kpi-value {
  font-size: 1.8rem;
  font-weight: bold;
  color: #2c3e50;
  margin: 0;
}

.kpi-trend {
  font-size: 0.8rem;
  font-weight: bold;
  margin: 0.25rem 0 0 0;
}

.kpi-trend.up {
  color: #27ae60;
}

.kpi-trend.down {
  color: #e74c3c;
}

.kpi-trend.stable {
  color: #95a5a6;
}

/* チャートセクション */
.charts-section {
  margin-bottom: 3rem;
}

.charts-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
  gap: 2rem;
}

.chart-container {
  background: white;
  padding: 1.5rem;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}

.chart-title {
  color: #2c3e50;
  margin-bottom: 1rem;
}

.chart-placeholder {
  height: 250px;
  background: #f8f9fa;
  border: 2px dashed #dee2e6;
  border-radius: 4px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  text-align: center;
  color: #6c757d;
}

/* インサイトセクション */
.insights-section {
  margin-bottom: 3rem;
}

.insights-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
  gap: 1.5rem;
}

.insight-card {
  background: white;
  padding: 1.5rem;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
  border-left: 4px solid #95a5a6;
}

.insight-card.high {
  border-left-color: #e74c3c;
}

.insight-card.medium {
  border-left-color: #f39c12;
}

.insight-card.low {
  border-left-color: #3498db;
}

.insight-header {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin-bottom: 1rem;
}

.insight-icon {
  font-size: 1.5rem;
}

.insight-title {
  font-size: 1.1rem;
  color: #2c3e50;
  margin: 0;
  flex: 1;
}

.insight-priority {
  padding: 0.25rem 0.5rem;
  border-radius: 12px;
  font-size: 0.7rem;
  font-weight: bold;
}

.insight-priority.high {
  background: #fadbd8;
  color: #e74c3c;
}

.insight-priority.medium {
  background: #fef2e0;
  color: #f39c12;
}

.insight-priority.low {
  background: #d6eaf8;
  color: #3498db;
}

.insight-content {
  margin-bottom: 1rem;
}

.insight-description {
  color: #7f8c8d;
  margin-bottom: 1rem;
}

.insight-impact,
.insight-action {
  margin-bottom: 0.5rem;
  font-size: 0.9rem;
}

.insight-footer {
  border-top: 1px solid #ecf0f1;
  padding-top: 1rem;
}

.implement-button {
  background: #27ae60;
  color: white;
  border: none;
  padding: 0.5rem 1rem;
  border-radius: 4px;
  cursor: pointer;
  font-size: 0.9rem;
  transition: background-color 0.3s;
}

.implement-button:hover:not(:disabled) {
  background: #229954;
}

.implement-button:disabled {
  background: #95a5a6;
  cursor: not-allowed;
}

/* 予測分析セクション */
.predictions-section {
  margin-bottom: 3rem;
}

.predictions-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 1.5rem;
}

.prediction-card {
  background: white;
  padding: 1.5rem;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}

.prediction-title {
  color: #2c3e50;
  margin-bottom: 1rem;
}

.prediction-content p {
  margin-bottom: 0.5rem;
  color: #7f8c8d;
}

@media (max-width: 768px) {
  .kpi-grid {
    grid-template-columns: 1fr;
  }
  
  .charts-grid {
    grid-template-columns: 1fr;
  }
  
  .insights-grid {
    grid-template-columns: 1fr;
  }
  
  .predictions-grid {
    grid-template-columns: 1fr;
  }
  
  .analysis-controls {
    flex-direction: column;
    align-items: flex-start;
  }
}
</style>