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
        <button class="nav-button" @click="active = 'tourists'">查看游客</button>
        
      </div>
    </aside>

    <!-- 右侧内容区 -->
    <main class="content">
      <CompleteGuideInfo v-if="active === 'completeInfo'" />
      <RouteList v-if="active === 'list'" :showDelete="showDelete" @view-details="viewRouteDetails" />
      <myTouristList v-if="active === 'tourists'" @start-chat="selectTouristForChat" />
      <RouteDetails v-if="active === 'details'" :routeId="routeId" />
      <ChatBox v-if="active === 'chatTourist'" 
        :sender-role="2" 
        :sender-id="guideId" 
        :receiver-role="1" 
        :receiver-id="selectedTouristId" />


    </main>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import CompleteGuideInfo from './CompleteInfo.vue'
import RouteList from '@/components/RouteList.vue'
import RouteDetails from '@/components/RouteDetails.vue'
import myTouristList from './myTouristList.vue'
import ChatBox from '@/components/ChatBox.vue'

const active = ref('');  // 当前显示的内容
const routeId = ref(null);  // 当前选中的路线 ID
const showDelete = ref(false);  // 控制删除按钮
const guideId = localStorage.getItem('guide_id');  // 导游的 ID
const selectedTouristId = ref(null);  // 当前选中的游客 ID

// 切换到查看路线详情页面
const viewRouteDetails = (id) => {
  active.value = 'details';
  routeId.value = id;
}

// 选择游客进行聊天
const selectTouristForChat = (touristId) => {
  selectedTouristId.value = touristId;
  active.value = 'chatTourist';  // 切换到聊天界面
}


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

