<!-- ダッシュボード画面 - 工場設備の概要情報を表示 -->
<template>
  <div class="dashboard">
    <h2 class="page-title">📊 ダッシュボード</h2>
    <p class="page-description">工場設備の稼働状況とシステムの概要をご覧いただけます</p>

    <!-- システム概要カード -->
    <div class="overview-section">
      <div class="stat-cards">
        <div class="stat-card">
          <div class="stat-icon">🏭</div>
          <div class="stat-content">
            <h3 class="stat-number">{{ stats.totalEquipment }}</h3>
            <p class="stat-label">総設備数</p>
          </div>
        </div>
        
        <div class="stat-card">
          <div class="stat-icon">✅</div>
          <div class="stat-content">
            <h3 class="stat-number">{{ stats.operationalEquipment }}</h3>
            <p class="stat-label">稼働中設備</p>
          </div>
        </div>
        
        <div class="stat-card">
          <div class="stat-icon">⚠️</div>
          <div class="stat-content">
            <h3 class="stat-number">{{ stats.alertsCount }}</h3>
            <p class="stat-label">アラート</p>
          </div>
        </div>
        
        <div class="stat-card">
          <div class="stat-icon">🔧</div>
          <div class="stat-content">
            <h3 class="stat-number">{{ stats.maintenanceToday }}</h3>
            <p class="stat-label">本日のメンテナンス</p>
          </div>
        </div>
      </div>
    </div>

    <!-- 技術スタック情報 -->
    <div class="tech-stack-section">
      <h3 class="section-title">🔧 使用技術スタック</h3>
      <div class="tech-grid">
        <div class="tech-card">
          <h4>Azure Functions</h4>
          <p>データの処理や分析を行います</p>
        </div>
        <div class="tech-card">
          <h4>Azure SQL Database</h4>
          <p>収集したデータを保存します</p>
        </div>
        <div class="tech-card">
          <h4>Azure Cosmos DB</h4>
          <p>IoTデバイスからのデータをリアルタイム処理</p>
        </div>
        <div class="tech-card">
          <h4>Power BI</h4>
          <p>データの可視化と分析結果の共有</p>
        </div>
      </div>
    </div>

    <!-- クイックアクション -->
    <div class="quick-actions-section">
      <h3 class="section-title">⚡ クイックアクション</h3>
      <div class="action-buttons">
        <router-link to="/monitoring" class="action-button">
          <span class="action-icon">📺</span>
          <span class="action-text">設備監視</span>
        </router-link>
        <router-link to="/maintenance" class="action-button">
          <span class="action-icon">🔧</span>
          <span class="action-text">メンテナンス管理</span>
        </router-link>
        <router-link to="/analytics" class="action-button">
          <span class="action-icon">📈</span>
          <span class="action-text">データ分析</span>
        </router-link>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Dashboard',
  data() {
    return {
      // 統計データ（実際のアプリではAPIから取得）
      stats: {
        totalEquipment: 24,
        operationalEquipment: 22,
        alertsCount: 3,
        maintenanceToday: 2
      }
    }
  },
  mounted() {
    // コンポーネントがマウントされた時の処理
    this.loadDashboardData()
  },
  methods: {
    // ダッシュボードデータの読み込み
    loadDashboardData() {
      // ここで実際のAPIからデータを取得する処理を実装
      console.log('ダッシュボードデータを読み込み中...')
    }
  }
}
</script>

<style scoped>
.dashboard {
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

/* 統計カード */
.stat-cards {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1.5rem;
  margin-bottom: 3rem;
}

.stat-card {
  background: white;
  padding: 1.5rem;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
  display: flex;
  align-items: center;
  gap: 1rem;
}

.stat-icon {
  font-size: 2.5rem;
}

.stat-number {
  font-size: 2rem;
  font-weight: bold;
  color: #2c3e50;
  margin: 0;
}

.stat-label {
  color: #7f8c8d;
  margin: 0;
}

/* 技術スタック */
.tech-stack-section {
  margin-bottom: 3rem;
}

.tech-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1.5rem;
}

.tech-card {
  background: white;
  padding: 1.5rem;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}

.tech-card h4 {
  color: #3498db;
  margin-bottom: 0.5rem;
}

.tech-card p {
  color: #7f8c8d;
  margin: 0;
}

/* クイックアクション */
.action-buttons {
  display: flex;
  gap: 1.5rem;
  flex-wrap: wrap;
}

.action-button {
  background: #3498db;
  color: white;
  padding: 1rem 2rem;
  border-radius: 8px;
  text-decoration: none;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  transition: background-color 0.3s;
}

.action-button:hover {
  background: #2980b9;
}

.action-icon {
  font-size: 1.5rem;
}

.action-text {
  font-weight: bold;
}

@media (max-width: 768px) {
  .stat-cards {
    grid-template-columns: 1fr;
  }
  
  .tech-grid {
    grid-template-columns: 1fr;
  }
  
  .action-buttons {
    flex-direction: column;
  }
}
</style>