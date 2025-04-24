   <!-- 最新可以 -->
   <template>
    <div class="chat-box">
      <div class="chat-history">
        <div v-for="msg in messages" :key="msg.id" class="chat-message" :class="{ self: msg.fromMe, other: !msg.fromMe }">
          <div class="message-content">
            <span>{{ msg.content }}</span>
          </div>
          <small>{{ formatTimestamp(msg.timestamp) }}</small>
        </div>
      </div>
      <div class="chat-input">
        <input v-model="newMessage" @keyup.enter="sendMessage" placeholder="输入消息..." />
        <button @click="sendMessage">发送</button>
      </div>
    </div>
  </template>
  
  <script setup>
  import { ref, onMounted, onBeforeUnmount, watch, nextTick } from 'vue'
  import axios from '@/utils/request'
  
  const props = defineProps({
    senderRole: Number,
    senderId: Number,
    receiverRole: Number,
    receiverId: Number,
  })
  
  const messages = ref([])  // 存储消息内容
  const newMessage = ref('')  // 输入框内容
  let socket = null
  
  // 加载历史消息
  const loadHistory = async () => {
    const res = await axios.get('/messages/history', {
      params: {
        sender_id: props.senderId,
        sender_role: props.senderRole,
        receiver_id: props.receiverId,
        receiver_role: props.receiverRole,
      }
    })
    messages.value = res.data.map(m => {
      const fromMe = m.sender_role === props.senderRole
      return {
        ...m,
        fromMe
      }
    })
  }
  
  // 建立 WebSocket 连接
  const connectSocket = () => {
    if (socket) socket.close()  // 断开旧连接
  
    const url = `ws://localhost:8001/ws/chat/${props.senderRole}/${props.senderId}`
    socket = new WebSocket(url)
  
    socket.onmessage = (event) => {
      const data = JSON.parse(event.data)
  
      const fromMe = data.from === `${props.senderRole}_${props.senderId}`
      messages.value.push({
        content: data.content,
        timestamp: data.timestamp,
        fromMe: fromMe
      })
    }
  }
  
  // 发送消息
  const sendMessage = () => {
    if (newMessage.value.trim() === '') return
  
    const msg = {
      receiver_role: props.receiverRole,
      receiver_id: props.receiverId,
      content: newMessage.value,
      is_group: false
    }
  
    // 先本地添加消息到列表中，立即显示
    messages.value.push({
      content: newMessage.value,
      timestamp: new Date().toISOString(),
      fromMe: true
    })
  
    socket?.send(JSON.stringify(msg))  // 发送消息到服务器
    newMessage.value = ''  // 清空输入框
  }
  
  // 格式化时间戳为年月日 时分秒格式
  const formatTimestamp = (ts) => {
    const date = new Date(ts)
    return date.toLocaleString('zh-CN', {
      year: 'numeric',
      month: '2-digit',
      day: '2-digit',
      hour: '2-digit',
      minute: '2-digit',
      second: '2-digit',
    })
  }
  
  onMounted(() => {
    loadHistory()
    connectSocket()
  })
  
  onBeforeUnmount(() => {
    if (socket) socket.close()
  })
  
  // 监听聊天对象变化，重新加载数据和连接
  watch(() => [props.receiverRole, props.receiverId], () => {
    loadHistory()
    connectSocket()
  })
  
  // 自动滚动到底部，确保每次消息更新后显示最新消息
  watch(messages, async () => {
  await nextTick();  // 等待 DOM 更新
  const chatBox = document.querySelector('.chat-history');  // 获取聊天历史容器
  if (chatBox) {
    console.log("滚动到最新消息", chatBox.scrollHeight, chatBox.scrollTop);
    chatBox.scrollTop = chatBox.scrollHeight;  // 滚动到底部
  }
});

  </script>
  
  <style scoped>
  .chat-box {
    display: flex;
    flex-direction: column;
    height: 100%;
    max-height: 100%;
    box-sizing: border-box;
    padding: 10px;
    overflow: hidden;
  }
  
  /* 聊天历史区域，允许滚动 */
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
  
  /* 每条消息的容器 */
  .chat-message {
    display: flex;
    flex-direction: column;
    margin-bottom: 10px;
    word-wrap: break-word;
    line-height: 1.4;
  }
  
  /* 自己的消息靠右 */
  .chat-message.self {
    align-items: flex-end;
  }
  
  /* 他人消息靠左 */
  .chat-message.other {
    align-items: flex-start;
  }
  
  /* 消息气泡样式 */
  .message-content {
    display: inline-block;
    max-width: 75%;
    padding: 10px 14px;
    border-radius: 12px;
    word-wrap: break-word;
    background-color: #f0f0f0;
    color: #333;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  }
  
  /* 自己的消息颜色 */
  .chat-message.self .message-content {
    background-color: #daf8da;
  }
  
  /* 时间戳样式 */
  .chat-message small {
    color: #888;
    font-size: 0.75rem;
    margin-top: 5px;
  }
  
  /* 输入区域 */
  .chat-input {
    display: flex;
    align-items: center;
    gap: 10px;
  }
  
  .chat-input input {
    flex-grow: 1;
    padding: 10px;
    border-radius: 6px;
    border: 1px solid #ccc;
    font-size: 1rem;
  }
  
  .chat-input button {
    padding: 10px 16px;
    background-color: #4CAF50;
    color: white;
    border: none;
    border-radius: 6px;
    cursor: pointer;
    font-size: 1rem;
  }
  
  .chat-input button:hover {
    background-color: #45a049;
  }
  </style>
  

  
  
  