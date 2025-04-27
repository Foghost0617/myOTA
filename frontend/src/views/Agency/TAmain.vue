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
  



  <!-- 最新可用 -->
  <!-- <template>
    <div class="dashboard">
  
      <aside class="sidebar">
        <h2>旅社后台</h2>
  
        <div class="nav-group">
          <h3>路线管理</h3>
          <button @click="active = 'add'" class="button">添加路线</button>
          <button @click="active = 'list'" class="button">查看路线</button>
          <button @click="active = 'uploadImage'" class="button">添加景点图像</button>
        </div>
  
        <div class="nav-group">
          <h3>游客管理</h3>
          <button @click="active = 'createGroupChat'">创建群聊</button>
          
          <button class="button" @click="active = 'handleApplications'">处理申请</button>
          <button class="button">游客列表</button>
        </div>
  
        <div class="nav-group">
          <h3>行程管理</h3>
          <button @click="active = 'assignGuide'" class="button">指派导游</button> 
          <button class="button">查看行程</button>
        </div>
      </aside>
  
     
      <main class="content">
        <AddRoute v-if="active === 'add'" />
        
        <RouteList v-if="active === 'list'" :showDelete="showDelete" @view-details="viewRouteDetails" />
        <RouteDetails v-if="active === 'details'" :routeId="routeId" />
        <AssignGuide v-if="active === 'assignGuide'" />
        <HandleApplications v-if="active === 'handleApplications'" />
        <UploadSpotImage v-if="active === 'uploadImage'" />
        <CreateGroupChat 
            v-if="active === 'createGroupChat'" 
            :creator-id="agencyId" 
            :creator-role="creatorRole" 
          />
      </main>
    </div>
  </template>
  
  <script setup>
  import { ref } from 'vue';
  import AddRoute from './AddRoute.vue';
  import RouteList from '@/components/RouteList.vue';
  import RouteDetails from '@/components/RouteDetails.vue';
  import AssignGuide from './AssignGuide.vue'; 
  import HandleApplications from './HandleApplications.vue'
  import  UploadSpotImage from './UploadSpotImage.vue'
  import CreateGroupChat from '@/components/CreateGroupChat.vue';



  const active = ref('');  // 初始时不显示任何内容，等用户点击按钮
  const routeId = ref(null);  // 保存选中的 routeId
  
  // 判定是否显示删除按钮（例如：管理员角色可以删除，游客不可删除）
  const showDelete = ref(true);  // 假设管理员可以删除，游客不可删除，可以根据角色修改这个值
  
  // 切换到查看详情页面，并传递 routeId
  const viewRouteDetails = (id) => {
    console.log('从routelist接收到 routeId:', id);  // 检查传入的 routeId
    active.value = 'details';
    routeId.value = id;
  };
  const agencyId= parseInt(localStorage.getItem('agency_id') || '0');
  const role = parseInt(localStorage.getItem('role') || '0');
  console.log('当前角色id：',agencyId)
  console.log('当前角色role：',role)
  const userId = localStorage.getItem('user_id'||'0');  // 导游的 ID
  const creatorId = userId
  const creatorRole = parseInt(localStorage.getItem('role') || '0');


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
</style> -->


  

<template>
  <div class="dashboard">
    <!-- 左侧侧边栏 -->
    <aside class="sidebar">
      <h2>旅社后台</h2>

      <div class="nav-group">
        <h3>路线管理</h3>
        <button @click="() => handleNavClick('add')" class="nav-button">添加路线</button>
        <button @click="() => handleNavClick('list')" class="nav-button">查看路线</button>
        <button @click="() => handleNavClick('uploadImage')" class="nav-button">添加景点图像</button>
        <button @click="() => handleNavClick('groupList')" class="nav-button">查看我的群聊</button> 
      </div>

      <div class="nav-group">
        <h3>游客管理</h3>
        <button @click="() => handleNavClick('createGroupChat')" class="nav-button">创建群聊</button>
        <button @click="() => handleNavClick('handleApplications')" class="nav-button">处理申请</button>
        <button class="nav-button">游客列表</button>
      </div>

      <div class="nav-group">
        <h3>行程管理</h3>
        <button @click="() => handleNavClick('assignGuide')" class="nav-button">指派导游</button>
        <button class="nav-button">查看行程</button>
      </div>
    </aside>

    <!-- 右侧内容区，增加滑动处理 -->
    <main class="content">
      <div class="placeholder-box scrollable">
        <AddRoute v-if="active === 'add'" />
        <RouteList v-if="active === 'list'" :showDelete="showDelete" @view-details="viewRouteDetails" />
        <RouteDetails v-if="active === 'details'" :routeId="routeId" />
        <AssignGuide v-if="active === 'assignGuide'" />
        <HandleApplications v-if="active === 'handleApplications'" />
        <UploadSpotImage v-if="active === 'uploadImage'" />
        <CreateGroupChat
          v-if="active === 'createGroupChat'"
          :creator-id="userId"
          :creator-role="creatorRole"
        />
        <GroupChatList 
            v-if="active === 'groupList'" 
            :user-id="userId" 
            @chat-selected="handleChatSelected" 
        />
        <GroupChat
            v-if="activeChat" 
            :group-id="activeChat" 
            :user-id="userId"
            :role="role"
        />
      </div>
    </main>
  </div>
</template>
<script setup>
import { ref } from 'vue';
import AddRoute from './AddRoute.vue';
import RouteList from '@/components/RouteList.vue';
import RouteDetails from '@/components/RouteDetails.vue';
import AssignGuide from './AssignGuide.vue';
import HandleApplications from './HandleApplications.vue';
import UploadSpotImage from './UploadSpotImage.vue';
import CreateGroupChat from '@/components/CreateGroupChat.vue';
import GroupChat from '@/components/GroupChat.vue';
import GroupChatList from '@/components/GroupChatList.vue';

const active = ref('');
const routeId = ref(null);

const agencyId = parseInt(localStorage.getItem('agency_id') || '0');
const role = parseInt(localStorage.getItem('role') || '0');
const userId = parseInt(localStorage.getItem('user_id') || '0');
const creatorId = userId;
const creatorRole = role;

const showDelete = ref(true);
// 当前选择的群聊 ID
const activeChat = ref(null);

// 点击切换功能模块
const handleNavClick = (module) => {
  console.log('当前选择模块:', module);
  active.value = module;
  routeId.value = null; // 切换时清空选中的路线
  activeChat.value = null; // 切换到其他模块时清空群聊框
};

// 查看路线详情
const viewRouteDetails = (id) => {
  console.log('从 RouteList 接收到 routeId:', id);
  active.value = 'details';
  routeId.value = id;
};


// 处理选中的群聊
const handleChatSelected = (groupId) => {
  activeChat.value = groupId;
  active.value = '';  // 取消激活群聊列表，显示群聊聊天
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
  width: 220px;
  background-color: #2c3e50;  /* 深灰色 */
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

/* 按钮统一样式 */
.nav-button {
  display: block;
  width: 100%;
  padding: 10px;
  margin-bottom: 6px;
  background-color: #34495e;  /* 深灰色 */
  border: none;
  color: white;
  border-radius: 4px;
  cursor: pointer;
  text-align: left;
}

.nav-button:hover {
  background-color: #1abc9c;  /* 绿色 */
}

/* 右侧内容区 */
.content {
  flex: 1;
  padding: 30px;
  background-color: #ecf0f1;  /* 浅灰色 */
}

.content h1 {
  font-size: 24px;
  color: #2c3e50;  /* 深灰色 */
  margin-bottom: 20px;
}

.placeholder-box {
  background-color: white;
  padding: 20px;
  border-radius: 6px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
}

.scrollable {
  max-height: calc(100vh - 60px); /* 限制最大高度，避免内容过多 */
  overflow-y: auto;
}
</style>


