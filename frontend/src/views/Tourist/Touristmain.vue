<template>
  <div class="dashboard">
    <!-- 左侧导航栏 -->
    <aside class="sidebar">
      <h2>游客界面</h2>

      <div class="nav-group">
        <h3>旅游路线</h3>
        <button @click="active = 'list'" class="button">查看路线</button>
        <button class="nav-button" @click="active = 'route-signup'">我要报名</button>
      </div>

      <div class="nav-group">
        <h3>联系导游</h3>
        <button class="nav-button">私聊导游</button>
        <button class="nav-button">团内群聊</button>
      </div>

      <div class="nav-group">
        <h3>我要投诉</h3>
        <button class="nav-button">投诉</button>
      </div>
    </aside>

    <!-- 右侧内容区 -->
    <main class="content">
      <RouteSignup v-if="active === 'route-signup'" />
      
      <!-- 这里展示 AllRouteList 组件 -->
      <AllRouteList v-if="active === 'list'" @view-details="viewRouteDetails" />

      <!-- 展示 RouteDetails 组件，传递 routeId -->
      <!-- <RouteDetails v-if="active === 'details'" :routeId="routeId.value" /> -->
      <RouteDetails v-if="active === 'details' && routeId !== null" :routeId="routeId" />


    </main>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import RouteSignup from './RouteSignup.vue';
import AllRouteList from '@/components/AllRouteList.vue'; // 引入 AllRouteList 组件
import RouteDetails from '@/components/RouteDetails.vue'; // 引入 RouteDetails 组件
import { nextTick } from 'vue'

const active = ref('');  // 初始时不显示任何内容，等用户点击按钮
const routeId = ref(null);  // 保存选中的 routeId

// 监听 AllRouteList 组件的事件


const viewRouteDetails = (id) => {
  routeId.value = id
  nextTick(() => {
    active.value = 'details'
  })
}
</script>


  
  <style scoped>
  .dashboard {
    display: flex;
    height: 100vh;
    font-family: Arial, sans-serif;
  }
  
  /* 左侧侧边栏 */
  .sidebar {
    width: 220px;
    background-color: #2c3e50;
    color: white;
    padding: 20px;
  }
  
  .sidebar h2 {
    font-size: 20px;
    margin-bottom: 20px;
  }
  
  .nav-group {
    margin-bottom: 30px;
  }
  
  .nav-group h3 {
    font-size: 16px;
    margin-bottom: 10px;
  }
  
  .nav-button {
    display: block;
    width: 100%;
    padding: 10px;
    margin-bottom: 6px;
    background-color: #34495e;
    border: none;
    color: white;
    border-radius: 4px;
    cursor: pointer;
    text-align: left;
  }
  
  .nav-button:hover {
    background-color: #1abc9c;
  }
  
  /* 右侧内容区 */
  .content {
    flex: 1;
    padding: 30px;
    background-color: #ecf0f1;
  }
  
  .content h1 {
    font-size: 24px;
    color:#2c3e50;
    margin-bottom: 20px;
  }
  
  .placeholder-box {
    background-color: white;
    padding: 20px;
    border-radius: 6px;
    box-shadow: 0 0 10px rgba(0,0,0,0.1);
  }
  </style>