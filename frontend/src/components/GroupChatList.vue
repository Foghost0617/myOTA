
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
    <div v-if="groupChats.length === 0" class="no-chats">暂时没有加入任何群聊</div>
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
console.log('GroupChatList 组件的数据:', props.userId);
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
  emit('chat-selected', groupId); // 触发父组件事件，传递选中的群聊 ID
};
</script>

<style scoped>
.group-chat-list {
  padding: 20px;
  background-color: #fafafa;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

h2 {
  font-size: 18px;
  font-weight: bold;
  color: #333;
  margin-bottom: 16px;
}

.no-chats {
  color: #666;
  font-size: 14px;
  text-align: center;
}

.chat-item {
  padding: 12px 16px;
  margin-bottom: 12px;
  border: 1px solid #ddd;
  border-radius: 8px;
  cursor: pointer;
  transition: background-color 0.3s, transform 0.2s;
  background-color: #fff;
}

.chat-item:hover {
  background-color: #f7f7f7;
  transform: scale(1.02);
}

.chat-name {
  font-weight: 600;
  font-size: 16px;
  color: #333;
}

.chat-time {
  color: #999;
  font-size: 13px;
  margin-top: 6px;
}
</style>
