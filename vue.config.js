const { defineConfig } = require('@vue/cli-service')

module.exports = defineConfig({
  transpileDependencies: true,
  
  // 開発サーバー設定
  devServer: {
    port: 8080,
    open: true,
    host: '0.0.0.0',
    allowedHosts: 'all'
  },
  
  // ビルド設定
  publicPath: process.env.NODE_ENV === 'production' ? '/factory-management/' : '/',
  
  // PWA設定（将来的な拡張用）
  pwa: {
    name: '工場設備管理システム',
    themeColor: '#2c3e50',
    msTileColor: '#2c3e50'
  }
})