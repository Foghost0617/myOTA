<!-- <template>
  <div class="dashboard">
    
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
        <button @click="active = 'createGroupChat'">创建群聊</button>
        
      </div>
    </aside>

    
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
        <CreateGroupChat 
            v-if="active === 'createGroupChat'" 
            :creator-id="guideId" 
            :creator-role="creatorRole" 
          />

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
import CreateGroupChat from '@/components/CreateGroupChat.vue';

const active = ref('');  // 当前显示的内容
const routeId = ref(null);  // 当前选中的路线 ID
const showDelete = ref(false);  // 控制删除按钮

const selectedTouristId = ref(null);  // 当前选中的游客 ID

  const guideId = localStorage.getItem('guide_id'||'0');  // 导游的 ID
  const role = parseInt(localStorage.getItem('role') || '0');
  const userId = localStorage.getItem('user_id'||'0');  // 导游的 ID
  console.log('当前角色id：',guideId)
  console.log('当前角色role：',role)


  const creatorId = userId;
  const creatorRole = parseInt(localStorage.getItem('role') || '0');


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
</style> -->


<template>
  <div class="dashboard">
    <!-- 左侧导航栏 -->
    <aside class="sidebar">
      <h2>导游后台</h2>

      <div class="nav-group">
        <h3>个人信息</h3>
        <button class="nav-button" @click="handleNavClick('completeInfo')">完善个人信息</button>
      </div>

      <div class="nav-group">
        <h3>路线管理</h3>
        <button class="nav-button" @click="handleNavClick('list')">查看路线</button>
      </div>

      <div class="nav-group">
        <h3>游客管理</h3>
        <button class="nav-button" @click="handleNavClick('tourists')">查看游客</button>
        <button class="nav-button" @click="handleNavClick('createGroupChat')">创建群聊</button>
        <button class="nav-button" @click="handleNavClick('groupList')">查看我的群聊</button> 
      </div>
    </aside>

    <!-- 右侧内容区 -->
    <main class="content">
      <h1>待定内容，会根据左侧按钮展示不同组件</h1>
      <div class="placeholder-box">
        <CompleteGuideInfo v-if="active === 'completeInfo'" />
        <RouteList v-if="active === 'list'" :showDelete="showDelete" @view-details="viewRouteDetails" />
        <myTouristList v-if="active === 'tourists'" @start-chat="selectTouristForChat" />
        <RouteDetails v-if="active === 'details'" :routeId="routeId" />
        <ChatBox
          v-if="active === 'chatTourist'"
          :sender-role="2"
          :sender-id="guideId"
          :receiver-role="1"
          :receiver-id="selectedTouristId"
        />
        <GroupChatList 
            v-if="active === 'groupList'" 
            :user-id="userId" 
            @chat-selected="handleChatSelected" 
        />
        <CreateGroupChat
          v-if="active === 'createGroupChat'"
          :creator-id="userId"
          :creator-role="creatorRole"
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
import { ref } from 'vue'
import CompleteGuideInfo from './CompleteInfo.vue'
import RouteList from '@/components/RouteList.vue'
import RouteDetails from '@/components/RouteDetails.vue'
import myTouristList from './myTouristList.vue'
import ChatBox from '@/components/ChatBox.vue'
import GroupChatList from '@/components/GroupChatList.vue';
import CreateGroupChat from '@/components/CreateGroupChat.vue'
import GroupChat from '@/components/GroupChat.vue';

const active = ref('')        // 当前显示的内容
const routeId = ref(null)     // 当前选中的路线 ID
const showDelete = ref(false) // 是否显示删除按钮
const selectedTouristId = ref(null) // 当前选中的游客 ID
const activeChat = ref(null);  

const guideId = parseInt(localStorage.getItem('guide_id') || '0')   // 导游角色表id
const userId = parseInt(localStorage.getItem('user_id') || '0')     // 用户表id
const role=parseInt(localStorage.getItem('role')||'0')
// const creatorId = userId
const creatorRole = parseInt(localStorage.getItem('role') || '0')

console.log('当前角色id(guide_id)：', guideId)
console.log('当前用户id(user_id)：', userId)
console.log('当前角色role：', creatorRole)

// 切换模块，清空群聊框
// 切换模块，清空群聊框
const handleNavClick = (module) => {
  active.value = module
  routeId.value = null // 切换时清空选中的路线
  selectedTouristId.value = null // 清空选中的游客
  
  // 如果切换到群聊列表外的内容，则清空群聊
  if (module !== 'groupList') {
    activeChat.value = null
  }
}

// 查看路线详情
const viewRouteDetails = (id) => {
  active.value = 'details'
  routeId.value = id
}

// 选择游客进行聊天
const selectTouristForChat = (touristId) => {
  selectedTouristId.value = touristId
  active.value = 'chatTourist'
}

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

/* 按钮统一样式 */
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



