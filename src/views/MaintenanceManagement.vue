<!-- メンテナンス管理画面 - 設備のメンテナンススケジュール管理 -->
<template>
  <div class="maintenance-management">
    <h2 class="page-title">🔧 メンテナンス管理</h2>
    <p class="page-description">設備のメンテナンススケジュールを管理し、予防保全を実現します</p>

    <!-- タブナビゲーション -->
    <div class="tab-navigation">
      <button 
        v-for="tab in tabs"
        :key="tab.id"
        @click="activeTab = tab.id"
        class="tab-button"
        :class="{ active: activeTab === tab.id }"
      >
        {{ tab.label }}
      </button>
    </div>

    <!-- スケジュール一覧タブ -->
    <div v-if="activeTab === 'schedule'" class="tab-content">
      <div class="schedule-controls">
        <select v-model="scheduleFilter" class="control-select">
          <option value="">全期間</option>
          <option value="today">今日</option>
          <option value="week">今週</option>
          <option value="month">今月</option>
        </select>
        
        <button @click="showAddModal = true" class="add-button">
          ➕ メンテナンス追加
        </button>
      </div>

      <div class="schedule-list">
        <div 
          v-for="item in filteredSchedule"
          :key="item.id"
          class="schedule-item"
          :class="item.priority"
        >
          <div class="schedule-header">
            <h3 class="schedule-title">{{ item.equipmentName }}</h3>
            <span class="schedule-date">{{ formatDate(item.scheduledDate) }}</span>
          </div>
          
          <div class="schedule-details">
            <p class="schedule-type">{{ item.maintenanceType }}</p>
            <p class="schedule-description">{{ item.description }}</p>
            <div class="schedule-meta">
              <span class="priority-badge" :class="item.priority">
                {{ getPriorityLabel(item.priority) }}
              </span>
              <span class="status-badge" :class="item.status">
                {{ getStatusLabel(item.status) }}
              </span>
            </div>
          </div>
          
          <div class="schedule-actions">
            <button 
              v-if="item.status === 'pending'"
              @click="startMaintenance(item.id)"
              class="action-button start"
            >
              開始
            </button>
            <button 
              v-if="item.status === 'in-progress'"
              @click="completeMaintenance(item.id)"
              class="action-button complete"
            >
              完了
            </button>
            <button 
              @click="editSchedule(item.id)"
              class="action-button edit"
            >
              編集
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- 履歴タブ -->
    <div v-if="activeTab === 'history'" class="tab-content">
      <div class="history-list">
        <div 
          v-for="record in maintenanceHistory"
          :key="record.id"
          class="history-item"
        >
          <div class="history-header">
            <h3 class="history-title">{{ record.equipmentName }}</h3>
            <span class="history-date">{{ formatDate(record.completedDate) }}</span>
          </div>
          
          <div class="history-details">
            <p class="history-type">{{ record.maintenanceType }}</p>
            <p class="history-technician">担当者: {{ record.technician }}</p>
            <p class="history-duration">作業時間: {{ record.duration }}時間</p>
            <p class="history-notes">{{ record.notes }}</p>
          </div>
        </div>
      </div>
    </div>

    <!-- 統計タブ -->
    <div v-if="activeTab === 'stats'" class="tab-content">
      <div class="stats-grid">
        <div class="stat-card">
          <h3 class="stat-title">今月の予定</h3>
          <p class="stat-number">{{ monthlyStats.scheduled }}</p>
        </div>
        <div class="stat-card">
          <h3 class="stat-title">完了済み</h3>
          <p class="stat-number">{{ monthlyStats.completed }}</p>
        </div>
        <div class="stat-card">
          <h3 class="stat-title">平均作業時間</h3>
          <p class="stat-number">{{ monthlyStats.avgDuration }}h</p>
        </div>
        <div class="stat-card">
          <h3 class="stat-title">予防保全率</h3>
          <p class="stat-number">{{ monthlyStats.preventiveRate }}%</p>
        </div>
      </div>

      <div class="equipment-status-overview">
        <h3 class="section-title">設備別メンテナンス状況</h3>
        <div class="equipment-status-list">
          <div 
            v-for="equipment in equipmentStatus"
            :key="equipment.id"
            class="equipment-status-item"
          >
            <div class="equipment-info">
              <h4>{{ equipment.name }}</h4>
              <p>次回メンテナンス: {{ formatDate(equipment.nextMaintenance) }}</p>
            </div>
            <div class="equipment-health" :class="equipment.healthStatus">
              {{ getHealthLabel(equipment.healthStatus) }}
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- メンテナンス追加モーダル（簡略版） -->
    <div v-if="showAddModal" class="modal-overlay" @click="showAddModal = false">
      <div class="modal-content" @click.stop>
        <h3>新規メンテナンス登録</h3>
        <p>メンテナンス登録機能は開発中です。</p>
        <button @click="showAddModal = false" class="modal-close">閉じる</button>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'MaintenanceManagement',
  data() {
    return {
      activeTab: 'schedule',
      scheduleFilter: '',
      showAddModal: false,
      tabs: [
        { id: 'schedule', label: '📅 スケジュール' },
        { id: 'history', label: '📋 履歴' },
        { id: 'stats', label: '📊 統計' }
      ],
      // メンテナンススケジュールデータ
      maintenanceSchedule: [
        {
          id: 1,
          equipmentName: '射出成形機 A1',
          maintenanceType: '定期点検',
          description: '月次定期点検・部品交換',
          scheduledDate: new Date(Date.now() + 86400000), // 明日
          priority: 'high',
          status: 'pending'
        },
        {
          id: 2,
          equipmentName: '組立ロボット B2',
          maintenanceType: '予防保全',
          description: 'センサー校正・動作確認',
          scheduledDate: new Date(Date.now() + 172800000), // 2日後
          priority: 'medium',
          status: 'pending'
        },
        {
          id: 3,
          equipmentName: '品質検査装置 C3',
          maintenanceType: '緊急修理',
          description: 'エラー修正・部品交換',
          scheduledDate: new Date(),
          priority: 'urgent',
          status: 'in-progress'
        }
      ],
      // メンテナンス履歴
      maintenanceHistory: [
        {
          id: 1,
          equipmentName: 'パッケージング装置 D4',
          maintenanceType: '定期点検',
          technician: '田中技術者',
          completedDate: new Date(Date.now() - 86400000),
          duration: 3,
          notes: '正常に完了。次回メンテナンスは3ヶ月後。'
        },
        {
          id: 2,
          equipmentName: '搬送コンベア E5',
          maintenanceType: '部品交換',
          technician: '佐藤技術者',
          completedDate: new Date(Date.now() - 172800000),
          duration: 2,
          notes: 'ベルト交換完了。動作正常。'
        }
      ],
      // 月間統計
      monthlyStats: {
        scheduled: 8,
        completed: 6,
        avgDuration: 2.5,
        preventiveRate: 85
      },
      // 設備健康状態
      equipmentStatus: [
        {
          id: 1,
          name: '射出成形機 A1',
          nextMaintenance: new Date(Date.now() + 86400000),
          healthStatus: 'good'
        },
        {
          id: 2,
          name: '組立ロボット B2',
          nextMaintenance: new Date(Date.now() + 172800000),
          healthStatus: 'good'
        },
        {
          id: 3,
          name: '品質検査装置 C3',
          nextMaintenance: new Date(),
          healthStatus: 'warning'
        }
      ]
    }
  },
  computed: {
    filteredSchedule() {
      if (!this.scheduleFilter) return this.maintenanceSchedule
      
      const now = new Date()
      const today = new Date(now.getFullYear(), now.getMonth(), now.getDate())
      
      return this.maintenanceSchedule.filter(item => {
        const itemDate = new Date(item.scheduledDate)
        
        switch (this.scheduleFilter) {
          case 'today':
            return itemDate.toDateString() === today.toDateString()
          case 'week':
            const weekLater = new Date(today.getTime() + 7 * 24 * 60 * 60 * 1000)
            return itemDate >= today && itemDate <= weekLater
          case 'month':
            const monthLater = new Date(today.getTime() + 30 * 24 * 60 * 60 * 1000)
            return itemDate >= today && itemDate <= monthLater
          default:
            return true
        }
      })
    }
  },
  methods: {
    formatDate(date) {
      return date.toLocaleDateString('ja-JP')
    },
    
    getPriorityLabel(priority) {
      const labels = {
        urgent: '緊急',
        high: '高',
        medium: '中',
        low: '低'
      }
      return labels[priority] || '不明'
    },
    
    getStatusLabel(status) {
      const labels = {
        pending: '待機中',
        'in-progress': '作業中',
        completed: '完了'
      }
      return labels[status] || '不明'
    },
    
    getHealthLabel(health) {
      const labels = {
        good: '良好',
        warning: '注意',
        critical: '要対応'
      }
      return labels[health] || '不明'
    },
    
    startMaintenance(id) {
      const item = this.maintenanceSchedule.find(item => item.id === id)
      if (item) {
        item.status = 'in-progress'
        console.log(`メンテナンス開始: ${item.equipmentName}`)
      }
    },
    
    completeMaintenance(id) {
      const item = this.maintenanceSchedule.find(item => item.id === id)
      if (item) {
        item.status = 'completed'
        console.log(`メンテナンス完了: ${item.equipmentName}`)
      }
    },
    
    editSchedule(id) {
      console.log(`スケジュール編集: ID ${id}`)
      // 編集機能は開発中
    }
  }
}
</script>

<style scoped>
.maintenance-management {
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

/* タブナビゲーション */
.tab-navigation {
  display: flex;
  gap: 0.5rem;
  margin-bottom: 2rem;
  border-bottom: 1px solid #ecf0f1;
}

.tab-button {
  background: none;
  border: none;
  padding: 1rem 1.5rem;
  cursor: pointer;
  font-size: 1rem;
  color: #7f8c8d;
  border-bottom: 2px solid transparent;
  transition: all 0.3s;
}

.tab-button.active {
  color: #3498db;
  border-bottom-color: #3498db;
}

.tab-button:hover {
  color: #2980b9;
}

/* スケジュール管理 */
.schedule-controls {
  display: flex;
  gap: 1rem;
  margin-bottom: 2rem;
  flex-wrap: wrap;
}

.control-select {
  padding: 0.5rem 1rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 1rem;
}

.add-button {
  background: #27ae60;
  color: white;
  border: none;
  padding: 0.5rem 1rem;
  border-radius: 4px;
  cursor: pointer;
  font-size: 1rem;
  transition: background-color 0.3s;
}

.add-button:hover {
  background: #229954;
}

/* スケジュール項目 */
.schedule-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.schedule-item {
  background: white;
  padding: 1.5rem;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
  border-left: 4px solid #95a5a6;
}

.schedule-item.urgent {
  border-left-color: #e74c3c;
}

.schedule-item.high {
  border-left-color: #f39c12;
}

.schedule-item.medium {
  border-left-color: #3498db;
}

.schedule-item.low {
  border-left-color: #27ae60;
}

.schedule-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}

.schedule-title {
  font-size: 1.2rem;
  color: #2c3e50;
  margin: 0;
}

.schedule-date {
  color: #7f8c8d;
  font-weight: bold;
}

.schedule-meta {
  display: flex;
  gap: 0.5rem;
  margin-top: 0.5rem;
}

.priority-badge,
.status-badge {
  padding: 0.25rem 0.5rem;
  border-radius: 12px;
  font-size: 0.8rem;
  font-weight: bold;
}

.priority-badge.urgent {
  background: #fadbd8;
  color: #e74c3c;
}

.priority-badge.high {
  background: #fef2e0;
  color: #f39c12;
}

.priority-badge.medium {
  background: #d6eaf8;
  color: #3498db;
}

.priority-badge.low {
  background: #d5f4e6;
  color: #27ae60;
}

.status-badge.pending {
  background: #fef9e7;
  color: #f1c40f;
}

.status-badge.in-progress {
  background: #d6eaf8;
  color: #3498db;
}

.status-badge.completed {
  background: #d5f4e6;
  color: #27ae60;
}

.schedule-actions {
  display: flex;
  gap: 0.5rem;
  margin-top: 1rem;
  padding-top: 1rem;
  border-top: 1px solid #ecf0f1;
}

.action-button {
  padding: 0.5rem 1rem;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 0.9rem;
  transition: background-color 0.3s;
}

.action-button.start {
  background: #3498db;
  color: white;
}

.action-button.complete {
  background: #27ae60;
  color: white;
}

.action-button.edit {
  background: #95a5a6;
  color: white;
}

/* 統計 */
.stats-grid {
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
  text-align: center;
}

.stat-title {
  color: #7f8c8d;
  margin-bottom: 0.5rem;
}

.stat-number {
  font-size: 2rem;
  font-weight: bold;
  color: #2c3e50;
}

/* 設備状態 */
.equipment-status-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.equipment-status-item {
  background: white;
  padding: 1rem;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.equipment-health {
  padding: 0.25rem 0.5rem;
  border-radius: 12px;
  font-size: 0.8rem;
  font-weight: bold;
}

.equipment-health.good {
  background: #d5f4e6;
  color: #27ae60;
}

.equipment-health.warning {
  background: #fef2e0;
  color: #f39c12;
}

/* モーダル */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0,0,0,0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.modal-content {
  background: white;
  padding: 2rem;
  border-radius: 8px;
  max-width: 500px;
  width: 90%;
}

.modal-close {
  background: #95a5a6;
  color: white;
  border: none;
  padding: 0.5rem 1rem;
  border-radius: 4px;
  cursor: pointer;
  margin-top: 1rem;
}

@media (max-width: 768px) {
  .tab-navigation {
    flex-wrap: wrap;
  }
  
  .schedule-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 0.5rem;
  }
  
  .equipment-status-item {
    flex-direction: column;
    align-items: flex-start;
    gap: 0.5rem;
  }
}
</style>