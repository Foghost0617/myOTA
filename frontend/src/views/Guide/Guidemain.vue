<template>
  <div class="dashboard">
    <!-- 左侧导航栏 -->
    <aside class="sidebar">
      <h2>导游后台</h2>

      <div class="nav-group">
        <h3>个人信息</h3>
        <button class="nav-button" @click="active = 'completeInfo'">
          完善个人信息
        </button>
      </div>

      <div class="nav-group">
        <h3>路线管理</h3>
        <button @click="active = 'list'" class="button">查看路线</button>
      </div>

      <div class="nav-group">
        <h3>游客管理</h3>
        <button class="nav-button">联系游客</button>
        <button class="nav-button">群聊管理</button>
      </div>
    </aside>

    <!-- 右侧内容区 -->
    <main class="content">
      <CompleteGuideInfo v-if="active === 'completeInfo'" />
      <RouteList v-if="active === 'list'" :showDelete="showDelete" @view-details="viewRouteDetails" />
      <RouteDetails v-if="active === 'details'" :routeId="routeId" /> <!-- 显式传递 routeId -->
    </main>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import CompleteGuideInfo from './CompleteInfo.vue'
import RouteList from '@/components/RouteList.vue';  // 引入 RouteList 组件
import RouteDetails from '@/components/RouteDetails.vue';  // 引入 RouteDetails 组件

const active = ref('');  // 默认不显示任何内容
const routeId = ref(null);  // 保存选中的 routeId

// 判定是否显示删除按钮（假设导游不能删除）
const showDelete = ref(false);  // 控制删除按钮的显示

// 切换到查看详情页面，并传递 routeId
const viewRouteDetails = (id) => {
  console.log('从routelist接收到 routeId:', id);  // 检查传入的 routeId
  active.value = 'details';  // 切换到详情页面
  routeId.value = id;  // 设置选中的 routeId
};
</script>


  
<style scoped>
  * {
    box-sizing: border-box;
  }

  .dashboard {
    display: flex;
    height: 100vh;
    font-family: Arial, sans-serif;
  }

  /* 左侧侧边栏 */
  .sidebar {
    width: 20%; /* 左侧占 20% */
    background-color: #2c3e50;
    color: white;
    padding: 20px;
    box-sizing: border-box; /* 确保 padding 不影响宽度计算 */
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

  /* 统一按钮样式 */
  .button, .nav-button {
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

  .button:hover, .nav-button:hover {
    background-color: #1abc9c;
  }

  /* 右侧内容区 */
  .content {
    flex: 1; /* 右侧占剩余空间，即 80% */
    padding: 30px;
    background-color: #ecf0f1;
    box-sizing: border-box; /* 确保 padding 不影响宽度计算 */
  }

  .content h1 {
    font-size: 24px;
    color: #2c3e50;
    margin-bottom: 20px;
  }

  .placeholder-box {
    background-color: white;
    padding: 20px;
    border-radius: 6px;
    box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
  }
</style>

