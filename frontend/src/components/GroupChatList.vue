
<!-- <template>
    <div class="group-chat-list">
      <h2>我的群聊</h2>
      <div v-if="groupChats.length === 0">暂时没有加入任何群聊</div>
      <ul v-else>
        <li v-for="chat in groupChats" :key="chat.group_id" class="chat-item">
          <div class="chat-name">{{ chat.group_name }}</div>
          <div class="chat-time">创建时间：{{ formatTime(chat.created_at) }}</div>
        </li>
      </ul>
    </div>
  </template>


<script setup>
import { ref, onMounted } from 'vue'
import axios from '@/utils/request'

// 父组件传入 userId
const props = defineProps({
  userId: {
    type: Number,
    required: true
  }
})

const groupChats = ref([])

onMounted(async () => {
  try {
    const res = await axios.get('/groupchats/user-groups', {
      params: {
        user_id: props.userId
      }
    })
    groupChats.value = res.data || []
  } catch (err) {
    console.error('加载群聊列表失败：', err)
    alert('无法加载群聊列表')
  }
})
// 补一个小工具函数，格式化时间（直接在这里补）
function formatTime(timeString) {
  const date = new Date(timeString)
  return date.toLocaleString()
}
</script> -->




<template>
    <div class="group-chat-list">
      <h2>我的群聊</h2>
      <div v-if="groupChats.length === 0">暂时没有加入任何群聊</div>
      <ul v-else>
        <li
          v-for="chat in groupChats"
          :key="chat.group_id"
          class="chat-item"
          @click="selectChat(chat.group_id)"
        >
          <div class="chat-name">{{ chat.group_name }}</div>
          <div class="chat-time">创建时间：{{ formatTime(chat.created_at) }}</div>
        </li>
      </ul>
    </div>
  </template>
  
  <script setup>
  import { ref, onMounted } from 'vue';
  import axios from '@/utils/request';
  
  const props = defineProps({
    userId: {
      type: Number,
      required: true
    }
  });
  
  const emit = defineEmits(['chat-selected']);
  const groupChats = ref([]);
  
  onMounted(async () => {
    try {
      const res = await axios.get('/groupchats/user-groups', {
        params: {
          user_id: props.userId
        }
      });
      groupChats.value = res.data || [];
    } catch (err) {
      console.error('加载群聊列表失败：', err);
      alert('无法加载群聊列表');
    }
  });
  
  // 格式化时间
  function formatTime(timeString) {
    const date = new Date(timeString);
    return date.toLocaleString();
  }
  
  // 选择群聊
  const selectChat = (groupId) => {
    emit('chat-selected', groupId);  // 触发父组件事件，传递选中的群聊 ID
  };
  </script>
  
  <style scoped>
  .group-chat-list {
    padding: 20px;
  }
  
  .chat-item {
    padding: 10px;
    margin-bottom: 10px;
    border: 1px solid #ccc;
    border-radius: 8px;
    cursor: pointer;
    transition: background-color 0.3s;
  }
  
  .chat-item:hover {
    background-color: #f0f0f0;
  }
  
  .chat-name {
    font-weight: bold;
    font-size: 16px;
  }
  
  .chat-time {
    color: #888;
    font-size: 12px;
    margin-top: 4px;
  }
  </style>
  
