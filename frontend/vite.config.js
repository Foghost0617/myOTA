import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

// https://vite.dev/config/
export default defineConfig({
  plugins: [vue()],
  resolve: {
    alias: {
      '@': '/src',  // 让 @ 符号指向 src 文件夹
    },
  },
  server: {
    proxy: {
      '/routes': {
        target: 'http://localhost:8003', // 后端的地址
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/routes/, ''),
      },
    },
  },
})
