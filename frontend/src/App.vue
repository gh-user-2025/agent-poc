<template>
  <div id="app">
    <header class="header">
      <h1>工場設備管理システム</h1>
      <nav class="navigation">
        <router-link to="/" class="nav-link">ホーム</router-link>
        <router-link to="/equipment-status" class="nav-link">設備稼働状況</router-link>
      </nav>
    </header>
    
    <main class="main-content">
      <router-view></router-view>
    </main>
    
    <footer class="footer">
      <p>&copy; 2024 工場設備管理システム</p>
    </footer>
  </div>
</template>

<script>
export default {
  name: 'App'
}
</script>

<style>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

#app {
  font-family: Arial, sans-serif;
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

.header {
  background-color: #2c3e50;
  color: white;
  padding: 1rem 2rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.header h1 {
  font-size: 1.5rem;
}

.navigation {
  display: flex;
  gap: 1rem;
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

.main-content {
  flex: 1;
  padding: 2rem;
  background-color: #f8f9fa;
}

.footer {
  background-color: #34495e;
  color: white;
  padding: 1rem 2rem;
  text-align: center;
}
</style>