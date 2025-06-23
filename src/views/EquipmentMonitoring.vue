<!-- 設備監視画面 - リアルタイムで設備の稼働状況を監視 -->
<template>
  <div class="equipment-monitoring">
    <h2 class="page-title">📺 設備監視</h2>
    <p class="page-description">工場設備のリアルタイム稼働状況を監視できます</p>

    <!-- フィルターとコントロール -->
    <div class="controls-section">
      <div class="filter-controls">
        <select v-model="selectedLine" class="control-select">
          <option value="">全ライン</option>
          <option value="line1">製造ライン1</option>
          <option value="line2">製造ライン2</option>
          <option value="line3">製造ライン3</option>
        </select>
        
        <select v-model="statusFilter" class="control-select">
          <option value="">全状態</option>
          <option value="operational">稼働中</option>
          <option value="maintenance">メンテナンス中</option>
          <option value="alert">アラート発生</option>
        </select>
        
        <button @click="refreshData" class="refresh-button">
          🔄 データ更新
        </button>
      </div>
    </div>

    <!-- 設備一覧 -->
    <div class="equipment-grid">
      <div 
        v-for="equipment in filteredEquipment" 
        :key="equipment.id"
        class="equipment-card"
        :class="equipment.status"
      >
        <div class="equipment-header">
          <h3 class="equipment-name">{{ equipment.name }}</h3>
          <span class="equipment-status" :class="equipment.status">
            {{ getStatusLabel(equipment.status) }}
          </span>
        </div>
        
        <div class="equipment-details">
          <div class="detail-row">
            <span class="detail-label">生産ライン:</span>
            <span class="detail-value">{{ equipment.line }}</span>
          </div>
          <div class="detail-row">
            <span class="detail-label">稼働率:</span>
            <span class="detail-value">{{ equipment.efficiency }}%</span>
          </div>
          <div class="detail-row">
            <span class="detail-label">温度:</span>
            <span class="detail-value">{{ equipment.temperature }}°C</span>
          </div>
          <div class="detail-row">
            <span class="detail-label">最終更新:</span>
            <span class="detail-value">{{ formatTime(equipment.lastUpdate) }}</span>
          </div>
        </div>
        
        <div class="equipment-actions" v-if="equipment.status === 'alert'">
          <button @click="acknowledgeAlert(equipment.id)" class="alert-button">
            ⚠️ アラート確認
          </button>
        </div>
      </div>
    </div>

    <!-- データが見つからない場合 -->
    <div v-if="filteredEquipment.length === 0" class="no-data">
      <p>条件に一致する設備が見つかりません</p>
    </div>
  </div>
</template>

<script>
export default {
  name: 'EquipmentMonitoring',
  data() {
    return {
      selectedLine: '',
      statusFilter: '',
      // サンプル設備データ（実際のアプリではAPIから取得）
      equipmentList: [
        {
          id: 1,
          name: '射出成形機 A1',
          line: '製造ライン1',
          status: 'operational',
          efficiency: 95,
          temperature: 185,
          lastUpdate: new Date(Date.now() - 300000) // 5分前
        },
        {
          id: 2,
          name: '組立ロボット B2',
          line: '製造ライン1',
          status: 'operational',
          efficiency: 88,
          temperature: 45,
          lastUpdate: new Date(Date.now() - 120000) // 2分前
        },
        {
          id: 3,
          name: '品質検査装置 C3',
          line: '製造ライン2',
          status: 'alert',
          efficiency: 72,
          temperature: 35,
          lastUpdate: new Date(Date.now() - 60000) // 1分前
        },
        {
          id: 4,
          name: 'パッケージング装置 D4',
          line: '製造ライン2',
          status: 'maintenance',
          efficiency: 0,
          temperature: 25,
          lastUpdate: new Date(Date.now() - 1800000) // 30分前
        },
        {
          id: 5,
          name: '搬送コンベア E5',
          line: '製造ライン3',
          status: 'operational',
          efficiency: 100,
          temperature: 30,
          lastUpdate: new Date(Date.now() - 180000) // 3分前
        }
      ]
    }
  },
  computed: {
    // フィルタリングされた設備リスト
    filteredEquipment() {
      return this.equipmentList.filter(equipment => {
        const lineMatch = !this.selectedLine || equipment.line === this.selectedLine
        const statusMatch = !this.statusFilter || equipment.status === this.statusFilter
        return lineMatch && statusMatch
      })
    }
  },
  mounted() {
    // リアルタイム更新の開始
    this.startRealTimeUpdates()
  },
  beforeUnmount() {
    // リアルタイム更新の停止
    this.stopRealTimeUpdates()
  },
  methods: {
    // ステータスラベルの取得
    getStatusLabel(status) {
      const labels = {
        operational: '稼働中',
        maintenance: 'メンテナンス中',
        alert: 'アラート発生'
      }
      return labels[status] || '不明'
    },
    
    // 時刻フォーマット
    formatTime(date) {
      return date.toLocaleTimeString('ja-JP')
    },
    
    // データ更新
    refreshData() {
      console.log('設備データを更新中...')
      // 実際のアプリではAPIからデータを再取得
      this.equipmentList.forEach(equipment => {
        equipment.lastUpdate = new Date()
      })
    },
    
    // アラート確認
    acknowledgeAlert(equipmentId) {
      const equipment = this.equipmentList.find(eq => eq.id === equipmentId)
      if (equipment) {
        equipment.status = 'operational'
        console.log(`設備 ${equipment.name} のアラートを確認しました`)
      }
    },
    
    // リアルタイム更新の開始
    startRealTimeUpdates() {
      this.updateInterval = setInterval(() => {
        // 実際のアプリではWebSocketやServerSentEventsを使用
        this.simulateDataUpdate()
      }, 30000) // 30秒間隔
    },
    
    // リアルタイム更新の停止
    stopRealTimeUpdates() {
      if (this.updateInterval) {
        clearInterval(this.updateInterval)
      }
    },
    
    // データ更新のシミュレーション
    simulateDataUpdate() {
      this.equipmentList.forEach(equipment => {
        // 稼働率をランダムに変動
        if (equipment.status === 'operational') {
          equipment.efficiency = Math.max(70, Math.min(100, 
            equipment.efficiency + (Math.random() - 0.5) * 10))
        }
        equipment.lastUpdate = new Date()
      })
    }
  }
}
</script>

<style scoped>
.equipment-monitoring {
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

/* コントロール */
.controls-section {
  margin-bottom: 2rem;
}

.filter-controls {
  display: flex;
  gap: 1rem;
  flex-wrap: wrap;
  align-items: center;
}

.control-select {
  padding: 0.5rem 1rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 1rem;
}

.refresh-button {
  background: #3498db;
  color: white;
  border: none;
  padding: 0.5rem 1rem;
  border-radius: 4px;
  cursor: pointer;
  font-size: 1rem;
  transition: background-color 0.3s;
}

.refresh-button:hover {
  background: #2980b9;
}

/* 設備グリッド */
.equipment-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 1.5rem;
}

.equipment-card {
  background: white;
  padding: 1.5rem;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
  border-left: 4px solid #95a5a6;
}

.equipment-card.operational {
  border-left-color: #27ae60;
}

.equipment-card.maintenance {
  border-left-color: #f39c12;
}

.equipment-card.alert {
  border-left-color: #e74c3c;
}

.equipment-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}

.equipment-name {
  font-size: 1.2rem;
  color: #2c3e50;
  margin: 0;
}

.equipment-status {
  padding: 0.25rem 0.5rem;
  border-radius: 12px;
  font-size: 0.8rem;
  font-weight: bold;
}

.equipment-status.operational {
  background: #d5f4e6;
  color: #27ae60;
}

.equipment-status.maintenance {
  background: #fef2e0;
  color: #f39c12;
}

.equipment-status.alert {
  background: #fadbd8;
  color: #e74c3c;
}

.equipment-details {
  margin-bottom: 1rem;
}

.detail-row {
  display: flex;
  justify-content: space-between;
  margin-bottom: 0.5rem;
}

.detail-label {
  color: #7f8c8d;
  font-weight: 500;
}

.detail-value {
  color: #2c3e50;
  font-weight: bold;
}

.equipment-actions {
  border-top: 1px solid #ecf0f1;
  padding-top: 1rem;
}

.alert-button {
  background: #e74c3c;
  color: white;
  border: none;
  padding: 0.5rem 1rem;
  border-radius: 4px;
  cursor: pointer;
  font-size: 0.9rem;
  transition: background-color 0.3s;
}

.alert-button:hover {
  background: #c0392b;
}

.no-data {
  text-align: center;
  padding: 3rem;
  color: #7f8c8d;
}

@media (max-width: 768px) {
  .equipment-grid {
    grid-template-columns: 1fr;
  }
  
  .filter-controls {
    flex-direction: column;
    align-items: stretch;
  }
}
</style>