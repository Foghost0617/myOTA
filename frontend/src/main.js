import { createApp } from 'vue'
import './style.css'
import App from './App.vue'
import router from './router'

// createApp(App).mount('#app')
const app = createApp(App)
app.use(router)
app.mount('#app')

// import { createApp } from 'vue';
// import YourComponent from './views/Agency/AddRoute.vue';  // 你要查看的组件

// createApp(YourComponent).mount('#app');
