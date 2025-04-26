<template>
    <div class="group-chat-chat">
      <h2>群聊 {{ groupId }}</h2>
      <div class="group-chat">
        <div class="chat-history" ref="chatHistory">
          <!-- 显示聊天记录 -->
          <div v-for="message in messages" :key="message.message_id" class="message-item">
            <div class="sender">{{ message.sender_id }}: </div>
            <div class="message-content">
              <p v-if="!message.is_location">{{ message.content }}</p>
              <div v-if="message.is_location">
                <p>位置: <a :href="`https://www.google.com/maps?q=${message.latitude},${message.longitude}`" target="_blank">查看位置</a></p>
              </div>
            </div>
            <div class="timestamp">{{ message.timestamp }}</div>
          </div>
        </div>
        <div class="send-message">
          <input v-model="newMessage" placeholder="请输入消息" @keyup.enter="sendMessage" />
          <button @click="sendMessage">发送</button>
        </div>
      </div>
    </div>
  </template>
  
  <script setup>
  import { ref, onMounted, onBeforeUnmount } from 'vue';
  import axios from '@/utils/request'
  
  const props = defineProps({
    groupId: {
      type: Number,
      required: true,
    },
    userId: {
      type: Number,
      required: true,
    },
    role: {
      type: Number,
      required: true,
    },
  });
  
  const messages = ref([]);  // 存储聊天消息
  const newMessage = ref(''); // 存储用户输入的消息
  const socket = ref(null);   // WebSocket实例
  
  // 获取群聊历史记录
  const fetchChatHistory = async () => {
    try {
      const response = await axios.get(`/groupchats/${props.groupId}/history`);
      messages.value = response.data;  // 将获取到的历史记录设置到 messages 中
      scrollToBottom();  // 确保历史记录加载后滚动到底部
    } catch (error) {
      console.error('获取聊天记录失败', error);
    }
  };
  
  // 建立 WebSocket 连接
  const connectWebSocket = () => {
    socket.value = new WebSocket(`ws://localhost:8009/groupchats/ws/group-chat/${props.groupId}`);
    
    socket.value.onopen = () => {
      console.log('WebSocket连接成功');
    };
  
    socket.value.onmessage = (event) => {
      const message = JSON.parse(event.data);
      messages.value.push(message);
      scrollToBottom();  // 新消息到来时滚动到底部
    };
  
    socket.value.onclose = () => {
      console.log('WebSocket连接关闭');
    };
  
    socket.value.onerror = (error) => {
      console.error('WebSocket发生错误', error);
    };
  };
  
  // 发送消息
  const sendMessage = () => {
    if (newMessage.value.trim()) {
      const messageData = {
        sender_id: props.userId,  // 使用父组件传入的用户 ID
        sender_role: props.role,  // 使用父组件传入的角色
        group_id: props.groupId,
        content: newMessage.value,
        is_location: false, // 如果需要发送位置消息，可以设置为 true 并添加经纬度
      };
  
      socket.value.send(JSON.stringify(messageData));
      newMessage.value = '';  // 发送完消息清空输入框
    }
  };
  
  // 滚动到底部
  const scrollToBottom = () => {
    const chatHistory = document.querySelector('.chat-history');
    chatHistory.scrollTop = chatHistory.scrollHeight;
  };
  
  // 初始化连接
  onMounted(() => {
    fetchChatHistory();  // 先获取历史记录
    connectWebSocket();  // 然后连接 WebSocket
  });
  
  // 组件卸载时关闭 WebSocket
  onBeforeUnmount(() => {
    if (socket.value) {
      socket.value.close();
    }
  });
  </script>
  
  <style scoped>
  .group-chat-chat {
    width: 100%;
    max-width: 600px;
    margin: auto;
  }
  
  .group-chat {
    display: flex;
    flex-direction: column;
  }
  
  .chat-history {
    height: 400px;
    overflow-y: auto;
    margin-bottom: 10px;
  }
  
  .message-item {
    padding: 10px;
    border-bottom: 1px solid #ddd;
  }
  
  .sender {
    font-weight: bold;
  }
  
  .timestamp {
    font-size: 0.8em;
    color: gray;
  }
  
  .send-message {
    display: flex;
    justify-content: space-between;
    align-items: center;
  }
  
  .send-message input {
    width: 80%;
    padding: 5px;
  }
  
  .send-message button {
    padding: 5px 10px;
  }
  </style>
 