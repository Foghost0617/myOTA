<!-- <template>
    <div class="group-chat-chat">
      <h2>群聊 {{ groupId }}</h2>
      <div class="group-chat">
        <div class="chat-history" ref="chatHistory">
     
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
  </style> -->
 
<!-- new -->
  <!-- <template>
    <div class="group-chat-chat">
      <h2>群聊 {{ groupId }}</h2>
      <div class="group-chat">
        <div class="chat-history" ref="chatHistory">
          
          <div v-for="message in messages" :key="message.message_id" class="message-item" :class="{'my-message': message.sender_id === props.userId, 'other-message': message.sender_id !== props.userId}">
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
  import axios from '@/utils/request';
  
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
  console.log(props.data)

  const messages = ref([]);  // 存储聊天消息
  const newMessage = ref(''); // 存储用户输入的消息
  const socket = ref(null);   // WebSocket实例
  
  // 获取群聊历史记录
  const fetchChatHistory = async () => {
  try {
    const response = await axios.get(`/groupchats/${props.groupId}/history`);
    console.log("获取到的聊天记录:", response.data);  // 打印获取到的聊天记录
    messages.value = response.data;  // 将获取到的历史记录设置到 messages 中
    scrollToBottom();  // 确保历史记录加载后滚动到底部
  } catch (error) {
    console.error('获取聊天记录失败', error);
  }
};

  
  // 建立 WebSocket 连接
  const connectWebSocket = () => {
  socket.value = new WebSocket(`ws://localhost:8009/groupchats/ws/group-chat/${props.groupId}`);
  console.log("尝试连接 WebSocket...");

  socket.value.onopen = () => {
    console.log('WebSocket连接成功');
  };

  socket.value.onmessage = (event) => {
    const message = JSON.parse(event.data);
    console.log("收到新消息:", message);  // 打印接收到的新消息
    messages.value.push(message);  // 将新消息加入到消息列表
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
      sender_id: props.userId,
      sender_role: props.role,
      group_id: props.groupId,
      content: newMessage.value,
      is_location: false, // 如果需要发送位置消息，可以设置为 true 并添加经纬度
    };

    console.log("发送的消息数据:", messageData);
    socket.value.send(JSON.stringify(messageData));  // 发送消息到 WebSocket
    messages.value.push(messageData);  // 立即更新本地消息列表，显示新发送的消息
    newMessage.value = '';  // 清空输入框
    scrollToBottom();  // 发送消息后滚动到底部
  }
};

  
// 滚动到底部
const scrollToBottom = () => {
  const chatHistory = document.querySelector('.chat-history');
  if (chatHistory) {
    chatHistory.scrollTop = chatHistory.scrollHeight;  // 保证每次新消息来时滚动到底部
  }
};
  // 初始化连接
onMounted(() => {
  console.log("接收到的 props:", props);
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
    max-height: 400px;  /* 限制最大高度 */
    overflow-y: auto;   /* 超过最大高度时启用滚动 */
    margin-bottom: 10px;
  }
  
  .message-item {
    padding: 10px;
    border-radius: 10px;
    margin-bottom: 10px;
    max-width: 70%;
    word-wrap: break-word;
    display: flex;
    flex-direction: column;
  }
  
  .my-message {
    background-color: #dcf8c6;  /* 绿色背景 */
    align-self: flex-end;  /* 自己的消息靠右 */
  }
  
  .other-message {
    background-color: #f1f0f0;  /* 灰色背景 */
    align-self: flex-start;  /* 其他人的消息靠左 */
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
  </style> -->
  
  <template>
    <div class="group-chat-chat">
      <!-- <h2>群聊 {{ groupId }}</h2> -->
      <div class="group-chat">
        <div class="chat-history" ref="chatHistory">
          <!-- 显示聊天记录 -->
          <div
            v-for="message in messages"
            :key="message.message_id"
            class="message-item"
            :class="{
              'my-message': Number(message.sender_id) === Number(props.userId),
              'other-message': Number(message.sender_id) !== Number(props.userId)
            }"
          >
            <div class="message-content">
              <p v-if="!message.is_location">{{ message.content }}</p>
              <div v-if="message.is_location">
                <p>位置: <a :href="`https://www.google.com/maps?q=${message.latitude},${message.longitude}`" target="_blank">查看位置</a></p>
              </div>
            </div>
            <div class="sender-id">{{ message.sender_id }}</div> <!-- 显示 ID -->
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
  import axios from '@/utils/request';
  
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
      console.log("获取到的聊天记录:", response.data);  // 打印获取到的聊天记录
      messages.value = response.data;  // 将获取到的历史记录设置到 messages 中
      scrollToBottom();  // 确保历史记录加载后滚动到底部
    } catch (error) {
      console.error('获取聊天记录失败', error);
    }
  };
  
  // 建立 WebSocket 连接
  const connectWebSocket = () => {
    socket.value = new WebSocket(`ws://localhost:8001/groupchats/ws/group-chat/${props.groupId}`);
    console.log("尝试连接 WebSocket...");
  
    socket.value.onopen = () => {
      console.log('WebSocket连接成功');
    };
  
    socket.value.onmessage = (event) => {
      const message = JSON.parse(event.data);
      console.log("收到新消息:", message);  // 打印接收到的新消息
  
      messages.value.push(message);  // 将新消息加入到消息列表
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
        sender_id: props.userId,
        sender_role: props.role,
        group_id: props.groupId,
        content: newMessage.value,
        is_location: false, // 如果需要发送位置消息，可以设置为 true 并添加经纬度
      };
  
      console.log("发送的消息数据:", messageData);  // 打印发送的消息数据
      socket.value.send(JSON.stringify(messageData));  // 发送消息到 WebSocket
      newMessage.value = '';  // 清空输入框
      scrollToBottom();  // 发送消息后滚动到底部
    }
  };
  
  // 滚动到底部
  const scrollToBottom = () => {
    const chatHistory = document.querySelector('.chat-history');
    if (chatHistory) {
      chatHistory.scrollTop = chatHistory.scrollHeight;  // 保证每次新消息来时滚动到底部
    }
  };
  
  // 初始化连接
  onMounted(() => {
    console.log("接收到的 props:", props);  // 打印传入的props
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
    max-width: 850px;
    margin: auto;
    padding: 15px;
    max-height: 700px;
  }
  
  .group-chat {
    display: flex;
    flex-direction: column;
    background-color: #f9f9f9;
    border-radius: 8px;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  }
  
  .chat-history {
    flex-grow: 1;
    overflow-y: auto;
    padding: 10px;
    background-color: #fff;
    border: 1px solid #e0e0e0;
    border-radius: 10px;
    margin-bottom: 10px;
    max-height: 70vh; /* 控制最大高度 */
  }

  .message-item {
    padding: 10px;
    border-radius: 10px;
    margin-bottom: 12px;
    max-width: 75%;
    word-wrap: break-word;
    display: flex;
    flex-direction: column;
    position: relative;
    font-size: 14px;
  }

  /* 我的消息 */
  .my-message {
    background-color: #daf8da;
    align-self: flex-end;
    margin-left: auto;
    color: #333;
  }

  /* 他人的消息 */
  .other-message {
    background-color: rgb(230, 226, 226); /* 浅灰色 */
    align-self: flex-start;
    margin-right: auto;
    color: #333;
  }

  .message-content {
    font-size: 14px;
    word-wrap: break-word;
    margin-bottom: 6px;
  }

  .sender-id {
    font-size: 0.75em;
    color: #888;
    margin-top: 4px;
  }

  .timestamp {
    font-size: 0.75em;
    color: #aaa;
    position: absolute;
    bottom: 5px;
    right: 10px;
  }

  .send-message {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-top: 10px;
  }

  .send-message input {
    width: 80%;
    padding: 8px;
    border-radius: 4px;
    border: 1px solid #ddd;
    font-size: 14px;
  }

  .send-message button {
    padding: 8px 12px;
    background-color: #4CAF50; /* 绿色 */
    color: white;
    border: none;
    border-radius: 4px;
    cursor: pointer;
  }

  .send-message button:hover {
    background-color: #45a049;
  }
</style>

  
  
  
  
  