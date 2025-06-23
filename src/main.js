import { createApp } from 'vue'
import App from './App.vue'
import router from './router'

// Vue アプリケーションの作成と設定
const app = createApp(App)

// ルーターの使用
app.use(router)

// アプリケーションをマウント
app.mount('#app')