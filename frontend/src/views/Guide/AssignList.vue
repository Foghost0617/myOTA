<template>
    <div class="manage-guide-assignments">
      <h2>导游指派记录管理</h2>
  
      <div v-if="routeGuides.length === 0" class="no-records">暂无指派记录</div>
      <div v-else>
        <table>
          <thead>
            <tr>
              <th>路线ID</th>
              <th>导游ID</th>
              <th>行程开始日期</th>
              <th>行程结束日期</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="routeGuide in routeGuides" :key="routeGuide.id">
              <td>{{ routeGuide.route_id }}</td>
              <td>{{ routeGuide.guide_id }}</td>
              <td>{{ routeGuide.trip_start_time }}</td>
              <td>{{ routeGuide.trip_end_time }}</td>
            </tr>
          </tbody>
        </table>
      </div>
  
      <div v-if="statusMessage" class="status-message">
        {{ statusMessage }}
      </div>
    </div>
  </template>
  
  <script setup>
  import { ref, onMounted } from 'vue';
  import axios from '@/utils/request';  // 假设你有一个配置好的 axios 实例
  
  // 接收父组件传递的 guideId
  const props = defineProps({
    guideId: {
      type: Number,
      required: true
    }
  });
  
  const routeGuides = ref([]);
  const statusMessage = ref('');
  
  // 获取导游指派记录
  onMounted(async () => {
    try {
      const response = await axios.get(`/route_guide/guide/${props.guideId}`);
      routeGuides.value = response.data;  // 直接使用返回的数据，不再需要 map 操作
    } catch (error) {
      console.error('获取导游指派记录失败:', error);
      statusMessage.value = '获取指派记录失败，请重试';
    }
  });
  </script>
  
  <style scoped>
  .manage-guide-assignments {
    padding: 20px;
    font-family: 'Arial', sans-serif;
    color: #333;
  }
  
  h2 {
    font-size: 24px;
    color: #444;
    margin-bottom: 20px;
  }
  
  .no-records {
    text-align: center;
    font-size: 18px;
    color: #888;
    padding: 20px;
  }
  
  table {
    width: 100%;
    border-collapse: collapse;
    margin-bottom: 20px;
    background-color: #fff;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  }
  
  th,
  td {
    padding: 12px;
    border: 1px solid #ddd;
    text-align: center;
    font-size: 16px;
    color: #555;
  }
  
  th {
    background-color: #f4f4f4;
    font-weight: bold;
  }
  
  .status-message {
    margin-top: 20px;
    padding: 12px;
    background-color: #ffeb3b;
    color: #333;
    text-align: center;
    border-radius: 4px;
    font-size: 16px;
  }
  
  .status-message.error {
    background-color: #f8d7da;
    color: #721c24;
  }
  
  .status-message.success {
    background-color: #d4edda;
    color: #155724;
  }
  </style>
  