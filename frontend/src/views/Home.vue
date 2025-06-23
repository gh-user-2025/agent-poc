<template>
  <div class="home">
    <h1>ホーム画面</h1>
    <p class="welcome-message">工場設備管理システムへようこそ</p>
    
    <div class="dashboard-summary">
      <div class="summary-card">
        <h3>総設備数</h3>
        <div class="count">{{ equipmentSummary.total }}</div>
      </div>
      <div class="summary-card running">
        <h3>稼働中</h3>
        <div class="count">{{ equipmentSummary.running }}</div>
      </div>
      <div class="summary-card idle">
        <h3>待機中</h3>
        <div class="count">{{ equipmentSummary.idle }}</div>
      </div>
      <div class="summary-card maintenance">
        <h3>メンテナンス中</h3>
        <div class="count">{{ equipmentSummary.maintenance }}</div>
      </div>
      <div class="summary-card error">
        <h3>エラー</h3>
        <div class="count">{{ equipmentSummary.error }}</div>
      </div>
    </div>

    <div class="quick-actions">
      <h2>クイックアクション</h2>
      <div class="action-buttons">
        <router-link to="/equipment-status" class="action-button primary">
          設備状況を確認
        </router-link>
        <button class="action-button" @click="refreshData">
          データを更新
        </button>
        <button class="action-button" @click="showMaintenanceSchedule">
          メンテナンス予定
        </button>
      </div>
    </div>

    <div class="recent-alerts" v-if="recentAlerts.length > 0">
      <h2>最近のアラート</h2>
      <div class="alert-list">
        <div v-for="alert in recentAlerts" :key="alert.id" class="alert-item" :class="alert.severity">
          <div class="alert-time">{{ formatTime(alert.timestamp) }}</div>
          <div class="alert-message">{{ alert.message }}</div>
          <div class="alert-equipment">{{ alert.equipmentName }}</div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Home',
  data() {
    return {
      equipmentSummary: {
        total: 0,
        running: 0,
        idle: 0,
        maintenance: 0,
        error: 0
      },
      recentAlerts: []
    }
  },
  methods: {
    loadSampleData() {
      // サンプルデータの読み込み
      const sampleEquipment = [
        { id: 1, name: '射出成形機-1', status: 'running', location: 'ライン A' },
        { id: 2, name: '射出成形機-2', status: 'running', location: 'ライン A' },
        { id: 3, name: '組立ロボット-1', status: 'idle', location: 'ライン B' },
        { id: 4, name: '組立ロボット-2', status: 'running', location: 'ライン B' },
        { id: 5, name: '検査装置-1', status: 'maintenance', location: 'ライン C' },
        { id: 6, name: 'コンプレッサー-1', status: 'running', location: '共通設備' },
        { id: 7, name: 'コンプレッサー-2', status: 'error', location: '共通設備' }
      ];

      // 設備サマリーの計算
      this.equipmentSummary.total = sampleEquipment.length;
      this.equipmentSummary.running = sampleEquipment.filter(eq => eq.status === 'running').length;
      this.equipmentSummary.idle = sampleEquipment.filter(eq => eq.status === 'idle').length;
      this.equipmentSummary.maintenance = sampleEquipment.filter(eq => eq.status === 'maintenance').length;
      this.equipmentSummary.error = sampleEquipment.filter(eq => eq.status === 'error').length;

      // サンプルアラートデータ
      this.recentAlerts = [
        {
          id: 1,
          timestamp: new Date(Date.now() - 300000), // 5分前
          message: '温度異常が検出されました',
          equipmentName: 'コンプレッサー-2',
          severity: 'error'
        },
        {
          id: 2,
          timestamp: new Date(Date.now() - 1800000), // 30分前
          message: 'メンテナンス時期に到達しました',
          equipmentName: '検査装置-1',
          severity: 'warning'
        }
      ];
    },
    refreshData() {
      this.loadSampleData();
      alert('データを更新しました');
    },
    showMaintenanceSchedule() {
      alert('メンテナンス予定画面は準備中です');
    },
    formatTime(timestamp) {
      return timestamp.toLocaleString('ja-JP');
    }
  },
  mounted() {
    this.loadSampleData();
  }
}
</script>

<style scoped>
.home {
  max-width: 1200px;
  margin: 0 auto;
}

.welcome-message {
  font-size: 1.2rem;
  margin-bottom: 2rem;
  color: #666;
}

.dashboard-summary {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1rem;
  margin-bottom: 2rem;
}

.summary-card {
  background: white;
  padding: 1.5rem;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
  text-align: center;
  border-left: 4px solid #3498db;
}

.summary-card.running {
  border-left-color: #27ae60;
}

.summary-card.idle {
  border-left-color: #f39c12;
}

.summary-card.maintenance {
  border-left-color: #e74c3c;
}

.summary-card.error {
  border-left-color: #c0392b;
}

.summary-card h3 {
  margin-bottom: 0.5rem;
  color: #333;
  font-size: 0.9rem;
}

.count {
  font-size: 2rem;
  font-weight: bold;
  color: #2c3e50;
}

.quick-actions {
  background: white;
  padding: 2rem;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
  margin-bottom: 2rem;
}

.quick-actions h2 {
  margin-bottom: 1rem;
  color: #2c3e50;
}

.action-buttons {
  display: flex;
  gap: 1rem;
  flex-wrap: wrap;
}

.action-button {
  padding: 0.75rem 1.5rem;
  border: none;
  border-radius: 4px;
  background-color: #95a5a6;
  color: white;
  text-decoration: none;
  cursor: pointer;
  transition: background-color 0.3s;
  font-size: 1rem;
}

.action-button:hover {
  background-color: #7f8c8d;
}

.action-button.primary {
  background-color: #3498db;
}

.action-button.primary:hover {
  background-color: #2980b9;
}

.recent-alerts {
  background: white;
  padding: 2rem;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.recent-alerts h2 {
  margin-bottom: 1rem;
  color: #2c3e50;
}

.alert-list {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.alert-item {
  display: grid;
  grid-template-columns: 150px 1fr 150px;
  gap: 1rem;
  padding: 1rem;
  border-radius: 4px;
  border-left: 4px solid #3498db;
}

.alert-item.error {
  border-left-color: #e74c3c;
  background-color: #fdf2f2;
}

.alert-item.warning {
  border-left-color: #f39c12;
  background-color: #fefbf3;
}

.alert-time {
  font-size: 0.9rem;
  color: #666;
}

.alert-message {
  font-weight: bold;
}

.alert-equipment {
  font-size: 0.9rem;
  color: #666;
  text-align: right;
}

@media (max-width: 768px) {
  .action-buttons {
    flex-direction: column;
  }
  
  .alert-item {
    grid-template-columns: 1fr;
    text-align: left;
  }
  
  .alert-equipment {
    text-align: left;
  }
}
</style>