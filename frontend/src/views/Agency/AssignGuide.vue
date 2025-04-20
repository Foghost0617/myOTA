<template>
    <div class="assign-guide">
      <h2>指派导游</h2>
  
      <div v-if="routes.length === 0">暂无可指派的路线</div>
      <div v-else>
        <form @submit.prevent="assignGuideToRoute">
          <div class="form-group">
            <label for="route">选择路线</label>
            <select v-model="selectedRoute" id="route" required>
              <option v-for="route in routes" :key="route.id" :value="route.id">{{ route.name }}</option>
            </select>
          </div>
  
          <div class="form-group">
            <label for="guide">选择导游</label>
            <select v-model="selectedGuide" id="guide" required>
              <option v-for="guide in guides" :key="guide.id" :value="guide.id">{{ guide.guide_name }}</option>
            </select>
          </div>
  
          <button type="submit" class="button">指派导游</button>
        </form>
      </div>
  
      <div v-if="assignStatus" class="status-message">
        {{ assignStatus }}
      </div>
    </div>
  </template>
  
  <script setup>
  import { ref, onMounted } from 'vue';
  import axios from '@/utils/request'
  
  const selectedRoute = ref(null);
  const selectedGuide = ref(null);
  const routes = ref([]);
  const guides = ref([]);
  const assignStatus = ref('');  // 指派状态消息
   const agency_id = parseInt(localStorage.getItem('agency_id') || '0');
  // 获取所有可指派的路线和导游
  onMounted(async () => {
  try {
    const agencyId = agency_id;
    const routeResponse = await axios.get(`/routes/assign/${agencyId}`); // 这里调用你的后端接口，传递 agency_id
    routes.value = routeResponse.data;

    const guideResponse = await axios.get('/guides/allguides'); // 假设你有一个获取导游列表的 API
    guides.value = guideResponse.data;
  } catch (error) {
    console.error('获取数据失败:', error);
    assignStatus.value = '获取数据失败，请重试';
  }
});
;
  
  // 指派导游
  const assignGuideToRoute = async () => {
    if (!selectedRoute.value || !selectedGuide.value) {
      assignStatus.value = '请选择路线和导游';
      return;
    }
  
    try {
      const response = await axios.post('/route_guide/create', {
        route_id: selectedRoute.value,
        guide_id: selectedGuide.value,
      });
  
      if (response.data) {
        assignStatus.value = '导游指派成功';
      } else {
        assignStatus.value = '导游指派失败，请重试';
      }
    } catch (error) {
      console.error('指派导游失败:', error);
      assignStatus.value = '指派导游失败，请重试';
    }
  };
  </script>
  
  <style scoped>
  .assign-guide {
    padding: 20px;
  }
  
  .status-message {
    margin-top: 10px;
    color: green;
  }
  
  .form-group {
    margin-bottom: 15px;
  }
  
  button {
    padding: 10px 15px;
    background-color: #4CAF50;
    color: white;
    border: none;
    cursor: pointer;
  }
  
  button:disabled {
    background-color: #ccc;
    cursor: not-allowed;
  }
  </style>
  