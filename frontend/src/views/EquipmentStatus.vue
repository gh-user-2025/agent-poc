<template>
  <div class="equipment-status">
    <h1>設備稼働状況</h1>
    
    <div class="filters">
      <div class="filter-group">
        <label for="location-filter">場所フィルター:</label>
        <select id="location-filter" v-model="selectedLocation" @change="filterEquipment">
          <option value="">すべて</option>
          <option value="ライン A">ライン A</option>
          <option value="ライン B">ライン B</option>
          <option value="ライン C">ライン C</option>
          <option value="共通設備">共通設備</option>
        </select>
      </div>
      <div class="filter-group">
        <label for="status-filter">状態フィルター:</label>
        <select id="status-filter" v-model="selectedStatus" @change="filterEquipment">
          <option value="">すべて</option>
          <option value="running">稼働中</option>
          <option value="idle">待機中</option>
          <option value="maintenance">メンテナンス中</option>
          <option value="error">エラー</option>
        </select>
      </div>
      <button class="refresh-btn" @click="refreshData" :disabled="isLoading">
        🔄 {{ isLoading ? '更新中...' : '更新' }}
      </button>
    </div>

    <div class="equipment-grid">
      <div 
        v-for="equipment in filteredEquipment" 
        :key="equipment.id"
        class="equipment-card"
        :class="equipment.status"
        @click="selectEquipment(equipment)"
      >
        <div class="equipment-header">
          <h3>{{ equipment.name }}</h3>
          <div class="status-badge" :class="equipment.status">
            {{ getStatusText(equipment.status) }}
          </div>
        </div>
        
        <div class="equipment-info">
          <p><strong>場所:</strong> {{ equipment.location }}</p>
          <p><strong>タイプ:</strong> {{ equipment.type }}</p>
          <p><strong>稼働時間:</strong> {{ equipment.operatingHours }}h</p>
          <p><strong>最終点検:</strong> {{ equipment.lastMaintenance }}</p>
        </div>
        
        <div class="sensor-data">
          <div class="sensor-item">
            <span>温度</span>
            <span class="sensor-value" :class="{ warning: equipment.temperature > 80 }">
              {{ equipment.temperature }}°C
            </span>
          </div>
          <div class="sensor-item">
            <span>圧力</span>
            <span class="sensor-value" :class="{ warning: equipment.pressure > 95 }">
              {{ equipment.pressure }}%
            </span>
          </div>
          <div class="sensor-item">
            <span>振動</span>
            <span class="sensor-value" :class="{ warning: equipment.vibration > 7 }">
              {{ equipment.vibration }}mm/s
            </span>
          </div>
        </div>
      </div>
    </div>

    <!-- 設備詳細モーダル -->
    <div v-if="selectedEquipmentDetail" class="modal-overlay" @click="closeModal">
      <div class="modal-content" @click.stop>
        <div class="modal-header">
          <h2>{{ selectedEquipmentDetail.name }} - 詳細情報</h2>
          <button class="close-btn" @click="closeModal">×</button>
        </div>
        
        <div class="modal-body">
          <div class="detail-section">
            <h3>基本情報</h3>
            <div class="detail-grid">
              <div><strong>設備ID:</strong> {{ selectedEquipmentDetail.id }}</div>
              <div><strong>名前:</strong> {{ selectedEquipmentDetail.name }}</div>
              <div><strong>タイプ:</strong> {{ selectedEquipmentDetail.type }}</div>
              <div><strong>場所:</strong> {{ selectedEquipmentDetail.location }}</div>
              <div><strong>状態:</strong> {{ getStatusText(selectedEquipmentDetail.status) }}</div>
              <div><strong>稼働時間:</strong> {{ selectedEquipmentDetail.operatingHours }}h</div>
            </div>
          </div>
          
          <div class="detail-section">
            <h3>センサーデータ</h3>
            <div class="sensor-details">
              <div class="sensor-detail-item">
                <span>温度</span>
                <span class="value">{{ selectedEquipmentDetail.temperature }}°C</span>
                <span class="threshold">(閾値: 85°C)</span>
              </div>
              <div class="sensor-detail-item">
                <span>圧力</span>
                <span class="value">{{ selectedEquipmentDetail.pressure }}%</span>
                <span class="threshold">(閾値: 95%)</span>
              </div>
              <div class="sensor-detail-item">
                <span>振動</span>
                <span class="value">{{ selectedEquipmentDetail.vibration }}mm/s</span>
                <span class="threshold">(閾値: 8mm/s)</span>
              </div>
            </div>
          </div>
          
          <div class="detail-section">
            <h3>履歴</h3>
            <div class="history-list">
              <div v-for="record in selectedEquipmentDetail.history" :key="record.id" class="history-item">
                <span class="history-time">{{ record.timestamp }}</span>
                <span class="history-event">{{ record.event }}</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import ApiService from '@/services/apiService'

export default {
  name: 'EquipmentStatus',
  data() {
    return {
      allEquipment: [],
      filteredEquipment: [],
      selectedLocation: '',
      selectedStatus: '',
      selectedEquipmentDetail: null,
      isLoading: false,
      useApiData: true // APIデータを使用するかどうかのフラグ
    }
  },
  methods: {
    async loadDataFromApi() {
      this.isLoading = true
      try {
        // 設備一覧を取得
        const response = await ApiService.getEquipment()
        this.allEquipment = response.equipment
        this.filteredEquipment = [...this.allEquipment]
        
        console.log('APIから設備データを取得しました')
      } catch (error) {
        console.error('APIからの設備データ取得に失敗しました:', error)
        // APIが利用できない場合はサンプルデータを使用
        this.loadSampleData()
        this.useApiData = false
      } finally {
        this.isLoading = false
      }
    },
    loadSampleData() {
      // サンプル設備データ（フォールバック用）
      this.allEquipment = [
        {
          id: 1,
          name: '射出成形機-1',
          type: '射出成形機',
          status: 'running',
          location: 'ライン A',
          operatingHours: 2450,
          lastMaintenance: '2024-01-15',
          temperature: 75,
          pressure: 82,
          vibration: 4.2,
          history: [
            { id: 1, timestamp: '2024-01-20 10:30', event: '稼働開始' },
            { id: 2, timestamp: '2024-01-15 15:00', event: '定期メンテナンス完了' }
          ]
        },
        {
          id: 2,
          name: '射出成形機-2',
          type: '射出成形機',
          status: 'running',
          location: 'ライン A',
          operatingHours: 2380,
          lastMaintenance: '2024-01-10',
          temperature: 78,
          pressure: 85,
          vibration: 3.8,
          history: [
            { id: 1, timestamp: '2024-01-20 09:15', event: '稼働開始' },
            { id: 2, timestamp: '2024-01-10 14:30', event: '定期メンテナンス完了' }
          ]
        },
        {
          id: 3,
          name: '組立ロボット-1',
          type: '組立ロボット',
          status: 'idle',
          location: 'ライン B',
          operatingHours: 1680,
          lastMaintenance: '2024-01-05',
          temperature: 45,
          pressure: 65,
          vibration: 2.1,
          history: [
            { id: 1, timestamp: '2024-01-20 11:00', event: '待機状態' },
            { id: 2, timestamp: '2024-01-05 16:45', event: '定期メンテナンス完了' }
          ]
        },
        {
          id: 4,
          name: '組立ロボット-2',
          type: '組立ロボット',
          status: 'running',
          location: 'ライン B',
          operatingHours: 1720,
          lastMaintenance: '2024-01-08',
          temperature: 52,
          pressure: 72,
          vibration: 2.8,
          history: [
            { id: 1, timestamp: '2024-01-20 08:30', event: '稼働開始' },
            { id: 2, timestamp: '2024-01-08 13:20', event: '定期メンテナンス完了' }
          ]
        },
        {
          id: 5,
          name: '検査装置-1',
          type: '検査装置',
          status: 'maintenance',
          location: 'ライン C',
          operatingHours: 3200,
          lastMaintenance: '2024-01-20',
          temperature: 35,
          pressure: 0,
          vibration: 0,
          history: [
            { id: 1, timestamp: '2024-01-20 13:00', event: 'メンテナンス開始' },
            { id: 2, timestamp: '2024-01-18 17:30', event: '稼働停止' }
          ]
        },
        {
          id: 6,
          name: 'コンプレッサー-1',
          type: 'コンプレッサー',
          status: 'running',
          location: '共通設備',
          operatingHours: 5680,
          lastMaintenance: '2023-12-20',
          temperature: 68,
          pressure: 88,
          vibration: 5.2,
          history: [
            { id: 1, timestamp: '2024-01-01 00:00', event: '連続稼働中' },
            { id: 2, timestamp: '2023-12-20 10:00', event: '定期メンテナンス完了' }
          ]
        },
        {
          id: 7,
          name: 'コンプレッサー-2',
          type: 'コンプレッサー',
          status: 'error',
          location: '共通設備',
          operatingHours: 5420,
          lastMaintenance: '2023-12-15',
          temperature: 95,
          pressure: 102,
          vibration: 8.5,
          history: [
            { id: 1, timestamp: '2024-01-20 14:25', event: '温度異常検出' },
            { id: 2, timestamp: '2024-01-20 14:20', event: 'アラート発生' }
          ]
        }
      ];
      
      this.filteredEquipment = [...this.allEquipment];
    },
    async filterEquipment() {
      if (this.useApiData) {
        // APIでフィルタリング
        try {
          const filters = {}
          if (this.selectedLocation) filters.location = this.selectedLocation
          if (this.selectedStatus) filters.status = this.selectedStatus
          
          const response = await ApiService.getEquipment(filters)
          this.filteredEquipment = response.equipment
        } catch (error) {
          console.error('フィルタリング中にエラーが発生しました:', error)
          // ローカルフィルタリングにフォールバック
          this.localFilterEquipment()
        }
      } else {
        // ローカルフィルタリング
        this.localFilterEquipment()
      }
    },
    localFilterEquipment() {
      this.filteredEquipment = this.allEquipment.filter(equipment => {
        const locationMatch = !this.selectedLocation || equipment.location === this.selectedLocation;
        const statusMatch = !this.selectedStatus || equipment.status === this.selectedStatus;
        return locationMatch && statusMatch;
      });
    },
    getStatusText(status) {
      const statusMap = {
        'running': '稼働中',
        'idle': '待機中',
        'maintenance': 'メンテナンス中',
        'error': 'エラー'
      };
      return statusMap[status] || '不明';
    },
    async selectEquipment(equipment) {
      if (this.useApiData) {
        try {
          // APIから最新の詳細情報を取得
          const response = await ApiService.getEquipmentDetail(equipment.id)
          this.selectedEquipmentDetail = response.equipment
        } catch (error) {
          console.error('設備詳細取得に失敗しました:', error)
          // フォールバックとして渡された設備情報を使用
          this.selectedEquipmentDetail = equipment
        }
      } else {
        this.selectedEquipmentDetail = equipment
      }
    },
    closeModal() {
      this.selectedEquipmentDetail = null;
    },
    async refreshData() {
      if (this.useApiData) {
        await this.loadDataFromApi()
        // フィルターが設定されている場合は再適用
        if (this.selectedLocation || this.selectedStatus) {
          await this.filterEquipment()
        }
        console.log('設備データを更新しました')
      } else {
        this.loadSampleData()
        this.filterEquipment()
        console.log('サンプルデータを更新しました')
      }
    }
  },
  async mounted() {
    // 初期データ読み込み
    if (this.useApiData) {
      await this.loadDataFromApi()
    } else {
      this.loadSampleData()
    }
  }
}
</script>

<style scoped>
.equipment-status {
  max-width: 1400px;
  margin: 0 auto;
}

.filters {
  background: white;
  padding: 1.5rem;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
  margin-bottom: 2rem;
  display: flex;
  gap: 2rem;
  align-items: center;
  flex-wrap: wrap;
}

.filter-group {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.filter-group label {
  font-weight: bold;
  color: #2c3e50;
}

.filter-group select {
  padding: 0.5rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 1rem;
}

.refresh-btn {
  padding: 0.75rem 1.5rem;
  background-color: #3498db;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 1rem;
  transition: background-color 0.3s;
}

.refresh-btn:hover {
  background-color: #2980b9;
}

.equipment-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
  gap: 1.5rem;
}

.equipment-card {
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
  padding: 1.5rem;
  cursor: pointer;
  transition: transform 0.2s, box-shadow 0.2s;
  border-left: 4px solid #3498db;
}

.equipment-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(0,0,0,0.15);
}

.equipment-card.running {
  border-left-color: #27ae60;
}

.equipment-card.idle {
  border-left-color: #f39c12;
}

.equipment-card.maintenance {
  border-left-color: #e74c3c;
}

.equipment-card.error {
  border-left-color: #c0392b;
}

.equipment-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}

.equipment-header h3 {
  margin: 0;
  color: #2c3e50;
}

.status-badge {
  padding: 0.25rem 0.75rem;
  border-radius: 12px;
  font-size: 0.8rem;
  font-weight: bold;
  color: white;
}

.status-badge.running {
  background-color: #27ae60;
}

.status-badge.idle {
  background-color: #f39c12;
}

.status-badge.maintenance {
  background-color: #e74c3c;
}

.status-badge.error {
  background-color: #c0392b;
}

.equipment-info {
  margin-bottom: 1rem;
}

.equipment-info p {
  margin: 0.25rem 0;
  color: #666;
}

.sensor-data {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.sensor-item {
  display: flex;
  justify-content: space-between;
  padding: 0.5rem;
  background-color: #f8f9fa;
  border-radius: 4px;
}

.sensor-value {
  font-weight: bold;
  color: #27ae60;
}

.sensor-value.warning {
  color: #e74c3c;
}

/* モーダルスタイル */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.modal-content {
  background: white;
  border-radius: 8px;
  width: 90%;
  max-width: 800px;
  max-height: 90vh;
  overflow-y: auto;
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.5rem;
  border-bottom: 1px solid #eee;
}

.modal-header h2 {
  margin: 0;
  color: #2c3e50;
}

.close-btn {
  background: none;
  border: none;
  font-size: 1.5rem;
  cursor: pointer;
  color: #999;
}

.close-btn:hover {
  color: #333;
}

.modal-body {
  padding: 1.5rem;
}

.detail-section {
  margin-bottom: 2rem;
}

.detail-section h3 {
  margin-bottom: 1rem;
  color: #2c3e50;
  border-bottom: 2px solid #3498db;
  padding-bottom: 0.5rem;
}

.detail-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1rem;
}

.detail-grid div {
  padding: 0.5rem;
  background-color: #f8f9fa;
  border-radius: 4px;
}

.sensor-details {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.sensor-detail-item {
  display: grid;
  grid-template-columns: 1fr auto auto;
  gap: 1rem;
  padding: 1rem;
  background-color: #f8f9fa;
  border-radius: 4px;
}

.sensor-detail-item .value {
  font-weight: bold;
  color: #2c3e50;
}

.sensor-detail-item .threshold {
  color: #666;
  font-size: 0.9rem;
}

.history-list {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.history-item {
  display: grid;
  grid-template-columns: auto 1fr;
  gap: 1rem;
  padding: 0.75rem;
  background-color: #f8f9fa;
  border-radius: 4px;
}

.history-time {
  color: #666;
  font-size: 0.9rem;
}

.history-event {
  font-weight: bold;
}

@media (max-width: 768px) {
  .filters {
    flex-direction: column;
    align-items: stretch;
  }
  
  .equipment-grid {
    grid-template-columns: 1fr;
  }
  
  .modal-content {
    width: 95%;
    margin: 1rem;
  }
  
  .detail-grid {
    grid-template-columns: 1fr;
  }
  
  .sensor-detail-item {
    grid-template-columns: 1fr;
    text-align: center;
  }
  
  .history-item {
    grid-template-columns: 1fr;
    text-align: center;
  }
}
</style>