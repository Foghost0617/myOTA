<template>
    <div class="manage-guide-assignments">
      <h2>指派记录管理</h2>
  
      <div v-if="routeGuides.length === 0" class="no-records">暂无指派记录</div>
      <div v-else>
        <table>
          <thead>
            <tr>
              <th>路线ID</th>
              <th>导游ID</th>
              <th>行程开始日期</th>
              <th>行程结束日期</th>
              <th>操作</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="routeGuide in routeGuides" :key="routeGuide.id">
              <td>{{ routeGuide.route_id }}</td>
              <td>{{ routeGuide.guide_id }}</td>
              <td>{{ routeGuide.trip_start_time }}</td>
              <td>{{ routeGuide.trip_end_time }}</td>
              <td>
                <button @click="deleteRouteGuide(routeGuide.id)">删除</button>
              </td>
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
  
  // 接收父组件传递的 agencyId
  const props = defineProps({
    agencyId: {
      type: Number,
      required: true
    }
  });
  
  const routeGuides = ref([]);
  const statusMessage = ref('');
  
  // 获取所有指派记录
  onMounted(async () => {
    try {
      const response = await axios.get(`/route_guide/${props.agencyId}/all`);
      routeGuides.value = response.data;  // 直接使用返回的数据，不再需要 map 操作
    } catch (error) {
      console.error('获取指派记录失败:', error);
      statusMessage.value = '获取指派记录失败，请重试';
    }
  });
  
  // 删除指派记录
  const deleteRouteGuide = async (routeGuideId) => {
    if (!window.confirm('确认要删除这条指派记录吗？')) return;
  
    try {
      const response = await axios.delete(`/route_guide/del/${routeGuideId}`);
      statusMessage.value = response.data.message;  // 返回的删除成功信息
      // 刷新列表
      routeGuides.value = routeGuides.value.filter(guide => guide.id !== routeGuideId);
    } catch (error) {
      console.error('删除指派记录失败:', error);
      statusMessage.value = '删除指派记录失败，请重试';
    }
  };
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
  
  button {
    padding: 6px 15px;
    background-color: #f44336;
    color: white;
    border: none;
    cursor: pointer;
    border-radius: 4px;
    font-size: 14px;
    transition: background-color 0.3s ease;
  }
  
  button:hover {
    background-color: #d32f2f;
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
  
  