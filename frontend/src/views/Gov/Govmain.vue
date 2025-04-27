<!-- 
<template>
  <div class="dashboard">
    
    <aside class="sidebar">
      <h2>文旅后台</h2>

      <div class="nav-group">
        <h3>运营情况</h3>
        <button @click="active = 'enrollments'">查看路线报名</button>
        <button @click="active = 'createGroupChat'">创建群聊</button>
        <button @click="active = 'groupList'">查看我的群聊</button> 
      </div>

      <div class="nav-group">
        <h3>游客投诉</h3>
        <button @click="active = 'complaints'">查看投诉</button>
      </div>
    </aside>

   
    <main class="content">
      <h1>待定内容，会根据左侧按钮展示不同组件？</h1>
      <div class="placeholder-box">
        <ComplaintList v-if="active === 'complaints'" />
        <RouteEnrollmentCount v-if="active === 'enrollments'" />
  
        <CreateGroupChat 
            v-if="active === 'createGroupChat'" 
            :creator-id="creatorId" 
            :creator-role="creatorRole" 
          />
        <GroupChatList v-if="active === 'groupList'" :user-id="userId" />

      </div>
    </main>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import ComplaintList from './ComplaintList.vue'; // 路径按实际调整
import RouteEnrollmentCount from './RouteEnrollmentCount.vue';
import CreateGroupChat from '@/components/CreateGroupChat.vue';
import GroupChatList from '@/components/GroupChatList.vue'

// 记录当前激活的模块
const active = ref('');

// 获取本地存储的 govId 和 role
const govId = parseInt(localStorage.getItem('gov_id') || '0');
const role = parseInt(localStorage.getItem('role') || '0');
const userId=parseInt(localStorage.getItem('user_id')||'0')

console.log('主页面当前角色id：', govId);
console.log('主页面当前角色role：', role);

const creatorId = userId;
const creatorRole = parseInt(localStorage.getItem('role') || '0');

console.log(creatorId,creatorRole,'传进群聊的id和role')
console.log(userId,'传进群聊的uerId')


</script> -->




<template>
  <div class="dashboard">
    <!-- 左侧导航栏 -->
    <aside class="sidebar">
      <h2>文旅后台</h2>

      <div class="nav-group">
        <h3>运营情况</h3>
        <button class="nav-button" @click="handleNavClick('enrollments')">查看路线报名</button>
        <button class="nav-button" @click="handleNavClick('createGroupChat')">创建群聊</button>
        <button class="nav-button" @click="handleNavClick('groupList')">查看我的群聊</button> 
      </div>

      <div class="nav-group">
        <h3>游客投诉</h3>
        <button class="nav-button" @click="handleNavClick('complaints')">查看投诉</button>
      </div>
    </aside>

    <!-- 右侧内容区 -->
    <main class="content">
      <h1>待定内容，会根据左侧按钮展示不同组件</h1>
      <div class="placeholder-box">
        <ComplaintList v-if="active === 'complaints'" />
        <RouteEnrollmentCount v-if="active === 'enrollments'" />
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
import ComplaintList from './ComplaintList.vue';
import RouteEnrollmentCount from './RouteEnrollmentCount.vue';
import CreateGroupChat from '@/components/CreateGroupChat.vue';
import GroupChatList from '@/components/GroupChatList.vue';
import GroupChat from '@/components/GroupChat.vue';

// 当前激活的模块
const active = ref('');
// 当前选择的群聊 ID
const activeChat = ref(null);

// 获取本地存储的 govId 和 role
const govId = parseInt(localStorage.getItem('gov_id') || '0');
const role = parseInt(localStorage.getItem('role') || '0');
const userId = parseInt(localStorage.getItem('user_id') || '0');

// const creatorId = userId;
const creatorRole = role;
console.log('目前角色role',role)
// 处理选中的群聊
const handleChatSelected = (groupId) => {
  activeChat.value = groupId;
  console.log('选择的群聊ID:', groupId);
  active.value = '';  // 取消激活群聊列表，显示群聊聊天
};

// 切换模块，清空群聊框
const handleNavClick = (module) => {
  console.log('当前选择模块:', module);
  active.value = module;
  activeChat.value = null; // 切换到其他模块时清空群聊框
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
