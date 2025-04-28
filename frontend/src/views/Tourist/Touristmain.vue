<!-- <template>
  <div class="dashboard">
    
    <aside class="sidebar">
      <h2>游客界面</h2>

      <div class="nav-group">
        <h3>旅游路线</h3>
        <button @click="active = 'list'" class="button">查看路线</button>
        <button class="nav-button" @click="active = 'route-signup'">我要报名</button>
      </div>

      <div class="nav-group">
        <h3>联系导游</h3>
        <button class="nav-button" @click="active = 'guides'">查看导游</button> 
        <button class="nav-button">团内群聊</button>
      </div>

      
  
      <div class="nav-group">
      <h3>我要投诉</h3>
      <button class="nav-button" @click="active = 'complaint'">投诉</button>
      </div>


      
    </aside>

    
    <main class="content">
      <RouteSignup v-if="active === 'route-signup'" />
      
      
      <AllRouteList v-if="active === 'list'" @view-details="viewRouteDetails" />


      
      <RouteDetails v-if="active === 'details' && routeId !== null" :routeId="routeId" />


      <AllGuides v-if="active === 'guides'"@start-chat="selectGuideForChat " />

      <ChatBox v-if="active === 'chatGuide'" 
        :sender-role="1" 
        :sender-id="touristId" 
        :receiver-role="2" 
        :receiver-id="selectedGuideId" />

        <SubmitComplaint v-if="active === 'complaint'" />



    </main>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import RouteSignup from './RouteSignup.vue';
import AllRouteList from '@/components/AllRouteList.vue'; // 引入 AllRouteList 组件
import RouteDetails from '@/components/RouteDetails.vue'; // 引入 RouteDetails 组件
import AllGuides from './AllGuides.vue'; // 引入 AllGuides 组件
import SubmitComplaint from './SubmitComplaint.vue'

import ChatBox from '@/components/ChatBox.vue'
import { nextTick } from 'vue'

const active = ref('');  // 初始时不显示任何内容，等用户点击按钮
const routeId = ref(null);  // 保存选中的 routeId
const selectedGuideId = ref(null);  // ⬅️ 加上这句就能解决问题
const touristId = localStorage.getItem('tourist_id'||'0');  
const role = parseInt(localStorage.getItem('role') || '0');
  console.log('当前角色id：',touristId)
  console.log('当前角色role：',role)

// 监听 AllRouteList 组件的事件


const viewRouteDetails = (id) => {
  routeId.value = id
  nextTick(() => {
    active.value = 'details'
  })
}

// 选择游客进行聊天
const selectGuideForChat = (guideId) => {
  selectedGuideId.value = guideId;
  active.value = 'chatGuide';  // 切换到聊天界面
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
  </style> -->


  <!-- <template>
    <div class="dashboard">
    
      <aside class="sidebar">
        <h2>游客界面</h2>
  
        <div class="nav-group">
          <h3>旅游路线</h3>
          <button @click="handleNavClick('list')" class="nav-button">查看路线</button>
          <button @click="handleNavClick('route-signup')" class="nav-button">我要报名</button>
        </div>
  
        <div class="nav-group">
          <h3>联系导游</h3>
          <button @click="handleNavClick('guides')" class="nav-button">查看导游</button>
          <button @click="handleNavClick('groupList')" class="nav-button">查看我的群聊</button> 
        </div>
  
        <div class="nav-group">
          <h3>我要投诉</h3>
          <button @click="handleNavClick('complaint')" class="nav-button">投诉</button>
        </div>
      </aside>
  
      <main class="content">
        <RouteSignup v-if="active === 'route-signup'" />
        <AllRouteList v-if="active === 'list'" @view-details="viewRouteDetails" />
        <RouteDetails v-if="active === 'details' && routeId !== null" :routeId="routeId" />
        <AllGuides 
          v-if="active === 'guides'" 
          :tourist-id="touristId" 
          @start-chat="selectGuideForChat" 
        />
        <ChatBox 
          v-if="active === 'chatGuide'" 
          :sender-role="1" 
          :sender-id="touristId" 
          :receiver-role="2" 
          :receiver-id="selectedGuideId" 
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
        <SubmitComplaint v-if="active === 'complaint'" />
      </main>
    </div>
  </template>
  
  <script setup>
  import { ref } from 'vue';
  import RouteSignup from './RouteSignup.vue';
  import AllRouteList from '@/components/AllRouteList.vue'; // 引入 AllRouteList 组件
  import RouteDetails from '@/components/RouteDetails.vue'; // 引入 RouteDetails 组件
  import AllGuides from './AllGuides.vue'; // 引入 AllGuides 组件
  import SubmitComplaint from './SubmitComplaint.vue';
  import ChatBox from '@/components/ChatBox.vue';
  import GroupChat from '@/components/GroupChat.vue';
  import GroupChatList from '@/components/GroupChatList.vue';
  
  import { nextTick } from 'vue';
  
  const active = ref('');  // 初始时不显示任何内容，等用户点击按钮
  const activeChat = ref(null);
  const routeId = ref(null);  // 保存选中的 routeId
  const selectedGuideId = ref(null);  // 保存选中的导游的 ID
  
  const touristId = localStorage.getItem('tourist_id') || '0';  
  const role = parseInt(localStorage.getItem('role') || '0');
  const userId = parseInt(localStorage.getItem('user_id') || '0');
  
  // 监听 AllRouteList 组件的事件
  const viewRouteDetails = (id) => {
    routeId.value = id;
    nextTick(() => {
      active.value = 'details';
    });
  }
  // 选择导游进行聊天
  const selectGuideForChat = (guideId) => {
    selectedGuideId.value = guideId;
    active.value = 'chatGuide';  // 切换到聊天界面
  }
  
  // 切换模块，清空群聊框
  const handleNavClick = (module) => {
    console.log('当前选择模块:', module);
    active.value = module;
    activeChat.value = null; // 切换到其他模块时清空群聊框
    if (module !== 'chatGuide') {
        selectedGuideId.value = null;  // 离开聊天时清空选中的导游ID
    }
  };
  
  const handleChatSelected = (groupId) => {
    activeChat.value = groupId;
    console.log('选择的群聊ID:', groupId);
    active.value = '';  // 取消激活群聊列表，显示群聊聊天
  };
  </script> -->
  
  
  <template>
    <div class="dashboard">
      <!-- 左侧导航栏 -->
      <aside class="sidebar">
        <h2>游客界面</h2>
    
        <div class="nav-group">
          <h3>旅游路线</h3>
          <button @click="handleNavClick('list')" class="nav-button">查看路线</button>
          <button @click="handleNavClick('route-signup')" class="nav-button">我要报名</button>
        </div>
    
        <div class="nav-group">
          <h3>联系导游</h3>
          <button @click="handleNavClick('guides')" class="nav-button">查看导游</button>
          <button @click="handleNavClick('groupList')" class="nav-button">查看我的群聊</button> 
        </div>
    
        <div class="nav-group">
          <h3>我要投诉</h3>
          <button @click="handleNavClick('complaint')" class="nav-button">投诉</button>
        </div>
      </aside>
    
      <!-- 右侧内容区 -->
      <main class="content">
        <RouteSignup v-if="active === 'route-signup'" />
        <AllRouteList v-if="active === 'list'" @view-details="viewRouteDetails" />
        <RouteDetails v-if="active === 'details' && routeId !== null" :routeId="routeId" />
        <AllGuides 
          v-if="active === 'guides'" 
          :tourist-id="touristId" 
          @start-chat="selectGuideForChat" 
        />
        <ChatBox 
          v-if="active === 'chatGuide'" 
          :sender-role="1" 
          :sender-id="touristId" 
          :receiver-role="2" 
          :receiver-id="selectedGuideId" 
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
        <SubmitComplaint v-if="active === 'complaint'" />
      </main>
    </div>
  </template>
  
  <script setup>
  import { ref } from 'vue';
  import RouteSignup from './RouteSignup.vue';
  import AllRouteList from '@/components/AllRouteList.vue';
  import RouteDetails from '@/components/RouteDetails.vue';
  import AllGuides from './AllGuides.vue';
  import SubmitComplaint from './SubmitComplaint.vue';
  import ChatBox from '@/components/ChatBox.vue';
  import GroupChat from '@/components/GroupChat.vue';
  import GroupChatList from '@/components/GroupChatList.vue';
  
  import { nextTick } from 'vue';
  
  const active = ref('');  // 初始时不显示任何内容，等用户点击按钮
  const activeChat = ref(null);
  const routeId = ref(null);  // 保存选中的 routeId
  const selectedGuideId = ref(null);  // 保存选中的导游的 ID
  
  const touristId = localStorage.getItem('tourist_id') || '0';  
  const role = parseInt(localStorage.getItem('role') || '0');
  const userId = parseInt(localStorage.getItem('user_id') || '0');
  
  // 监听 AllRouteList 组件的事件
  const viewRouteDetails = (id) => {
    routeId.value = id;
    nextTick(() => {
      active.value = 'details';
    });
  };
  
  // 选择导游进行聊天
  const selectGuideForChat = (guideId) => {
    selectedGuideId.value = guideId;
    active.value = 'chatGuide';  // 切换到聊天界面
  };
  
  // 切换模块，清空群聊框
  const handleNavClick = (module) => {
    console.log('当前选择模块:', module);
    active.value = module;
    activeChat.value = null; // 切换到其他模块时清空群聊框
    if (module !== 'chatGuide') {
        selectedGuideId.value = null;  // 离开聊天时清空选中的导游ID
    }
  };
  
  const handleChatSelected = (groupId) => {
    activeChat.value = groupId;
    console.log('选择的群聊ID:', groupId);
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
    overflow-y: auto; /* 如果侧边栏内容超出，添加滚动条 */
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
    overflow-y: auto;  /* 使内容区支持纵向滚动 */
    max-height: 100vh; /* 限制内容区的最大高度为视口高度 */
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
  
  
  
  