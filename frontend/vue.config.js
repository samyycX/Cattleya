const { defineConfig } = require('@vue/cli-service')
module.exports = defineConfig({
  transpileDependencies: true,
  assetsDir: 'static',
  publicPath: '/',
  // devServer: {
  //   historyApiFallback: { // 解决刷新404问题
  //     index: '/index.html'
  //   },
  //   proxy: {
  //     '/api': {
  //       target: 'http://127.0.0.1:8000',
  //       changeOrigin: true
  //     }
  //   }
  // }
})
