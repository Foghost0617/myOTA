<!-- <template>
  <div>
    <h2>导游列表</h2>
    <div v-if="loading">加载中...</div>
    <div v-else-if="guides.length === 0">暂无导游数据</div>
    <ul v-else class="guide-list">
      <li v-for="guide in guides" :key="guide" class="guide-item">
        <div><strong>导游ID：</strong>{{ guide }}</div>
        <div><strong>姓名：</strong>{{ guide.guide_name || '未填写' }}</div>
        <div><strong>电话：</strong>{{ guide.phone || '未填写' }}</div>
        <button @click="startChat(guide)">私聊该导游</button>
      </li>
    </ul>

    <div v-if="selectedGuideId">
      <ChatBox
        :sender-role="1"
        :sender-id="touristId"
        :receiver-role="2"
        :receiver-id="selectedGuideId"
      />
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from '@/utils/request'
import ChatBox from '@/components/ChatBox.vue'

const props = defineProps({
  touristId: {
    type: String,
    required: true
  }
})

const guides = ref([]) // 存储导游列表
const loading = ref(true) // 加载状态
const selectedGuideId = ref(null) // 当前选中的导游ID，用于聊天功能

// 获取导游列表
onMounted(async () => {
  try {
    const response = await axios.get(`/tourist_route/get_guides_by_tourist/${props.touristId}`)
    // 去重，只保留唯一的导游ID
    const uniqueGuideIds = [...new Set(response.data.guide_ids)];
    guides.value = uniqueGuideIds
  } catch (error) {
    console.error('获取导游列表失败:', error)
    guides.value = []
  } finally {
    loading.value = false
  }
})

// 私聊按钮点击事件
const startChat = (guideId) => {
  if (!props.touristId) {
    console.error('导游 ID 为空，无法开始聊天')
    return
  }
  selectedGuideId.value = guideId
  console.log('导游id是：', guideId)
  console.log('游客id是：', props.touristId)
}
</script> -->



<template>
  <div>
    <h2>导游列表</h2>
    <div v-if="loading">加载中...</div>
    <div v-else-if="guides.length === 0">暂无导游数据</div>
    <ul v-else class="guide-list">
      <li v-for="guide in guides" :key="guide" class="guide-item">
        <!-- <div><strong>导游ID：</strong>{{ guide }}</div> -->
        <div><strong>姓名：</strong>{{ guide.guide_name || '未填写' }}</div>
        <div><strong>电话：</strong>{{ guide.phone || '未填写' }}</div>
        <button @click="startChat(guide)">私聊该导游</button>
      </li>
    </ul>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from '@/utils/request'
import ChatBox from '@/components/ChatBox.vue'

const props = defineProps({
  touristId: {
    type: String,
    required: true
  }
})

const emit = defineEmits(['start-chat']) // 定义 start-chat 事件

const guides = ref([]) // 存储导游列表
const loading = ref(true) // 加载状态
const selectedGuideId = ref(null) // 当前选中的导游ID，用于聊天功能

// 获取导游列表
onMounted(async () => {
  try {
    const response = await axios.get(`/tourist_route/get_guides_by_tourist/${props.touristId}`)
    // 去重，只保留唯一的导游ID
    const uniqueGuideIds = [...new Set(response.data.guide_ids)];
    guides.value = uniqueGuideIds
  } catch (error) {
    console.error('获取导游列表失败:', error)
    guides.value = []
  } finally {
    loading.value = false
  }
})

// 私聊按钮点击事件
const startChat = (guideId) => {
  if (!props.touristId) {
    console.error('导游 ID 为空，无法开始聊天')
    return
  }
  selectedGuideId.value = guideId
  emit('start-chat', guideId)  // 触发 start-chat 事件
}


</script>


<style scoped>
h2 {
    font-size: 24px;
    color: #2c3e50;
    margin-bottom: 20px;
}

.guide-list {
    list-style: none;
    padding: 0;
}

.guide-item {
    background: #fff;
    color: #34495e;
    padding: 16px;
    margin-bottom: 12px;
    border-radius: 8px;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
    transition: box-shadow 0.2s ease;
}

.guide-item:hover {
    box-shadow: 0 4px 16px rgba(0, 0, 0, 0.15);
}

.guide-item strong {
    color: #16a085;
}

button {
    background-color: #3498db;
    color: white;
    border: none;
    padding: 8px 16px;
    border-radius: 5px;
    cursor: pointer;
    transition: background-color 0.3s ease;
}

button:hover {
    background-color: #2980b9;
}

button:focus {
    outline: none;
}

button:active {
    background-color: #21618c;
}
</style>

