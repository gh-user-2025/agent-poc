<!-- 工場設備管理アプリのメインコンポーネント -->
<template>
  <div id="app">
    <!-- ヘッダーナビゲーション -->
    <header class="app-header">
      <div class="container">
        <h1 class="app-title">🏭 工場設備管理システム</h1>
        <nav class="app-nav">
          <router-link to="/" class="nav-link">ダッシュボード</router-link>
          <router-link to="/monitoring" class="nav-link">設備監視</router-link>
          <router-link to="/maintenance" class="nav-link">メンテナンス管理</router-link>
          <router-link to="/analytics" class="nav-link">データ分析</router-link>
        </nav>
      </div>
    </header>

    <!-- メインコンテンツ -->
    <main class="app-main">
      <div class="container">
        <router-view></router-view>
      </div>
    </main>

    <!-- フッター -->
    <footer class="app-footer">
      <div class="container">
        <p>&copy; 2024 工場設備管理システム - Azure クラウド対応プロトタイプ</p>
      </div>
    </footer>
  </div>
</template>

<script>
export default {
  name: 'App',
  data() {
    return {
      // アプリケーションの基本情報
      appInfo: {
        version: '1.0.0',
        lastUpdate: new Date().toLocaleDateString('ja-JP')
      }
    }
  }
}
</script>

<style>
/* グローバルスタイル */
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  background-color: #f5f5f5;
  color: #333;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 20px;
}

/* ヘッダースタイル */
.app-header {
  background-color: #2c3e50;
  color: white;
  padding: 1rem 0;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.app-header .container {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.app-title {
  font-size: 1.8rem;
  font-weight: bold;
}

.app-nav {
  display: flex;
  gap: 2rem;
}

.nav-link {
  color: white;
  text-decoration: none;
  padding: 0.5rem 1rem;
  border-radius: 4px;
  transition: background-color 0.3s;
}

.nav-link:hover,
.nav-link.router-link-active {
  background-color: #34495e;
}

/* メインコンテンツスタイル */
.app-main {
  min-height: calc(100vh - 140px);
  padding: 2rem 0;
}

/* フッタースタイル */
.app-footer {
  background-color: #34495e;
  color: white;
  text-align: center;
  padding: 1rem 0;
  margin-top: auto;
}

/* レスポンシブデザイン */
@media (max-width: 768px) {
  .app-header .container {
    flex-direction: column;
    gap: 1rem;
  }
  
  .app-nav {
    flex-wrap: wrap;
    justify-content: center;
    gap: 1rem;
  }
  
  .app-title {
    font-size: 1.5rem;
  }
}
</style>