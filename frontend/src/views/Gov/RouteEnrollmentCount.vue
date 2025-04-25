<template>
    <div class="route-stats-container">
      <h2 class="title">路线报名统计</h2>
  
      <div class="select-group">
        <label class="select-label">选择路线：</label>
        <select v-model="selectedRouteId" @change="fetchCount" class="custom-select">
          <option disabled value="">请选择路线</option>
          <option v-for="route in routes" :key="route.id" :value="route.id">
            {{ route.name }}
          </option>
        </select>
      </div>
  
      <div v-if="countResult" class="result-card">
        <p class="route-name">路线名称：<span>{{ countResult.route_name }}</span></p>
        <p class="signup-count">报名人数：<span>{{ countResult.count }}</span> 人</p>
      </div>
  
      <div v-else-if="selectedRouteId" class="loading">正在加载报名人数...</div>
    </div>
  </template>
  
  <script setup>
  import { ref, onMounted } from 'vue'
  import axios from '@/utils/request'
  
  const routes = ref([])
  const selectedRouteId = ref('')
  const countResult = ref(null)
  
  const fetchRoutes = async () => {
    try {
      const res = await axios.get('/routes/all')
      routes.value = res.data
    } catch (err) {
      console.error('获取路线失败', err)
    }
  }
  
  const fetchCount = async () => {
    if (!selectedRouteId.value) return
    countResult.value = null
    try {
      const res = await axios.get(`/routes/enrollment-count/${selectedRouteId.value}`)
      countResult.value = res.data
    } catch (err) {
      console.error('获取报名人数失败', err)
    }
  }
  
  onMounted(fetchRoutes)
  </script>
  
  <style scoped>
  .route-stats-container {
    padding: 24px;
    max-height: 80vh;
    overflow-y: auto;
    background-color: #f9fafb;
    color: #1f2937;
    border-radius: 12px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.05);
  }
  
  .title {
    font-size: 1.5rem;
    font-weight: 700;
    margin-bottom: 20px;
  }
  
  .select-group {
    margin-bottom: 20px;
  }
  
  .select-label {
    font-size: 0.95rem;
    font-weight: 500;
    margin-bottom: 6px;
    display: block;
    color: #374151;
  }
  
  .custom-select {
    width: 100%;
    padding: 10px 12px;
    font-size: 0.95rem;
    border-radius: 8px;
    border: 1px solid #d1d5db;
    background-color: #ffffff;
    color: #111827;
    appearance: none;
    background-image: url('data:image/svg+xml;charset=US-ASCII,%3csvg%20fill%3d%22none%22%20viewBox%3d%220%200%2024%2024%22%20stroke%3d%22currentColor%22%3e%3cpath%20stroke-linecap%3d%22round%22%20stroke-linejoin%3d%22round%22%20stroke-width%3d%222%22%20d%3d%22M19%209l-7%207-7-7%22%20/%3e%3c/svg%3e');
    background-repeat: no-repeat;
    background-position: right 0.75rem center;
    background-size: 1rem;
  }
  
  .result-card {
    background-color: #ffffff;
    border-radius: 10px;
    padding: 16px;
    box-shadow: 0 1px 4px rgba(0,0,0,0.08);
  }
  
  .route-name, .signup-count {
    font-size: 1rem;
    margin-bottom: 8px;
  }
  
  .route-name span {
    font-weight: 600;
  }
  
  .signup-count span {
    font-weight: bold;
    color: #2563eb;
  }
  
  .loading {
    color: #6b7280;
    font-style: italic;
  }
  </style>
  
  