import { createApp } from 'vue'
import { createRouter, createWebHistory } from 'vue-router'
import App from './App.vue'
import Home from './views/Home.vue'
import EquipmentStatus from './views/EquipmentStatus.vue'

const routes = [
  { path: '/', component: Home },
  { path: '/equipment-status', component: EquipmentStatus }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

const app = createApp(App)
app.use(router)
app.mount('#app')