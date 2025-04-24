<template>
    <div class="p-4 max-w-xl mx-auto">
      <h2 class="text-xl font-bold mb-4">我要投诉</h2>
  
      <textarea
        v-model="content"
        placeholder="请输入投诉内容"
        rows="5"
        class="w-full p-2 border rounded-md resize-none"
      ></textarea>
  
      <button
        @click="submitComplaint"
        class="mt-4 bg-red-500 hover:bg-red-600 text-white px-4 py-2 rounded"
      >
        提交
      </button>
  
      <p v-if="message" class="mt-4 text-green-600">{{ message }}</p>
      <p v-if="error" class="mt-4 text-red-600">{{ error }}</p>
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
      message.value = '投诉已提交，我们会尽快处理。'
      error.value = ''
      content.value = ''
    } catch (err) {
      error.value = '提交失败，请稍后重试'
      message.value = ''
    }
  }
  </script>
  
  <style scoped>
  textarea {
    font-size: 1rem;
  }
  </style>
  