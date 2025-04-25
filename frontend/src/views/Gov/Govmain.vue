
<template>
    <div class="dashboard"><!--水平布局-->
      <!-- 左侧导航栏 -->
      <aside class="sidebar">
        <h2>文旅后台</h2>
  
        <div class="nav-group">
          <h3>运营情况</h3>
          <button @click="active = 'enrollments'">查看路线报名</button>
        </div>
  
        <div class="nav-group">
          <h3>游客投诉</h3>
          <button @click="active = 'complaints'">查看投诉</button>

        </div>
  
      </aside>
  

      <!-- 右侧内容区 -->
      <main class="content">
        <h1>待定内容，会根据左侧按钮展示不同组件？</h1>
        <div class="placeholder-box">
          <ComplaintList v-if="active === 'complaints'" />
          <RouteEnrollmentCount v-if="active === 'enrollments'" /> <!-- 新增模块 -->
        </div>
      </main>
    </div>
  </template>
  
  <script setup>
  import { ref } from 'vue'
  import ComplaintList from './ComplaintList.vue'  // 路径按实际调整
  import RouteEnrollmentCount from './RouteEnrollmentCount.vue'
  const active = ref('')  // ⬅️ 这是关键，记录当前激活的模块
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