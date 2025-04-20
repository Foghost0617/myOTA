<!-- <template>
    <div class="dashboard">
      
      <aside class="sidebar">
        <h2>旅社后台</h2>
  
        <div class="nav-group">
          <h3>路线管理</h3>
          <button @click="active = 'add'" class="button">添加路线</button>
          <button @click="active = 'list'" class="button">查看路线</button>
        </div>
  
        <div class="nav-group">
          <h3>游客管理</h3>
          <button class="button">处理申请</button>
          <button class="button">游客列表</button>
        </div>
  
        <div class="nav-group">
          <h3>行程管理</h3>
          <button class="button">安排行程</button>
          <button class="button">查看行程</button>
        </div>
      </aside>
  
      
      <main class="content">
        <AddRoute v-if="active === 'add'" />
        
        <RouteList v-if="active === 'list'" @view-details="viewRouteDetails" />
        <RouteDetails v-if="active === 'details'" :routeId="routeId" />
      </main>
    </div>
  </template> -->
  
  <!-- <script setup>
  import { ref } from 'vue'
  import AddRoute from './AddRoute.vue'
  import RouteList from '@/components/RouteList.vue'
 import RouteDetails from '@/components/RouteDetails.vue'

  
  const active = ref('')  // 初始时不显示任何内容，等用户点击按钮
  const routeId = ref(null);  // 保存选中的 routeId
  // 切换到查看详情页面，并传递 routeId
  const viewRouteDetails = (id) => {
      console.log('从routelist接收到 routeId:', id);  // 检查传入的 routeId
      active.value = 'details';
      routeId.value = id;
  };

  </script> -->
  

  <template>
    <div class="dashboard">
      <!-- 左侧导航栏 -->
      <aside class="sidebar">
        <h2>旅社后台</h2>
  
        <div class="nav-group">
          <h3>路线管理</h3>
          <button @click="active = 'add'" class="button">添加路线</button>
          <button @click="active = 'list'" class="button">查看路线</button>
        </div>
  
        <div class="nav-group">
          <h3>游客管理</h3>
          <button class="button">处理申请</button>
          <button class="button">游客列表</button>
        </div>
  
        <div class="nav-group">
          <h3>行程管理</h3>
          <button @click="active = 'assignGuide'" class="button">指派导游</button> <!-- 新增指派导游按钮 -->
          <button class="button">查看行程</button>
        </div>
      </aside>
  
      <!-- 右侧内容区 -->
      <main class="content">
        <AddRoute v-if="active === 'add'" />
        <!-- 在查看路线时，传递 showDelete 控制删除按钮的显示 -->
        <RouteList v-if="active === 'list'" :showDelete="showDelete" @view-details="viewRouteDetails" />
        <RouteDetails v-if="active === 'details'" :routeId="routeId" /> <!-- 显式传递 routeId -->
        <AssignGuide v-if="active === 'assignGuide'" /> <!-- 新增指派导游组件 -->
      </main>
    </div>
  </template>
  
  <script setup>
  import { ref } from 'vue';
  import AddRoute from './AddRoute.vue';
  import RouteList from '@/components/RouteList.vue';
  import RouteDetails from '@/components/RouteDetails.vue';
  import AssignGuide from './AssignGuide.vue'; 

  const active = ref('');  // 初始时不显示任何内容，等用户点击按钮
  const routeId = ref(null);  // 保存选中的 routeId
  
  // 判定是否显示删除按钮（例如：管理员角色可以删除，游客不可删除）
  const showDelete = ref(false);  // 假设管理员可以删除，游客不可删除，可以根据角色修改这个值
  
  // 切换到查看详情页面，并传递 routeId
  const viewRouteDetails = (id) => {
    console.log('从routelist接收到 routeId:', id);  // 检查传入的 routeId
    active.value = 'details';
    routeId.value = id;
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

  /* 合并 add 和 nav-button 样式 */
  .button {
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

  .button:hover {
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


  

