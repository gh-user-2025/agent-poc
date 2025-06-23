import { createRouter, createWebHistory } from 'vue-router'
import Dashboard from '../views/Dashboard.vue'
import EquipmentMonitoring from '../views/EquipmentMonitoring.vue'
import MaintenanceManagement from '../views/MaintenanceManagement.vue'
import DataAnalytics from '../views/DataAnalytics.vue'

// ルート定義
const routes = [
  {
    path: '/',
    name: 'Dashboard',
    component: Dashboard,
    meta: { title: 'ダッシュボード' }
  },
  {
    path: '/monitoring',
    name: 'EquipmentMonitoring',
    component: EquipmentMonitoring,
    meta: { title: '設備監視' }
  },
  {
    path: '/maintenance',
    name: 'MaintenanceManagement',
    component: MaintenanceManagement,
    meta: { title: 'メンテナンス管理' }
  },
  {
    path: '/analytics',
    name: 'DataAnalytics',
    component: DataAnalytics,
    meta: { title: 'データ分析' }
  }
]

// ルーター作成
const router = createRouter({
  history: createWebHistory(),
  routes
})

// ナビゲーションガード
router.beforeEach((to, from, next) => {
  // ページタイトルの設定
  document.title = `${to.meta.title} - 工場設備管理システム`
  next()
})

export default router