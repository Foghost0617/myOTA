<!-- <template>
    <div>
      <h1>负责游客列表</h1>
      <div v-if="loading">加载中...</div>
      <div v-else-if="tourists.length === 0">暂无游客数据</div>
      <ul v-else class="tourist-list">
        <li v-for="tourist in tourists" :key="tourist.id" class="tourist-item">
          <div><strong>游客ID：</strong>{{ tourist.id }}</div>
          <div><strong>姓名：</strong>{{ tourist.name || '未填写' }}</div>
          <div><strong>电话：</strong>{{ tourist.phone || '未填写' }}</div>
        </li>
      </ul>
    </div>
  </template>
  
  <script setup>
  import { ref, onMounted } from 'vue'
  import axios from '@/utils/request'
  
  const tourists = ref([])
  const loading = ref(true)
  
  const guideId = localStorage.getItem('guide_id')
  
  onMounted(async () => {
    try {
      const response = await axios.get(`guides/${guideId}/tourists`)
      tourists.value = response.data
      console.log(response.data)
    } catch (error) {
      console.error('获取游客失败:', error)
      tourists.value = []
    } finally {
      loading.value = false
    }
  })
  </script>
  
  <style scoped>
  .tourist-list {
    list-style: none;
    padding: 0;
  }
  
  .tourist-item {
    background: #ffffff;
    color: #2c3e50; /* 字体颜色改为深灰，更清晰 */
    padding: 16px;
    margin-bottom: 12px;
    border-radius: 8px;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
    transition: box-shadow 0.2s ease;
  }
  
  .tourist-item:hover {
    box-shadow: 0 4px 16px rgba(0, 0, 0, 0.15);
  }
  
  .tourist-item strong {
    color: #34495e; /* 加粗字段标题颜色 */
  }
  
  h1 {
    color: #2c3e50;
    margin-bottom: 20px;
    font-size: 24px;
  }
  </style> -->
  
  <template>
    <div>
      <h1>负责游客列表</h1>
      <div v-if="loading">加载中...</div>
      <div v-else-if="tourists.length === 0">暂无游客数据</div>
      <ul v-else class="tourist-list">
        <li v-for="tourist in tourists" :key="tourist.id" class="tourist-item">
          <div><strong>游客ID：</strong>{{ tourist.id }}</div>
          <div><strong>姓名：</strong>{{ tourist.name || '未填写' }}</div>
          <div><strong>电话：</strong>{{ tourist.phone || '未填写' }}</div>
          <!-- 新增私聊按钮 -->
          <button @click="$emit('start-chat', tourist.id)">私聊该游客</button>
        </li>
      </ul>
  
      <!-- 控制显示聊天框 -->
      <div v-if="selectedTouristId">
        <ChatBox
          :sender-role="2"
          :sender-id="guideId"
          :receiver-role="1"
          :receiver-id="selectedTouristId"
        />
      </div>
    </div>
  </template>
  
  <script setup>
  import { ref, onMounted } from 'vue'
  import axios from '@/utils/request'
  import ChatBox from '@/components/ChatBox.vue'
  
  const tourists = ref([])
  const loading = ref(true)
  const guideId = localStorage.getItem('guide_id')
  console.log('导游id是：')
  console.log(guideId)
  const selectedTouristId = ref(null) // 记录当前选择的游客 ID
  
  // 获取游客列表
  onMounted(async () => {
    try {
      const response = await axios.get(`guides/${guideId}/tourists`)
      tourists.value = response.data
    } catch (error) {
      console.error('获取游客失败:', error)
      tourists.value = []
    } finally {
      loading.value = false
    }
  })
  
  const startChat = (touristId) => {
    if (!guideId) {
      console.error("导游 ID 为空，无法开始聊天");
      return;
    }
    selectedTouristId.value = touristId
    console.log('游客id是：', touristId)
    console.log('导游id是：', guideId)
    // 这里可以进一步处理 WebSocket 连接
  }
  </script>
  
  <style scoped>
  .tourist-list {
    list-style: none;
    padding: 0;
    margin: 0;
  }
  
  .tourist-item {
    background: #ffffff;
    color: #2c3e50;
    padding: 18px;
    margin-bottom: 16px;
    border-radius: 12px;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
    transition: box-shadow 0.3s ease, transform 0.3s ease;
  }
  
  .tourist-item:hover {
    box-shadow: 0 6px 20px rgba(0, 0, 0, 0.2);
    transform: translateY(-5px);
  }
  
  .tourist-item strong {
    color: #34495e;
    font-weight: 600;
  }
  
  button {
    background-color: #1abc9c;
    color: white;
    border: none;
    padding: 10px 18px;
    border-radius: 6px;
    cursor: pointer;
    font-size: 14px;
    transition: background-color 0.3s ease, transform 0.2s ease;
  }
  
  button:hover {
    background-color: #16a085;
    transform: translateY(-2px);
  }
  
  button:focus {
    outline: none;
  }
  
  h1 {
    font-size: 24px;
    color: #2c3e50;
    margin-bottom: 20px;
    font-weight: 700;
  }
  
  </style>
  