<template>
  <div class="complaint-container">
    <h2>我要投诉</h2>
    <textarea v-model="content" placeholder="请输入投诉内容"></textarea>
    <button @click="submitComplaint">提交</button>
    <p v-if="message" class="message">{{ message }}</p>
    <p v-if="error" class="error">{{ error }}</p>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import axios from '@/utils/request'

const content = ref('')
const message = ref('')
const error = ref('')

const submitComplaint = async () => {
  const tourist_id = localStorage.getItem('tourist_id')
  if (!tourist_id || !content.value.trim()) {
    error.value = '请输入内容，且需登录后才能投诉'
    message.value = ''
    return
  }

  try {
    await axios.post('/complaints/submit', {
      tourist_id: Number(tourist_id),
      content: content.value,
    })
    message.value = '投诉已提交，文旅局会尽快处理。'
    error.value = ''
    content.value = ''
  } catch (err) {
    error.value = '提交失败，请稍后重试'
    message.value = ''
  }
}
</script>

<style scoped>
.complaint-container {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
  background-color: #fff;
  border-radius: 8px;
}

h2 {
  font-size: 20px;
  color: #333;
  margin-bottom: 10px;
}

textarea {
  width: 90%;
  padding: 10px;
  font-size: 14px;
  border: 1px solid #ccc;
  border-radius: 4px;
  margin-bottom: 10px;
  resize: none;
  height: 150px; 
  color: #000; /* 设置输入文字为黑色 */
  background-color: #f9f9f9; /* 设置浅白色背景 */
}

button {
  width: 90%;
  padding: 10px;
  background-color: #e74c3c;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

button:hover {
  background-color: #c0392b;
}

.message {
  color: green;
  margin-top: 10px;
}

.error {
  color: red;
  margin-top: 10px;
}
</style>
