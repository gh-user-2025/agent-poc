/**
 * API サービス
 * バックエンドAPIとの通信を担当するサービスクラス
 */

const API_BASE_URL = process.env.VUE_APP_API_URL || 'http://localhost:5000/api'

class ApiService {
  
  /**
   * HTTPリクエストの共通処理
   */
  async request(url, options = {}) {
    const config = {
      headers: {
        'Content-Type': 'application/json',
        ...options.headers
      },
      ...options
    }

    try {
      const response = await fetch(`${API_BASE_URL}${url}`, config)
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`)
      }
      
      return await response.json()
    } catch (error) {
      console.error('API request failed:', error)
      throw error
    }
  }

  /**
   * ヘルスチェック
   */
  async healthCheck() {
    return this.request('/health')
  }

  /**
   * 設備一覧取得
   */
  async getEquipment(filters = {}) {
    const params = new URLSearchParams()
    
    if (filters.location) {
      params.append('location', filters.location)
    }
    if (filters.status) {
      params.append('status', filters.status)
    }
    
    const queryString = params.toString()
    const url = queryString ? `/equipment?${queryString}` : '/equipment'
    
    return this.request(url)
  }

  /**
   * 設備詳細取得
   */
  async getEquipmentDetail(equipmentId) {
    return this.request(`/equipment/${equipmentId}`)
  }

  /**
   * 設備サマリー取得
   */
  async getEquipmentSummary() {
    return this.request('/equipment/summary')
  }

  /**
   * アラート一覧取得
   */
  async getAlerts(filters = {}) {
    const params = new URLSearchParams()
    
    if (filters.severity) {
      params.append('severity', filters.severity)
    }
    if (filters.status) {
      params.append('status', filters.status)
    }
    if (filters.limit) {
      params.append('limit', filters.limit)
    }
    
    const queryString = params.toString()
    const url = queryString ? `/alerts?${queryString}` : '/alerts'
    
    return this.request(url)
  }

  /**
   * センサーデータ取得
   */
  async getSensorData(equipmentId) {
    return this.request(`/sensor-data/${equipmentId}`)
  }

  /**
   * IoTデータ処理（Azure Functionsへのリクエスト）
   */
  async processIoTData(iotData) {
    // Azure Functions のエンドポイントを使用
    const functionsUrl = process.env.VUE_APP_FUNCTIONS_URL || 'http://localhost:7071'
    
    try {
      const response = await fetch(`${functionsUrl}/api/iot-data-processor`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(iotData)
      })
      
      if (!response.ok) {
        throw new Error(`Azure Functions error! status: ${response.status}`)
      }
      
      return await response.json()
    } catch (error) {
      console.error('IoT data processing failed:', error)
      throw error
    }
  }

  /**
   * データ変換処理（Azure Functionsへのリクエスト）
   */
  async transformData(transformRequest) {
    const functionsUrl = process.env.VUE_APP_FUNCTIONS_URL || 'http://localhost:7071'
    
    try {
      const response = await fetch(`${functionsUrl}/api/data-transformer`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(transformRequest)
      })
      
      if (!response.ok) {
        throw new Error(`Data transformation error! status: ${response.status}`)
      }
      
      return await response.json()
    } catch (error) {
      console.error('Data transformation failed:', error)
      throw error
    }
  }
}

// シングルトンインスタンスをエクスポート
export default new ApiService()