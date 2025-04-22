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
  </style>
  
  